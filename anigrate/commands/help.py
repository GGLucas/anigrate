import sys

from anigrate.config import Config
from anigrate.util import (register, arguments, Commands,
                        Commands_Season, Commands_Season_Order,
                        Commands_Order, choose, HAVE_DATEUTIL)

from anigrate.help.generic import HELP_TOP, HELP_BOTTOM
from anigrate.help.subjects import Subjects
from anigrate.help.configuration import ConfigHelp

@register("config", shorthelp="output current configuration")
@arguments(0)
def cm_config():
    """
    config
        Output the currently used configuration in a format usable for 
        a config file.
    """
    Config.write(sys.stdout)

@register("help", shorthelp="display help text")
def cm_help(*command):
    """
    help
        Display a help information screen listing all the commands and options.
    """
    command = " ".join(command)

    if not command:
        # Help top part
        print(HELP_TOP % {"command":sys.argv[0]})

        # List all commands
        for name in Commands_Order:
            func = Commands[name]
            print("    "+name.ljust(18)+
            (func.shorthelp if hasattr(func, "shorthelp") else ""))

        # List all commands
        print("")
        for name in Commands_Season_Order:
            func = Commands_Season[name]
            print("    season "+name.ljust(11)+
            (func.shorthelp if hasattr(func, "shorthelp") else ""))

        # Help bottom part
        print(HELP_BOTTOM % {"command":sys.argv[0]})
    elif command == "commands":
        for name in Commands_Order:
            func = Commands[name]
            print(func.__doc__.lstrip("\n"))
    elif command == "configuration":
        print(Subjects["configuration"])
        for name in sorted(ConfigHelp):
            print("    "+name)
        print("")
    elif command == "options":
        for name in sorted(ConfigHelp):
            print(ConfigHelp[name].lstrip("\n"))
        print("")
    elif command == "dates":
        print(Subjects['dates'])

        if HAVE_DATEUTIL:
            print(" The python `dateutil` package is installed.\n")
        else:
            print(" The python `dateutil` package is NOT installed.\n")
    else:
        if command in Subjects:
            print(Subjects[command])
        elif command in ConfigHelp:
            print(ConfigHelp[command])
        elif command.startswith("season "):
            cmd = choose(Commands_Season, command[7:], value_only=True)
            if cmd:
                for func in cmd:
                    print(func.__doc__)
            else:
                print("Help subject `%s` not found." % command)
        else:
            cmd = choose(Commands, command, value_only=True)
            if cmd:
                for func in cmd:
                    print(func.__doc__)
            else:
                print("Help subject `%s` not found." % command)

@register("version", shorthelp="display version information")
@arguments(0)
def cm_version():
    """
        version
            Display anigrate version and copyright information.
    """
    print('Anigrate '+str(Config.ANIGRATE_VERSION)+
          ' <'+Config.ANIGRATE_URI+'>\n'
          'Copyright (C) 2009-2010 Lucas de Vries <lucas@glacicle.org>\n'
          'License WTFPL: <http://sam.zoy.org/wtfpl>\n')
