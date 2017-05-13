# -*- coding: utf-8 -*-

import os

from colorama import Fore, init as colorama_init
from git import Repo

from .common import get_input, get_yes
from .config import get_config, Config
from .logger import get_logger

LOGGER = get_logger()

colorama_init(autoreset=True)


def restore_directory(func):
    def func_wrapper(*args, **kwargs):
        cwd = os.getcwd()
        result = func(*args, **kwargs)
        os.chdir(cwd)
        return result
    return func_wrapper


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


@restore_directory
def install():
    config = get_config()
    base_dir = config.location
    LOGGER.debug("Directory: {}".format(base_dir))
    for component in config.components:
        comp_dir = os.path.join(base_dir, component.name)
        if os.path.isdir(os.path.join(base_dir, component.name)):
            repo = Repo(comp_dir)
            print("Component already installed, on branch {}.".format(repo.active_branch))
        else:
            Repo.clone_from(component.repo, comp_dir)
        os.chdir(comp_dir)


@restore_directory
def update():
    config = get_config()
    base_dir = config.location
    for component in config.components:
        print("Updating component {}... ".format(component.name), end="")
        success = False
        comp_dir = os.path.join(base_dir, component.name)
        repo = Repo(comp_dir)
        if repo.active_branch.name == component.rev:
            origin = repo.remotes.origin
            if not repo.is_dirty():
                origin.pull()
                success = True

        if success:
            print(Fore.GREEN + "✔", end="")
        else:
            print(Fore.RED + "✘", end="")
        print()


def display():
    config = get_config()
    for component in config.components:
        comp_dir = os.path.join(config.location, component.name)
        repo = Repo(comp_dir)
        print("Status of component {}... ".format(component.name))
        print("  Branch: {}".format(repo.active_branch.name))
        print("  Is Dirty: {}".format(repo.is_dirty()))
        print()
