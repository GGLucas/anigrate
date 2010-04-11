import os

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relation, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from anigrate.config import Config

Base = declarative_base()
Session = scoped_session(sessionmaker())
Base.query = Session.query_property()

def bind_session(connstr="", engine=None):
    """
        Bind the database to a connection string or engine.
    """
    # Create engine
    engine = create_engine(connstr, echo=Config.echo) if connstr else engine

    # Bind engine to Base and Metadata
    Base.metadata.bind = engine
    Session.configure(bind=engine)

    # Check for sqlite and create the database if it doesn't exist there
    if connstr.startswith("sqlite:///") and \
    not engine.has_table(Series.__tablename__):
            Base.metadata.create_all()

class Series(Base):
    """An entire series."""
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    rating = Column(Integer, default=0)
    current = Column(Integer)
    ctime = Column(DateTime)
    mtime = Column(DateTime)
    dropped = Column(Boolean, default=False)
    category = Column(String(255), default="")
    duration = Column(Integer, default=24)

    seasontotal = Column(Integer, default=1)
    epscurrent = Column(Integer, default=0)
    epstotal = Column(Integer, default=0)
    epsall = Column(Integer, default=0)
    finished = Column(Boolean, default=False)

    def __unicode__(self):
        return self.title
    __repr__ = __str__ = __unicode__

    @classmethod
    def exists(cls, title, category):
        return bool(
            Series.query.filter(
                Series.title.ilike(title)
            ).filter(
                Series.category.ilike(category)
            ).count()
        )

    @property
    def current_season(self):
        return self.season_bynum(self.current)

    def season_bynum(self, num):
        for season in self.seasons:
            if season.num == num:
                return season

    def getlink(self):
        """Get the link to open for this series."""
        if Config.has_option("link", self.category):
            return Config.get("link", self.category) % self.title
        elif Config.has_option("link", "default"):
            return Config.get("link", "default") % self.title
        else:
            return DEFAULT_LINK % self.title

    def eval_finished(self):
        """Evaluate whether the series is finished."""
        self.finished = True
        self.seasontotal = 0
        self.epsall = 0

        for season in self.seasons:
            if season.current_watched < season.episode_total \
            or season.episode_total == 0:
                self.finished = False

            self.epsall += season.current_watched
            if season.num == self.current:
                self.epscurrent = season.current_watched
                self.epstotal = season.episode_total

            self.seasontotal += 1

        return self.finished

class Season(Base):
    """One season of a series."""
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    num = Column(Integer)

    series_id = Column(ForeignKey("series.id"))
    series = relation(Series, primaryjoin=(series_id == Series.id), backref="seasons")

    episode_total = Column(Integer, default=0)
    current_watched = Column(Integer, default=0)

class Watched(Base):
    """A 'watched episodes' event attached to a season."""
    __tablename__ = "watched"
    id = Column(Integer, primary_key=True)

    season_id = Column(ForeignKey("seasons.id"))
    seasonnum = Column(Integer)
    season = relation(Season, primaryjoin=(season_id == Season.id),
                              backref="watched")

    series_id = Column(ForeignKey("series.id"))
    series = relation(Series, primaryjoin=(series_id == Series.id),
                              backref="watched")

    time = Column(DateTime)

    startep = Column(Integer)
    finishep = Column(Integer)
