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
