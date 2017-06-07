import subprocess


def get_input(question, default=""):
    add = "[{}] ".format(default) if default != "" else ""
    user = input("{}: {}".format(question, add)).strip()
    if user == "":
        user = default
    return user


def get_yes(question, yes=False):
    user = input("{}: [{}] ".format(question, 'yes' if yes is True else 'no')).strip().lower()
    return user in ('yes', 'y')


def call(command):
    command = command.strip().split()
    command = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return command


def output(line, level=0):
    line = ("│ " * level) + line
    print(line)