import pytest
from datetime import datetime
from unittest.mock import MagicMock
from app.models import Tournament
from app.repositories.player import PlayerRepo
from app.schemas.player import PlayerInDBInput
from app.exceptions.player import (
    PlayerNotFoundError,
    PlayerEmailExistsError,
    PlayerCreationError,
)
from tests.repositories.config import db_session


@pytest.fixture
def player_repo(db_session):
    repo = PlayerRepo()
    repo.db = db_session
    repo._validate_player_registration = MagicMock()
    return repo


@pytest.fixture
def tournament(db_session):
    tournament = Tournament(
        name="Test Tournament", max_players=10, start_at=datetime.now()
    )
    db_session.add(tournament)
    db_session.commit()
    return tournament


@pytest.fixture
def player_data(tournament):
    return PlayerInDBInput(
        name="John Doe", email="john@example.com", tournament_id=tournament.id
    )


@pytest.fixture
def created_player(player_repo, player_data):
    return player_repo.create_player(player_data)


class TestPlayerCreation:
    def test_create_player(self, player_repo, player_data):
        player = player_repo.create_player(player_data)
        assert player.name == player_data.name
        assert player.email == player_data.email
        assert player.tournament_id == player_data.tournament_id
        assert player.id is not None
        assert isinstance(player.registered_at, datetime)

    def test_create_duplicate_player(self, player_repo, player_data, created_player):
        with pytest.raises(PlayerEmailExistsError) as excinfo:
            player_repo.create_player(player_data)
        assert (
            f"Player with email '{player_data.email}' already exists in tournament {player_data.tournament_id}"
            in str(excinfo.value)
        )

    def test_tournament_full(self, player_repo, player_data):
        player_repo._validate_player_registration.side_effect = PlayerCreationError(
            "Tournament is full"
        )

        with pytest.raises(PlayerCreationError) as excinfo:
            player_repo.create_player(player_data)
        assert "Tournament is full" in str(excinfo.value)


class TestPlayerRetrieval:
    def test_get_player(self, player_repo, created_player):
        player = player_repo.get_player(created_player.id)
        assert player.id == created_player.id
        assert player.name == created_player.name
        assert player.email == created_player.email

    def test_get_nonexistent_player(self, player_repo):
        with pytest.raises(PlayerNotFoundError) as excinfo:
            player_repo.get_player(999)
        assert "Player with id 999 not found" in str(excinfo.value)

    def test_get_players(self, player_repo, created_player):
        players = player_repo.get_players()
        assert len(players) >= 1
        assert any(player.id == created_player.id for player in players)

    def test_get_players_by_tournament(self, player_repo, created_player):
        players = player_repo.get_players_by_tournament(created_player.tournament_id)
        assert len(players) >= 1
        assert any(player.id == created_player.id for player in players)

    def test_get_players_count_by_tournament(self, player_repo, created_player):
        count = player_repo.get_players_count_by_tournament(
            created_player.tournament_id
        )
        assert count >= 1


class TestPlayerUpdate:
    def test_update_player(self, player_repo, created_player, tournament):
        updated_data = PlayerInDBInput(
            name="Jane Doe", email="jane@example.com", tournament_id=tournament.id
        )
        updated_player = player_repo.update_player(created_player.id, updated_data)
        assert updated_player.name == updated_data.name
        assert updated_player.email == updated_data.email
        assert updated_player.tournament_id == updated_data.tournament_id

    def test_update_nonexistent_player(self, player_repo, player_data):
        with pytest.raises(PlayerNotFoundError) as excinfo:
            player_repo.update_player(999, player_data)
        assert "Player with id 999 not found" in str(excinfo.value)

    def test_update_duplicate_email(
        self, player_repo, created_player, tournament, db_session
    ):
        another_player_data = PlayerInDBInput(
            name="Another Player",
            email="another@example.com",
            tournament_id=tournament.id,
        )
        another_player = player_repo.create_player(another_player_data)

        update_data = PlayerInDBInput(
            name="Updated Name", email=created_player.email, tournament_id=tournament.id
        )

        with pytest.raises(PlayerEmailExistsError) as excinfo:
            player_repo.update_player(another_player.id, update_data)
        assert (
            f"Player with email '{created_player.email}' already exists in tournament {tournament.id}"
            in str(excinfo.value)
        )


class TestPlayerDeletion:
    def test_delete_player(self, player_repo, created_player):
        assert player_repo.delete_player(created_player.id) is True
        with pytest.raises(PlayerNotFoundError) as excinfo:
            player_repo.get_player(created_player.id)
        assert f"Player with id {created_player.id} not found" in str(excinfo.value)

    def test_delete_nonexistent_player(self, player_repo):
        with pytest.raises(PlayerNotFoundError) as excinfo:
            player_repo.delete_player(999)
        assert "Player with id 999 not found" in str(excinfo.value)