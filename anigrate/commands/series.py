import datetime

from anigrate.models import Session, Series, Season, Watched
from anigrate.util import register, selector, selector_literal, arguments, promptfor, debug, checkint

@register("add", shorthelp="add a new series")
@arguments(0, 5)
@selector_literal
def cm_add(name=None, category=None, progress=None, rating=None, duration=None):
    """
    add [category] [watched[/total][*seasons],..] [rating] [duration]: [name]
        Add a new series entry with name specified by (name).
        Optionally, you can specify the category, duration, amount of episodes
        watched, amount of episodes total, amount of seasons and rating.

        If no name is specified as selector, the add command will prompt for it 
        and any other arguments not specified either.
    """

    # Prompt for any missing arguments
    if not name:
        name = promptfor("Enter new series title")

        if not name:
            debug(" Error: Please input a series title.", False)

        if category is None:
            category = promptfor("Enter category", "")

        if progress is None:
            progress = promptfor("Enter series initial progress", "0/0")

        if rating is None:
            rating = promptfor("Enter series rating", "0")

        if duration is None:
            duration = promptfor("Enter episode duration in minutes", "24")

    # Check integer arguments
    if rating:
        rating = checkint(rating, "rating")
    else:
        rating = 0

    if duration:
        duration = checkint(duration, "duration")
    else:
        duration = 24

    # Check category
    if category is None:
        category = ""

    # Parse progress argument
    if progress:
        seasons = []

        for season in progress.split(","):
            # Amount of seasons to create like this
            if "*" in season:
                season, times = season.split("*", 1)
                times = checkint(times, "season multiplier")
            else:
                times = 1

            # Watched and total
            if "/" in season:
                watched, total = season.split("/")

                watched = checkint(watched, "watched amount")

                if total:
                    total = checkint(total, "total episodes")
                else:
                    total = watched
            else:
                watched = checkint(season, "watched amount")
                total = 0

            seasons.extend([(watched, total),]*times)
    else:
        seasons = ((0, 0),)

    # Check if series exists
    if Series.exists(name, category):
        debug("Error: A series with this title already exists in this"
              " category.", False)

    # Create series
    series = Series(
        title=name,
        rating=rating,
        category=category,
        duration=duration,
    )

    series.ctime = series.mtime = datetime.datetime.now()
    Session.add(series)

    # Create every season
    for num, (current, total) in enumerate(seasons):
        # Season entry
        season = Season(
            num=num,
            series=series,
            episode_total=total,
            current_watched=current,
        )

        Session.add(season)

        # Log entry
        if current > 0:
            watched = Watched(
                season=season,
                seasonnum=num,
                series=series,
                time=datetime.datetime.now(),
                startep=0,
                finishep=current,
            )

            Session.add(watched)

    # Series info
    series.current = num
    series.eval_finished()

    Session.commit()

@register("category", shorthelp="set series category")
@arguments(1, 2)
@selector
def cm_category(selector, value=None):
    """
    category [category]: (selector)
        Mark all series matched by (selector) as having category [category].
    """
    ## TODO: If selector is empty, show incremental switch

    for series in selector.all():
        orig = series.category

        # Prompt if not given
        if value is None:
            new = promptfor("Enter new category for series `%s`" % 
            series.title, orig, True)
        else:
            new = value

        series.category = new

    Session.commit()

@register("rate", shorthelp="set series rating")
@arguments(1, 2)
@selector
def cm_rate(selector, value=None):
    """
    rate [score]: [selector]
        Rate all series matched by [selector] with [score].
    """
    ## TODO: If selector is empty, show incremental switch

    if value is not None:
        value = checkint(value, "rating")

    for series in selector.all():
        orig = series.rating

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new rating for series `%s`" % 
            series.title, orig, True)

            # Convert to number
            if new == "":
                new = orig
            else:
                new = checkint(new, "rating", exit=False)
                continue
        else:
            new = value

        series.rating = new

    Session.commit()

@register("duration", shorthelp="set series duration")
@arguments(1, 2)
@selector
def cm_duration(selector, value=None):
    """
    duration [time]: [selector]
        Set the average duration of an episode in series matching [selector].
        This is used to calculate total watching time, defaults to 24 minutes
        per episode for every series.
    """
    ## TODO: If selector is empty, show incremental switch

    if value is not None:
        value = checkint(value, "duration")

    for series in selector.all():
        orig = series.duration

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new duration for series `%s`" % 
            series.title, orig, True)

            # Convert to number
            if new == "":
                new = orig
            else:
                new = checkint(new, "duration", exit=False)
                continue
        else:
            new = value

        series.duration = new

    Session.commit()
