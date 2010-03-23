from anigrate.util import register, selector
from anigrate.models import Base

@register("initialise")
def initialise():
    """
    initialise
        Initialise the database with all the necessary tables.
    """
    Base.metadata.create_all()
