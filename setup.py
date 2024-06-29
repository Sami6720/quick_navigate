import os

if __name__ == '__main__':
    file_path_base = os.path.join(
        os.environ['HOME'], '.qn')
    file_path = os.path.join(file_path_base, 'config.sh')
    os.makedirs(file_path_base, exist_ok=True)
    with open(file_path, 'a') as file:
        file.write("alias s='python  ~/quick_navigate/main.py --name show; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias a='python  ~/quick_navigate/main.py --name add; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias r='python  ~/quick_navigate/main.py --name remove; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias c='python  ~/quick_navigate/main.py --name cwd; source ~/.qn/curr_aliases.sh'\n")
        file.write("alias u='python  ~/quick_navigate/main.py --name udpate; source ~/.qn/curr_aliases.sh'\n")
