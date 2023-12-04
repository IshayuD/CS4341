from teamutils import positions


class Player:
    def __init__(self, player_id: int, name: str, position: str, height: float, weight: float, age: int,
                 years_of_exp: int, salary: float, current_team: str, point_avg: float,
                 assist_avg: float, steal_avg: float, block_avg: float) -> None:
        """
        :param player_id: The player's ID
        :param name: The player's name
        :param position: The player's position on a team
        :param height: The player's height in inches
        :param weight: The player's weight in lbs
        :param age: The player's age
        :param years_of_exp: How many years of experience the player has under their belt
        :param salary: The player's salary
        :param current_team: The player's current team
        :param point_avg: Average number of points per game
        :param assist_avg: Average assists per game
        :param steal_avg: Average number of steals a game
        :param block_avg: Average number of blocks a game
        """
        self.player_id = player_id
        self.name = name
        self.position = position
        self.height = height
        self.weight = weight
        self.age = age
        self.years_of_exp = years_of_exp
        self.salary = salary
        self.current_team = current_team  # Redundant field
        self.point_avg = point_avg
        self.assist_avg = assist_avg
        self.steal_avg = steal_avg
        self.block_avg = block_avg

        # No YOE is the same as 0 YOE
        if self.years_of_exp is None:
            self.years_of_exp = 0

    def is_valid_player(self) -> bool:
        """
        A function for determining if a player fits all constraints.\n
        Must be greater than 0: height, weight, age, salary, all averages\n
        Can be None: years_of_exp, current_team, all averages\n
        Age must be greater than or equal 19 and less than 50\n
        years_of_exp can be 0, but must be 31 or less (max age - min age)\n
        Position must be a valid position (C, PF, SF, PG, or SG)
        :rtype: bool
        :returns: True if the player fits all constraints
        """
        constraints = [
            ('player_id', lambda x: x < 0 or x is None),
            ('name', lambda x: len(x) <= 0 or x is None),
            ('position', lambda x: len(x) <= 0 or x is None or not positions.__contains__(x)),
            ('height', lambda x: x <= 0 or x > 500),
            ('weight', lambda x: x <= 0 or x > 500),
            ('age', lambda x: x < 19 or x > 50),
            ('years_of_exp', lambda x: x < 0 or x > 31),
            ('salary', lambda x: x <= 0),
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

    def __str__(self):
        return self.name + ", " + self.current_team


class InvalidPlayerError(Exception):
    def __init__(self, message="An invalid player was provided!"):
        self.message = message
        super().__init__(self.message)


class PlayerNotFoundError(Exception):
    def __init__(self, message="The player was not found!", player=None):
        self.player = player
        self.message = message
        if player is not None:
            self.message = "The player, " + player + ", was not found on the team!"

        super().__init__(self.message)