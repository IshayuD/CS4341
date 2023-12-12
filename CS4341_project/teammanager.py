from player import Player
from team import Team, TeamNotFoundError, TooManyPlayersError


class TeamManager:
    """
    A class meant to manage the teams.
    """
    def __init__(self):
        self.teams = []

    def add_team(self, team: Team) -> None:
        """
        Adds a team to the teams list
        :param team:
        :raises TeamExistsError: Raised if the team already exists
        """
        if self.is_existing_team(team):
            raise TeamExistsError(team=team)
        self.teams.append(team)

    def is_existing_team(self, team: Team | str) -> bool:
        """
        Checks if the provided team is already in the teams list
        :param team: The team to check
        :return: True if the team is already in the teams list, False otherwise
        """
        if type(team) is str:
            for team_inst in self.teams:
                if team_inst.name == team:
                    return True
            return False
        return any(team.__eq__(t) for t in self.teams)

    def get_team(self, team_name: str) -> Team:
        """
        :param team_name: The name of the team to get
        :return: The team
        :raises TeamNotFoundError: Raised if the provided team is not found
        """
        for team_inst in self.teams:
            if team_inst.name == team_name:
                return team_inst
        raise TeamNotFoundError(team_name)

    def update_teams(self, new_player: Player, current_team: str) -> None:
        """
        Isolates updating the team. Creates a new team in home#teams if the team does not exist yet.
        :param new_player: The new player to add
        :param current_team: The team to add/add player to
        """
        if self.is_existing_team(current_team):
            # Add to existing team
            new_team = self.get_team(current_team)
            try:
                new_team.add_player(new_player)
            except TooManyPlayersError:
                new_player.__setattr__('current_team', None)
            return

        # Create team
        new_team = Team(name=current_team, player_count=0, point_avg=0, assist_avg=0, steal_avg=0,
                        block_avg=0)
        # Add team
        self.add_team(new_team)
        new_team.add_player(new_player)

    def print_teams(self) -> None:
        """
        Prints the teams. Primarily for testing purposes
        """
        print(*self.teams)


class TeamExistsError(Exception):
    def __init__(self, message="The team already exists!", team=None):
        self.team = team
        self.message = message
        if team is not None:
            if type(team) is Team:
                self.message = "The team, " + team.name + ", is already a team!"
            elif type(team) is str:
                self.message = "The team, " + team + ", is already a team!"

        super().__init__(self.message)
