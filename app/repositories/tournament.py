from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db import SessionLocal
from app.models import Tournament
from app.schemas.tournament import TournamentInDBInput


class TournamentRepo:
    def __init__(self):
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to connect to database: {str(e)}")

    def get_tournaments(self):
        try:
            tournaments = self.db.query(Tournament).all()
            return tournaments
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to fetch tournaments: {str(e)}")

    def get_tournament(self, tournament_id: int):
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise ValueError(f"Tournament with id {tournament_id} not found")
            return tournament
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to fetch tournament {tournament_id}: {str(e)}")

    def create_tournament(self, data: TournamentInDBInput):
        try:
            new_tournament = Tournament(
                name=data.name, max_players=data.max_players, start_at=data.start_at
            )
            self.db.add(new_tournament)
            self.db.commit()
            self.db.refresh(new_tournament)
            return new_tournament
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Tournament with this name already exists in the database")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to create tournament: {str(e)}")

    def update_tournament(self, tournament_id: int, data: TournamentInDBInput):
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise ValueError(f"Tournament with id {tournament_id} not found")

            tournament.name = data.name
            tournament.max_players = data.max_players
            tournament.start_at = data.start_at

            self.db.commit()
            self.db.refresh(tournament)
            return tournament
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Tournament with this name already exists in the database")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to update tournament: {str(e)}")

    def delete_tournament(self, tournament_id: int) -> bool:
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise ValueError(f"Tournament with id {tournament_id} not found")

            self.db.delete(tournament)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Failed to delete tournament: {str(e)}")
