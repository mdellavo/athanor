from sqlalchemy.orm import sessionmaker, scoped_session, class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declared_attr, DeclarativeMeta

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

    objects = Session.query_property()

    @property
    def columns(self):
        return [ i.key for i in class_mapper(self.__class__).iterate_properties
                 if isinstance(i, ColumnProperty) ]

    @property
    def relationships(self):
        return [ i.key for i in class_mapper(self.__class__).iterate_properties
                 if isinstance(i, RelationshipProperty) ]
    @property
    def primary_key(self):
        return [i.key for i in class_mapper(self.__class__).primary_key]

    @property
    def attributes(self):
        return self.columns + self.relationships

    @classmethod
    def create(cls, **data):
        o = cls(**data)
        Session.add(o)
        Session.commit()
        return o

    def delete(self):
        Session.delete(self)
        Session.commit()

    def __repr__(self):
        val = lambda k: str(getattr(self, i)).replace('\'', '\\\'')
        keys = ["'%s'" % val(i) for i in self.primary_key]
        return '<%s(%s)>' % (self.__class__.__name__, ', '.join(keys))
    
    def update(self, data):
        for attr in self.columns:
            if attr in data and data[attr] != getattr(self, attr):
                setattr(self, attr, data[attr])
        return self

    def save(self):
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
        return self.to_dict()

    @classmethod
    def get(cls, id):
        return cls.objects.get(id)

    @classmethod
    def get_by(cls, column, value):
        try:
            return cls.objects.filter(column==value).one()
        except NoResultFound:
            return None

    @classmethod
    def find(cls, criteria, order_by=None):
        return cls.objects.filter(criteria).order_by(order_by)

    @classmethod
    def find_one(cls, criteria, order_by=None):

        try:
            return cls.find(criteria, order_by).one()
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
        return cls.__or_create__(cls.get(id), data, update)

    @classmethod
    def get_by_or_create(cls, column, value, data, update=True):
        return cls.__or_create__(cls.get_by(column, value), data, update)

    @classmethod
    def find_or_create(cls, criteria, data, update=True):
        return cls.__or_create__(cls.find_one(criteria), data, update)


Base = declarative_base(cls=BaseModel, metaclass=BaseDeclarativeMeta)
