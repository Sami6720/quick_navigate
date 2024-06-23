import os

if __name__ == '__main__':
    bashrc_path = os.path.join(
        os.environ['HOME'], '.bashrc')
    with open(bashrc_path, 'a') as file:
        file.write('\n#HARP SET UP STUFF\n')
        file.write("alias s='python  ~/quick_navigate/main.py -s'\n")
        file.write("alias a='python  ~/quick_navigate/main.py -a'\n")
        file.write("alias r='python  ~/quick_navigate/main.py -r'\n")
        file.write("alias c='python  ~/quick_navigate/main.py -c'\n")
        file.write('#HARP SET UP STUFF\n')
