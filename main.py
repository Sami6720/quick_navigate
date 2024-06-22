import os
from typing import Dict, List, Tuple


class Quick_Navigate():

    def __init__(self) -> None:
        #TODO: Need to make this better
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

    def collect_aliases(self) -> List[Dict[str, str]]:
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

        d: List[Dict[str, str]] = []
        for i in range(s+1, e, 1):
            d.append(self.parse_alias(self.lines[i]))

        return d

    def parse_alias(self, line: str) -> Dict[str, str]:
        """Parse alias

            Example alias
            alias cppu='salloc -c 4 --mem=20G -t 6:00:00' #NAME:cppu#CONTENT:...#TIMESTAMP:...#TYPE:...
        """

        attrs = line.split('#')
        attrs.pop(0)

        d = {}
        for attr in attrs:
            key, val = attr.split('::')
            d[key.strip()] = val.strip()

        return d

    def show_aliases(self) -> None:
        alias_sort = sorted(self.aliaes, key=lambda x: x['NAME'])

        print(self.table_format.format('Name', 'Content'))
        for alias in alias_sort:
            print(self.table_format.format(alias['NAME'], alias['CONTENT']))

    def create_alias_string(self, name, content, time) -> str:
        alias_string = f"alias {name}='{content}' #NAME:{name}#CONTENT:{content}#TIMESTAMP:{time}"
        return alias_string

    def add_alias(self):
        raise NotImplementedError

    def remove_alias(self):
        raise NotImplementedError

    def update_alias(self):
        raise NotImplementedError


if __name__ == '__main__':
    qn = Quick_Navigate()
    qn.show_aliases()
