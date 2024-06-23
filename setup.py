import os

if __name__ == '__main__':
    bashrc_path = os.path.join(
        os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'], '.bashrc')
    with open(bashrc_path, 'a') as file:
        file.write('\n#HARP SET UP STUFF\n')
        file.write("alias s='python -m quick_navigate.main -s'\n")
        file.write("alias a='python -m quick_navigate.main -a'\n")
        file.write("alias r='python -m quick_navigate.main -r'\n")
        file.write("alias c='python -m quick_navigate.main -c'\n")
        file.write('#HARP SET UP STUFF\n')
