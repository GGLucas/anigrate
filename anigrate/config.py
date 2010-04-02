import sys
import os
import codecs

from ConfigParser import ConfigParser
from StringIO import StringIO

# Parser
Config = ConfigParser()

# Configuration constants
Config.ANIGRATE_URI = "http://anigrate.glacicle.org"
Config.ANIGRATE_VERSION = "1.0.0"
Config.CONF_DIR = os.getenv("HOME")+"/.anigrate"
Config.DB_LOCATION = Config.CONF_DIR+"/db"
Config.CONF_LOCATION = Config.CONF_DIR+"/config"

# Color constants
Config.COLORS_AVAILABLE = ["black", "red", "green", "yellow", 
                           "blue", "magenta", "cyan", "white",]
Config.itemcolor = {}

# Easy functions for working with colored text
## Color a bit of text
Config.color = lambda elem, text: (
       text if elem not in Config.itemcolor else Config.itemcolor[elem]+text
)

## Color many bits of text and paste them together
Config.multicolor = lambda *text: "".join((
       text if (i%2) else (
         Config.itemcolor[text]
          if text in Config.itemcolor else
         ""
       )
    for i, text in enumerate(text))
)

# Set defaults
Config.readfp(StringIO("""
[anigrate]
default_mode=prefix
default_sort=split
default_log_limit=0
default_hist_limit=20
paranoia=1

[database]

[appearance]
color_enabled=yes
unicode_enabled=yes
date_format=%a %d %b, %Y
time_format=%H:%M
progress_format=season %S to ep %E
old_cutoff=14
log_reversed=yes
list_columns=title,progress,season,rating
list_column_sizes=48,7,6,7
log_columns=episode,date,time
log_column_sizes=48,16,7
hist_columns=title,progress,date,time
hist_column_sizes=28,18,16,6

[weblist]
title_list=Watch List
title_log=Watch Log
title_stats=Watch Stats
default=@title
css=
header=
footer=

[link]
default=http://en.wikipedia.org/wiki/Special:Search?search=%s
anime=http://myanimelist.net/anime.php?q=%s
tv=http://www.tv.com/search.php?qs=%s

[color]
normal=
line=
unknown=bold,magenta
header=bold,yellow
log_line=bold,black
series_normal=bold,cyan
series_watching=bold,blue
series_dropped=bold,red
seasonnum=bold,magenta
epcount=bold,blue
date_new=bold,green
date_old=
time_new=bold,green
time_old=
log_new=bold,green
log_old=
score_top=bold,green
score_high=green
score_normal=white
score_low=red
score_critical=bold,red
stat_name=bold,white
stat_year=bold,cyan
stat_num=bold,magenta
stat_perc=bold,blue
"""))

# Set default database location
Config.set("database", "uri", "sqlite:///"+Config.DB_LOCATION)

# Read configs
Config.read([Config.CONF_LOCATION, os.path.join(os.getcwd(), "anigraterc")])

# Parse colors into escape codes
if Config.getboolean("appearance", "color_enabled"):
    # Reset color
    Config.itemcolor["reset"] = "\033[0m"

    # Set all colors
    for item in Config.options("color"):
        attr = 0
        color = 37

        # Get all attributes
        for elem in Config.get("color", item).split(","):
            if elem == "bold":
                attr = 1
            elif elem in Config.COLORS_AVAILABLE:
                color = 30+Config.COLORS_AVAILABLE.index(elem)

        # Build escape code
        Config.itemcolor[item] = "\033[%d;%dm" % (attr, color)


# Check if UTF-8 should be enabled
if Config.getboolean("appearance", "unicode_enabled"):
    # Force stdout and stderr to use utf-8
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
