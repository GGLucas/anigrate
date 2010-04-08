#!/usr/bin/env python
import sys
sys.path.append(".")

from anigrate.help.subjects import Subjects
from anigrate.help.configuration import ConfigHelp
from anigrate.util import (Commands_Order, Commands,
                          Commands_Season, Commands_Season_Order)
import anigrate.commands

HEADER = """<!DOCTYPE html>
<title>Anigrate: simple cli watch list management</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
  html {
    font-family: "Helvetica", sans-serif;
    font-size: 0.9em;
    padding: 0 1em;
    margin: 0 10%;
  }

  h1,h2,h3,h4 {
    margin: .5em 0;
  }

  p {
    margin: 0.5em 0;
  }

  a {
    text-decoration: none;
  }

  ul {
    list-style-type: square;
  }

  img {
    border: 2px solid #eee;
  }

  section > h1 {
    font-size: 1.4em;
    margin-top: 1em;
  }

  section > h2 {
    font-size: 85%;
  }

  section > section {
    font-size: 0.9em;
  }

  section > section > small {
    font-size: 85%;
    font-weight: bold;
    color: #555;
  }

  section > section > h1 {
    font-size: 100%;
  }

  section > section > h2 {
    font-size: 85%;
    color: #444;
  }

  nav ul {
    column-width: 15em;
    -moz-column-width: 15em;
    -webkit-column-width: 15em;
  }
</style>

<header>
  <hgroup>
    <h1>Anigrate</h1>
    <h2>simple cli watch list management</h2>
  </hgroup>

  <nav><ul>
    <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#install">Installation</a></li>
    <li><a href="#usage">Usage Examples</a></li>
    <li><a href="#selectors">Selectors</a></li>
    <li><a href="#dbformat">Database Formats</a></li>
    <li><a href="#dates">Date Formats</a></li>
    <li><a href="#commands">Commands</a></li>
    <li><a href="#configuration">Configuration Options</a></li>
    <li><a href="#configexample">Example Configuration</a></li>
  </ul></nav>
</header>

<section id="screenshots">
  <h1>Screenshots</h1>
  <a href="http://anigrate.glacicle.org/cli_shot1.png">
  <img src="http://anigrate.glacicle.org/cli_shot1.thumb.png" alt="" /></a>
  <a href="http://anigrate.glacicle.org/cli_shot2.png">
  <img src="http://anigrate.glacicle.org/cli_shot2.thumb.png" alt="" /></a>
  <a href="http://anigrate.glacicle.org/web_shot1.png">
  <img src="http://anigrate.glacicle.org/web_shot1.thumb.png" alt="" /></a>
  <a href="http://anigrate.glacicle.org/web_shot2.png">
  <img src="http://anigrate.glacicle.org/web_shot2.thumb.png" alt="" /></a>
  <a href="http://anigrate.glacicle.org/web_shot3.png">
  <img src="http://anigrate.glacicle.org/web_shot3.thumb.png" alt="" /></a>
  <a href="http://anigrate.glacicle.org/web_shot4.png">
  <img src="http://anigrate.glacicle.org/web_shot4.thumb.png" alt="" /></a>
</section>

<section id='about'>
  <h1>About</h1>
  <p>Anigrate is a simple, no-nonsense watch list manager for anime and tv 
  series made for people who like to do most of their work in a shell, yet 
  want something full-featured to keep track of their series for them.</p>

  <p>Features include a full log view of everything ever watched, a public web list 
  for showing off or simply for a pretty view of your watch list and detailed 
  statistics about your watching behaviour.</p>

  <p>Anigrate uses a simple sqlite database in your home directory by default, 
  there's no need to configure or set anything up other than the main binary. 
  However, if you want to, you can connect to a remote mysql database and keep 
  track of your watch list centrally. The web interface can be run stand-alone 
  with a simple command, but can also be used through wsgi (and, if flup is 
  installed, you can run an fcgi or scgi server).</p>
</section>

<section id="features">
  <h1>Features</h1>
  <ul>
    <li>Full per-episode watch log including seasons.</li>
    <li>Extensive series selector system for easy target specification.</li>
    <li>Organisation of series into multiple categories.</li>
    <li>Setting per episode duration individually per series, and 
    calculating the total time spent watching from this.</li>
    <li>Specifying your rating for a series and sorting by rating.</li>
    <li>Various watch statistics; episodes watched per month/year/day of 
    the week/hour of the day/etc.</li>
    <li>View-only weblist server (http, wsgi, fcgi, scgi) that can 
    display all this information in a pretty public list.</li>

    <li>
      <strong>[New]</strong>
      Import database from <a href="http://myanimelist.net">myanimelist.net</a>
      or <a href="http://anidb.net">anidb.net</a> export formats.
    </li>
    <li>Support for local or remote databases in any format supported by
    <a href="http://sqlalchemy.org">sqlalchemy</a>.</li>
  </ul>
</section>

<section id="contact">
  <h1>Contact</h1>
  <p>Anigrate is written and maintained by <a 
    href="mailto:lucas@glacicle.org">Lucas de Vries</a>. Feel free to 
  send over an email for any bug reports or suggestions.</p>
</section>

<section id="install">
  <h1>Installation</h1>
  <p>If you are an arch linux user, there is a package available at the 
  arch user repository at <a 
    href="http://aur.archlinux.org/packages.php?ID=33454">
    http://aur.archlinux.org/packages.php?ID=33454</a><p>

  <p>You can also clone the git repository and simply copy the anigrate 
  binary to a folder in your path.</p>

  <p> Web interface for git repository: 
  <a href="http://git.glacicle.org/anigrate/">
    http://git.glacicle.org/anigrate/</a><br/>
  Clone: <code>git clone git://glacicle.org/projects/anigrate.git</code></p>
</section>

<section id="usage">
  <h1>Usage Examples</h1>
  <p>In its most basic form, anigrate is rather easy to use, some examples for
  common watch list management tasks:<p>

  <h2>Adding a new series</h2>
  <a href="#cmd-add"><code>$ anigrate add</code></a>
  <p>The add command will prompt you for any information required, then adds a
  new series with that information. Alternatively you can specify them manually:
  </p>
  <pre>
    $ anigrate add anime: Ginga Eiyuu Densetsu
    $ anigrate add tv: how i met your mother
  </pre>

  <h2>Incrementing a series watch count</h2>
  <a href="#cmd-watch"><code>$ anigrate watch: how i met your mother</code></a>
  <p>This command will increment the watch count on the specified series and
  display the current log afterwards. You can also specify the amount of 
  episodes or a specific episode number, as well as the total amount of 
  episodes this season. Note that you don't need to type the entire name
  of the series, only the first bit.</p>
  <pre>
    $ anigrate watch +3: how i
    $ anigrate watch 12/110: ginga
  </pre>

  <h2>Viewing your current progress</h2>
  <a href="#cmd-list"><code>$ anigrate list: ginga eiyuu</code></a>
  <p>By using the <code>list</code> command, you can see how far along you
  are in a series. Not specifying any series (ie calling <code>$ anigrate 
  list</code>) will show you your progress on every series.</p>
</section>

<section id="selectors">
  <h1>Selectors</h1>
  <p>Selectors are used to find series to act upon. In its most basic form, a 
  selector is simply the name of a series or the beginning of a name of a 
  series (note that the selector will match any series that start with the 
  specified name). Within the selector, the options listed below can be given.

  <h2>+finished/+completed, +watching, +dropped, +undropped</h2>
  <p>Put any of these in a separate argument anywhere in the selector and it 
  will only match series that satisfy the condition.</p>

  <h2>=&lt;category&gt;
  =%&lt;category&gt;</h2>
      <p>Will only match series in the specified category. If a % is specified,
      exactly match the category behind it, otherwise match any categories
      that start with the specified string.</p>

  <h2>%exact</h2>
      <p>When specified, only match series that exactly match the full selector.</p>

  <h2>%contains</h2>
      <p>When specified, match all series containing the selector.</p>

  <h2>%suffix</h2>
      <p>When specified, match all series that end with the selector.</p>

  <h2>%prefix</h2>
      <p>Default behaviour: match all series that start with the selector.</p>

  <h2>@rating, @activity, @watched, @title
  @-rating, @-activity, @-watched, @-title</h2>
      <p>Set field to sort by, you can sort by series rating, series latest 
      activity, amount of episodes watched and title respectively.
      Specifying a "-" reverses the order.</p>

  <h2>@split
  @-split</h2>
      <p>Default sort method, sorts by activity but splits into watching,
      finished and dropped groups first.</p>
</section>

<section id='dbformat'>
  <h1>Database Formats</h1>
  <p>Database formats are used to determine how to read or write series
  from or to a file, the following format specifiers are available:</p>

  <h2>csv</h2>
      <p>Uses a simple csv file with series titles and other info.</p>

  <h2>anidb</h2>
      <p>Uses anidb.net's csv-minimal MyList export template.</p>

  <h2>myanimelist  [IMPORT ONLY]</h2>
      <p>Uses myanimelist.net's xml export format.
      When importing from myanimelist be sure to uncompress it before feeding
      it to anigrate; you can use pipes for this. For example:</p>
      <code>$ gunzip -c animelist_0000_-_0000.xml.gz | anigrate import - 
      myanimelist</code>
</section>

<section id='dates'>
  <h1>Date Formats</h1>
  <p>Some commands allow a date to be specified as an argument. By default, dates
  are parsed in YYYYMMDD format. If the `dateutil` package has been installed 
  on the system, any format that can be parsed by it becomes acceptable.</p>
</section>
"""

FOOTER = """
"""

def generate_html(filename):
    with open(filename, 'w') as fd:
        # Header
        fd.write(HEADER)

        # Commands
        fd.write("<section id=\"commands\">\n")
        fd.write("<h1>Commands</h1>\n")
        fd.write("""<p>
        See `%(command)s help $command` for extended information about the arguments
        and usage of a specific command.</p>

        <p>You can use the shortest unambiguous form to specify each of these commands
        (for example "li" will suffice for "list" and both "hi" and "hist" will
        suffice for "history").</p>

        <p>Positional arguments can be set to a single period character (".") in order
        to specify they should remain set to their default values.
        </p>""")
        fd.write("<nav><ul>\n")

        for command in Commands_Order:
            fd.write("<li><a href='#cmd-%(cmd)s'>%(cmd)s</a></li>\n" %
                                         { "cmd": command })

        for command in Commands_Season_Order:
            fd.write("<li><a href='#seasoncmd-%(cmd)s'>season %(cmd)s</a></li>\n" %
                                         { "cmd": command })

        fd.write("</ul></nav>\n")

        for command in Commands_Order:
            # Section
            fd.write("<section id='cmd-%s'>\n" % command)

            # Title
            doc = Commands[command].__doc__.split("\n")
            fd.write("<h1>" + doc[1].lstrip() + "</h1>\n")

            # Documentation
            fd.write("<p>" + "\n".join(doc[2:]).replace("\n\n", "</p><p>")
                           + "</p>\n")

            fd.write("</section>\n")

        for command in Commands_Season_Order:
            # Section
            fd.write("<section id='seasoncmd-%s'>\n" % command)

            # Title
            doc = Commands_Season[command].__doc__.split("\n")
            fd.write("<h1>" + doc[1].lstrip() + "</h1>\n")

            # Documentation
            fd.write("<p>" + "\n".join(doc[2:]).replace("\n\n", "</p><p>")
                           + "</p>\n")

            fd.write("</section>\n")

        fd.write("</section>\n")

        # Configuration
        fd.write("<section id=\"configuration\">\n")
        fd.write("<h1>Configuration</h1>\n")
        fd.write("""<p>
        There are a number of configuration options available to be set. The 
        default location for your config file is in $HOME/.anigrate/config. You 
        can print a list of options currently set by running `anigrate config`.

        The following configuration options are available, run `anigrate help 
        $OPTION` for more information about one of them, or run `anigrate help 
        options` to see the complete list of extended information.
        </p>""")
        fd.write("<nav><ul>\n")

        for option in sorted(ConfigHelp):
            fd.write("<li><a href='#conf-%(opt)s'>%(opt)s</a></li>\n" %
                                         { "opt": option })

        fd.write("</ul></nav>\n")

        for option in sorted(ConfigHelp):
            # Section
            fd.write("<section id='conf-%s'>\n" % option)

            # Title
            doc = ConfigHelp[option].split("\n")
            fd.write("<h1>" + doc[1].lstrip() + "</h1>\n")

            # Default
            if doc[2].lstrip().startswith("Default: "):
                fd.write("<small>%s</small>" % doc[2])
                del doc[2]

            # Default pre
            for i, line in enumerate(doc):
                if line.strip() == "Default:":
                    doc[i] = "</p><h2>Default</h2><pre>"
                    doc[-1] += "</pre><p>"
                    break

            # Documentation
            fd.write("<p>" + "\n".join(doc[2:]).replace("\n\n", "</p><p>") 
                           + "</p>\n")

            fd.write("</section>\n")

        fd.write("</section>\n")

        # Config Example
        fd.write("<section id=\"configexample\">\n")
        fd.write("<h1>Configuration Example</h1>\n<pre>\n")

        with open("config.example") as config:
            fd.write("".join(config))

        fd.write("</pre>\n</section>\n")

        # Footer
        fd.write(FOOTER)

if __name__ == '__main__':
    generate_html('README.html')
