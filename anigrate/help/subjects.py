Subjects = {
    "selectors": """
Selectors:
    Selectors are used to find series to act upon. In its most basic form, a 
    selector is simply the name of a series or the beginning of a name of a 
    series (note that the selector will match any series that start with the 
    specified name). Within the selector, the options listed below can be given.

    +finished/+completed, +watching, +dropped, +undropped:
        Put any of these in a separate argument anywhere in the selector and it 
        will only match series that satisfy the condition.

    =<category>
    =%<category>
        Will only match series in the specified category. If a % is specified,
        exactly match the category behind it, otherwise match any categories
        that start with the specified string.

    %exact
        When specified, only match series that exactly match the full selector.

    %contains
        When specified, match all series containing the selector.

    %suffix
        When specified, match all series that end with the selector.

    %prefix
        Default behaviour: match all series that start with the selector.

    @rating, @activity, @watched, @title
    @-rating, @-activity, @-watched, @-title
        Set field to sort by, you can sort by series rating, series latest 
        activity, amount of episodes watched and title respectively.
        Specifying a "-" reverses the order.

    @split
    @-split
        Default sort method, sorts by activity but splits into watching,
        finished and dropped groups first.

""",

    "dbformat": """
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
""",

    "dates": """
Date Formats:
    Some commands allow a date to be specified as an argument. By default, dates
    are parsed in YYYYMMDD format. If the `dateutil` package has been installed 
    on the system, any format that can be parsed by it becomes acceptable.
        """,

    "configuration": """
Configuration:
    There are a number of configuration options available to be set. The 
    default location for your config file is in $HOME/.anigrate/config. You 
    can print a list of options currently set by running `anigrate config`.

    The following configuration options are available, run `anigrate help 
    $OPTION` for more information about one of them, or run `anigrate help 
    options` to see the complete list of extended information.
    """
}
