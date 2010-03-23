import os

## Application info
ANIGRATE_URI = "http://anigrate.glacicle.org"
ANIGRATE_VERSION = 1.0

## Places
CONF_DIR = os.getenv("HOME")+"/.anigrate"
DB_LOCATION = CONF_DIR+"/db"
CONF_LOCATION = CONF_DIR+"/config"

## Default weblink titles
DEFAULT_TITLE_LIST = "Watch List"
DEFAULT_TITLE_LOG = "Watch Log"
DEFAULT_TITLE_STATS = "Watch Stats"
DEFAULT_LINK = "http://en.wikipedia.org/wiki/Special:Search?search=%s"

## Date formats
DATE_FORMAT = "%a %d %b, %Y {LINE} %H:%M"
DATE_FORMAT_HTML = "%a %d %b, %Y %H:%M"

## Default colors
COLOR = {
    "normal": "\033[0m",
    "unknown": "\033[1;35m",
    "header": "\033[1;33m",
    "log_line": "\033[1;30m",

    "series_normal": "\033[1;36m",
    "series_watching": "\033[1;34m",
    "series_dropped": "\033[1;31m",
    "seasonnum": "\033[1;35m",
    "epcount": "\033[1;34m",

    "score_top": "\033[1;32m",
    "score_high": "\033[0;32m",
    "score_normal": "\033[0;37m",
    "score_low": "\033[0;31m",
    "score_critical": "\033[1;31m",

    "stat_name": "\033[1;37m",
    "stat_year": "\033[1;36m",
    "stat_num": "\033[1;35m",
    "stat_perc": "\033[1;34m",
}

## Color names
COLORS_AVAILABLE = ["black", "red", "green", "yellow", 
                    "blue", "magenta", "cyan", "white",]
