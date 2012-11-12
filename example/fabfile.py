"""
fabric-git-betwixt

Selective fabric deployment of a compiled project using a git repository *betwixt and between* your source code and target machine.

This is an example fabfile.py that uses betwixt.

http://joelpurra.github.com/fabric-git-betwixt/
"""



from fabric.api import *
from fabric.colors import red
from betwixt.api import deploy, clean



# COMPUTER SYSTEM TASKS
@task
def localhost():
	'''Use localhost as remote target (for testing)'''
	shared_init()
	env.target_name = "localhost"
	env.hosts = ["localhost"]

	# Deploying to a directory in ~ to see what is going on.
	env.remote_target_directory = ("$HOME/dev/deployment/%s/" % (env.target_name))

	# Use a local directory as the upstream git repository.
	env.repo_address_compiled_upstream = os.path.join(env.original_directory, (".compiled/%s-fake-upstream/" % (env.target_name))

	# Placeholder commands when testing the deployment scripts
	env.start_service_command = "sudo echo \"Simulating starting the service\""
	env.stop_service_command = "sudo echo \"Simulating stopping the service\""

	# Don't ask for confirmation when testing deployment.
	env.are_you_sure = True

	# Set up local "upstream" repository.
	create_fake_upstream_directory()


@task
def production():
	'''Use production as remote target'''
	shared_init()
	print(red("Production server, beware!"))
	env.target_name = "production"
	env.hosts = ["example.com"]

	# Set up access to the production server.
	env.user = "deployment"
	env.key_filename = ["~/.ssh/deployment_id_rsa"]

	# Directory on the remote server to put the github repository in. This would also be the root on a web server.
	env.remote_target_directory = ("/data/web/%s/" % (env.target_name))

	# You can use, for example, a private github repository for containing your compiled production code.
	# This will also maintain a nice deployment/push/commit/change history.
	env.repo_address_compiled_upstream = ("git@github.com:organization/example.com-compiled-%s.git" % (env.target_name))

	# Start/stop web server after successfully pushing all code.
	env.start_service_command = "sudo /usr/bin/supervisorctl start example.com"
	env.stop_service_command = "sudo /usr/bin/supervisorctl stop example.com"


def shared_init():
	env.project_name = "myProjectName"
	env.copy_script_path = "copy-files-to-target.sh"



# EOF