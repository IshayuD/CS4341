from player import Player, InvalidPlayerError, PlayerNotFoundError
from teamutils import all_averages


class Team:
    def __init__(self, name: str, player_count: int, point_avg: float, assist_avg: float, steal_avg: float,
                 block_avg: float) -> None:
        """
        :param name: The team name
        :param player_count: Number of players on the team
        :param point_avg: The average points on the team
        :param assist_avg: The average assists on the team
        :param steal_avg: The average steals on the team
        :param block_avg: The average blocks on the team
        """
        self.name = name
        self.player_count = player_count
        self.point_avg = point_avg
        self.assist_avg = assist_avg
        self.steal_avg = steal_avg
        self.block_avg = block_avg

        self.players = None
        self.initialize_values()

    def __str__(self) -> str:
        if self.players is None:
            return self.name + ", NO PLAYERS"
        return self.name + ", " + str(self.players)

    def __repr__(self) -> str:
        return "{" + self.__str__() + "}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Team):
            return False
        return self.name.__eq__(other.name)

    def initialize_values(self) -> None:
        """
        Initializes the values of the team.
        player_count = 0
        all averages = 0
        :return:
        """
        # Initialize player count to 0
        if self.player_count is None:
            self.player_count = 0

        # Initialize all the averages to 0
        for avg in all_averages:
            value = getattr(self, avg)
            if value is None:
                setattr(self, avg, 0)

        # Initialize players to a list
        self.players = []

    def find_player(self) -> Player:
        """
        Find the ideal player for the team
        :return: The computed main player for the team
        """
        # TODO: Implement this.
        raise NotImplementedError

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team if player_count is less than 17
        :param player: The player to add to the team
        :raises InvalidPlayerError: Raises if an invalid player is provided
        :raises TooManyPlayersError: Raises if there are 17 or more players on the team
        """
        # Validate player
        if not player.is_valid_player():
            raise InvalidPlayerError

        if self.player_count >= 17:
            raise TooManyPlayersError

        # Check if player is on the team.
        if not self.player_in_team(player):
            # Add player to players
            self.players.append(player)

            # Update related values (with error handling)
            self.player_count = self.player_count + 1

            # Try-catch statement to check if there was a problem
            # If there is an error, undo what was just done and raise the error
            # If there are no errors, update the player's attribute (irreversible)
            try:
                self.add_player_to_averages(player)
            except InvalidPlayerError | PlayerNotFoundError as err:
                self.player_count = self.player_count - 1
                self.players.remove(player)
                raise err
            else:
                # Player was successfully added
                # Update player's current_team attribute
                player.__setattr__('current_team', self.name)

    def add_player_to_averages(self, player: Player) -> None:
        """
        Updates every average value in teamutils.all_averages to include player
        :param player: The player to update averages from
        :raises InvalidPlayerError: Raises if an invalid player is provided
        :raises PlayerNotFoundError: Raises if the player is not on the team
        """

        # Validate player
        if not player.is_valid_player():
            raise InvalidPlayerError

        # Check that player is on team
        if not self.player_in_team(player):
            raise PlayerNotFoundError

        # Update all averages
        # (Old Average * Old Count) + Added Average / New Count = New Average
        for avg in all_averages:
            player_avg = getattr(player, avg)
            team_avg = getattr(self, avg)
            updated_avg = (team_avg * (self.player_count - 1) + player_avg) / self.player_count
            setattr(self, avg, updated_avg)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team
        :param player: The player to remove from the team
        :raises InvalidPlayerError: Raises if an invalid player is provided
        :raises PlayerNotFoundError: Raises if the player is not on the team
        """
        # Validate player
        if not player.is_valid_player():
            raise InvalidPlayerError

        # Check that player is on team
        if not self.player_in_team(player):
            raise PlayerNotFoundError

        # Update related values (with error handling)
        self.player_count = self.player_count - 1

        # remove player from players
        self.players.remove(player)

        # Try-catch statement to check if there was a problem
        # If there is an error, undo what was just done and raise the error
        # If there are no errors, update the player's attribute (irreversible)
        try:
            self.remove_player_from_averages(player)
        except InvalidPlayerError | PlayerNotFoundError as err:
            self.player_count = self.player_count + 1
            self.players.append(player)
            raise err
        else:
            # Player was successfully removed
            # Update player's current_team attribute
            player.__setattr__('current_team', None)

    def remove_player_from_averages(self, player: Player) -> None:
        """
        Updates every average value in teamutils.all_averages to include player
        :param player: The player to update averages from
        :raises InvalidPlayerError: Raises if an invalid player is provided
        :raises PlayerNotFoundError: Raises if the player is not on the team
        """

        # Validate player
        if not player.is_valid_player():
            raise InvalidPlayerError

        # Check that player is on team
        if not self.player_in_team(player):
            raise PlayerNotFoundError

        # Update all averages
        # (Old Average * Old Count) - Removed Average / New Count = New Average
        for avg in all_averages:
            # If there is no one left on the team, set average to 0
            if self.player_count == 0:
                setattr(self, avg, 0)
                continue

            player_avg = getattr(player, avg)
            team_avg = getattr(self, avg)
            updated_avg = (team_avg * (self.player_count + 1) - player_avg) / self.player_count
            setattr(self, avg, updated_avg)

    def player_in_team(self, player: Player) -> bool:
        """
        :param player: The player to check if it is in players
        :return: True if the player is in players
        """
        # One-liner that sees if player is inside of self.players
        # Uses Player.__eq__() to compare two players
        return any(player.__eq__(p) for p in self.players)

    def is_valid_team(self) -> bool:
        """
        A function for determining if a team fits all constraints.\n
        Must be greater than 0: age, all averages\n
        Can be None: all averages
        :rtype: bool
        :returns: True if the player fits all constraints
        """
        constraints = [
            ('name', lambda x: len(x) <= 0 or x is None),
            ('player_count', lambda x: x < 0 or x is None),
            ('point_avg', lambda x: x < 0),
            ('assist_avg', lambda x: x < 0),
            ('steal_avg', lambda x: x < 0),
            ('block_avg', lambda x: x < 0)
        ]
        valid_team = True
        for attribute, constraint in constraints:
            value = getattr(self, attribute)
            if constraint(value):
                valid_team = False
                break
        return valid_team


class TooManyPlayersError(Exception):
    def __init__(self, message="Too many players!"):
        self.message = message
        super().__init__(self.message)


class TeamNotFoundError(Exception):
    def __init__(self, message="The team was not found!", team=None):
        self.team = team
        self.message = message
        if team is not None:
            if type(team) is Team:
                self.message = "The team, " + team.name + ", was not found!"
            elif type(team) is str:
                self.message = "The team, " + team + ", was not found!"

        super().__init__(self.message)


class InvalidTeamError(Exception):
    def __init__(self, message="An invalid team was provided!"):
        self.message = message
        super().__init__(self.message)
