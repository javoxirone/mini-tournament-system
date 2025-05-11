import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from datetime import datetime

from app.schemas.player import PlayerInDBInput, PlayerInDBOutput
from app.exceptions.player import (
    PlayerNotFoundError,
    PlayerFetchError,
    PlayerCreationError,
    PlayerUpdateError,
    PlayerDeletionError,
    PlayerEmailExistsError
)
from app.services.player import (
    create_player,
    get_player,
    get_players,
    get_players_by_tournament,
    get_players_count_by_tournament,
    update_player,
    delete_player
)


@pytest.fixture
def mock_player_repo():
    with patch("app.services.player.PlayerRepo") as mock_repo:
        # Configure the mock to return a mock instance
        mock_instance = MagicMock()
        mock_repo.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def player_data():
    return PlayerInDBInput(
        name="Test Player",
        email="test@example.com",
        tournament_id=1
    )


@pytest.fixture
def player_output():
    return PlayerInDBOutput(
        id=1,
        name="Test Player",
        email="test@example.com",
        tournament_id=1,
        registered_at=datetime.now()
    )


class TestPlayerCreation:
    def test_create_player_success(self, mock_player_repo, player_data, player_output):
        mock_player_repo.create_player.return_value = player_output

        result = create_player(player_data)

        assert result == player_output
        mock_player_repo.create_player.assert_called_once_with(player_data)

    def test_create_player_email_exists(self, mock_player_repo, player_data):
        mock_player_repo.create_player.side_effect = PlayerEmailExistsError(
            email=player_data.email, tournament_id=player_data.tournament_id
        )

        with pytest.raises(HTTPException) as excinfo:
            create_player(player_data)
        assert excinfo.value.status_code == 409
        assert f"Player with email '{player_data.email}'" in str(excinfo.value.detail)

    def test_create_player_creation_error(self, mock_player_repo, player_data):
        mock_player_repo.create_player.side_effect = PlayerCreationError("Creation error")

        with pytest.raises(HTTPException) as excinfo:
            create_player(player_data)
        assert excinfo.value.status_code == 500
        assert "Creation error" in str(excinfo.value.detail)


class TestPlayerRetrieval:
    def test_get_player_success(self, mock_player_repo, player_output):
        mock_player_repo.get_player.return_value = player_output

        result = get_player(1)

        assert result == player_output
        mock_player_repo.get_player.assert_called_once_with(1)

    def test_get_player_not_found(self, mock_player_repo):
        mock_player_repo.get_player.side_effect = PlayerNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            get_player(1)
        assert excinfo.value.status_code == 404
        assert "Player with id 1 not found" in str(excinfo.value.detail)

    def test_get_player_fetch_error(self, mock_player_repo):
        mock_player_repo.get_player.side_effect = PlayerFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_player(1)
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)

    def test_get_players_success(self, mock_player_repo, player_output):
        mock_player_repo.get_players.return_value = [player_output]

        result = get_players()

        assert result == [player_output]
        mock_player_repo.get_players.assert_called_once()

    def test_get_players_fetch_error(self, mock_player_repo):
        mock_player_repo.get_players.side_effect = PlayerFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_players()
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)

    def test_get_players_by_tournament_success(self, mock_player_repo, player_output):
        mock_player_repo.get_players_by_tournament.return_value = [player_output]

        result = get_players_by_tournament(1)

        assert result == [player_output]
        mock_player_repo.get_players_by_tournament.assert_called_once_with(1)

    def test_get_players_by_tournament_error(self, mock_player_repo):
        mock_player_repo.get_players_by_tournament.side_effect = PlayerFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_players_by_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)

    def test_get_players_count_by_tournament_success(self, mock_player_repo):
        mock_player_repo.get_players_count_by_tournament.return_value = 5

        result = get_players_count_by_tournament(1)

        assert result == 5
        mock_player_repo.get_players_count_by_tournament.assert_called_once_with(1)

    def test_get_players_count_by_tournament_error(self, mock_player_repo):
        mock_player_repo.get_players_count_by_tournament.side_effect = PlayerFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_players_count_by_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)


class TestPlayerUpdate:
    def test_update_player_success(self, mock_player_repo, player_data, player_output):
        mock_player_repo.update_player.return_value = player_output

        result = update_player(1, player_data)

        assert result == player_output
        mock_player_repo.update_player.assert_called_once_with(1, player_data)

    def test_update_player_not_found(self, mock_player_repo, player_data):
        mock_player_repo.update_player.side_effect = PlayerNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            update_player(1, player_data)
        assert excinfo.value.status_code == 404

    def test_update_player_email_exists(self, mock_player_repo, player_data):
        mock_player_repo.update_player.side_effect = PlayerEmailExistsError(
            email=player_data.email, tournament_id=player_data.tournament_id
        )

        with pytest.raises(HTTPException) as excinfo:
            update_player(1, player_data)
        assert excinfo.value.status_code == 409
        assert f"Player with email '{player_data.email}'" in str(excinfo.value.detail)

    def test_update_player_error(self, mock_player_repo, player_data):
        mock_player_repo.update_player.side_effect = PlayerUpdateError("Update error")

        with pytest.raises(HTTPException) as excinfo:
            update_player(1, player_data)
        assert excinfo.value.status_code == 500
        assert "Update error" in str(excinfo.value.detail)


class TestPlayerDeletion:
    def test_delete_player_success(self, mock_player_repo):
        mock_player_repo.delete_player.return_value = True

        result = delete_player(1)

        assert result is True
        mock_player_repo.delete_player.assert_called_once_with(1)

    def test_delete_player_not_found(self, mock_player_repo):
        mock_player_repo.delete_player.side_effect = PlayerNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            delete_player(1)
        assert excinfo.value.status_code == 404
        assert "Player with id 1 not found" in str(excinfo.value.detail)

    def test_delete_player_error(self, mock_player_repo):
        mock_player_repo.delete_player.side_effect = PlayerDeletionError("Deletion error")

        with pytest.raises(HTTPException) as excinfo:
            delete_player(1)
        assert excinfo.value.status_code == 500
        assert "Deletion error" in str(excinfo.value.detail)