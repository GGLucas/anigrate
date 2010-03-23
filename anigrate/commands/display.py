from anigrate.util import register, selector

@register("info")
@selector
def cm_info(selector):
    """
    info: [selector]
        Output a no-nonsense list with information on all series matched by
        [selector], useful for piping into other binaries. If no selector is 
        given, match all series.

        Outputs series info in format:
            title\tcurrent_episode\ttotal_episodes\tcurrent_season\trating

        ie. each item is separated by a tab character for easy parsing.
    """

    for series in selector.all():
        print("%s\t%d\t%d\t%d\t%d" % (
               series.title, series.epscurrent,
               series.epstotal, series.current,
               series.rating
            ))

@register("match")
@selector
def cm_match(selector):
    """
    match: [selector]
        Output a simple no-nonsense list of series matched by [selector],
        useful for piping into other binaries. If no selector is given, match
        all series.
    """
    # Display header
    for sel in selector.all():
        print(sel.title)
