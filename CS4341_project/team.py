from player import Player, InvalidPlayerError, PlayerNotFoundError
from teamutils import all_averages


class Team:
    def __init__(self, team_id: int, name: str, player_count: int, cap_space: float,
                 point_avg: float, assist_avg: float, rebound_avg: float, steal_avg: float,
                 block_avg: float, turnover_avg: float) -> None:
        """
        :param team_id: The team's ID
        :param name: The team name
        :param player_count: Number of players on the team
        :param cap_space: The salary cap of the team in US dollars
        :param point_avg: The average points on the team
        :param assist_avg: The average assists on the team
        :param rebound_avg: The rebound average on the team
        :param steal_avg: The average steals on the team
        :param block_avg: The average blocks on the team
        :param turnover_avg: The average turnovers on the team
        """
        self.team_id = team_id
        self.name = name
        self.player_count = player_count
        self.cap_space = cap_space
        self.point_avg = point_avg
        self.assist_avg = assist_avg
        self.rebound_avg = rebound_avg
        self.steal_avg = steal_avg
        self.block_avg = block_avg
        self.turnover_avg = turnover_avg

        self.players = None
        self.initialize_values()

    def initialize_values(self) -> None:
        """
        Initializes the values of the team.
        player_count = 0
        cap_space = 0
        all averages = 0
        :return:
        """
        # Initialize player count to 0
        if self.player_count is None:
            self.player_count = 0

        # Initialize cap space to 0
        if self.cap_space is None:
            self.cap_space = 0

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

    def increase_cap(self, amount) -> None:
        """
        Increases the cap by the provided amount
        :param amount: The amount to increase the cap by
        """
        self.cap_space = self.cap_space + amount

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
        if not self.players.__contains__(player):
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
        if not self.players.__contains__(player):
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
        if not self.players.__contains__(player):
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
        if not self.players.__contains__(player):
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


class TooManyPlayersError(Exception):
    def __init__(self, message="Too many players!"):
        self.message = message
        super().__init__(self.message)
