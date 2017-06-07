gitvier
=======


.. image:: https://travis-ci.org/MasterOdin/gitvier.svg?branch=master
    :target: https://travis-ci.org/MasterOdin/gitvier
    :alt: Build Status
.. image:: https://img.shields.io/pypi/v/gitvier.svg
    :target: https://pypi.python.org/pypi/gitvier/
    :alt: PyPI Version
.. image:: https://img.shields.io/pypi/status/gitvier.svg
    :target: https://pypi.python.org/pypi/gitvier
    :alt: Gitvier Development Status
.. image:: https://img.shields.io/pypi/pyversions/gitvier.svg
    :target: https://pypi.python.org/pypi/gitvier/
    :alt: Supported Python Versions
.. image:: https://img.shields.io/github/license/MasterOdin/gitvier.svg
    :target: https://github.com/MasterOdin/gitvier/blob/master/LICENSE
    :alt: License


Gitvier is a CLI "component management" tool for when you've got a container repository and then that repository relies
on a bunch of components to operate, which you're then actively working on those components. As such, it aims to allow
the user to try and manage these components, allowing for installing, updating, etc. as well as running commands over
some/all components. However, it differs from something like GitMan in that it will not explicitly revert dependencies
to specified revisions unless explicitly forced as most likely if you install a component on "master" and the
component is currently on branch "develop", if you run "gitvier update", you don't expect that component to be put back
onto master, but rather that maybe just do a git pull on this component (and all others). I primarily built this
to support the usecase of `Submitty`_ and for my research projects.

This borrows concepts heavily from `GitMan`_ which is a great dependency
manager with Git, but less useful as a "component manager" (hence the existance of this tool).

Roadmap
-------

- [x] Install
- [ ] Update
- [ ] Branch
- [ ] Add
- [ ] Commit
- [ ] Push

Dependencies
------------

* Python 3.5+
* Git
* colorama (maybe?)
* GitPython
* PyYAML

Installation
------------
From Pip::

    pip3 install gitvier

From Source::

    git clone https://github.com/MasterOdin/gitvier
    python3 setup.py install


Usage
-----
::

    $ gitvier --help
    usage: gitvier [-h] [-V] [-v | -q] <command> ...

    A component manager for when your components live in Git.

    positional arguments:
      <command>
        init         create a new gitvier configuration file
        install      install all components specified in config
        update       update all installed components if in original branch and not
                     dirty
        list         list all components, if they're installed, branch they're on
                     and if currently dirty

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -v, --verbose  how verbose of output should occur, default is just WARN+,
                     one v for info+, two v for debug+
      -q, --quiet    only output errors and inputs

Gitvier Config File
-------------------

Gitvier operates over a `.gitvier.yml` config file which contains the various components of our system. At the root
level you can specify a `location` (defaults to current directory if omitted) where all components would live and
`components` which is a list of components which contain the following elements::

    name: <component_name/subfolder where component will be installed to>
    repo: <git_url>
    rev: <branch or tag or commit hash or branch/tag@timestamp>
    commands: <list of bash commands to run after install/update> (optional)

An example of a `.gitvier.yml` file (taken from `Submitty`_)::

    location: .
    components:
    - name: RainbowGrades
      repo: https://github.com/Submitty/RainbowGrades
      rev: master
    - name: grading
      repo: https://github.com/Submitty/AutoGrading
      rev: master



License
-------

Gitvier is licensed under the MIT License, which can be viewed
`here <https://github.com/MasterOdin/gitvier/blob/master/LICENSE.rst>`_.

.. _Submitty: https://github.com/Submitty/Submitty
.. _Gitman: https://github.com/jacebrowning/gitman