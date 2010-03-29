# coding=utf-8
from anigrate.config import Config

class Display(object):
    def __init__(self, header=None, footer=None, line=None):
        if Config.getboolean("appearance","unicode_enabled"):
            self.hsep = u" │ "
            self.vsep = u"─"
            self.vjoin = (u"─┴─", u"─┼─", u"─┬─")
        else:
            self.hsep = " | "
            self.vsep = "-"
            self.vjoin = ("-+-", "-+-", "-+-")

        if line: self.line = line
        if header: self.header = header
        if footer: self.footer = footer

    def _date(self, datetime):
        """
            Display a date in default format.
        """
        return datetime.strftime(Config.get("appearance", "date_format"))

    def _time(self, datetime):
        """
            Display a date in default format.
        """
        return datetime.strftime(Config.get("appearance", "time_format"))

    def _column(self, text, size, color="normal", color_line="line", hsep=True, offset=0):
        """
            Format a string to represent a column
        """
        if hasattr(text, "__iter__"):
            # Make a list for convenience
            text = list(text)
        else:
            # Put single string into the list
            text = [text]

        # Insert our color
        if color:
            text.insert(0, color)

        # Check for column offset
        if offset:
            text.insert(0, " "*offset)
            text.insert(0, "normal")

        # Check for text length matching up to column size
        total_length = 0
        textitems = len(text)/2

        for i in range(textitems):
            itx = i*2+1
            textlen = len(text[itx])

            if total_length+textlen > size:
                # We've reached the final point, cut off the text
                text[itx] = text[itx][:size-total_length-textlen-2]+".."
                text = text[:itx+1]
                break
            elif (total_length+textlen < size and 
                  i == textitems-1):
                # The last item is still too small, justify it
                text[itx] = text[itx].ljust(size-total_length)

            total_length += textlen

        # Insert our separator
        if hsep:
            text.extend((color_line, self.hsep))

        # Put it through multicolor
        return Config.multicolor(*text)

    def _vline(self, length=None, column_sizes=None, color="line"):
        """
            Create a vertical line with columns.
        """
        if length:
            # Just return a single vertical line
            return self.vsep*length
        elif column_sizes:
            line = ""
            columns = len(column_sizes)

            # Add join separators at all sizes
            for i, length in enumerate(column_sizes):
                # Check if join type was specified
                if hasattr(length, "__iter__"):
                    jtype = length[1]
                    length = length[0]
                else:
                    jtype = 1

                # Add separator on line
                line += (self.vsep*length+
                        (self.vjoin[jtype] if i != columns-1 else ""))

            return Config.color(color, line)
        else:
            return ""

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

    def _progress(self, season, episode, color="normal"):
        """
            Get a list of color+text for the progress column.
        """
        text = Config.get("appearance", "progress_format")
        season = str(season)
        episode = str(episode)
        before = ""

        if "%S" in text:
            before, text = text.split("%S", 1)

            if "%E" in before:
                before, after = before.split("%E", 1)
                output = (
                    color, before,
                    "epcount", episode,
                    color, after,
                    "seasonnum", season,
                    color, text
                )
            elif "%E" in text:
                after, text = text.split("%E", 1)
                output = (
                    color, before,
                    "seasonnum", season,
                    color, after,
                    "epcount", episode,
                    color, text
                )
            else:
                output = (
                    color, before,
                    "seasonnum", season,
                    color, text
                )
        else:
            if "%E" in text:
                before, text = text.split("%E", 1)
                output = (
                    color, before,
                    "epcount", episode,
                    color, text
                )
            else:
                output = (color, text)

        return output

    def header(self):
        return ""

    def footer(self):
        return ""

    def line(self, entry):
        return ""
