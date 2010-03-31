from __future__ import print_function

from anigrate.display import Display
from anigrate.display.serieslist import ListDisplay
from anigrate.config import Config

class HistDisplay(Display):
    """
        Display a history log in a preset format.
    """

    def __init__(self, selector=None, log=None, limit=None, date=None, header=None, footer=None, line=None):
        Display.__init__(self, header, footer, line)

        if limit is None:
            limit = Config.getint("anigrate", "default_hist_limit")

        if selector:
            self.selector = selector
            self.log = selector.log(limit=limit, date=date)
        elif log:
            self.selector = None
            self.log = log

        # Get all columns and sizes from the configuration
        self.columns = map(str.strip, Config.get("appearance", "hist_columns") .split(","))
        self.column_sizes = map(int, Config.get("appearance", "hist_column_sizes") .split(","))

        # Check if some sizes are missing
        self.column_count = len(self.columns)
        sizes = len(self.column_sizes)

        # Add any missing sizes as default
        if self.column_count > sizes:
            self.column_sizes += (
              [Config.getint("appearance","default_column_size")]*
              (self.column_count-sizes))

    def output(self, print=print):
        """
            Output all the lines in the table by calling the given print function.
        """
        print("")
        print(self.header())
        print(self._vline(column_sizes=[(size, 2) for size in self.column_sizes]))

        for entry in self.log:
            line = self.line(entry)

            # Check if we just got a list of lines
            if hasattr(line, "__iter__"):
                for line in line:
                    print(line)
            else:
                print(line)

        print(self._vline(column_sizes=[(size, 0) for size in self.column_sizes]))
        print(self.footer())

    def header(self):
        """
            Generate the header line to display above the table.
        """
        line = ""

        # Generate columns
        Columns = {
            "title": "History",
        }

        # List columns in string
        for i, column in enumerate(self.columns):
            line += self._column(
                Columns[column] if column in Columns else "",
                self.column_sizes[i],
                color="header",
                hsep=False,
                offset=int(i == 0),
            )

        return line

    def line(self, entry):
        """
            Generate the table entry to display for one log entry.
        """
        series = entry.series
        line = ""

        # Get colors to use for columns
        rating_color = self._rating_color(series.rating) if series.rating > 0 else "normal"
        normal_color = "normal"

        # Generate columns
        Columns = {
            "title": (rating_color, series.title),
            "progress": self._progress(entry.seasonnum, entry.finishep),
            "date": (normal_color, self._date(entry.time)),
            "time": (normal_color, self._time(entry.time)),
        }

        # List columns in string
        for i, column in enumerate(self.columns):
            line += self._column(
                Columns[column] if column in Columns else (normal_color, "???"),
                self.column_sizes[i],
                color=None,
                hsep=(i != self.column_count-1),
                offset=int(i == 0),
            )

        return line
