from app.db import SessionLocal
from app.models import Player
from app.schemas.player import PlayerInDBInput, PlayerInDBOutput
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions.player import (
    PlayerDatabaseConnectionError,
    PlayerFetchError,
    PlayerNotFoundError,
    PlayerCreationError,
    PlayerUpdateError,
    PlayerDeletionError,
    PlayerEmailExistsError,
)


class PlayerRepo:
    def __init__(self):
        """Initialize database connection."""
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise PlayerDatabaseConnectionError(
                f"Failed to connect to database: {str(e)}"
            )

    def get_players(self) -> list[PlayerInDBOutput]:
        """
        Get all players.

        :return: List of players
        :rtype: list[PlayerInDBOutput]
        """
        try:
            players = self.db.query(Player).all()
            return [PlayerInDBOutput.model_validate(player) for player in players]
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(f"Failed to fetch players: {str(e)}")

    def get_players_by_tournament(self, tournament_id: int) -> list[PlayerInDBOutput]:
        """
        Get players in a tournament.

        :param tournament_id: ID of tournament
        :type tournament_id: int
        :return: List of players in tournament
        :rtype: list[PlayerInDBOutput]
        """
        try:
            players = (
                self.db.query(Player)
                .filter(Player.tournament_id == tournament_id)
                .all()
            )
            return [PlayerInDBOutput.model_validate(player) for player in players]
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(
                f"Failed to fetch players for tournament {tournament_id}: {str(e)}"
            )

    def get_players_count_by_tournament(self, tournament_id: int) -> int:
        """
        Get number of players in a tournament.

        :param tournament_id: ID of tournament
        :type tournament_id: int
        :return: Number of players
        :rtype: int
        """
        try:
            players_count = (
                self.db.query(Player)
                .filter(Player.tournament_id == tournament_id)
                .count()
            )
            return players_count
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(
                "Failed to fetch players for tournament {tournament_id}: {str(e)}"
            )

    def _validate_player_registration(self, tournament_id: int):
        """
        Check if tournament has space for another player.

        :param tournament_id: ID of tournament
        :type tournament_id: int
        :raises: PlayerCreationError if tournament is full
        """
        from app.services.tournament import get_tournament

        tournament = get_tournament(tournament_id)

        allowed_num_of_players = tournament.max_players
        registered_num_of_players = self.get_players_count_by_tournament(tournament_id)
        if allowed_num_of_players <= registered_num_of_players:
            raise PlayerCreationError(
                f"Tournament {tournament.name} already has {registered_num_of_players} players."
            )

    def create_player(self, data: PlayerInDBInput) -> PlayerInDBOutput:
        """
        Create a new player.

        :param data: Player data
        :type data: PlayerInDBInput
        :return: Created player
        :rtype: PlayerInDBOutput
        """
        try:
            self._validate_player_registration(data.tournament_id)

            new_player = Player(
                name=data.name, email=data.email, tournament_id=data.tournament_id
            )
            self.db.add(new_player)
            self.db.commit()
            self.db.refresh(new_player)
            return PlayerInDBOutput.model_validate(new_player)
        except IntegrityError:
            self.db.rollback()
            raise PlayerEmailExistsError(
                email=data.email, tournament_id=data.tournament_id
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerCreationError(f"Failed to create player: {str(e)}")

    def get_player(self, player_id: int) -> PlayerInDBOutput:
        """
        Get a player by ID.

        :param player_id: ID of player
        :type player_id: int
        :return: Player data
        :rtype: PlayerInDBOutput
        """
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise PlayerNotFoundError(player_id)
            return PlayerInDBOutput.model_validate(player)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(f"Failed to fetch player {player_id}: {str(e)}")

    def update_player(self, player_id: int, data: PlayerInDBInput) -> PlayerInDBOutput:
        """
        Update a player's data.

        :param player_id: ID of player
        :type player_id: int
        :param data: Updated player data
        :type data: PlayerInDBInput
        :return: Updated player
        :rtype: PlayerInDBOutput
        """
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise PlayerNotFoundError(player_id)
            player.name = data.name
            player.email = data.email
            player.tournament_id = data.tournament_id
            self.db.commit()
            self.db.refresh(player)
            return PlayerInDBOutput.model_validate(player)
        except IntegrityError:
            self.db.rollback()
            raise PlayerEmailExistsError(
                email=data.email, tournament_id=data.tournament_id
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerUpdateError(f"Failed to update player {player_id}: {str(e)}")

    def delete_player(self, player_id: int) -> bool:
        """
        Delete a player.

        :param player_id: ID of player
        :type player_id: int
        :return: True if successful
        :rtype: bool
        """
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise PlayerNotFoundError(player_id)

            self.db.delete(player)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerDeletionError(f"Failed to delete player {player_id}: {str(e)}")
