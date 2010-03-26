# coding=utf-8
from __future__ import print_function
from anigrate.display import Display
from anigrate.config import Config

class ListDisplay(Display):
    """
        Display a list of series in a preset format.
    """

    def __init__(self, series, header=None, footer=None, line=None):
        Display.__init__(self, header, footer, line)

        self.columns = map(str.strip, Config.get("appearance", "list_columns") .split(","))
        self.column_sizes = map(int, Config.get("appearance", "list_column_sizes") .split(","))
        self.column_count = len(self.columns)
        self.column_size_count = len(self.column_sizes)
        self.series = series

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

        for i, column in enumerate(self.columns):
            line += self._column({
                "title": "Series",
                "progress": "Watched",
                "season": "Season",
                "rating": "Rating",
            }[column], 
                self.column_sizes[i] if 
                   self.column_size_count > i
                else 10,

                color = "header",
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
        color = "series_normal" if series.finished else (
            "series_dropped" if series.dropped else
            "series_watching"
        )

        for i, column in enumerate(self.columns):
            line += self._column({
                "title": series.title,
                "progress":  (
                     "%-3d/%3d" % (series.epscurrent, series.epstotal)
                        if series.epstotal > 0 else 
                      Config.multicolor("clear", "%-3d/" % series.epscurrent,
                                        "unknown", " ??")
                ),
                "season": "%d" % series.current,
                "rating": "%d" % series.rating if series.rating > 0 else "??",
            }[column], 
                self.column_sizes[i] if 
                   self.column_size_count > i
                else 10,

                color = (color if column != "rating" 
                         else self._rating_color(series.rating)),
                hsep=(i != self.column_count-1),
            )

        return line


    def output(self, print=print, indent="  "):
        """
            Output all the lines in the table by calling the given print function.
        """
        print(indent)
        print(indent+self.header())
        print(indent+self._vline(column_sizes=self.column_sizes))

        for series in self.series:
            print(indent+self.line(series))

        print(indent)
        print(indent+self.footer())
        print(indent)
