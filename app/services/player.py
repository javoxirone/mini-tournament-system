from fastapi import HTTPException
from app.exceptions.player import (
    PlayerEmailExistsError,
    PlayerCreationError,
    PlayerNotFoundError,
    PlayerFetchError,
    PlayerUpdateError,
    PlayerDeletionError,
)
from app.repositories.player import PlayerRepo
from app.schemas.player import PlayerInDBInput, PlayerInDBOutput


def create_player(data: PlayerInDBInput) -> PlayerInDBOutput:
    """
    Creates new player on the database.

    :param data: Player data.
    :type data: PlayerInDBInput

    :return: New player data.
    :rtype: PlayerInDBOutput
    """
    player_repo = PlayerRepo()
    try:
        new_player = player_repo.create_player(data)
        return new_player
    except PlayerEmailExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PlayerCreationError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_player(player_id: int) -> PlayerInDBOutput:
    """
    Fetches single player based on player_id.

    :param player_id: Player ID.
    :type player_id: int

    :return: Player data.
    :rtype: PlayerInDBOutput
    """
    player_repo = PlayerRepo()
    try:
        return player_repo.get_player(player_id)
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_players() -> list[PlayerInDBOutput]:
    """
    Fetches the list of players from the database.

    :return: List of players.
    :rtype: list[PlayerInDBOutput]
    """
    player_repo = PlayerRepo()
    try:
        return player_repo.get_players()
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_players_by_tournament(tournament_id: int) -> list[PlayerInDBOutput]:
    """
    Fetches the list of players based on tournament_id.

    :param tournament_id: Tournament ID.
    :type tournament_id: int

    :return: List of players.
    :rtype: list[PlayerInDBOutput]
    """
    player_repo = PlayerRepo()
    try:
        return player_repo.get_players_by_tournament(tournament_id)
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_players_count_by_tournament(tournament_id: int) -> int:
    """
    Fetches the number of registered players in a tournament.

    :param tournament_id: Tournament ID.
    :type tournament_id: int

    :return: Number of registered players.
    :rtype: int
    """
    player_repo = PlayerRepo()
    try:
        return player_repo.get_players_count_by_tournament(tournament_id)
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_player(player_id: int, data: PlayerInDBInput) -> PlayerInDBOutput:
    """
    Updates the player data based on player_id.

    :param player_id: Player ID.
    :type player_id: int

    :param data: Player data.
    :type data: PlayerInDBInput

    :return: Updated player data.
    :rtype: PlayerInDBOutput
    """
    player_repo = PlayerRepo()
    try:
        updated_player = player_repo.update_player(player_id, data)
        return updated_player
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerEmailExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PlayerUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_player(player_id: int) -> bool:
    """
    Deletes a player based on player_id.

    :param player_id: Player ID.
    :type player_id: int

    :return: True if the player was deleted successfully, False otherwise.
    :rtype: bool
    """
    player_repo = PlayerRepo()
    try:
        return player_repo.delete_player(player_id)
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerDeletionError as e:
        raise HTTPException(status_code=500, detail=str(e))
