import shlex
import os
import sys
import traceback
import readline
from bahash_builtins import builtins, builtin_exec 
# Need to trim down/streamline imports

# Note: This is windows compatible! Not OSX however, current readline usage doesn't account for libedit on OSX
# Note: Tab completion available!
# Note: supports append ( >> )

if sys.version_info[0] != 2:
	print "This shell is written for Python 2! If this somehow compiled, please do not run it." 	
		
def main():
	readline.parse_and_bind('tab: complete') # Enable local file tab completion and history
	# Need to initialize history file here

	while True:
		try:
			dir = os.getcwd()
			input = raw_input('{} >> '.format(dir)) # Print >>, take user input (blocking)
			if input[0][0] == '!':
				#history TODO
				pass
			args = shlex.split(input) # Use shell lexer module to parse input into list of strings
			run = builtins.get(args[0], builtin_exec) # Store relevant function into run variable (builtin_exec being default) 
			retVal = run(args) # Execute function stored in run with arguments args, storing the return value in retVal
			

		
		except KeyboardInterrupt: # Can use Finally to run commands regardless, or else to run things when no exception
			print "\r\nCaught interrupt signal! Killing any child processes..." #TODO
			continue

		except EOFError:
			print "\r\nLogout"
			break
		
		except ValueError:
			print "Unable to parse command. Do you have a non-paired delimiter? Think (), [], '', or \"\""
			traceback.print_exc()

		except OSError:
			print "Received an OS Error. Does the file or command you're looking for exist, or are you running out of memory?"
		
		except Exception:
			print "Error: I'm unsure of how to parse/execute the previous input. I caught the following exception:"
			traceback.print_exc()





if __name__ == '__main__':
	main()
else:
	print "This program doesn't work as an import. It must be run as the primary module."
