# add EAV, add factory class

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from model import Base
from decl_enum import DeclEnum
from utils import pluralize, underscore

from decimal import Decimal
from datetime import datetime

class AttributeDataType(DeclEnum):
    BOOLEAN = 'B', 'Boolean'
    FLOAT = 'F', 'Float'
    STRING = 'S', 'String'
    INTEGER = 'I', 'Integer'
    DECIMAL = 'D', 'Decimal'

class EntityAttribute:
    TYPE_MAP = {
        bool:  AttributeDataType.BOOLEAN,
        float: AttributeDataType.FLOAT,
        str: AttributeDataType.STRING,
        int: AttributeDataType.INTEGER,
        Decimal: AttributeDataType.DECIMAL
    }

    CASTERS = {
        AttributeDataType.BOOLEAN: lambda x: bool(int(x)),
        AttributeDataType.FLOAT: float,
        AttributeDataType.STRING: str,
        AttributeDataType.INTEGER: int,
        AttributeDataType.DECIMAL: Decimal
    }

    key = Column(String(50), nullable=False, primary_key=True)
    type = Column(AttributeDataType.db_type(), nullable=False)
    value = Column(String)

    @property
    def casted_value(self):
        return self.CASTERS[self.type](self.value)

    @classmethod
    def build(cls, key, value):
        return cls(key=key,
                   value=value,
                   type=cls.TYPE_MAP[type(value)])


# FIXME assuming id pk on cls
def build_eav(cls):
    data_class_name = cls.__name__ + 'Attribute'
    base_name = underscore(cls.__name__) 
    fk_name = base_name + '_id'
    fk = pluralize(base_name) + '.id'
    data_class = type(data_class_name, (EntityAttribute, Base), {
            fk_name: Column(Integer, ForeignKey(fk), primary_key=True)
    })

    cls.data_map = relation(
        data_class, 
        collection_class=attribute_mapped_collection('key')
    )
    
    cls.data = association_proxy('data_map', 'casted_value',
                                 creator=data_class.build)

    return data_class
