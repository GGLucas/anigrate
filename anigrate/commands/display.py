from anigrate.util import register, selector, arguments
from anigrate.display.list import ListDisplay

@register("info")
@arguments(1)
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
@arguments(1)
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

@register("list")
@arguments(1)
@selector
def cm_list(selector):
    """
    list: [selector]
        List all series matched by [selector].
        If no selector is given, match all series.
    """
    ListDisplay(selector.all()).output()
