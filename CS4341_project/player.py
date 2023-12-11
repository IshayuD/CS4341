from teamutils import positions, is_valid_position


class Player:
    def __init__(self, name: str, position: str, age: int, games: int, games_started: int, minutes_played: int,
                 current_team: str, point_avg: float, assist_avg: float, steal_avg: float, block_avg: float) -> None:
        """
        :param name: The player's name
        :param position: The player's position on a team
        :param age: The player's age
        :param games: The number of games the player has played in
        :param games_started: The number of games the player has started in (more significant than number of games)
        :param minutes_played: The number of minutes the player has played per game on average. Not included in other
        averages
        :param current_team: The player's current team
        :param point_avg: Average number of points per game
        :param assist_avg: Average assists per game
        :param steal_avg: Average number of steals a game
        :param block_avg: Average number of blocks a game
        """
        self.name = name
        self.position = position
        self.age = age
        self.games = games
        self.games_started = games_started
        self.minutes_played = minutes_played
        self.current_team = current_team  # Redundant field
        self.point_avg = point_avg
        self.assist_avg = assist_avg
        self.steal_avg = steal_avg
        self.block_avg = block_avg

    def is_valid_player(self) -> bool:
        """
        A function for determining if a player fits all constraints.\n
        Must be greater than 0: age, all averages\n
        Can be None: current_team, all averages\n
        Age must be greater than or equal 19 and less than 50\n

        Position must be a valid position (C, PF, SF, PG, or SG)
        :rtype: bool
        :returns: True if the player fits all constraints
        """
        constraints = [
            ('name', lambda x: len(x) <= 0 or x is None),
            ('position', lambda x: len(x) <= 0 or x is None or not is_valid_position(x)),
            ('age', lambda x: x < 19 or x > 50),
            ('games', lambda x: x < 0),
            ('games_started', lambda x: x < 0),
            ('minutes_played', lambda x: x < 0 or x > 500),
            ('current_team', lambda x: len(x) <= 0),  # TODO: Will likely cause a bug with remove_player (len(None) = 0)
            ('point_avg', lambda x: x < 0),
            ('assist_avg', lambda x: x < 0),
            ('steal_avg', lambda x: x < 0),
            ('block_avg', lambda x: x < 0)
        ]
        valid_player = True
        for attribute, constraint in constraints:
            value = getattr(self, attribute)
            if constraint(value):
                valid_player = False
                break
        return valid_player

    def __str__(self) -> str:
        if self.current_team is None:
            return self.name + ", NO TEAM"
        return self.name + ", " + self.current_team

    def __repr__(self) -> str:
        return "{" + self.__str__() + "}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.name.__eq__(other.name)


class InvalidPlayerError(Exception):
    def __init__(self, message="An invalid player was provided!"):
        self.message = message
        super().__init__(self.message)


class PlayerNotFoundError(Exception):
    def __init__(self, message="The player was not found!", player=None):
        self.player = player
        self.message = message
        if player is not None:
            self.message = "The player, " + player.name + ", was not found on the team!"

        super().__init__(self.message)
