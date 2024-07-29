import os

if __name__ == '__main__':

    cont = input(
        "[WARNING] Running the setup.py file will remove any previous installation's config you had. Enter y to continue: ")

    if cont == 'y':

        install_path = input("Enter the path of your installation. IE Where the main.py file is located: ")

        file_path_base = os.path.join(
            os.environ['HOME'], '.qn')
        file_path = os.path.join(file_path_base, 'config.sh')
        os.remove(file_path)
        os.makedirs(file_path_base, exist_ok=True)
        with open(file_path, 'a') as file:
            file.write(
                f"alias s='python  {install_path}/main.py --name show; source ~/.qn/curr_aliases.sh'\n")
            file.write(
                f"alias a='python  {install_path}/main.py --name add; source ~/.qn/curr_aliases.sh'\n")
            file.write(
                f"alias r='python  {install_path}/main.py --name remove; source ~/.qn/curr_aliases.sh'\n")
            file.write(
                f"alias c='python  {install_path}/main.py --name cwd; source ~/.qn/curr_aliases.sh'\n")
            file.write(
                f"alias u='python  {install_path}/main.py --name udpate; source ~/.qn/curr_aliases.sh'\n")

        print("""Setup completed. Please enter the line `~/.qn/config.sh` in your .bashrc and source it.""")
    else:
        print("The setup was not completed")
