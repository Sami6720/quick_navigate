import os
from typing import List, Tuple
from datetime import datetime


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
        self.bashrc_path = os.path.join(
            os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'], '.bashrc')
        self.harp_stuff = '#HARP STUFF\n'
        self.create_bashrc_file()
        with open(self.bashrc_path, 'r') as file:
            self.lines = file.readlines()
        self.aliaes = self.collect_aliases()
        self.table_format = "{:<8} {:<25}"
        self.harp_stuff_start_end = self.find_start_end()

    def create_bashrc_file(self) -> None:

        if '.bashrc' not in os.listdir(os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']):
            with open(self.bashrc_path):
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
        alias_sort = sorted(self.aliaes, key=lambda x: x.name)

        print(self.table_format.format('Name', 'Content'))
        for alias in alias_sort:
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
        with open(self.bashrc_path, 'w') as file:
            file.writelines(self.lines)

    def add_alias(self, name: str, content: str) -> None:

        self.aliaes.append(
            Alias(name=name, content=content,
                  time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        )
        self.insert_aliases_into_lines()
        self.write_out_lines()

    def remove_alias(self, name: str):

        for idx, alias in enumerate(self.aliaes):
            if alias.name == name:
                self.aliaes.pop(idx)
                self.insert_aliases_into_lines()
                self.write_out_lines()
                return

        print(f"Alias doesn't exisit")

    def update_alias(self):
        raise NotImplementedError


if __name__ == '__main__':
    qn = Quick_Navigate()
    qn.show_aliases()

