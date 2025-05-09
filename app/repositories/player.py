from app.db import SessionLocal
from app.models import Player
from app.schemas.player import PlayerInDBInput, PlayerInDBOutput
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class PlayerRepo:
    def __init__(self):
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to connect to database: {str(e)}")

    def get_players(self):
        try:
            players = self.db.query(Player).all()
            return players
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to fetch players: {str(e)}")

    def get_players_by_tournament(self, tournament_id: int):
        try:
            players = (
                self.db.query(Player)
                .filter(Player.tournament_id == tournament_id)
                .all()
            )
            return players
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(
                f"Failed to fetch players for tournament {tournament_id}: {str(e)}"
            )

    def create_player(self, data: PlayerInDBInput):
        try:
            new_player = Player(
                name=data.name, email=data.email, tournament_id=data.tournament_id
            )
            self.db.add(new_player)
            self.db.commit()
            self.db.refresh(new_player)
            return PlayerInDBOutput(
                id=new_player.id,
                name=new_player.name,
                email=new_player.email,
                tournament_id=new_player.tournament_id,
                registered_at=new_player.registered_at,
            )
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Player with this email already exists in the tournament")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to create player: {str(e)}")

    def get_player(self, player_id: int):
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise ValueError(f"Player with id {player_id} not found")
            return player
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to fetch player {player_id}: {str(e)}")

    def update_player(
        self, player_id: int, data: PlayerInDBInput
    ) -> PlayerInDBOutput | None:
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise ValueError(f"Player with id {player_id} not found")
            player.name = data.name
            player.email = data.email
            player.tournament_id = data.tournament_id
            self.db.commit()
            self.db.refresh(player)
            return PlayerInDBOutput(
                id=player.id,
                name=player.name,
                email=player.email,
                tournament_id=player.tournament_id,
                registered_at=player.registered_at,
            )
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Player with this email already exists in the tournament")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to update player {player_id}: {str(e)}")

    def delete_player(self, player_id: int) -> bool:
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                return False
            self.db.delete(player)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to delete player {player_id}: {str(e)}")