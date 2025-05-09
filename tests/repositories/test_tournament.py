import pytest
from datetime import datetime
from app.repositories.tournament import TournamentRepo
from app.schemas.tournament import TournamentInDBInput
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
        assert tournament.start_at == tournament_data.start_at
        assert isinstance(tournament.start_at, datetime)

    def test_create_duplicate_tournament(self, tournament_repo, tournament_data):
        tournament_repo.create_tournament(tournament_data)
        with pytest.raises(
            ValueError, match="Tournament with this name already exists"
        ):
            tournament_repo.create_tournament(tournament_data)


class TestTournamentRetrieval:
    def test_get_tournament(self, tournament_repo, created_tournament):
        tournament = tournament_repo.get_tournament(created_tournament.id)
        assert tournament.id == created_tournament.id
        assert tournament.name == created_tournament.name
        assert tournament.max_players == created_tournament.max_players

    def test_get_nonexistent_tournament(self, tournament_repo):
        with pytest.raises(ValueError, match="Tournament with id 999 not found"):
            tournament_repo.get_tournament(999)

    def test_get_tournaments(self, tournament_repo, created_tournament):
        tournaments = tournament_repo.get_tournaments()
        assert len(tournaments) == 1
        assert tournaments[0].id == created_tournament.id


class TestTournamentUpdate:
    def test_update_tournament(self, tournament_repo, created_tournament):
        updated_data = TournamentInDBInput(
            name="Test Tournament 2", max_players=15, start_at=datetime.now()
        )
        updated_tournament = tournament_repo.update_tournament(
            created_tournament.id, updated_data
        )

    def test_update_nonexistent_tournament(self, tournament_repo, tournament_data):
        with pytest.raises(ValueError, match="Tournament with id 999 not found"):
            tournament_repo.update_tournament(999, tournament_data)


class TestTournamentDeletion:
    def test_delete_tournament(self, tournament_repo, created_tournament):
        assert tournament_repo.delete_tournament(created_tournament.id) is True
        with pytest.raises(
            ValueError, match=f"Tournament with id {created_tournament.id} not found"
        ):
            tournament_repo.get_tournament(created_tournament.id)

    def test_delete_nonexistent_tournament(self, tournament_repo):
        with pytest.raises(ValueError, match="Tournament with id 999 not found"):
            tournament_repo.delete_tournament(999)