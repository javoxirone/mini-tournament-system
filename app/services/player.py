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
    player_repo = PlayerRepo()
    try:
        new_player = player_repo.create_player(data)
        return new_player
    except PlayerEmailExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PlayerCreationError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_player(player_id: int) -> PlayerInDBOutput:
    player_repo = PlayerRepo()
    try:
        return player_repo.get_player(player_id)
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_players() -> list[PlayerInDBOutput]:
    player_repo = PlayerRepo()
    try:
        return player_repo.get_players()
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_players_by_tournament(tournament_id: int) -> list[PlayerInDBOutput]:
    player_repo = PlayerRepo()
    try:
        return player_repo.get_players_by_tournament(tournament_id)
    except PlayerFetchError as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_player(player_id: int, data: PlayerInDBInput) -> PlayerInDBOutput:
    player_repo = PlayerRepo()
    try:
        updated_player = player_repo.update_player(player_id, data)
        return updated_player
    except PlayerEmailExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PlayerUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_player(player_id: int) -> bool:
    player_repo = PlayerRepo()
    try:
        return player_repo.delete_player(player_id)
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerDeletionError as e:
        raise HTTPException(status_code=500, detail=str(e))
