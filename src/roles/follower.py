from roles.role import Role


class Follower:
    def run(self) -> Role:
        return Role.CANDIDATE
