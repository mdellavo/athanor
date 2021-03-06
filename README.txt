                                README
                                ======

Author: Marc DellaVolpe
Date: 2012-04-23 10:33:25 EDT


Table of Contents
=================
1 Athanor
    1.1 Examples
    1.2 BaseModel
        1.2.1 Class Methods and Attributes
        1.2.2 Instance Methods
    1.3 Types
        1.3.1 UTCDateTime
        1.3.2 DeclEnum, EnumSymbol
    1.4 Mixins
        1.4.1 StampedMixin
        1.4.2 TrackedMixin
    1.5 Todo
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

   See examples.py

1.2 BaseModel 
==============

   BaseModel is base class for SQLAlchemy mapped objects that provides
   a number of utilities to inspect, create, find, fetch and update
   objects/columns.  It also provides "magic finders" that will supply
   dynamic getters and finders such as get_by_foo and find_by_bar.

   Many of these utilities are familiar to Django's ORM.

1.2.1 Class Methods and Attributes 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* .__tablename__ 
  + Description 
    Automatically computes __tablename__ unless overriden as the
    plural of the words_with_underscores version of the class name.
    Override if the magic falls on it's face.
    
  + Example 
    FooBar -> foo_bars
    
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
    
* def create(cls, **data): 
  + Description 
    Creates and object from data kwargs, adds it to the session and
    commits.  Override in subclass if you want to enforce behavior
    on creation (e.g. If you want to always pass in a created_by user)
  + Returns 
    A the created object after it has been committed to the database.
  + Example 
    Foo.create(user=user, name='marc')
    
* def get_or_create(cls, id, data, update=True): 
  + Description 
    Attempts to fetch an object by given primary key.  If no object
    is found then an object will be created from the given data
    dictionary.  If update is True, existing objects will be
    updated from the data dictionary.
  + Returns 
    Returns a tuple of the object and a boolean indicating whether
    or not it was created.
  + Example 
    obj, created = Foo.get_or_create(1, {'name': 'marc', 'user': user})
    
* def get_by_or_create(cls, column, value, data, update=True): 
  + Description 
    Attempts to fetch an object by given column and value.  If no object
    is found then an object will be created from the given data
    dictionary.  If update is True, existing objects will be
    updated from the data dictionary.
  + Returns 
    Returns a tuple of the object and a boolean indicating whether
    or not it was created.
  + Example 
    obj, created = Foo.get_by_or_create(Foo.name, 'marc', {'name': 'marc', 'user': user})
    
* def find_or_create(cls, criteria, data, update=True): 
  + Description 
    Attempts to fetch an object by given criteria.  If no object
    is found then an object will be created from the given data
    dictionary.  If update is True, existing objects will be
    updated from the data dictionary.
  + Returns 
    Returns a tuple of the object and a boolean indicating whether
    or not it was created.
  + Example 
    obj, created = Foo.get_by_or_create(and_(Foo.name=='marc', Foo.active=True), {'name': 'marc', 'user': user})
    

1.2.2 Instance Methods 
~~~~~~~~~~~~~~~~~~~~~~~

* def __repr__(self): 
  + Description 
    Convenience method to build a simple representation of a mapped
    instance from the class name and includes the objects primary key(s).
  + Returns 
    A string
  + Example 
    print foo
    
* .columns: 
  + Description 
    A list of an objects column names
    
* .relationships: 
  + Description 
    A list of an objects relationship names
    
* .primary_key: 
  + Description 
    A list of an object's primary key names
    
* .attributes: 
  + Description 
    A list of an object's columns and relationships
    
* def to_dict(self, include=None, exclude=None): 
  + Description 
    Build a dict representation of an object.  Pass a list of field
    names to include to only includes fields explicitly listed. Pass
    a list of fields names to exclude to omit fields.  No
    relationships are traversed, if you want to include
    relationships, subclass and manually include those fields.
  + Returns 
    A dictionary of an object's fields.
  + Example 
    foo.to_dict(exclude=['id'])
    
* def __json__(self): 
  + Description 
    A method to handle JSON serialization.  A common convention is
    to call __json__ if such a method exists on an object when
    converting to JSON. By default calls to_dict().
  + Returns 
    A dict suitable for serialization.
    
* def update(self, data): 
  + Description 
    Update an object from a dictionary.
  + Returns 
    The object updated
  + Example 
    foo.update({'name': 'marc'})
    
* def save(self): 
  + Description 
    Commits the session.  This method does not restrict the commit
    to only the object in question.  This is a simple convenience to
    make code look a bit more literate at the cost of possible
    unintentional side effects
  + Returns 
    None
  + Example 
    foo.save()
    
* def delete(self): 
  + Description 
    Deletes an object
  + Returns 
    None
  + Example 
    foo.delete()
    

1.3 Types 
==========

1.3.1 UTCDateTime 
~~~~~~~~~~~~~~~~~~
* Description 
  UTCDateTime will take a time-zone aware datetime and store it as
  UTC in the database automatically.
  

1.3.2 DeclEnum, EnumSymbol 
~~~~~~~~~~~~~~~~~~~~~~~~~~~
    See [http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/]

    Included here for easy install
    

1.4 Mixins 
===========

1.4.1 StampedMixin 
~~~~~~~~~~~~~~~~~~~
* Description 
  StampedMixin adds created_on and modified_on columns to a
  table. These columns will updated as needed. 
  

1.4.2 TrackedMixin 
~~~~~~~~~~~~~~~~~~~
* Description 
  TrackedMixin adds created_by and modified_by columns to a table
  that relate to a User object.  Use the .touch(user) method to
  update modified_by.
  

1.5 Todo 
=========
   - tests
   - ReST docs
   - A simple makefile
   

1.6 Author 
===========
   Marc DellaVolpe (marc.dellavolpe@gmail.com)
