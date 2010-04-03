import datetime

from anigrate.display.serieslist import ListDisplay
from anigrate.config import Config
from anigrate.util import showdate, showtime

class LogDisplay(ListDisplay):
    def __init__(self, selector=None, series=None, header=None, footer=None, line=None, limit=None):
        if selector:
            self.selector = selector
            self.series = selector.log_all()
        elif series:
            self.selector = None
            self.series = series

        # Check log limit
        if limit is None:
            self.limit = Config.getint("anigrate", "default_log_limit")
        else:
            self.limit = limit

        # Date after which log entries count as old
        self.old_cutoff = datetime.datetime.now()-datetime.timedelta(
                           days=Config.getint("appearance","old_cutoff"))

        # Get all columns and sizes from the configuration
        self.log_columns = map(str.strip, Config.get("appearance", "log_columns").split(","))
        self.log_column_sizes = map(int, Config.get("appearance", "log_column_sizes").split(","))

        # Check if some sizes are missing
        self.log_column_count = len(self.log_columns)
        sizes = len(self.log_column_sizes)

        # Add any missing sizes as default
        if self.log_column_count > sizes:
            self.log_column_sizes += (
              [10]*(self.log_column_count-sizes))

        ListDisplay.__init__(self, header=header, footer=footer, line=line)

        # Get the absolute positions of the list columns
        abstopcols = [sum(self.log_column_sizes[:i+1])+3*i for i in 
                       range(self.log_column_count)]

        absbotcols = [sum(self.column_sizes[:i+1])+3*i for i in 
                       range(self.column_count)]

        # Swap them if there are more log cols
        if self.log_column_count >= self.column_count:
            absbotcols, abstopcols = abstopcols, absbotcols
            absswap = True
        else:
            absswap = False

        # Calculate the joins between log and list columns
        self.log_column_joins_top = []
        self.log_column_joins_bottom = []

        for i, col in enumerate(absbotcols):
            # Get size of column
            size = col-absbotcols[i-1]-3 if i > 0 else col

            # Get position in list
            try:
                num = abstopcols.index(col)
            except ValueError:
                num = -1

            # Check for type of join
            if num != -1 and num != (self.column_count if absswap else self.log_column_count)-1:
                self.log_column_joins_top.append((size, 1))
                self.log_column_joins_bottom.append((size, 1))
            else:
                if absswap:
                    self.log_column_joins_top.append((size, 2))
                    self.log_column_joins_bottom.append((size, 0))
                else:
                    self.log_column_joins_top.append((size, 0))
                    self.log_column_joins_bottom.append((size, 2))

    def line(self, series):
        # Get list line first
        lines = [ListDisplay.line(self, series)]

        # Vertical separator
        lines.append(self._vline(column_sizes=self.log_column_joins_top, color="log_line"))

        # Get log entries
        log = list(series.watched)

        # Check if the log should be reversed
        if Config.getboolean("appearance", "log_reversed"):
            log.reverse()

        # Check if we have a limit
        if self.limit:
            log = log[:self.limit]

        # Build log 
        for entry in log:
            # Create empty line to fill
            isold = entry.time < self.old_cutoff
            normalcolor = "log_old" if isold else "log_new"
            lines.append("")

            # Fill the line with the columns
            for i, column in enumerate(self.log_columns):
                if column == "episode":
                    # Season and episode info
                    text = self._progress(entry.seasonnum, entry.finishep)
                elif column == "date":
                    # Watch date
                    text = (
                        "date_old" if isold else "date_new",
                        showdate(entry.time)
                    )
                elif column == "time":
                    # Watch time
                    text = (
                        "time_old" if isold else "time_new",
                        showtime(entry.time)
                    )
                else:
                    # Unknown column
                    text = (normalcolor, "???")

                # Add to the end of log line
                lines[-1] += self._column(
                    text,
                    self.log_column_sizes[i], 
                    color=None,
                    color_line="log_line",
                    hsep=(i != self.log_column_count-1),
                    offset=int(i==0),
                )

        # Vertical separator
        lines.append(self._vline(column_sizes=self.log_column_joins_bottom, color="log_line"))

        return lines
