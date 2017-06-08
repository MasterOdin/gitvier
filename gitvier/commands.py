# -*- coding: utf-8 -*-

import os
import sys

from colorama import Fore, init as colorama_init
from git import Repo, CheckoutError
from git.exc import InvalidGitRepositoryError

from .common import get_input, get_yes, call as shell_call, output
from .config import get_config, Config

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
        print(".gitvier.yml file already exists. Use --force to overwrite.", file=sys.stderr)
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
    if config is None:
        print("Not a valid gitvier instance")
        return
    base_dir = config.location
    os.makedirs(base_dir, exist_ok=True)
    print("Directory: {}".format(base_dir))
    os.chdir(base_dir)
    output("├ Config loaded: " + config.config_file)
    output("├ Install Path: " + config.location)
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
        output("├── git clone {}".format(component.repo, comp_dir), level)
        repo = Repo.clone_from(component.repo, comp_dir)
        _checkout(repo, component, level)

    os.chdir(comp_dir)
    config = get_config(comp_dir)
    if config is not None:
        output("├── Config loaded: " + config.config_file, level)
        output("├── Install Path: " + config.location, level)
        output("├─┬ Installing Components:", level)
        count = 0
        for component in config.components:
            if count > 0:
                output("", 1)
            _install(config.location, component, level+1)

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


@restore_directory
def display():
    output("├ Components Statuses:")
    _display()


def _display(base_dir=None, level=0):
    config = get_config(base_dir)
    if config is None:
        return
    level += 1
    for component in config.components:
        output("├─┬ {} ({:s})".format(component.name, component.rev), level-1)
        comp_dir = os.path.join(config.location, component.name)

        if not os.path.isdir(comp_dir):
            output("├── Not Installed", level)
        else:
            os.chdir(comp_dir)
            try:
                repo = Repo(comp_dir)
                if repo.head.is_detached:
                    output("├── Revision: {:s}".format(repo.commit(repo.head).hexsha), level)
                else:
                    output("├── Branch: {:s}".format(repo.active_branch.name), level)
                output("├── Dirty: {}".format("True" if repo.is_dirty() else "False"), level)
                _display(comp_dir, level)
            except InvalidGitRepositoryError:
                output("├── Invalid Git repository", level)
