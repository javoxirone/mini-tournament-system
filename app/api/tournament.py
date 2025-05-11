from fastapi import APIRouter

from app.schemas.player import PlayerInDBInput, PlayerInRequest, PlayerInDBOutput
from app.schemas.tournament import TournamentInDBOutput, TournamentInDBInput
from app.services.player import create_player, get_players_by_tournament
from app.services.tournament import (
    create_tournament,
    get_tournament,
    get_tournaments,
    update_tournament,
    delete_tournament,
)

router = APIRouter()


@router.post("/tournaments", response_model=TournamentInDBOutput, status_code=201)
async def create_tournament_api_view(
    tournament: TournamentInDBInput,
) -> TournamentInDBOutput:
    new_tournament = create_tournament(tournament)
    return new_tournament


@router.get(
    "/tournaments/{tournament_id}", response_model=TournamentInDBOutput, status_code=200
)
async def get_tournament_api_view(tournament_id: int) -> TournamentInDBOutput:
    tournament = get_tournament(tournament_id)
    return tournament


@router.get("/tournaments", response_model=list[TournamentInDBOutput], status_code=200)
async def get_tournament_api_view() -> list[TournamentInDBOutput]:
    tournaments = get_tournaments()
    return tournaments


@router.put(
    "/tournaments/{tournament_id}", response_model=TournamentInDBOutput, status_code=200
)
async def update_tournament_api_view(
    tournament_id: int, data: TournamentInDBInput
) -> TournamentInDBOutput:
    updated_tournament = update_tournament(tournament_id, data)
    return updated_tournament


@router.get(
    "/tournaments/{tournament_id}/players",
    response_model=list[PlayerInDBOutput],
    status_code=200,
)
async def get_players_by_tournament_api_view(
    tournament_id: int,
) -> list[PlayerInDBOutput]:
    players = get_players_by_tournament(tournament_id)
    return players


@router.post(
    "/tournaments/{tournament_id}/register",
    response_model=TournamentInDBOutput,
    status_code=201,
)
async def register_player_api_view(
    tournament_id: int, player_data: PlayerInRequest
) -> TournamentInDBOutput:
    extended_player_data = PlayerInDBInput(
        **player_data.__dict__, tournament_id=tournament_id
    )
    create_player(extended_player_data)
    player_registered_tournament = get_tournament(tournament_id)
    return player_registered_tournament


@router.delete("/tournaments/{tournament_id}", status_code=204)
async def delete_tournament_api_view(tournament_id: int) -> None:
    delete_tournament(tournament_id)