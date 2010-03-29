import sys
import os
from optparse import OptionParser
from pprint import pprint

import sqlalchemy

from anigrate.models import Series, Season, Watched, bind_session
from anigrate.config import Config
from anigrate.selector import Selector
from anigrate.util import choose, debug, Commands

import anigrate.commands

def setopt(option, opt, value, parser):
    """
        Set a configuration option from optparse.
    """
    for option in value.split(":"):
        section, sep, rest = option.partition(".")
        option, sep, value = rest.partition("=")

        if section and option and value:
            if not Config.has_section(section):
                Config.create_section(section)

            Config.set(section, option, value)

def showhelp(option, opt_str, value, parser):
    """
        Switch to help command.
    """
    parser.largs.insert(0, "help")

def showversion(option, opt_str, value, parser):
    """
        Switch to version command.
    """
    parser.largs.insert(0, "version")

def parse_args():
    """
        Parse options from the commandline
    """
    parser = OptionParser(add_help_option=False)

    # Specific configuration file
    parser.add_option("-c", "--config", dest="config")

    # Specific database connection
    parser.add_option("-b", "--database", dest="database")

    # Debug mode
    parser.add_option("-d", "--debug", action="store_true")

    # Change config option(s)
    parser.add_option("-s", "--set", action="callback", callback=setopt, type=str)

    # Debug mode
    parser.add_option("-q", "--quiet", action="store_true")

    # Display help
    parser.add_option("-h", "--help", action="callback", callback=showhelp)

    # Display version
    parser.add_option("-v", "--version", action="callback", callback=showversion)

    # Parse
    options, args = parser.parse_args()

    # Check if we should set config path
    if options.config:
        if os.path.exists(options.config):
            Config.read(options.config)
        else:
            return -1, "Specified configuration file not found or not accessible."

    # Check if we should set database uri
    if options.database:
        Config.set("database", "uri", options.database)

    # Store flags in config
    Config.debug = options.debug
    Config.quiet = options.quiet

    return options, args

def main():
    # Parse arguments
    options, args = parse_args()

    # Add help argument if no arguments were specified
    if not args:
        args = ["help"]

    # Check for parse errors
    if options == -1:
        print("Error: "+args)
        sys.exit(1)

    # Try to bind to the database
    try:
        bind_session(Config.get("database", "uri"))
    except sqlalchemy.exc.ArgumentError:
        debug("Error: Invalid sqlalchemy connection string specified.")

    try:
        # Split arguments between function and selector
        func_args = []
        selector_args = []

        # Check if a selector exists
        if [arg for arg in args if arg.endswith(":")]:
            # Split args between arguments and the selector
            current = func_args
            for argument in args:
                if argument.endswith(":") and current == func_args:
                    # Switch from list when the first : is found
                    current.append(argument[:-1])
                    current = selector_args
                else:
                    # Add argument to appropriate list
                    current.append(argument)
        else:
            func_args = args

        # Get command name
        command_name = func_args.pop(0)

        # Get matching commands
        commands = choose(Commands, command_name)

        # Check if command is unique
        if not commands:
            print("Error: command %s does not exist." % command_name)
            sys.exit(1)
        if len(commands) > 1:
            print("Command `%s` is ambiguous, the following are available:" 
                     % command_name)

            # Print available commands
            for cmd in commands:
                print("  "+cmd[0])

            # Die
            sys.exit(1)

        # Get command function
        func = commands[0][1]

        # Check if we should prepare a selector
        if hasattr(func, "selector"):
            if func.selector == 1:
                selector_args = Selector(selector_args)
            elif func.selector == 2:
                selector_args = " ".join(selector_args)

            func_args.insert(0, selector_args)

        # Check for correct amount of arguments
        if hasattr(func, "minargs") and func.minargs > len(func_args):
            debug("Error: Too few arguments specified", raise_exception=False)
        elif hasattr(func, "maxargs") and func.maxargs < len(func_args):
            debug("Error: Too many arguments specified.", raise_exception=False)

        # Check for any arguments that should be set to None
        func_args = [None if arg == "." else arg for arg in func_args]

        # Call the function
        func(*func_args)

    except sqlalchemy.exc.OperationalError:
        debug("Error: Unable to communicate with the database or access denied.")
    except:
        debug("An unexpected error occurred, specify -d or --debug to see the python stack trace.")

if __name__ == '__main__':
    main()
