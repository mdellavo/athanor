from sqlalchemy import create_engine, Column, Integer, String
from athanor import Session, Base, StampedMixin, TrackedMixin, build_eav

class User(Base, StampedMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Foo(Base, StampedMixin, TrackedMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Tag(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

FooData = build_eav(Foo)

engine = create_engine('sqlite:///:memory:', echo=True)

Session.configure(bind=engine)
Base.metadata.create_all(engine)

user = User.create(name='marc')

foo = Foo.create(name='blah', created_by=user, modified_by=user)
print foo.to_dict()

foo.name = 'blah blah'
foo.touch(user)
foo.save()

print foo.to_dict()

print Foo.find_by_created_by(user)

tag = Tag.create(name='xxx')
print tag.to_dict()
print Tag.get_by_name('xxx')

foo.data['x'] = 0
foo.data['y'] = 1.0
foo.data['z'] = 'hello'

Session.commit()

print foo.data
