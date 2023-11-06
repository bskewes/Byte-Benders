### Copy from their database.ipynb file

import pandas as pd
from sqlalchemy import select

### They have custom modules - we'll recreate them as necessary to see what the code is doing

# data.data - session, engine, path - that's all the items I copied over, so that's okay


Session
path
engine

# Copy their code here anywya - not sure why it doesn't work

import os
from pathlib import Path
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv


load_dotenv(override=True)
FILENAME_SCHEDULE = 'gtfs.zip'

path = Path(os.getenv("DATA_PATH"))
zip_path = Path(path / FILENAME_SCHEDULE)

con_str = os.getenv("SQLDRIVER")
engine = create_engine(con_str)
Session = sessionmaker(engine)



#to make sure we have these things
# data.model - Shape, Trip, Stop, StopTime



### Take out trip

# This is a class created in the model.py file. Import all the things from there as well as required



from sqlalchemy.orm import DeclarativeBase ### Need this to make all the rest of the classes work

# Need all this stuff to make the class work
from typing import List ### Need this for the class Trip to work where it refers to lists - does this make 'List' a type?
from sqlalchemy.orm import mapped_column ### otherwise mapped_column doesn't work
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey, String, Table
from sqlalchemy.orm import relationship

# Need the session from above - run the SQLite code


class Base(DeclarativeBase):
    pass


class Trip(Base):
    __tablename__ = "trips"
    _gtfs_fields_ = (
        "trip_id",
        "route_id",
        "service_id",
        "shape_id",
        "trip_headsign",
        "direction_id",
        "wheelchair_accessible",
        "route_direction",
    )
    _gtfs_file_ = "trips"

    id: Mapped[str] = mapped_column(primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.id"))
    service_id: Mapped[str]
    shape_id: Mapped[str] = mapped_column(ForeignKey("shapes.id"))
    trip_headsign: Mapped[str] = mapped_column(nullable=True)
    direction_id: Mapped[int]
    wheelchair_accessible: Mapped[int]
    route_direction: Mapped[str]

    route: Mapped["Route"] = relationship(back_populates="trips")
    shape: Mapped[List["Shape"]] = relationship(back_populates="trips", uselist=True)
    stop_times: Mapped[List["StopTime"]] = relationship(
        back_populates="trips", uselist=True
    )
    locations: Mapped[List["Location"]] = relationship(
        back_populates="trip"
    )

    def __repr__(self) -> str:
        attrs = ["route_id", "service_id", "id", "trip_headsign"]
        return _simple_repr(self, attrs)


### Fetch trips

# The actual thing

with Session() as session:
    stmt = select(Trip).limit(10) # this is a selectable object
    trips = session.execute(stmt).scalars().all()

trips


session = Session() ### trying to run their code but separately from the with

# Can't open database file?

with Session() as session:
    session.add(1)



from sqlalchemy.orm import Session

Session(engine).execute(stmt)
Session(engine).add(1)



import sqlite3
db_name = r"C:\\Users\\jchen20\\WWPT\\Byte-Benders\\db.db"
db_name = "C:\\Users\\jchen20\\Workspace2\\WWPT\\Byte-Benders\\db.db"
db_name = r"C:\Users\jchen20\WWPT\Byte-Benders\db.db"
db_name = r"C:\Downloads\db.db"
con = sqlite3.connect(db_name)
cur = con.cursor()

open("C:\\Downloads\\testfordb.txt", "w")
open("C:\\Users\\jchen20\\Workspace2\\WWPT\\text.txt","w")
open("C:\\Users\\jchen20\\Workspace2\\WWPT\\db.db","w")