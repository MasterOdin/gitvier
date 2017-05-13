gitvier
=======

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

Dependencies
------------

* Python 3.5+
* Git

Others?

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
    usage: gitvier [-h] [-V] <command> ...

    A component manager based where your components live in Git.

    positional arguments:
      <command>
        init         Initialize a new gitvier directory

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

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

.. _Submitty: https://github.com/Submitty/Submitty
.. _Gitman: https://github.com/jacebrowning/gitman