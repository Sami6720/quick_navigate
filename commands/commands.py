import os
from commands.base import BaseCommand

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
            case 'remove':
                return Remove()

        raise Exception(
            f"Command {self.command_id} is not available in the command factory")

class Show(BaseCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        self.qn.show_aliases()


class Add(BaseCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        alias_name = input('Enter the name of the alias to create\n')
        while self.qn.check_name_exists(alias_name):
            print(f"Name already exists. Pick another name")
            alias_name = input()
        alias_content = input('Enter the content of the alias\n')
        self.qn.add_alias(name=alias_name, content=alias_content)
        self.qn.show_aliases()


class Remove(BaseCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        self.qn.show_aliases()
        self.qn.remove_alias(
            input(f"Enter the name of the alias you want to remove\n"))
        self.qn.show_aliases()


class Update(BaseCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        self.qn.show_aliases()
        alias_name = input(
            'Please enter the name of the alias you wanted update\n')
        new_n = input('Please enter new name\n')
        while self.qn.check_name_exists(new_n):
            print(f"Name already exists. Pick another name")
            new_n = input()
        new_c = input('Please enter new content\n')
        self.qn.update_alias(alias_name, new_c, new_n)
        self.qn.show_aliases()


class Cwd(BaseCommand):

    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        cwd = os.getcwd()
        content = f'cd {cwd};'
        alias_name = input('Enter the name of the alias to create\n')
        while self.qn.check_name_exists(alias_name):
            print(f"Name already exists. Pick another name")
            alias_name = input()
        alias_content = input(
            f'Current content is: {content}\nEnter the content to add after nav to cwd\n')
        self.qn.add_alias(name=alias_name, content=content + alias_content)
        self.qn.show_aliases()
