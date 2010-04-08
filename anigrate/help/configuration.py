ConfigHelp = {
"anigrate.default_mode":
    """
    anigrate.default_mode
        Default: "prefix"

        Specify a matching mode (prefix, suffix, contains, exact) to use 
        by default in selectors where none is specified.
    """,

"anigrate.default_sort":
    """
    anigrate.default_sort
        Default: "split"

        Specify a sort mode (rating, activity, watched, title, split) to use
        by default in selectors where none is specified.
    """,

"anigrate.default_log_limit":
    """
    anigrate.default_log_limit
        Default: 0

        The amount of log entries to display by default for the 'log' command.
    """,

"anigrate.default_hist_limit":
    """
    anigrate.default_hist_limit
        Default: 20

        The amount of log entries to display by default for the 'history' 
        command.
    """,

"anigrate.paranoia":
    """
    anigrate.paranoia
        Default: 1

        Decides when to alert you when you are about to perform operations
        on large amounts of series. This prevents you from accidentally typing
        'anigrate remove' and destroying your database.

        A level of 0 never alerts you, even if the command would destroy the 
        database. A level of 1 only alerts you for potentially 
        database-destroying operations and a level of 2 alerts whenever you 
        are about to modify more than one series at a time.
    """,

"anigrate.matcher_enabled":
    """
    anigrate.matcher_enabled
        Default: yes

        Whether to display an incremental series matcher when no selector is
        specified on some commands.
    """,

"anigrate.matcher_items":
    """
    anigrate.matcher_items
        Default: 15

        How many items to display in the matcher list by default.
    """,

"database.uri":
    """
    database.uri
        Default: sqlite:///$HOME/.anigrate/config

        Specifies the database to connect to. This should be a valid sqlite 
        connection string.

        For example: mysql://user:password@my-domain.org/anigrate-database
    """,

"appearance.color_enabled":
    """
    appearance.color_enabled
        Default: yes

        Whether to use color when outputting to the commandline.
    """,

"appearance.unicode_enabled":
    """
    appearance.unicode_enabled
        Default: yes

        Whether to use box drawing characters when outputting to the 
        commandline. Setting this to no will result in ascii characters
        being used instead.
    """,

"appearance.date_format":
    """
    appearance.date_format
        Default: %a %d %b, %Y

        The format used when displaying dates. Uses python strftime format
        specifiers.
    """,

"appearance.time_format":
    """
    appearance.time_format
        Default: %H:%M

        The format used when displaying times. Uses python strftime format
        specifiers.

    """,

"appearance.progress_format":
    """
    appearance.progress_format
        Default: season %S to ep %E

        The format to display progress indication in. You can use %S for
        the season and %E for the episode the progress should express.
    """,

"appearance.old_cutoff":
    """
    appearance.old_cutoff
        Default: 14

        The amount of days an entry should be in the past before it is
        considered "old" for display purposes.
    """,

"appearance.log_reversed":
    """
    appearance.log_reversed
        Default: yes

        Whether to reverse the order in which log entries are outputted.
        If no, log entries will be sorted from oldest to newest.
    """,

"appearance.list_columns":
    """
    appearance.list_columns
        Default: title,progress,season,rating

        The columns displayed when a list of series is required.

        Available columns:
            title
            progress
            season
            rating
    """,

"appearance.list_column_sizes":
    """
    appearance.list_column_sizes
        Default: 48,7,6,7

        The sizes of the columns in the list of series. Each size is
        given in the amount of characters it is allowed to take.
    """,

"appearance.log_columns":
    """
    appearance.log_columns
        Default: episode,date,time

        The columns displayed when a log entry is output.

        Available columns:
            episode
            date
            time
    """,

"appearance.log_column_sizes":
    """
    appearance.log_column_sizes
        Default: 48,16,7

        The sizes of the columns in a log entry. Each size is
        given in the amount of characters it is allowed to take.
    """,

"appearance.hist_columns":
    """
    appearance.hist_columns
        Default: title,progress,date,time

        The columns displayed in the history list.

        Available columns:
            title
            progress
            date
            time
    """,

"appearance.hist_column_sizes":
    """
    appearance.hist_column_sizes
        Default: 28,18,16,6

        The sizes of the columns in a history entry. Each size is
        given in the amount of characters it is allowed to take.
    """,





"link":
    """
    link
        This configuration section specifies how to build links to 
        informational websites according to a series' category. Each entry in 
        this section is the name of a category and each value the url of a 
        website with information.

        The "default" entry is used when no entry is found for the category a
        series is in.

        In the urls, %s is replaced by the title of the series information is 
        requested for.

        Default:
            [link]
            default=http://en.wikipedia.org/wiki/Special:Search?search=%s
            anime=http://myanimelist.net/anime.php?q=%s
            tv=http://www.tv.com/search.php?qs=%s
    """,

"color":
    """
    color
        This configuration section specifies the colors to use on the 
        commandline when appearance.color_enabled is on.

        Each entry specifies the color for one particular type of text.
        Colors are either in the format "bold,$COLOR" or just "$COLOR",
        where $COLOR is one of "black", "red", "green", "yellow", "blue",
        "magenta", "cyan" or "white".

        An empty entry uses the terminal's default colors.

        Default:
            [color]
            normal=
            line=
            unknown=bold,magenta
            header=bold,yellow
            log_line=bold,black
            series_normal=bold,cyan
            series_watching=bold,blue
            series_dropped=bold,red
            seasonnum=bold,magenta
            epcount=bold,blue
            date_new=bold,green
            date_old=
            time_new=bold,green
            time_old=
            log_new=bold,green
            log_old=
            score_top=bold,green
            score_high=green
            score_normal=white
            score_low=red
            score_critical=bold,red
            stat_name=bold,white
            stat_year=bold,cyan
            stat_num=bold,magenta
            stat_perc=bold,blue
    """,
}
