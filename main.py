from commands.commands import CommandFactory
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--name')
    args = parser.parse_args()
    cmf = CommandFactory(args.name)
    cmd = cmf.create_command()
    cmd.execute()
