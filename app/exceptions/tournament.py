class TournamentBaseException(Exception):
    """Base exception for all tournament-related errors."""
    pass


class TournamentDatabaseConnectionError(TournamentBaseException):
    """Raised when unable to connect to the database."""
    def __init__(self, message="Failed to connect to database"):
        self.message = message
        super().__init__(self.message)


class TournamentFetchError(TournamentBaseException):
    """Raised when there are error fetching tournaments."""
    def __init__(self, message="Failed to fetch tournaments"):
        self.message = message
        super().__init__(self.message)


class TournamentNotFoundError(TournamentBaseException):
    """Raised when a requested tournament is not found."""
    def __init__(self, tournament_id=None):
        self.tournament_id = tournament_id
        self.message = f"Tournament with id {tournament_id} not found" if tournament_id else "Tournament not found"
        super().__init__(self.message)


class TournamentCreationError(TournamentBaseException):
    """Raised when there's an error creating a tournament."""
    def __init__(self, message="Failed to create tournament"):
        self.message = message
        super().__init__(self.message)


class TournamentUpdateError(TournamentBaseException):
    """Raised when there's an error updating a tournament."""
    def __init__(self, message="Failed to update tournament"):
        self.message = message
        super().__init__(self.message)


class TournamentDeletionError(TournamentBaseException):
    """Raised when there's an error deleting a tournament."""
    def __init__(self, message="Failed to delete tournament"):
        self.message = message
        super().__init__(self.message)


class TournamentNameExistsError(TournamentBaseException):
    """Raised when attempting to create or update a tournament with a name that already exists."""
    def __init__(self, name=None):
        self.name = name
        self.message = f"Tournament with name '{name}' already exists" if name else "Tournament with this name already exists in the database"
        super().__init__(self.message)