import subprocess
import os
import sys


def builtin_cd(args):
	args[1] = os.path.expanduser(args[1])
	os.chdir(args[1])

def builtin_exec(args):
	# Note: A known limitation of this implementation is that builtins cannot be backgrounded
	proc = subprocess.Popen(args, executable = args[0], stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr)
	return proc.wait()

def builtin_history(args):
	pass

def builtin_kill(args):
	try:
		os.kill(int(args[1]), int(args[2]))

	except ValueError:
		print "Kill returned an error. Are you sure your input was correct?"

def builtin_exit(args):
	exit()

builtins = {
	'cd'      : builtin_cd,
	'history' : builtin_history,
	'kill'    : builtin_kill,
	'exit'    : builtin_exit,
	'quit'    : builtin_exit
}





if __name__ == '__main__':
	print "The bahash builtins don't work as a standalone program -- they're imported by the main module.\r\n"
else:
	pass	
