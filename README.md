# [fabric-git-betwixt](http://joelpurra.github.com/fabric-git-betwixt/)

Selective fabric deployment of a compiled project using a git repository *betwixt and between* your source code and target machine.



## Features

- Uses git to version control your [fabric](http://fabfile.org/) deployments, even when deploying built code with dependencies.
- Commits your compiled code to a git repository - local or external like github - to maintain history and for easy diffing.
- Uses your external copy script to select files for deployment.
- Uses [gitric](https://github.com/dbravender/gitric) to push code to the remote target, to increase deployment stability and reduce downtime of any deployed service or website.
- Tested and used to deploy to production environments from both Mac OSX and Ubuntu.
- Can deploy to the local machine for testing.



## Steps

1. You work on your source code project.
1. You compile/prepare/minify it.
1. You run betwixt through fabric:
 1. Betwixt calls your copy script, which selects files for deployment.
 1. Betwixt commits the selected files to an intermediate local repository.
 1. Betwixt pushes the files to an upstream repository, to keep history.
 1. Betwixt seeds (uploads) the files to the git repository on your remote target machine, without modifying "live" files.
 1. Betwixt stops your service or website.
 1. Betwixt checks out the files of the deployed version. This is a fast operation, minimizing downtime.
 1. Betwixt starts your service or website.



## Please note on first use

- Betwixt assumes that the upstream git repository for the compiled code is new and empty on first use. The master branch files will be replaced with the files you select in the copy script.
- Betwixt assumes that the target directory on the target machine is empty on first use. This is to initialize the git repository.
- Betwixt assumes you have set up ssh keys with write permission for the upstream git server you are using.



## Setup

See example files in `example/`.


### Requirements and dependencies

- [python](http://www.python.org/)
- [pip](http://www.pip-installer.org/)
- [git](http://git-scm.com/)
- [virtualenv](http://www.virtualenv.org/) (see `examples/install.sh` and `examples/wrapper.sh`)
- [fabric](http://fabfile.org/) (installed by pip)
- [gitric](https://github.com/dbravender/gitric) (installed by pip)


### Variables

See `examples/fabfile.py`.

- `env.project_name`: *required* string. Used in generated commit messages.
- `env.target_name`: *required* string. Used in folder names used for intermediate storage.
- `env.copy_script_path`: *required* string path. Used to specify the shell script used to copy compiled files selected to be deployed. Called with one parameter; the local intermediate folder to copy files to. See `examples/copy-files-to-target.sh`.
- `env.remote_target_directory`: *required* string path. Folder to deploy to on the target machine(s).
- `env.repo_address_compiled_upstream`: *required* string git url. Used to commit and store the compiled code for deployment. Can be a local repository (use with `create_fake_upstream_directory()` to create temporary storage) or an external repository, like on github.
- `env.start_service_command`: *required* string shell command. A command performed on the target machine after deployment has finished, usually to start some service or website.
- `env.stop_service_command`: *required* string shell command. A command performed on the target machine after deployment has finished, usually to stop some service or website.
- `env.are_you_sure`: boolean. Defaults to `False`; set to `True` to skip `deploy`/`clean` confirmations for the current targets.


### For your localhost test deployment

If your `env.repo_address_compiled_upstream` is a local test/temporary directory. Don't call it if you you use an external git server for the deployed repository, like on github.

- `create_fake_upstream_directory()`: call each time you are deploying to a local git repository to automate setup.



## Usage

Where `localhost`, `production` and other targets are defined by you:

	fab (localhost|production) (clean|deploy)

Preferred usage, with `virtualenv`, can be seen in `examples/wrapper.sh`.



## TODO

- Don't use the commonly used `deploy`/`clean` names for the tasks.
- Don't define tasks at all - leave that up to anyone who uses the package?
- Make `deploy`/`clean` less involved and more focused? The package takes care of deployment confirmation for example, which probably shouldn't be its responsibility.



## License
Copyright (c) 2012, Joel Purra <http://joelpurra.se/>
All rights reserved.

When using fabric-git-betwixt, comply to at least one of the three available licenses: BSD, MIT, GPL.
Please see the LICENSE file for details.


