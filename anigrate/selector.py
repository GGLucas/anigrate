from math import floor

from anigrate.models import Series, Watched, Session
from anigrate.config import Config
from anigrate.util import choose

from sqlalchemy.orm import eagerload
from sqlalchemy.sql import functions

SORT = {
    "rating":   [(Series.rating, "desc")],
    "activity": [(Series.mtime, "desc")],
    "watched":  [(Series.epscurrent, "desc")],
    "title":    [(Series.title, "asc")],
    "split":    [(Series.dropped, "asc"),
                 (Series.finished, "asc"),
                 (Series.mtime, "desc")],
}

FILTER = {
    "finished":  (Series.finished == True,
                  Series.dropped  == False,),
    "watching":  (Series.finished == False,
                  Series.dropped  == False,),
    "dropped":   (Series.dropped  == True,),
    "undropped": (Series.dropped  == False,),
}

MODE = {
    "exact":    Series.title.ilike,
    "contains": Series.title.contains,
    "suffix":   Series.title.endswith,
    "prefix":   Series.title.startswith,
}

class Selector(object):
    """
        Build a query from a command line selector list.
    """
    def __init__(self, selector=[]):
        self.parse_selector(selector)

    def parse_selector(self, selector):
        # Instance variables
        self.selector = selector
        self.string = []
        self.filters = []
        self.sort = []

        # Initial category
        category = "all"
        category_exact = False

        # Initial mode and sort
        default_mode = MODE[Config.get("anigrate", "default_mode")]
        sort = Config.get("anigrate", "default_sort")
        mode = None
        sortdir = True

        # Check for inverted default sort
        if sort[0] == "-":
            sortdir = False
            sort = sort[1:]

        # Retrieve sort list
        sort = SORT[sort]

        # Get filters
        for opt in self.selector:
            if opt[0] == "+":
                # Add state filter
                filt = choose(FILTER, opt[1:], allow_multi=False,
                                               value_only=True)
                if filt: self.filters.extend(filt)
            elif opt[0] == "%":
                # Change mode
                mode = choose(MODE, opt[1:], allow_multi=False,
                                             value_only=True)
            elif opt[0] == "@":
                # Change sort
                if len(opt) > 1 and opt[1] == "-":
                    # Inverted sort
                    sort = choose(SORT, opt[2:], allow_multi=False,
                                                 value_only=True)
                    sortdir = False
                else:
                    # Regular sort
                    sort = choose(SORT, opt[1:], allow_multi=False,
                                                 value_only=True)
                    sortdir = True
            elif opt[0] == "=":
                # Change category
                if len(opt) > 1 and opt[1] == "%":
                    # Exact match
                    category = opt[2:]
                    category_exact = True
                else:
                    # Non-exact match
                    category = opt[1:]
                    category_exact = False
            else:
                # Use as a title specifier
                self.string.append(opt)


        # Join the string list into a single string
        self.string = " ".join(self.string)

        # Replace wildcards in string
        self.string = self.string.replace("*", "%")

        # Filter on remaining string
        self.filters.append((mode if mode else default_mode)(self.string))

        # Filter or category
        if category != "all":
            if category_exact:
                self.filters.append(Series.category.ilike(category))
            else:
                self.filters.append(Series.category.startswith(category))

        # Sort the result
        if sort:
            for elem in sort:
                if (elem[1] == "desc" and sortdir) or \
                   (elem[1] == "asc" and not sortdir):
                    self.sort.append(elem[0].desc())
                else:
                    self.sort.append(elem[0].asc())

    def add_filters(self, query):
        # Add filters
        for filt in self.filters:
            query = query.filter(filt)

        # Add sort
        query = query.order_by(*self.sort)

        return query

    @property
    def query(self):
        return self.add_filters(Series.query)

    @property
    def log_query(self):
        # Build a log query
        query = Watched.query
        subquery = self.query.subquery()

        # Only display from matching series
        query = query.join((
            subquery,
            subquery.c.id == Watched.series_id))

        # Preload series objects
        query = query.options(eagerload('series'))

        # Order by date
        query = query.order_by(Watched.time.desc())

        return query

    @property
    def time(self):
        query = Session.query(
            functions.sum(Series.duration.op("*")(Series.epsall)))

        totalminutes = minutes = int(self.add_filters(query).one()[0])
        totaldays = minutes/1440.0
        times = []

        for duration in [525960,43200,10080, 1440, 60, 1]:
            amount = floor(minutes/duration)
            minutes -= amount*duration
            times.append(amount)

        return totalminutes, totaldays, times

    def __repr__(self):
        return str(self.query)

    def count(self):
        return self.query.count()

    def all(self):
        return self.query.all()

    def log_all(self):
        return self.query.options(eagerload('watched')).all()

    def season_all(self):
        return self.query.options(eagerload('seasons')).all()

    def all_all(self):
        return self.query.options(eagerload('seasons'), eagerload('watched')).all()

    def log(self, limit=None, date=None):
        query = self.log_query

        if date:
            query = query.filter(
                Watched.time < date
            )

        if limit:
            query = query.limit(limit)

        return query.all()
