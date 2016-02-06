import shlex
import os
import sys
import traceback
import readline
from bahash_builtins import builtins, builtin_exec, builtin_check_children, builtin_kill_children, children 
# Need to trim down/streamline imports

# Note: This is windows compatible! Not OSX however, current readline usage doesn't account for libedit on OSX
# Note: Tab completion available!
# Note: supports append ( >> )


if sys.version_info[0] != 2:
	print "This shell is written for Python 2! If this somehow compiled, please do not run it." 	
		
def main():
	prevrun = []
	warning = 0
	readline.parse_and_bind('tab: complete') # Enable local file tab completion and history
	#readline.read_history_file(history.his)
	# Need to initialize history file here TODO

	while True:
		try:
			dir = os.getcwd()
			input = raw_input('{} >> '.format(dir)) # Print >>, take user input (blocking)
			args = shlex.split(input) # Use shell lexer module to parse input into list of strings
			if input[0][0] == '!':
				if int(input[1][0]) > int(readline.get_current_history_length()):
					continue

				if readline.get_history_item(int(input[1][0])) is not None:
					args = shlex.split(readline.get_history_item(int(input[1][0])))

				if int(input[1][0]) == 0:
					args = prevrun
	
			run = builtins.get(args[0], builtin_exec) # Store relevant function into run variable (builtin_exec being default) 
			retVal = run(args) # Execute function stored in run with arguments args, storing the return value in retVal
			prevrun = args
			if warning > 0:
				warning = warning - 1 # This is a bit silly
			builtin_check_children()

		
		except KeyboardInterrupt: # Can use Finally to run commands regardless, or else to run things when no exception
			print "\r\nCaught interrupt signal! Killing any child processes..."
			builtin_kill_children()
			continue

		except EOFError:
			if len(children) > 0 and warning < 1:
				warning = warning + 3 # Two commands of leeway before next warning
				print "\r\nWarning: this shell still has child processes active. Pressing ^D again will kill them."
				continue
			builtin_kill_children()
			print "\r\nLogout"
			exit()
		
		except ValueError:
			print "Unable to parse command. Do you have a non-paired delimiter? Think (), [], '', or \"\""

		except OSError:
			print "Received an OS Error. Does the file or command you're looking for exist, or are you running out of memory?"
			#traceback.print_exc()
		
		except Exception:
			print "Error: I'm unsure of how to parse/execute the previous input. Common reasons for this are multiple redirects"
			print "on the same line, commands that don't syntactically make sense, or attempting to reach files that don't exist."
			print "Nothing but whitespace will also trigger this error."
			print "Additionally, I caught the following exception:"
			traceback.print_exc()





if __name__ == '__main__':
	main()
else:
	print "This program doesn't work as an import. It must be run as the primary module."
