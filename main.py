import shlex
import subprocess
import os
import sys
import traceback
from bahsh_builtins import builtins, builtin_exec 

# Note: This is windows compatible!

def main():
	while True:
		try:
			dir = os.getcwd()
			input = raw_input('{} >> '.format(dir)) #print >>, take user input (blocking)
			args = shlex.split(input) #use shell lexer module to parse input into list of strings	
			run = builtins.get(args[0], builtin_exec)
			ret = run(args)
			

		
		except KeyboardInterrupt: # Can use Finally to run commands regardless, or else to run things when no exception
			print "\nCaught interrupt signal! Quitting..."
			break
		
		except ValueError:
			print "Unable to parse command. Do you have a non-paired delimiter? Think (), [], '', or \"\""

		except OSError:
			print "Received an OS Error. Does the file or command you're looking for exist, or are you running out of memory?"
		
		except Exception:
			print "Error: I'm unsure of how to parse/execute the previous input. I caught the following exception:"
			traceback.print_exc()




if __name__ == '__main__':
	main()
else:
	print "This program doesn't work as an import. It must be run as the primary module."
