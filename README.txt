                                README
                                ======

Author: marc
Date: 2012-04-21 18:09:19 EDT


Table of Contents
=================
1 Athanor
    1.1 Examples
    1.2 BaseModel
        1.2.1 Class Methods and Attributes
        1.2.2 Instance Methods
    1.3 EAV
    1.4 Types
        1.4.1 UTCDateTime
    1.5 Shadow
    1.6 Author


1 Athanor 
----------

  Athanor is a set of utilities for SQLAlchemy.  

  Athanor provides simple conveinence functions for common patterns
  found in many applications.  Tools should be selected as the
  situation calls for. SQLAlchemy is marvelous package; Athanor is not
  an attempt to eliminate SQLAlchemy.
  
  See Also - [http://en.wikipedia.org/wiki/Athanor]

1.1 Examples 
=============

   

1.2 BaseModel 
==============

   BaseModel is base class for SQLAlchemy mapped objects that provides
   a number of utilities to inspect, create, find, fetch and update
   objects/columns.  It also provides "magic finders" that will supply
   dynamic getters and finders such as get_by_foo and find_by_bar.

   Many of these utilities are familiar to Django's ORM.

1.2.1 Class Methods and Attributes 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* .objects 
  + Description 
    The .objects attribute is query of all objects in the collection
    with no filters applied.  See SQLAlchemy's query_property.  The
    finders below use .objects so subclasses can override it if they
    need to apply any default options and criteria.
    
* def get(cls, id): 
  + Description 
    Gets an object by the collection's primary key. Returns None if
    no object is found
  + Returns 
    Returns an object if one exists or None if no object is found.
  + Example 
    Foo.get(1)
    
* def get_by(cls, column, value): 
  + Description 
    Gets an object by a column and value.
  + Returns 
    Returns an object if one exists or None if no object is found.
  + Example 
    Foo.get_by(Foo.id, 1)
    
* def find(cls, criteria, order_by=None): 
  + Description 
    Find the objects of .objects matching criteria by order_by
  + Returns 
    Returns an query of .objects with the criteria and order_by applied.
  + Example 
    Foo.find(and_(Foo.id > 10, Foo.id < 100))
    
* def find_one(cls, criteria, order_by=None): 
  + Description 
    Find the first object of .objects matching criteria by order_by
  + Returns 
    Returns and object or None is no such match exists.
  + Example 
    Foo.find_one(and_(Foo.id > 10, Foo.id < 100))
    
* def get_or_create(cls, id, data, update=True): 
* def get_by_or_create(cls, column, value, data, update=True): 
* def find_or_create(cls, criteria, data, update=True): 
  

1.2.2 Instance Methods 
~~~~~~~~~~~~~~~~~~~~~~~

* def __json__(self): 
* def update(self, data): 
* def save(self): 
* def to_dict(self, include=None, exclude=None): 
* def __repr__(self): 
* def columns(self): 
* def relationships(self): 
* def primary_key(self): 
* def attributes(self): 
* def create(cls, **data): 
* def delete(self): 
  

1.3 EAV 
========

   Provides and Entity-Attribute-Value (aka vertical table) pattern 

   XXX - Document me!

1.4 Types 
==========

   XXX - Document me!

1.4.1 UTCDateTime 
~~~~~~~~~~~~~~~~~~

1.5 Shadow 
===========

   XXX - Implement me!
   XXX - Document me!

1.6 Author 
===========
   Marc DellaVolpe
   marc.dellavolpe@gmail.com
