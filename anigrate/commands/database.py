from anigrate.util import register, selector
from anigrate.models import Base

@register("initialise", shorthelp="initialise the series database")
def initialise():
    """
    initialise
        Initialise the database with all the necessary tables. Note that this
        is only necessary for client/server databases like mysql. If an sqlite
        database is used (which it is by default), anigrate automatically 
        creates it for you.
    """
    Base.metadata.create_all()
