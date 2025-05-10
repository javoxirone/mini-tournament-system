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
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise PlayerDatabaseConnectionError(
                f"Failed to connect to database: {str(e)}"
            )

    def get_players(self) -> list[PlayerInDBOutput]:
        try:
            players = self.db.query(Player).all()
            return [PlayerInDBOutput.model_validate(player) for player in players]
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(f"Failed to fetch players: {str(e)}")

    def get_players_by_tournament(self, tournament_id: int) -> list[PlayerInDBOutput]:
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

    def create_player(self, data: PlayerInDBInput) -> PlayerInDBOutput:
        try:
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
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise PlayerNotFoundError(player_id)
            return PlayerInDBOutput.model_validate(player)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PlayerFetchError(f"Failed to fetch player {player_id}: {str(e)}")

    def update_player(self, player_id: int, data: PlayerInDBInput) -> PlayerInDBOutput:
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