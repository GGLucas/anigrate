

HELPTEXT = """
Usage: %s [COMMAND] [ARGS...]: [SELECTOR]
Manage a list of watched anime or television series.

Database:
    By default anigrate uses an sqlite database in $HOME/.anigrate/db,
    see the example anigraterc for all the other possibilities.

Commands:
    list: [selector]
        List all series matched by [selector].
        If no selector is given, match all series.

    log: (selector)
        Show a detailed log for series matching (selector).

    hist [num]: [selector]
        Show the last [num] watched episode entries for series matching
        [selector]. Num defaults to 15, matches all series if no selector
        is specified.

    add [category] [watched[/total][*seasons]] [rating] [duration]: (name)
        Add a new series entry with name specified by (name).
        Optionally, you can specify the category, duration, amount of episodes
        watched, amount of episodes total, amount of seasons and rating.

        Note that if you specify to create multiple seasons, every season will
        have the same watched and total amounts you specified here.

    category [category]: (selector)
        Mark all series matched by (selector) as having category [category].

    remove: (selector)
        Completely remove any series that match (selector).

    rate <score>: (selector)
        Rate all series matched by (selector) with <score>.

    [un]drop: (selector)
        Mark all series matched by (selector) as dropped or not dropped.

    length <length>: (selector)
        Set the active season's length in episodes.

    duration <time>: (selector)
        Set the average duration of an episode in series matching (selector).
        This is used to calculate total watching time, defaults to 24 minutes
        per episode for every series.

    time: [selector]
        Get the total watching time spent on series matching [selector].
        If no selector is given the total time for all series is given.

    watch [num]: (selector)
        Change the episodes watched count. Without [num] specified it will be
        incremented by one. Using specifiers like "+3" or "-2" you can increment
        or decrement the watched count by that number. Specifying an absolute
        number will watch up to that episode or remove everything from that
        episode on. Watch always uses the currently active season.

    season add [watched[/total]] [num]: (selector)
        Add a new season, if num is specified the season number is set to that, 
        otherwise it will default to one more than the previous season.

        Optionally, you can specify the watched/total episode amounts to be set 
        for this season.

    season remove [num]: (selector)
        Remove the season with number [num] from a series. If num is not
        specified the currently active season will be removed.

    season length <season> <length>: (selector)
        Set a season's length in episodes.

    season active <num>: (selector)
        Set season with number <num> as the active season. Can be a relative 
        offset like +1 or -2.

    stats: [selector]
        Show a list of various statistics about the times and dates episodes
        of series matching [selector] have been watched. If no selector is
        given, show statistics about all series.



    import [file] [format] [category]
        Import a list of series to put in the database from a file.
        If file is not specified or is "-", the file will be read from stdin.
        If category is specified, all new series imported will be set
        to that category. This allows for easier organisation.
        See "Database Formats" for an explanation on how those work.

    export [file] [format]: [selector]
        Export a list of series from in the database to a file.
        If file is not specified or is "-", the file will be output to stdout.
        If a selector is given, only series matching that selector will be 
        exported.
        See "Database Formats" for an explanation on how those work.


    runserver [type] [host] [port]
        Run a server displaying an html public list on [host] (default: localhost)
        and [port] (default: 4310). Type is set to "http" by default and will 
        host a simple http webserver not meant to be used in production. If 
        flup is installed, you can additionally specify [type] to be "fcgi", 
        "scgi" or "ajp" and it will host a server with that protocol.

        Note that the main anigrate binary can also be used as a wsgi script 
        and it will display the same html public list.

        You can specify any selector to display a list for in the address by 
        separating the terms with slashes. For example:

            http://localhost:4310/=anime/+watching/@title

    help
        Show this help message.

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

    %%exact
        When specified, only match series that exactly match the full selector.

    %%contains
        When specified, match all series containing the selector.

    %%suffix
        When specified, match all series that end with the selector.

    %%prefix
        Default behaviour: match all series that start with the selector.

    @rating, @activity, @watched, @title
        Set field to sort by, you can sort by series rating, series latest 
        activity, amount of episodes watched and title respectively.

    @split
        Default sort method, sorts by activity but splits into watching,
        finished and dropped groups first.

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

Examples:
    Here are some example use cases, note that every selector specifier or 
    command can be shortened to its smallest non-ambiguous prefix.

    anigrate list
        List all series in the database.

    anigrate li: =anime
        List all series in category "anime".

    anigrate li: +w
        List only series currently being watched.

    anigrate list: +c @r
        List all completed series sorted by the rating given.

    anigrate add anime: Mushishi
        Add a new series in category "anime" with name "Mushishi".

    anigrate watch: Mushishi
        Increment the watched count on the "Mushishi" series by one.

    anigrate w +3: Mus
        Increment the watched count by three on series prefixed by "Mus".
        ie. This command would match "Mus[shishi]" and thus increment
        that by three.

    anigrate season add: Mushishi
        Add a new season to series "Mushishi".

    anigrate se act 1: Mushishi
        Set season "1" as the active season on series "Mushishi".

    anigrate length 26: Mushishi
        Set the currently active season on series "Mushishi" as being
        26 episodes long.
"""

VERSIONTEXT = """Anigrate """+str(Config.ANIGRATE_VERSION)+
              """ <"""+Config.ANIGRATE_URI+""">

Copyright (C) 2009-2010 Lucas de Vries <lucas@glacicle.org>
License WTFPL: <http://sam.zoy.org/wtfpl>"""
