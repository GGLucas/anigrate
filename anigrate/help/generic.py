HELP_TOP = """
Usage: %(command)s [COMMAND] [ARGS...]: [SELECTOR]
Manage a list of watched anime or television series.

Commands: 
    See `%(command)s help $command` for extended information about the arguments
    and usage of a specific command.

    You can use the shortest unambiguous form to specify each of these commands
    (for example "li" will suffice for "list" and both "hi" and "hist" will
    suffice for "history").

    Positional arguments can be set to a single period character (".") in order
    to specify they should remain set to their default values.

    The following commands are available:
"""

HELP_BOTTOM = """
Selectors:
    See `%(command)s help selectors` for detailed information on how to use 
    selectors and what the items mean. The following items are supported:

    +finished, +completed, +watching, +dropped, +undropped
      filter on this state
    =<category>
      filter on this category
    %%exact, %%contains, %%suffix, %%prefix
      set match mode
    %%matcher
      use the interactive series matcher
    @rating, @activity, @watched, @title, @split
      set sort mode

Switches:
    The following command-line switches are available to be specified.

      -c, --config=CONFIG        load file CONFIG instead of the default 
                                   configuration file location
      -b, --database=URI         use database connection URI instead of the
                                   database specified in the configuration
      -q, --quiet                don't display messages when series properties
                                   are changed or added
      -d, --debug                enable debug mode, this displays python stack 
                                   traces when errors occur
      -s, --set=section.option=value   set a configuration option

Configuration:
    Anigrate looks in $HOME/.anigrate/config for your configuration by 
    default, to see the available configuration options, run `%(command)s help 
    configuration`. To list extensive information about every option, run 
    `%(command)s help options`.

Database:
    By default anigrate uses an sqlite database in $HOME/.anigrate/db,
    see the example anigraterc for other possibilities.

Import/Export Formats:
    For extended information on available database import and export formats, 
    see `%(command)s help dbformat`. The following formats are available:

    csv, anidb, myanimelist
"""

