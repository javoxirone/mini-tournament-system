class PlayerBaseException(Exception):
    """Base exception for all player-related errors."""
    pass


class PlayerDatabaseConnectionError(PlayerBaseException):
    """Raised when unable to connect to the database."""
    def __init__(self, message="Failed to connect to database"):
        self.message = message
        super().__init__(self.message)


class PlayerFetchError(PlayerBaseException):
    """Raised when there's an error fetching players."""
    def __init__(self, message="Failed to fetch players"):
        self.message = message
        super().__init__(self.message)


class PlayerNotFoundError(PlayerBaseException):
    """Raised when a requested player is not found."""
    def __init__(self, player_id=None):
        self.player_id = player_id
        self.message = f"Player with id {player_id} not found" if player_id else "Player not found"
        super().__init__(self.message)


class PlayerCreationError(PlayerBaseException):
    """Raised when there's an error creating a player."""
    def __init__(self, message="Failed to create player"):
        self.message = message
        super().__init__(self.message)


class PlayerUpdateError(PlayerBaseException):
    """Raised when there's an error updating a player."""
    def __init__(self, message="Failed to update player"):
        self.message = message
        super().__init__(self.message)


class PlayerDeletionError(PlayerBaseException):
    """Raised when there's an error deleting a player."""
    def __init__(self, message="Failed to delete player"):
        self.message = message
        super().__init__(self.message)


class PlayerEmailExistsError(PlayerBaseException):
    """Raised when attempting to create or update a player with an email that already exists in the tournament."""
    def __init__(self, email=None, tournament_id=None):
        self.email = email
        self.tournament_id = tournament_id
        if email and tournament_id:
            self.message = f"Player with email '{email}' already exists in tournament {tournament_id}"
        elif email:
            self.message = f"Player with email '{email}' already exists in the tournament"
        else:
            self.message = "Player with this email already exists in the tournament"
        super().__init__(self.message)


class TournamentPlayerLimitError(PlayerBaseException):
    """Raised when attempting to add a player to a tournament that has reached its player limit."""
    def __init__(self, tournament_id=None):
        self.tournament_id = tournament_id
        self.message = f"Tournament {tournament_id} has reached its player limit" if tournament_id else "Tournament has reached its player limit"
        super().__init__(self.message)