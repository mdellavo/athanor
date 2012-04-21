from sqlalchemy import DateTime 
from sqlalchemy.types import TypeDecorator

from pytz import UTC, timezone

from datetime import datetime

class UTCDateTime(TypeDecorator):
    impl = DateTime
    
    def convert_bind_param(self, value, engine):
        return value
    
    def convert_result_value(self, value, engine):
        return UTC.localize(value)

