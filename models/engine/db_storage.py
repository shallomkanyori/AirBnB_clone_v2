#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage."""

        usr = os.getenv('HBNB_MYSQL_USER', default='')
        pwd = os.getenv('HBNB_MYSQL_PWD', default='')
        host = os.getenv('HBNB_MYSQL_HOST', default='')
        db = os.getenv('HBNB_MYSQL_DB', default='')
        env = os.getenv('HBNB_ENV', default='')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                        usr, pwd, host, db),
                        pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current session for a dictionary of objects.

        Args:
            cls: the cls to get objects of. All objects if None. Optional.
        """

        if cls:
            cls = eval(cls) if type(cls) is str else cls

            res = self.__session.query(cls).all()

        else:
            all_cls = [User, State, City, Place, Review, Amenity]
            res = []

            for cls in all_cls:
                res.extend(self.__session.query(cls).all())

        res = {"{}.{}".format(o.__class__.__name__, o.id): o for o in res}
        # res = {f"{o.__class__.__name__}.{o.id}": o for o in res}
        return res

    def new(self, obj):
        """Adds new object to current database session"""

        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""

        self.__session.commit()

    def reload(self):
        """Creates all tables in the database and the current database session.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def delete(self, obj=None):
        """Deletes an object from the current database session.

        Args:
            obj: the object to delete. Optional.
        """

        if obj:
            self.__session.delete(obj)

    def close(self):
        """Closes the current database session."""
        self.__session.close()
