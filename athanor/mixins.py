from athanor.types import UTCDateTime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relation

from datetime import datetime

class StampedMixin(object):
    created_on = Column(UTCDateTime, default=datetime.utcnow, nullable=False)
    modified_on = Column(UTCDateTime, default=datetime.utcnow,
                         onupdate=datetime.now, nullable=False)

class TrackedMixin(object):
    @declared_attr
    def created_by_user_id(cls):
        return Column(Integer, ForeignKey('users.id'), nullable=False)

    @declared_attr
    def modified_by_user_id(cls):
        return Column(Integer, ForeignKey('users.id'), nullable=False)
    
    @declared_attr
    def created_by(cls):
        return relation(
            'User',
            primaryjoin='%s.created_by_user_id == User.id' % cls.__name__
        )
    
    @declared_attr
    def modified_by(cls):
        return relation(
            'User',
            primaryjoin='%s.modified_by_user_id == User.id' % cls.__name__
        )

    def touch(self, user):
        if not self.created_by:
            self.created_by = user

        self.modified_by = user
