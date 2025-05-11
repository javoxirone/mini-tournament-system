import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from datetime import datetime

from app.schemas.tournament import TournamentInDBInput, TournamentInDBOutput
from app.exceptions.tournament import (
    TournamentBaseException,
    TournamentNotFoundError,
    TournamentFetchError,
    TournamentCreationError,
    TournamentUpdateError,
    TournamentDeletionError,
    TournamentNameExistsError
)
from app.services.tournament import (
    create_tournament,
    get_tournament,
    get_tournaments,
    update_tournament,
    delete_tournament
)


@pytest.fixture
def mock_tournament_repo():
    with patch("app.services.tournament.TournamentRepo") as mock_repo:
        mock_instance = MagicMock()
        mock_repo.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def tournament_data():
    return TournamentInDBInput(
        name="Test Tournament",
        max_players=10,
        start_at=datetime.now()
    )


@pytest.fixture
def tournament_output():
    return TournamentInDBOutput(
        id=1,
        name="Test Tournament",
        max_players=10,
        start_at=datetime.now(),
        created_at=datetime.now()
    )


class TestTournamentCreation:
    def test_create_tournament_success(self, mock_tournament_repo, tournament_data, tournament_output):
        mock_tournament_repo.create_tournament.return_value = tournament_output

        result = create_tournament(tournament_data)

        assert result == tournament_output
        mock_tournament_repo.create_tournament.assert_called_once_with(tournament_data)

    def test_create_tournament_name_exists(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.create_tournament.side_effect = TournamentNameExistsError(tournament_data.name)

        with pytest.raises(HTTPException) as excinfo:
            create_tournament(tournament_data)
        assert excinfo.value.status_code == 409
        assert f"Tournament with name '{tournament_data.name}' already exists" in str(excinfo.value.detail)

    def test_create_tournament_creation_error(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.create_tournament.side_effect = TournamentCreationError("Creation error")

        with pytest.raises(HTTPException) as excinfo:
            create_tournament(tournament_data)
        assert excinfo.value.status_code == 500
        assert "Creation error" in str(excinfo.value.detail)

    def test_create_tournament_base_exception(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.create_tournament.side_effect = TournamentBaseException("Base exception")

        with pytest.raises(HTTPException) as excinfo:
            create_tournament(tournament_data)
        assert excinfo.value.status_code == 500
        assert "Base exception" in str(excinfo.value.detail)


class TestTournamentRetrieval:
    def test_get_tournament_success(self, mock_tournament_repo, tournament_output):
        mock_tournament_repo.get_tournament.return_value = tournament_output

        result = get_tournament(1)

        assert result == tournament_output
        mock_tournament_repo.get_tournament.assert_called_once_with(1)

    def test_get_tournament_not_found(self, mock_tournament_repo):
        mock_tournament_repo.get_tournament.side_effect = TournamentNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            get_tournament(1)
        assert excinfo.value.status_code == 404
        assert "Tournament with id 1 not found" in str(excinfo.value.detail)

    def test_get_tournament_fetch_error(self, mock_tournament_repo):
        mock_tournament_repo.get_tournament.side_effect = TournamentFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)

    def test_get_tournament_base_exception(self, mock_tournament_repo):
        mock_tournament_repo.get_tournament.side_effect = TournamentBaseException("Base exception")

        with pytest.raises(HTTPException) as excinfo:
            get_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Base exception" in str(excinfo.value.detail)

    def test_get_tournaments_success(self, mock_tournament_repo, tournament_output):
        mock_tournament_repo.get_tournaments.return_value = [tournament_output]

        result = get_tournaments()

        assert result == [tournament_output]
        mock_tournament_repo.get_tournaments.assert_called_once()

    def test_get_tournaments_fetch_error(self, mock_tournament_repo):
        mock_tournament_repo.get_tournaments.side_effect = TournamentFetchError("Fetch error")

        with pytest.raises(HTTPException) as excinfo:
            get_tournaments()
        assert excinfo.value.status_code == 500
        assert "Fetch error" in str(excinfo.value.detail)

    def test_get_tournaments_base_exception(self, mock_tournament_repo):
        mock_tournament_repo.get_tournaments.side_effect = TournamentBaseException("Base exception")

        with pytest.raises(HTTPException) as excinfo:
            get_tournaments()
        assert excinfo.value.status_code == 500
        assert "Base exception" in str(excinfo.value.detail)


class TestTournamentUpdate:
    def test_update_tournament_success(self, mock_tournament_repo, tournament_data, tournament_output):
        mock_tournament_repo.update_tournament.return_value = tournament_output

        result = update_tournament(1, tournament_data)

        assert result == tournament_output
        mock_tournament_repo.update_tournament.assert_called_once_with(1, tournament_data)

    def test_update_tournament_not_found(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.update_tournament.side_effect = TournamentNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            update_tournament(1, tournament_data)
        assert excinfo.value.status_code == 404
        assert "Tournament with id 1 not found" in str(excinfo.value.detail)

    def test_update_tournament_name_exists(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.update_tournament.side_effect = TournamentNameExistsError(tournament_data.name)

        with pytest.raises(HTTPException) as excinfo:
            update_tournament(1, tournament_data)
        assert excinfo.value.status_code == 409
        assert f"Tournament with name '{tournament_data.name}' already exists" in str(excinfo.value.detail)

    def test_update_tournament_update_error(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.update_tournament.side_effect = TournamentUpdateError("Update error")

        with pytest.raises(HTTPException) as excinfo:
            update_tournament(1, tournament_data)
        assert excinfo.value.status_code == 500
        assert "Update error" in str(excinfo.value.detail)

    def test_update_tournament_base_exception(self, mock_tournament_repo, tournament_data):
        mock_tournament_repo.update_tournament.side_effect = TournamentBaseException("Base exception")

        with pytest.raises(HTTPException) as excinfo:
            update_tournament(1, tournament_data)
        assert excinfo.value.status_code == 500
        assert "Base exception" in str(excinfo.value.detail)


class TestTournamentDeletion:
    def test_delete_tournament_success(self, mock_tournament_repo):
        mock_tournament_repo.delete_tournament.return_value = True

        result = delete_tournament(1)

        assert result is True
        mock_tournament_repo.delete_tournament.assert_called_once_with(1)

    def test_delete_tournament_not_found(self, mock_tournament_repo):
        mock_tournament_repo.delete_tournament.side_effect = TournamentNotFoundError(1)

        with pytest.raises(HTTPException) as excinfo:
            delete_tournament(1)
        assert excinfo.value.status_code == 404
        assert "Tournament with id 1 not found" in str(excinfo.value.detail)

    def test_delete_tournament_deletion_error(self, mock_tournament_repo):
        mock_tournament_repo.delete_tournament.side_effect = TournamentDeletionError("Deletion error")

        with pytest.raises(HTTPException) as excinfo:
            delete_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Deletion error" in str(excinfo.value.detail)

    def test_delete_tournament_base_exception(self, mock_tournament_repo):
        mock_tournament_repo.delete_tournament.side_effect = TournamentBaseException("Base exception")

        with pytest.raises(HTTPException) as excinfo:
            delete_tournament(1)
        assert excinfo.value.status_code == 500
        assert "Base exception" in str(excinfo.value.detail)