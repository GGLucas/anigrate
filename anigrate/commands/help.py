import sys

from anigrate.config import Config
from anigrate.util import register, arguments, Commands, Commands_Order, choose, HAVE_DATEUTIL

from anigrate.help.generic import HELP_TOP, HELP_BOTTOM
from anigrate.help.subjects import Subjects
from anigrate.help.configuration import ConfigHelp

@register("help", shorthelp="display help text")
@arguments(0, 1)
def cm_help(command=None):
    """
    help
        Display a help information screen listing all the commands and options.
    """

    if not command:
        # Help top part
        print(HELP_TOP % {"command":sys.argv[0]})

        # List all commands
        for name in Commands_Order:
            func = Commands[name]
            print("    "+name.ljust(16)+
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
