import subprocess
import os
import sys

children = [] # list of children processes

def builtin_cd(args):
	args[1] = os.path.expanduser(args[1])
	os.chdir(args[1])


def builtin_exec(args):
	# Note: A known limitation of this implementation is that builtins cannot be backgrounded
	if "&" not in args:
		proc = subprocess.Popen(args, executable = args[0], stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr)
		return proc.wait()

	else: #need to fork process	
		args.remove('&')
		while '&' in args:
			args.remove('&')
		if sys.platform == 'win32':
			proc = subprocess.Popen(args, 
		                        	executable = args[0], 
		                        	stdin = open(os.devnull, 'r'), #read
		                        	stdout = open(os.devnull, 'w'), #write
		                        	stderr = open('childerror.log', 'a'), #append
		                        	creationflags = subprocess.CREATE_NEW_PROCESS_GROUP )
		else: #Should work with OSX?
			proc = subprocess.Popen(args, 
		                        	executable = args[0], 
		                        	stdin = open(os.devnull, 'r'), #read
		                        	stdout = open(os.devnull, 'w'), #write
		                        	stderr = open('childerror.log', 'a'), #append
									preexec_fn = os.setpgrp)
		children.append(proc)
		print "Child process {} started.".format(proc.pid)
		return 0


def builtin_kill(args):
	try:
		os.kill(int(args[1]), int(args[2]))

	except ValueError:
		print "Kill returned an error. Are you sure your input was correct?"


def builtin_jobs(args):
	num = 1
	for proc in children:
		print "[{}] {}".format(num, proc.pid)
		num = num+1


def builtin_history(args):
	pass


def builtin_exit(args):
	exit()


builtins = {
	'cd'      : builtin_cd,
	'history' : builtin_history,
	'kill'    : builtin_kill,
	'exit'    : builtin_exit,
	'quit'    : builtin_exit,
	'jobs'    : builtin_jobs
}





if __name__ == '__main__':
	print "The bahash builtins don't work as a standalone program -- they're imported by the main module.\r\n"
else:
	pass	
