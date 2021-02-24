#!/usr/bin/env python

"""
fabric-git-betwixt

Selective fabric deployment of a compiled project using a git repository *betwixt and between* your source code and target machine.

https://joelpurra.github.io/fabric-git-betwixt/
"""


import os
from re import match
from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.colors import green, yellow, red
from fabric.contrib.console import confirm
from gitric.api import git_seed, git_reset


__author__ = "Joel Purra"
__copyright__ = "Copyright (c) 2012, Joel Purra <https://joelpurra.com/>"
__credits__ = ["Joel Purra"]
__license__ = "BSD, MIT, GPL"
__maintainer__ = "Joel Purra"
__email__ = "code+betwixt@joelpurra.com"
__status__ = "Development"


def script_init():
    """Setting defaults before executing the target with overrides"""
    env.copy_script_path = "copy-files-to-target.sh"

    # Directory script was run in
    env.original_directory = local_current_directory()

    # Confirmation dialogs
    env.are_you_sure = False


# MAIN TASKS
@task
def deploy():
    """(betwixt) Deploy the current state of the code to the remote target"""
    confirm_deployment()
    set_env_vars()
    with remote_target_directory():
        deploy_project()


@task
def clean():
    """(betwixt) Clean (delete all files) on the remote target"""
    confirm_clean()
    set_env_vars()
    with remote_target_directory():
        # https://serverfault.com/questions/122233/how-to-recursively-move-all-files-including-hidden-in-a-subfolder-into-a-paren
        # https://serverfault.com/a/122343/
        # bash expansion that doesn't include . or .. since those will give an error
        run("rm -Rf {,.[!.],..?}*")


# GIT TASKS
get_git_repo_root_command = "([ -d .git ] && echo \"$PWD/.git\") || (git rev-parse --git-dir 2> /dev/null)"


def local_get_git_repo_root():
    with hide("running", "stdout"):
        return os.path.abspath(rchop(rchop(rchop(local(get_git_repo_root_command, capture=True), "/"), ".git"), "/"))


def remote_get_git_repo_root():
    with hide("running", "stdout"):
        return os.path.abspath(rchop(rchop(rchop(run(get_git_repo_root_command), "/"), ".git"), "/"))


def local_is_git_repo_root():
    with hide("running", "stdout"):
        return (local_current_directory() == local_get_git_repo_root())


def remote_is_git_repo_root():
    with hide("running", "stdout"):
        return (remote_current_directory() == remote_get_git_repo_root())


def local_get_commit_hash():
    return local("git rev-parse HEAD", capture=True)


def local_is_dirty():
    return local("git status --porcelain", capture=True).strip() != ""


def compiled_clone_from_upstream():
    with local_compiled_git_directory():
        if not local_is_git_repo_root():
            local("git clone %s ." % (env.repo_address_compiled_upstream))


def compiled_clean():
    with local_compiled_git_directory():
        local("git clean -x -d -f")


def compiled_empty():
    with local_compiled_git_directory():
        local("rm -Rf *")


def compiled_reset():
    with local_compiled_git_directory():
        local("git reset --hard")


def compiled_pull_from_upstream():
    with local_compiled_git_directory():
        local("git pull")


def compiled_push_to_upstream():
    with local_compiled_git_directory():
        local("git push")


def compiled_commit():
    with local_compiled_git_directory():
        local("git add -u .")
        local("git add .")
        if local_is_dirty():
            local("git commit -m \"Based on %s commit %s\"" %
                  (env.project_name, env.project_commit_hash))


def compiled_seed_to_remote():
    with local_compiled_git_directory():
        git_seed(env.remote_target_directory, env.compiled_commit_hash)


def compiled_push_to_remote():
    with local_compiled_git_directory():
        git_reset(env.remote_target_directory, env.compiled_commit_hash)


# SERVICE CONTROL
def start_service():
    run(env.start_service_command)


def stop_service():
    run(env.stop_service_command)


# DEPLOYMENT
def confirm_deployment():
    if not env.are_you_sure:
        print(yellow("Deploying is potentially going to mess things up."))
        if not confirm("Are you sure you want to deploy?", default=False):
            abort("The user wasn't sure if deployment was the right thing to do.")


def copy_files_to_compiled_git_directory():
    with local_project_repo_root_directory():
        local((env.copy_script_path + " \"%s\"") %
              (env.compiled_git_directory))


def deploy_project():
    compiled_clone_from_upstream()
    compiled_clean()
    compiled_reset()
    compiled_empty()
    compiled_pull_from_upstream()
    copy_files_to_compiled_git_directory()
    compiled_commit()
    compiled_push_to_upstream()
    compiled_seed_to_remote()
    stop_service()
    compiled_push_to_remote()
    start_service()


# LOCALHOST FAKE UPSTREAM
def create_fake_upstream_directory():
    set_env_vars()
    with local_compiled_git_directory():
        if local_is_git_repo_root():
            return
    with fake_upstream_directory():
        non_bare_repo_directory_name = (
            "%s-fake-upstream-non-bare" % (env.target_name))
        # Create new repo with a single commit, so it has a commit hash
        # Otherwise git reset and other commands will fail
        with lcd(".."):
            local("mkdir -p %s" % (non_bare_repo_directory_name))
            with lcd(non_bare_repo_directory_name):
                local("git init")
                local("touch .gitignore")
                local("git add .gitignore")
                local("git commit -m \"Initial commit\"")
        # Create the actual fake upstream repo
        local("git clone --bare ../%s/ ." % (non_bare_repo_directory_name))
        # Remove the non-bare repo folder
        local("rm -Rf ../%s/" % (non_bare_repo_directory_name))

# CLEAN


def confirm_clean():
    if not env.are_you_sure:
        print(red("Cleaning is potentially going to mess things up."))
        if not confirm("Are you sure you want to clean (delete all files)?", default=False):
            abort("The user wasn't sure if cleaning was the right thing to do.")


# CONTEXT MANAGERS
@_contextmanager
def remote_target_directory():
    with hide("running", "stdout"):
        run("mkdir -p \"%s\"" % (env.remote_target_directory))
    with cd(env.remote_target_directory):
        run("pwd")
        yield


@_contextmanager
def local_project_repo_root_directory():
    with lcd(env.project_repo_root_directory):
        yield


@_contextmanager
def local_compiled_git_directory():
    with hide("running", "stdout"):
        local("mkdir -p \"%s\"" % (env.compiled_git_directory))
    with lcd(env.compiled_git_directory):
        yield


@_contextmanager
def fake_upstream_directory():
    with hide("running", "stdout"):
        local("mkdir -p \"%s\"" % (env.repo_address_compiled_upstream))
    with lcd(env.repo_address_compiled_upstream):
        yield


# Utils

# https://stackoverflow.com/questions/3663450/python-remove-substring-only-at-the-end-of-string
# https://stackoverflow.com/a/3663505/
def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring


def local_current_directory():
    with hide("running", "stdout"):
        return local("pwd", capture=True)


def remote_current_directory():
    with hide("running", "stdout"):
        return run("pwd", capture=True)


@runs_once
def set_env_vars():
    # Cleaning up some paths
    env.remote_target_directory = os.path.normpath(env.remote_target_directory)

    # Local compiled version will be stored here
    env.compiled_git_directory = os.path.join(
        env.original_directory, (".compiled/%s/" % (env.target_name)))

    env.compiled_git_directory = os.path.abspath(env.compiled_git_directory)

    # Project root directory
    with lcd(env.original_directory):
        with lcd(".."):
            env.project_repo_root_directory = local_current_directory()

    # Initialized to match local HEAD commit unless overridden
    # ("None" makes gitric take the HEAD)
    env.compiled_commit_hash = None

    # Current project commit hash used to set commit message in compiled repo
    env.project_commit_hash = local_get_commit_hash()


script_init()

# EOF
