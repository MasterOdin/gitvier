from .common import get_input, get_yes
from .config import get_config, Config
from .logger import get_logger

LOGGER = get_logger()


def init(force=False):
    config = get_config()
    if config is not None and not force:
        LOGGER.error(".gitvier.yml file already exists. Use --force to overwrite.")
        return
    config = Config()
    config.location = get_input("Location to install components", ".")

    while True:
        add = get_yes("Add a component")
        if add:
            repo = get_input("Git url")
            if repo == "":
                print("You must input a url")
                continue
            default = repo.split("/")[-1].replace(".git", "")
            name = get_input("Name of component", default)
            rev = get_input("Revision to use", "master")
            config.add_component(name, repo, rev)
        else:
            break

    config.save()


def install(force=False, clean=False):
    pass


def update(force=False, clean=False):
    pass


def display():
    pass

