import pytest
from datetime import datetime
from app.repositories.tournament import TournamentRepo
from app.schemas.tournament import TournamentInDBInput
from app.exceptions.tournament import TournamentNotFoundError, TournamentNameExistsError
from tests.repositories.config import db_session


@pytest.fixture
def tournament_repo(db_session):
    repo = TournamentRepo()
    repo.db = db_session
    return repo


@pytest.fixture
def tournament_data():
    return TournamentInDBInput(
        name="Test Tournament", max_players=10, start_at=datetime.now()
    )


@pytest.fixture
def created_tournament(tournament_repo, tournament_data):
    return tournament_repo.create_tournament(tournament_data)


class TestTournamentCreation:
    def test_create_tournament(self, tournament_repo, tournament_data):
        tournament = tournament_repo.create_tournament(tournament_data)
        assert tournament.name == tournament_data.name
        assert tournament.max_players == tournament_data.max_players
        assert isinstance(tournament.start_at, datetime)
        assert tournament.id is not None

    def test_create_duplicate_tournament(
        self, tournament_repo, tournament_data, created_tournament
    ):
        with pytest.raises(TournamentNameExistsError) as excinfo:
            tournament_repo.create_tournament(tournament_data)
        assert f"Tournament with name '{tournament_data.name}' already exists" in str(
            excinfo.value
        )


class TestTournamentRetrieval:
    def test_get_tournament(self, tournament_repo, created_tournament):
        tournament = tournament_repo.get_tournament(created_tournament.id)
        assert tournament.id == created_tournament.id
        assert tournament.name == created_tournament.name
        assert tournament.max_players == created_tournament.max_players
        assert (
            abs((tournament.start_at - created_tournament.start_at).total_seconds()) < 1
        )

    def test_get_nonexistent_tournament(self, tournament_repo):
        with pytest.raises(TournamentNotFoundError) as excinfo:
            tournament_repo.get_tournament(999)
        assert "Tournament with id 999 not found" in str(excinfo.value)

    def test_get_tournaments(self, tournament_repo, created_tournament):
        tournaments = tournament_repo.get_tournaments()
        assert len(tournaments) >= 1
        assert any(tournament.id == created_tournament.id for tournament in tournaments)


class TestTournamentUpdate:
    def test_update_tournament(self, tournament_repo, created_tournament):
        updated_data = TournamentInDBInput(
            name="Test Tournament 2", max_players=15, start_at=datetime.now()
        )
        updated_tournament = tournament_repo.update_tournament(
            created_tournament.id, updated_data
        )

        assert updated_tournament.id == created_tournament.id
        assert updated_tournament.name == updated_data.name
        assert updated_tournament.max_players == updated_data.max_players


    def test_update_nonexistent_tournament(self, tournament_repo, tournament_data):
        with pytest.raises(TournamentNotFoundError) as excinfo:
            tournament_repo.update_tournament(999, tournament_data)
        assert "Tournament with id 999 not found" in str(excinfo.value)

    def test_update_duplicate_name(
        self, tournament_repo, created_tournament, db_session
    ):
        another_tournament_data = TournamentInDBInput(
            name="Another Tournament", max_players=8, start_at=datetime.now()
        )
        another_tournament = tournament_repo.create_tournament(another_tournament_data)

        update_data = TournamentInDBInput(
            name=created_tournament.name,
            max_players=another_tournament.max_players,
            start_at=another_tournament.start_at,
        )

        with pytest.raises(TournamentNameExistsError) as excinfo:
            tournament_repo.update_tournament(another_tournament.id, update_data)
        assert (
            f"Tournament with name '{created_tournament.name}' already exists"
            in str(excinfo.value)
        )


class TestTournamentDeletion:
    def test_delete_tournament(self, tournament_repo, created_tournament):
        assert tournament_repo.delete_tournament(created_tournament.id) is True
        with pytest.raises(TournamentNotFoundError) as excinfo:
            tournament_repo.get_tournament(created_tournament.id)
        assert f"Tournament with id {created_tournament.id} not found" in str(
            excinfo.value
        )

    def test_delete_nonexistent_tournament(self, tournament_repo):
        with pytest.raises(TournamentNotFoundError) as excinfo:
            tournament_repo.delete_tournament(999)
        assert "Tournament with id 999 not found" in str(excinfo.value)