from sqlalchemy.orm import sessionmaker, scoped_session, class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declared_attr, DeclarativeMeta

from athanor.utils import pluralize, underscore

Session = scoped_session(sessionmaker())

class BaseDeclarativeMeta(DeclarativeMeta):
    def __getattr__(self, name):
        if name.startswith("get_by_"):
            field = name[len("get_by_"):]
            return lambda value: self.get_by(
                self.__getattribute__(self, field),
                value
            )
        elif name.startswith('find_by_'):
            field = name[len("find_by_"):]
            return lambda value: self.find(
                self.__getattribute__(self, field) == value
            )
        else:
            return super(BaseDeclarativeMeta, self).__getattribute__(name)


class BaseModel(object):
    '''
    BaseModel for MappedClasses.
    
    The declarative base, Base, is contstructed with BaseModel as the
    base class.

    BaseModel will generate a __tablename__ property if one is not
    specified.  The generated table name is generated as the
    pluralized, lower-cased, underscored version of the camel-case class name.

    BaseModel also includes a query property, .objects, if all objects
    in the collection.
    '''

    objects = Session.query_property()
    
    # Courtesy of http://techspot.zzzeek.org/files/2011/magic.py
    @declared_attr
    def __tablename__(cls):
        '''Generate a tablename for the class as the pluralized 
        words_with_underscores version of the class name'''

        return pluralize(underscore(cls.__name__))

    @classmethod
    def create(cls, **kwargs):
        '''Create an object from the passed kwargs, add it to the
        session and commit the session.   Returns the newly created object'''

        o = cls(**kwargs)
        Session.add(o)
        Session.commit()
        return o

    @classmethod
    def get(cls, id):
        '''Get an object by primary key.  Returns the object or None'''

        return cls.objects.get(id)

    @classmethod
    def get_by(cls, column, value):
        '''Get an object by a given column and value.  Returns the
        object or None'''

        try:
            return cls.objects.filter(column==value).one()
        except NoResultFound:
            return None

    @classmethod
    def find(cls, criteria, order_by=None):
        '''Find objects matching criteria.  Returns a Query object'''

        return cls.objects.filter(criteria).order_by(order_by)

    @classmethod
    def find_one(cls, criteria, order_by=None):
        '''Find one object matching criteria.  Returns the object or None'''

        try:
            return cls.find(criteria, orderby).one()
        except NoResultFound:
            return None
        
    @classmethod
    def __or_create__(cls, o, data, update):
        if not o:
            o = cls.create(**data)
            status = True
        elif update:
            o.update(data)
            status = False

        return o, status
        
    @classmethod
    def get_or_create(cls, id, data, update=True):
        '''Get an object by primary key or create one. If no object is
        found, create one from data.  If an object is found and update
        is True, update the found update with data.'''
        return cls.__or_create__(cls.get(id), data, update)

    @classmethod
    def get_by_or_create(cls, column, value, data, update=True):
        '''Get an object by given column and value or create one. If no object is
        found, create one from data.  If an object is found and update
        is True, update the found update with data.'''
        return cls.__or_create__(cls.get_by(column, value), data, update)

    @classmethod
    def find_or_create(cls, criteria, data, update=True):
        '''Find an object by given criteria or create one. If no object is
        found, create one from data.  If an object is found and update
        is True, update the found update with data.'''
        return cls.__or_create__(cls.find_one(criteria), data, update)

    @property
    def columns(self):
        '''Return a list of the object's field names'''
        return [ i.key for i in class_mapper(self.__class__).iterate_properties
                 if isinstance(i, ColumnProperty) ]

    @property
    def relationships(self):
        '''Return a list of the object's relationship names'''
        return [ i.key for i in class_mapper(self.__class__).iterate_properties
                 if isinstance(i, RelationshipProperty) ]
    @property
    def primary_key(self):
        '''Return a list of the object's primary key fields '''
        return [i.key for i in class_mapper(self.__class__).primary_key]

    @property
    def attributes(self):
        '''Return a list of the object's columns and relationships'''
        return self.columns + self.relationships

    def delete(self):
        '''Delete an object and commit the session'''
        Session.delete(self)
        Session.commit()

    def __repr__(self):
        '''Return a generic representation of the object include it's
        primary key values'''

        val = lambda k: str(getattr(self, i)).replace('\'', '\\\'')
        keys = ["'%s'" % val(i) for i in self.primary_key]
        return '<%s(%s)>' % (self.__class__.__name__, ', '.join(keys))
    
    def update(self, data):
        '''Update an object from a data dictionary'''
        for attr in self.columns:
            if attr in data and data[attr] != getattr(self, attr):
                setattr(self, attr, data[attr])
        return self

    def save(self):
        '''Commit changes to the database'''
        Session.commit()

    def to_dict(self, include=None, exclude=None):
        '''
        Returns a dict of attributes of a mapped instance
        '''

        cols = self.columns

        rv = {}
        for col in cols:

            if include and col not in include:
                continue

            if exclude and col in exclude:
                continue

            val = getattr(self, col)

            rv[col] = val
            
        return rv

    def __json__(self):
        '''Return a dictionary for JSON serialization.  By default
        this returns a dictionary of all of the objects's fields'''
        return self.to_dict()



Base = declarative_base(cls=BaseModel, metaclass=BaseDeclarativeMeta)
