# [fabric-git-betwixt](http://joelpurra.github.com/fabric-git-betwixt/) `example/`

> [fabric-git-betwixt](http://joelpurra.github.com/fabric-git-betwixt/): Selective fabric deployment of a compiled project using a git repository *betwixt and between* your source code and target machine.

This folder shows an example setup. You could copy the contents to a `deployment/` folder in your own project and modify it there.



## Usage

1. Edit the variables in `fabfile.py`.
1. Edit what folders/files you would like to deploy in `copy-files-to-target.sh`.
1. Run `./install.sh`.
1. Run `./wrapper.sh -l` to see available fabric tasks.
1. Run `./wrapper.sh localhost deploy` to test your deployment scripts.
1. Use `production` when you are confident everything works.



## Files


### `.gitignore`

Ignore betwixt deployment specific subfolders.


### `copy-files-to-target.sh`

Example file to copy files to the target output directory. Copy only file you want to deploy. **Requires editing.**


### `fabfile.py`

Defines fabric `@tasks` for `localhost` and `production`. Has most of the setup. **Requires editing.**


### `install.sh`

Installs [virtualenv](http://www.virtualenv.org/), a virtual python environment for deployment and adds betwixt with dependencies.


### `README.md`

See `README.md`.


### `requirements.txt`

Lists required python packages for `pip`.


### `wrapper.sh`

A wrapper that makes sure the right virtual environment is used.

