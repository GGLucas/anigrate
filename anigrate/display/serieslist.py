from __future__ import print_function
from anigrate.display import Display
from anigrate.config import Config

class ListDisplay(Display):
    """
        Display a list of series in a preset format.
    """

    def __init__(self, selector=None, series=None, header=None, footer=None, line=None):
        Display.__init__(self, header, footer, line)

        if selector:
            self.selector = selector
            self.series = selector.all()
        elif series:
            self.selector = None
            self.series = series

        # Get all columns and sizes from the configuration
        self.columns = map(str.strip, Config.get("appearance", "list_columns") .split(","))
        self.column_sizes = map(int, Config.get("appearance", "list_column_sizes") .split(","))

        # Check if some sizes are missing
        self.column_count = len(self.columns)
        sizes = len(self.column_sizes)

        # Add any missing sizes as default
        if self.column_count > sizes:
            self.column_sizes += (
              [Config.getinteger("appearance","default_column_size")]*
              (self.column_count-sizes))

    def _rating_color(self, rating):
        """
            Get the color to display for a certain rating.
        """
        return [
                "unknown", "score_critical",
                "score_critical", "score_critical",
                "score_low", "score_low",
                "score_normal", "score_normal",
                "score_high", "score_high",
                "score_top",
            ][rating]

    def header(self):
        """
            Generate the header line to display above the table.
        """
        line = ""

        # Generate columns
        Columns = {
            "title": "Series",
            "progress": "Watched",
            "season": "Season",
            "rating": "Rating",
        }

        # List columns in string
        for i, column in enumerate(self.columns):
            line += self._column(
                Columns[column] if column in Columns else "???",
                self.column_sizes[i],
                color="header",
                hsep=(i != self.column_count-1),
            )

        return line

    def footer(self):
        """
            Generate the footer line to display below the table.
        """
        return Config.color("normal", "%d series displayed." % len(self.series))


    def line(self, series):
        """
            Generate the table entry to display for one series.
        """
        line = ""

        # Get colors to use for columns
        rating_color = self._rating_color(series.rating)
        series_color = "series_normal" if series.finished else (
                       "series_dropped" if series.dropped else
                       "series_watching")

        # Generate columns
        Columns = {
            "title": (series_color, series.title),
            "season": (series_color, str(series.current)),
            "rating": (rating_color, str(series.rating or "??")),
        }

        # Generate "progress" column
        if series.epstotal > 0:
            ## Both current and total is known
            Columns["progress"] = (series_color, "%-3d/%3d" % (
                                    series.epscurrent, series.epstotal
                                  ))
        else:
            ## Total is as of yet unknown
            Columns["progress"] = (series_color, "%-3d/ " % series.epscurrent,
                                   "unknown", "??")

        # List columns in string
        for i, column in enumerate(self.columns):
            line += self._column(
                Columns[column] if column in Columns else "???",
                self.column_sizes[i],
                color=None,
                hsep=(i != self.column_count-1),
            )

        return line


    def output(self, print=print):
        """
            Output all the lines in the table by calling the given print function.
        """
        print("")
        print(self.header())
        print(self._vline(column_sizes=self.column_sizes))

        for series in self.series:
            line = self.line(series)

            # Check if we just got a list of lines
            if hasattr(line, "__iter__"):
                for line in line:
                    print(line)
            else:
                print(line)

        print("")
        print(self.footer())
        print("")
