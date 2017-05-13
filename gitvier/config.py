from collections import OrderedDict
import os
from typing import List, Optional

import yaml


def get_config(path=None):
    if not path:
        path = os.getcwd()
    config_file = os.path.join(path, '.gitvier.yml')
    if os.path.isfile(config_file):
        return Config(config_file)
    else:
        return None


class Component(object):
    def __init__(self, name: str, repo: str, rev: str, commands: List[str]):
        self.name = name
        self.repo = repo
        self.rev = rev
        self.commands = commands


class Config(object):
    """

    Attributes:
        components: List[Component]
    """

    def __init__(self, config_file=None):
        self.location = '.'
        self.components = []  # type: list[Component]

        if config_file is not None and os.path.isfile(config_file):
            self._load_config_file(config_file)
            self.config_file = config_file
        else:
            self.config_file = os.path.join(os.getcwd(), ".gitvier.yml")

    def _load_config_file(self, config_file: str):
        with open(config_file) as open_file:
            loaded_config = yaml.safe_load(open_file)

        if loaded_config is None:
            return

        if 'location' in loaded_config:
            self.location = loaded_config['location']
        self.location = os.path.abspath(os.path.expanduser(self.location))

        if 'components' in loaded_config and isinstance(loaded_config['components'], list):
            for component in loaded_config['components']:
                repo = component['repo']
                rev = 'master'
                commands = []
                if 'name' in component:
                    name = component['name']
                else:
                    name = repo.split("/")[-1].replace(".git", "")
                if 'rev' in component:
                    rev = component['rev']
                if 'commands' in component and isinstance(component['commands'], list):
                    commands = component['commands']
                self.components.append(Component(name, repo, rev, commands))

    def add_component(self, name: str, repo: str, rev: str, commands: Optional[List[str]] = None):
        if commands is None:
            commands = []
        self.components.append(Component(name, repo, rev, commands))

    def save(self):
        data = OrderedDict()
        data['location'] = self.location
        data['components'] = []
        for component in self.components:
            inner = OrderedDict()
            inner['name'] = component.name
            inner['repo'] = component.repo
            inner['rev'] = component.rev
            inner['commands'] = component.commands
            data['components'].append(inner)
        with open(self.config_file, 'w') as config_file:
            yaml.dump(data, config_file, default_flow_style=False)


def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)
