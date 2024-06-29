from commands.base import BaseCommand
from commands.show import Add, Cwd, Show, Update


class CommandFactory():

    def __init__(self, command_id: str) -> None:

        self.command_id = command_id

    def create_command(self) -> BaseCommand:

        match self.command_id:
            case 'show':
                return Show()
            case 'add':
                return Add()
            case 'cwd':
                return Cwd()
            case 'update':
                return Update()

        raise Exception(
            f"Command {self.command_id} is not available in the command factory")
