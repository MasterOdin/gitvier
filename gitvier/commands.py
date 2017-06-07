# -*- coding: utf-8 -*-

import os

from colorama import Fore, init as colorama_init
from git import Repo, CheckoutError
from git.exc import InvalidGitRepositoryError

from .common import get_input, get_yes, call as shell_call, output
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
    os.makedirs(base_dir, exist_ok=True)
    LOGGER.info("Directory: {}".format(base_dir))
    os.chdir(base_dir)
    output("├ Installing Components:")
    count = 0
    for component in config.components:
        if count > 0:
            output("", 1)
        _install(base_dir, component, 0)
    output("")


def _install(base_dir, component, level=0):
    output("├─┬ {} ({:s})".format(component.name, component.rev), level)
    comp_dir = os.path.join(base_dir, component.name)
    level += 1
    if os.path.isdir(os.path.join(base_dir, component.name)):
        try:
            repo = Repo(comp_dir)
            if repo.head.is_detached:
                output(
                    "├── Component already cloned, on hash " + repo.commit(repo.head).hexsha + ".",
                    level)
            else:
                output(
                    "├── Component already cloned, on branch {}.".format(repo.active_branch.name),
                    level)

            # we're detached, and if we're also in a 'clean' state, then we consider that
            # good enough to move to the tag/hash/branch
            if repo.head.is_detached and not repo.is_dirty():
                _checkout(repo, component, level)
            else:
                if component.rev != repo.active_branch.name:
                    output("├── Active branch not equal to requested revision, skipping",
                           level + 1)
                else:
                    output("├── git pull", level)
                    repo.remote('origin').pull()
        except InvalidGitRepositoryError:
            output("├── Folder exists for component, but is not git repo", level + 1)
    else:
        output("├── git clone " + component.repo, level)
        repo = Repo.clone_from(component.repo, comp_dir)
        _checkout(repo, component, level)

    config = get_config(comp_dir)
    if config is not None:
        output("├─┬ Installing Components:", level)
        count = 0
        for component in config.components:
            if count > 0:
                output("", 1)
            _install(comp_dir, component, level)

    os.chdir(comp_dir)
    if len(component.commands) > 0:
        output("├─┬ Running Commands:", level)
        for i in range(len(component.commands)):
            command = component.commands[i]
            if i == len(component.commands)-1:
                output("└── " + command, level + 1)
            else:
                output("├── " + command, level + 1)
            shell_call(command)


def _checkout(repo, component, level=0):
    for tag in repo.tags:
        if tag.name == component.rev:
            try:
                output("git checkout tags/{}".format(component.rev), level)
                repo.git.checkout('tags/' + component.rev)
            except CheckoutError:
                pass
            return

    try:
        output("├── git checkout {}".format(component.rev), level)
        repo.git.checkout(component.rev)
    except CheckoutError:
        pass


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
    output("├ Components Statuses:")
    config = get_config()
    for component in config.components:
        comp_dir = os.path.join(config.location, component.name)
        output("├─┬ {} ({:s})".format(component.name, component.rev))
        repo = Repo(comp_dir)
        output("├── Branch: {:s}".format(repo.active_branch.name), level=1)
        output("└── Dirty: {}".format("True" if repo.is_dirty() else "False"), level=1)
