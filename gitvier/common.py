
def get_input(question, default=""):
    add = "[{}] ".format(default) if default != "" else ""
    user = input("{}: {}".format(question, add)).strip()
    if user == "":
        user = default
    return user


def get_yes(question, yes=False):
    user = input("{}: [{}] ".format(question, 'yes' if yes is True else 'no')).strip().lower()
    return user in ('yes', 'y')
