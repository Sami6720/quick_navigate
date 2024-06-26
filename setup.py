import os

if __name__ == '__main__':
    file_path_base = os.path.join(
        os.environ['HOME'], '.qn')
    file_path = os.path.join(file_path_base, 'config.sh')
    os.makedirs(file_path_base, exist_ok=True)
    with open(file_path, 'a') as file:
        file.write("alias s='python  ~/quick_navigate/main.py -s; source ~/.qn/curr_aliases.sh'n")
        file.write("alias a='python  ~/quick_navigate/main.py -a; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias r='python  ~/quick_navigate/main.py -r; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias c='python  ~/quick_navigate/main.py -c; source ~/.qn/curr_aliases.sh'\n")
