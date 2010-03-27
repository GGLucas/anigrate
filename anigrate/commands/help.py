import sys

from anigrate.config import Config
from anigrate.util import register, arguments, Commands, Commands_Order, choose

@register("help", shorthelp="display help text")
@arguments(0, 1)
def cm_help(command=None):
    """
        help
            Display a help information screen listing all the commands and options.
    """

    if not command:
        ## Print help header
        # Help header
        print("""
Usage: %(command)s [COMMAND] [ARGS...]: [SELECTOR]
Manage a list of watched anime or television series.

Database:
    By default anigrate uses an sqlite database in $HOME/.anigrate/db,
    see the example anigraterc for all the other possibilities.

Commands: 
    See `%(command)s help $command` for extended information about the arguments
    and usage of a specific command. The following commands are available:
""" % {"command":sys.argv[0]})
        # List all commands
        for name in Commands_Order:
            func = Commands[name]
            print("    "+name.ljust(16)+
            (func.shorthelp if hasattr(func, "shorthelp") else ""))

        print("""
Selectors:
    See `%(command)s help selectors` for detailed information on how to use 
    selectors and what the items mean. The following items are supported:

    +finished, +completed, +watching, +dropped, +undropped
      filter on this state
    =<category>
      filter on this category
    %%exact, %%contains, %%suffix, %%prefix
      set match mode
    @rating, @activity, @watched, @title, @split
      set sort mode

Import/Export Formats:
    For extended information on available database import and export formats, 
    see `%(command)s help dbformat`. The following formats are available:

    csv, anidb, myanimelist
""" % {"command":sys.argv[0]})
    elif command == "selectors":
        print("""
Selectors:
    Selectors are used to find series to act upon. In its most basic form, a 
    selector is simply the name of a series or the beginning of a name of a 
    series (note that the selector will match any series that start with the 
    specified name). Within the selector, the options listed below can be given.

    +finished/+completed, +watching, +dropped, +undropped:
        Put any of these in a separate argument anywhere in the selector and it 
        will only match series that satisfy the condition.

    =<category>
        Will only match series in the specified category.

    %exact
        When specified, only match series that exactly match the full selector.

    %contains
        When specified, match all series containing the selector.

    %suffix
        When specified, match all series that end with the selector.

    %prefix
        Default behaviour: match all series that start with the selector.

    @rating, @activity, @watched, @title
        Set field to sort by, you can sort by series rating, series latest 
        activity, amount of episodes watched and title respectively.

    @split
        Default sort method, sorts by activity but splits into watching,
        finished and dropped groups first.

""")
    elif command == "dbformat":
        # Database format help.
        print("""
Database Formats:
    Database formats are used to determine how to read or write series
    from or to a file, the following format specifiers are available:

    csv
        Uses a simple csv file with series titles and other info.

    anidb
        Uses anidb.net's csv-minimal MyList export template.

    myanimelist  [IMPORT ONLY]
        Uses myanimelist.net's xml export format.
        When importing from myanimelist be sure to uncompress it before feeding
        it to anigrate; you can use pipes for this. For example:
          $ gunzip -c animelist_0000_-_0000.xml.gz | anigrate import - myanimelist
""")
    else:
        ## Print help about one command
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
