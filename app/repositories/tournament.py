from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db import SessionLocal
from app.models import Tournament
from app.schemas.tournament import TournamentInDBInput, TournamentInDBOutput
from app.exceptions.tournament import (
    TournamentDatabaseConnectionError,
    TournamentFetchError,
    TournamentNotFoundError,
    TournamentCreationError,
    TournamentUpdateError,
    TournamentDeletionError,
    TournamentNameExistsError
)


class TournamentRepo:
    def __init__(self):
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise TournamentDatabaseConnectionError(f"Failed to connect to database: {str(e)}")

    def get_tournaments(self) -> list[TournamentInDBOutput]:
        try:
            tournaments = self.db.query(Tournament).all()
            return [
                TournamentInDBOutput.model_validate(tournament)
                for tournament in tournaments
            ]
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentFetchError(f"Failed to fetch tournaments: {str(e)}")

    def get_tournament(self, tournament_id: int) -> TournamentInDBOutput:
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise TournamentNotFoundError(tournament_id)
            return TournamentInDBOutput.model_validate(tournament)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentFetchError(f"Failed to fetch tournament {tournament_id}: {str(e)}")

    def create_tournament(self, data: TournamentInDBInput) -> TournamentInDBOutput:
        try:
            new_tournament = Tournament(
                name=data.name, max_players=data.max_players, start_at=data.start_at
            )
            self.db.add(new_tournament)
            self.db.commit()
            self.db.refresh(new_tournament)
            return TournamentInDBOutput.model_validate(new_tournament)
        except IntegrityError:
            self.db.rollback()
            raise TournamentNameExistsError(data.name)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentCreationError(f"Failed to create tournament: {str(e)}")

    def update_tournament(
        self, tournament_id: int, data: TournamentInDBInput
    ) -> TournamentInDBOutput:
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise TournamentNotFoundError(tournament_id)

            tournament.name = data.name
            tournament.max_players = data.max_players
            tournament.start_at = data.start_at

            self.db.commit()
            self.db.refresh(tournament)
            return TournamentInDBOutput.model_validate(tournament)
        except IntegrityError:
            self.db.rollback()
            raise TournamentNameExistsError(data.name)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentUpdateError(f"Failed to update tournament: {str(e)}")

    def delete_tournament(self, tournament_id: int) -> bool:
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise TournamentNotFoundError(tournament_id)

            self.db.delete(tournament)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentDeletionError(f"Failed to delete tournament: {str(e)}")