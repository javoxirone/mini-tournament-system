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
    TournamentNameExistsError,
)


class TournamentRepo:
    def __init__(self):
        """Initialize database connection."""
        try:
            self.db = SessionLocal()
        except SQLAlchemyError as e:
            raise TournamentDatabaseConnectionError(
                f"Failed to connect to database: {str(e)}"
            )

    def get_tournaments(self) -> list[TournamentInDBOutput]:
        """
        Fetch all tournaments from the database.

        :return: List of tournament data objects
        :rtype: list[TournamentInDBOutput]
        """
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
        """
        Fetch a single tournament by ID.

        :param tournament_id: ID of tournament to fetch
        :type tournament_id: int
        :return: Tournament data object
        :rtype: TournamentInDBOutput
        """
        try:
            tournament = (
                self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
            )
            if not tournament:
                raise TournamentNotFoundError(tournament_id)
            return TournamentInDBOutput.model_validate(tournament)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise TournamentFetchError(
                f"Failed to fetch tournament {tournament_id}: {str(e)}"
            )

    def create_tournament(self, data: TournamentInDBInput) -> TournamentInDBOutput:
        """
        Create a new tournament.

        :param data: Tournament input data
        :type data: TournamentInDBInput
        :return: Created tournament data
        :rtype: TournamentInDBOutput
        """
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
        """
        Update an existing tournament.

        :param tournament_id: ID of tournament to update
        :type tournament_id: int
        :param data: New tournament data
        :type data: TournamentInDBInput
        :return: Updated tournament data
        :rtype: TournamentInDBOutput
        """
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
        """
        Delete a tournament.

        :param tournament_id: ID of tournament to delete
        :type tournament_id: int
        :return: True if deletion successful
        :rtype: bool
        """
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
