from fastapi import HTTPException

from app.repositories.tournament import TournamentRepo
from app.schemas.tournament import TournamentInDBOutput, TournamentInDBInput
from app.exceptions.tournament import (
    TournamentBaseException,
    TournamentFetchError,
    TournamentNotFoundError,
    TournamentCreationError,
    TournamentUpdateError,
    TournamentDeletionError,
    TournamentNameExistsError,
)


def create_tournament(data: TournamentInDBInput) -> TournamentInDBOutput:
    """
    This service creates a new tournament in the database and returns tournament data.

    :param data: Input data for the new tournament.
    :type data: TournamentInDBInput

    :return: Tournament data for the newly created tournament.
    :rtype: TournamentInDBOutput
    """
    tournament_repo = TournamentRepo()
    try:
        tournament = tournament_repo.create_tournament(data)
        return tournament
    except TournamentNameExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TournamentCreationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TournamentBaseException as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_tournament(tournament_id: int) -> TournamentInDBOutput:
    """
    Fetches a tournament from the database by its ID and handles exceptions.

    :param tournament_id: The ID of the tournament to fetch.
    :type tournament_id: int

    :return: The fetched tournament data.
    :rtype: TournamentInDBOutput
    """
    tournament_repo = TournamentRepo()
    try:
        tournament = tournament_repo.get_tournament(tournament_id)
        return tournament
    except TournamentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TournamentFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TournamentBaseException as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_tournaments() -> list[TournamentInDBOutput]:
    """
    Fetches a list of tournaments from the repository.

    :return: A list of tournament data.
    :rtype: list[TournamentInDBOutput]
    """
    tournament_repo = TournamentRepo()
    try:
        tournaments = tournament_repo.get_tournaments()
        return tournaments
    except TournamentFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TournamentBaseException as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_tournament(
    tournament_id: int, data: TournamentInDBInput
) -> TournamentInDBOutput:
    """
    Updated the existing tournament data on the database.

    :param tournament_id: The ID of the tournament to update.
    :type tournament_id: int

    :param data: The updated tournament data.
    :type data: TournamentInDBInput

    :return: The updated tournament data.
    :rtype: TournamentInDBOutput
    """
    tournament_repo = TournamentRepo()
    try:
        updated_tournament = tournament_repo.update_tournament(tournament_id, data)
        return updated_tournament
    except TournamentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TournamentNameExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TournamentUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TournamentBaseException as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_tournament(tournament_id: int) -> bool:
    """
    Deletes a tournament from the database.

    :param tournament_id: The ID of the tournament to delete.
    :type tournament_id: int

    :return: True if the tournament was deleted successfully, False otherwise.
    :rtype: bool
    """
    tournament_repo = TournamentRepo()
    try:
        return tournament_repo.delete_tournament(tournament_id)
    except TournamentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TournamentDeletionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except TournamentBaseException as e:
        raise HTTPException(status_code=500, detail=str(e))