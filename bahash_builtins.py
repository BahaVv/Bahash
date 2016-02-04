import subprocess
import os
import sys

if sys.version_info[0] != 2:
	print "These builtins were written for Python 2! If this somehow compiled, please do not run it."

children = [] # list of children processes

def builtin_cd(args):
	args[1] = os.path.expanduser(args[1])
	os.chdir(args[1])


def builtin_exec(args):
	# Note: A known limitation of this implementation is that builtins cannot be backgrounded
	input = sys.stdin
	output = sys.stdout
	err = sys.stderr 
	redirect = False
	if '<' in args:
		redirect = True
		idx = args.index('<')
		input = open(args[idx+1], 'r') 
		args = args[:idx]

	if '>' in args:
		if redirect == True:
			raise Exception("More than one redirect on the same line!")
		redirect = True
		idx = args.index('>')
		output = open(args[idx+1], 'w') 
		args = args[:idx]

	if '>>' in args:
		if redirect == True:
			raise Exception("More than one redirect on the same line!")
		redirect = True
		idx = args.index('>>')
		output = open(args[idx+1], 'a') 
		args = args[:idx]

	if '&' not in args:
		proc = subprocess.Popen(args, executable = args[0], stdin = input, stdout = output, stderr = err)
		return proc.wait()

	else: #need to fork process	
		if input is sys.stdin:
			input = open(os.devnull, 'r')
		if output is sys.stdout:
			output = open(os.devnull, 'w')
		if err is sys.stderr:
			err = open('childerror.log', 'a')

		args.remove('&')
		while '&' in args:
			args.remove('&')
		if sys.platform == 'win32':
			proc = subprocess.Popen(args, 
		                        	executable = args[0], 
		                        	stdin = input,
		                        	stdout = output,
		                        	stderr = err,
		                        	creationflags = subprocess.CREATE_NEW_PROCESS_GROUP )
		else: #Should work with OSX?
			proc = subprocess.Popen(args, 
		                        	executable = args[0], 
		                        	stdin = input,
		                        	stdout = output,
		                        	stderr = err,
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
