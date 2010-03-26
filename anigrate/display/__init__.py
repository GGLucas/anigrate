# coding=utf-8
from anigrate.config import Config

class Display(object):
    def __init__(self, header=None, footer=None, line=None):
        if Config.getboolean("appearance","unicode_enabled"):
            self.hsep = " │ "
            self.vsep = "─"
            self.vjoin = ("─┴─", "─┼─", "─┬─")
        else:
            self.hsep = " | "
            self.vsep = "-"
            self.vjoin = ("-+-", "-+-", "-+-")

        if line: self.line = line
        if header: self.header = header
        if footer: self.footer = footer

    def _display_date(self, datetime):
        """
            Display a date in default format.
        """
        return str(datetime)

    def _column(self, text, size, color="normal", color_line="line", hsep=True):
        """
            Format a string to represent a column
        """
        if len(text)-text.count("\033")*7 > size:
            text = text[:size-2]+".."
        else:
            text = text.ljust(size)

        if hsep:
            return Config.multicolor(color, text, color_line, self.hsep)
        else:
            return Config.color(color, text)

    def _vline(self, length=None, column_sizes=None, color="line"):
        """
            Create a vertical line with columns.
        """
        if length:
            return self.vsep*length
        elif column_sizes:
            line = ""
            for i, length in enumerate(column_sizes):
                line += self.vsep*(length)+(self.vjoin[1] if i != len(column_sizes)-1 else "")
            return Config.color(color, line)
