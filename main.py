import os
from typing import List, Tuple
from datetime import datetime
import argparse
from subprocess import run


class Alias():

    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name']
        self.content = kwargs['content']
        self.time = kwargs['time']

    def create_alias_string(self) -> str:
        alias_string = f"alias {self.name}='{self.content}' #NAME::{self.name}#CONTENT::{self.content}#TIME::{self.time}\n"
        return alias_string


class Quick_Navigate():

    def __init__(self) -> None:
        # TODO: Need to make this better
        self.curr_aliases_file_path = os.path.join(
            os.environ['HOME'], '.qn', 'curr_aliases.sh')
        self.harp_stuff = '#HARP STUFF\n'
        self.create_bashrc_file()
        with open(self.curr_aliases_file_path, 'r') as file:
            self.lines = file.readlines()
        self.aliaes = self.collect_aliases()
        self.table_format = "{:<8} {:<25}"
        self.harp_stuff_start_end = self.find_start_end()

    def create_bashrc_file(self) -> None:

        if 'curr_aliases.sh' not in os.listdir(os.path.join(
                os.environ['HOME'], '.qn')):
            with open(self.curr_aliases_file_path, 'a'):
                pass

    def find_start_end(self, ) -> Tuple[int, int]:

        s = 0
        for i in range(len(self.lines)):
            if self.lines[i] == self.harp_stuff:
                s = i
                break
        e = 0
        for j in range(len(self.lines) - 1, 0, -1):
            if self.lines[j] == self.harp_stuff:
                e = j
                break

        return s, e

    def collect_aliases(self) -> List[Alias]:
        """
        Collects all aliases and writes out harp stuff if not in lines.
        So next time needs to be written out.
        """

        s, e = self.find_start_end()

        if e == 0:
            self.lines.append(self.harp_stuff)
            self.lines.append(self.harp_stuff)
            s = len(self.lines) - 2
            e = len(self.lines) - 1

        d: List[Alias] = []
        for i in range(s+1, e, 1):
            d.append(self.parse_alias(self.lines[i]))

        return d

    def parse_alias(self, line: str) -> Alias:
        """Parse alias

            Example alias
            #NAME:cppu#CONTENT:...#TIMESTAMP:...#TYPE:...
            alias cppu='salloc -c 4 --mem=20G -t 6:00:00'
        """

        attrs = line.split('#')
        attrs.pop(0)

        d = {}
        for attr in attrs:
            key, val = attr.split('::')
            d[key.strip().lower()] = val.strip()

        alias = Alias(**d)

        return alias

    def show_aliases(self) -> None:
        alias_sort = sorted(self.aliaes, key=lambda x: datetime.strptime(
            x.time, "%d/%m/%Y, %H:%M:%S"), reverse=True)

        print(self.table_format.format('Name', 'Content'))
        for alias in alias_sort[:5]:
            print(self.table_format.format(alias.name, alias.content))

    def insert_aliases_into_lines(self):

        s, e = self.find_start_end()
        assert s != e

        for _ in range(s + 1, e):
            self.lines.pop(s + 1)

        for alias in self.aliaes:
            # +1 because we want to insert between self.harp_stuff
            self.lines.insert(s + 1, alias.create_alias_string())

    def write_out_lines(self):
        with open(self.curr_aliases_file_path, 'w') as file:
            file.writelines(self.lines)

    def check_name_exists(self, name: str):
        for alias in self.aliaes:
            if alias.name == name:
                return True
        return False

    def add_alias(self, name: str, content: str) -> None:

        self.aliaes.append(
            Alias(name=name, content=content,
                  time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        )
        self.insert_aliases_into_lines()
        self.write_out_lines()

    def remove_alias(self, name: str):
        #TODO: Need to fix why even after removal alias runs. Need to unset probably.

        for idx, alias in enumerate(self.aliaes):
            if alias.name == name:
                self.aliaes.pop(idx)
                self.insert_aliases_into_lines()
                self.write_out_lines()
                return

        print(f"Alias doesn't exisit")

    def update_alias(self, name, new_content, new_name):
        for idx, alias in enumerate(self.aliaes):
            if alias.name == name:
                alias_m = self.aliaes.pop(idx)
                alias_m.name = new_name
                alias_m.content = new_content
                self.aliaes.append(alias_m)
                self.insert_aliases_into_lines()
                self.write_out_lines()
                return

        print(f"Alias doesn't exisit")


    def get_alias(self, name: str) -> Alias:

        for x in self.aliaes:
            if x.name == name:
                return x

        raise ValueError(f"Alias {name} not found")

if __name__ == '__main__':

    #TODO: Add KeyboardInterrupt Exception handling.

    parser = argparse.ArgumentParser()

    parser.add_argument('--show', '-s', action='store_true')
    parser.add_argument('--add', '-a', action='store_true')
    parser.add_argument('--remove', '-r', action='store_true')
    parser.add_argument('--update', '-u', action='store_true')
    parser.add_argument('--cwd', '-c', action='store_true')

    args = parser.parse_args()

    qn = Quick_Navigate()

    if args.show:
        qn.show_aliases()

    if args.add:
        alias_name = input('Enter the name of the alias to create\n')
        while qn.check_name_exists(alias_name):
            print(f"Name already exists. Pick another name")
            alias_name = input()
        run("rm -rf ~/.qn/temp_add.sh;", shell=True)
        run(f"nvim -f ~/.qn/temp_add.sh", shell=True)
        try:
            with open(os.path.expanduser("~/.qn/temp_add.sh"), "r") as f:
                line = f.readline()
            alias_content = line.strip()
            qn.add_alias(name=alias_name, content=alias_content)
            qn.show_aliases()
        except FileNotFoundError as e:
            print("Content File not saved. Make sure to do :w after you add your content")

    if args.remove:
        qn.show_aliases()
        qn.remove_alias(
            input(f"Enter the name of the alias you want to remove\n"))
        qn.show_aliases()

    if args.update:
        qn.show_aliases()
        alias_name = input(
            'Please enter the name of the alias you wanted update\n')

        while not qn.check_name_exists(alias_name):
            print(f"Alias doesn't exist.")
            alias_name = input()

        run("rm -rf ~/.qn/temp_update.sh;", shell=True)
        alias = qn.get_alias(alias_name)
        run(f"nvim -c 'normal i{alias.content}' -f ~/.qn/temp_update.sh", shell=True)
        try:
            with open(os.path.expanduser("~/.qn/temp_update.sh"), "r") as f:
                line = f.readline()

            new_c = line.strip()
            qn.update_alias(alias_name, new_c, alias_name)
            qn.show_aliases()

        except FileNotFoundError as e:
            print(f"Press :w to make sure the update you made is saved and used")

    if args.cwd:
        cwd = os.getcwd()
        content = f'cd {cwd};'
        alias_name = input('Enter the name of the alias to create\n')
        while qn.check_name_exists(alias_name):
            print(f"Name already exists. Pick another name")
            alias_name = input()
        run("rm -rf ~/.qn/temp_cwd_add.sh;", shell=True)
        run(f"nvim -c 'normal i{content.strip()}' -f ~/.qn/temp_cwd_add.sh", shell=True)
        try:
            with open(os.path.expanduser("~/.qn/temp_cwd_add.sh"), "r") as f:
                line = f.readline()
            alias_content = line.strip()
            qn.add_alias(name=alias_name, content=alias_content)
            qn.show_aliases()
        except FileNotFoundError as e:
            print("Your add content file was not saved. Make sure to :w after you add your content")
