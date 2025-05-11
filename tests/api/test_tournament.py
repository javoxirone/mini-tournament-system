import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from datetime import datetime
from app.schemas.player import PlayerInRequest, PlayerInDBInput
from app.schemas.tournament import TournamentInDBOutput
from app.api.tournament import register_player_api_view

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_tournament_repo():
    with patch("app.services.tournament.TournamentRepo") as mock_repo:
        mock_instance = MagicMock()
        mock_repo.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def tournament_output():
    return TournamentInDBOutput(
        id=1,
        name="Test Tournament",
        max_players=10,
        start_at=datetime.now(),
        created_at=datetime.now(),
        registered_players=1,
    )


@pytest.fixture
def player_request_data():
    return PlayerInRequest(name="Test Player", email="test@example.com")


class TestRegisterPlayer:
    async def test_register_player_success(
        self, mock_tournament_repo, player_request_data, tournament_output
    ):
        with (
            patch("app.api.tournament.create_player") as mock_create_player,
            patch("app.api.tournament.get_tournament") as mock_get_tournament,
        ):
            mock_get_tournament.return_value = tournament_output
            mock_create_player.return_value = None

            result = await register_player_api_view(1, player_request_data)

            expected_player_data = PlayerInDBInput(
                **player_request_data.__dict__, tournament_id=1
            )
            mock_create_player.assert_called_once_with(expected_player_data)
            assert result == tournament_output
            mock_get_tournament.assert_called_once_with(1)

    async def test_register_player_tournament_not_found(
        self, mock_tournament_repo, player_request_data
    ):
        with (
            patch("app.api.tournament.create_player") as mock_create_player,
            patch("app.api.tournament.get_tournament") as mock_get_tournament,
        ):
            mock_get_tournament.side_effect = HTTPException(
                status_code=404, detail="Tournament with id 1 not found"
            )

            with pytest.raises(HTTPException) as excinfo:
                await register_player_api_view(1, player_request_data)

            assert excinfo.value.status_code == 404
            assert "Tournament with id 1 not found" in str(excinfo.value.detail)

    async def test_register_player_creation_error(
        self, mock_tournament_repo, player_request_data
    ):
        with patch("app.api.tournament.create_player") as mock_create_player:
            mock_create_player.side_effect = HTTPException(
                status_code=500, detail="Player creation failed"
            )

            with pytest.raises(HTTPException) as excinfo:
                await register_player_api_view(1, player_request_data)

            assert excinfo.value.status_code == 500
            assert "Player creation failed" in str(excinfo.value.detail)

    async def test_register_player_duplicate_email(
        self, mock_tournament_repo, player_request_data
    ):
        with patch("app.api.tournament.create_player") as mock_create_player:
            mock_create_player.side_effect = HTTPException(
                status_code=409,
                detail="Player with email 'test@example.com' already exists in tournament 1",
            )

            with pytest.raises(HTTPException) as excinfo:
                await register_player_api_view(1, player_request_data)

            assert excinfo.value.status_code == 409
            assert (
                "Player with email 'test@example.com' already exists in tournament 1"
                in str(excinfo.value.detail)
            )

    async def test_register_player_tournament_full(
        self, mock_tournament_repo, player_request_data
    ):
        with patch("app.api.tournament.create_player") as mock_create_player:
            mock_create_player.side_effect = HTTPException(
                status_code=500, detail="Tournament is full"
            )

            with pytest.raises(HTTPException) as excinfo:
                await register_player_api_view(1, player_request_data)

            assert excinfo.value.status_code == 500
            assert "Tournament is full" in str(excinfo.value.detail)