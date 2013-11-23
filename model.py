import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class Provider(Base, UserMixin):
    __tablename__ = "providers" 
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(16), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    tasks = relationship("Task", uselist=True, backref="providers")

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password
        
    @property
    def serialize_provider(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'email': self.email,
           'phoneNumber': self.phone_number
       }
       
class Patient(Base):
    __tablename__ = "patients" 
    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    birth_year = Column(Integer, nullable=False)
    phone_number = Column(String(16), nullable=False)
    photo_filename = Column(String(64), nullable=True)

    tasks = relationship("Task", uselist=True, backref="patients")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=None)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    status = Column(String(16), nullable=False, default="UNREAD")
    priority = Column(Integer, nullable=True)
    
    
    patient = relationship("Patient")
    provider = relationship("Provider")
    
    @property
    def serialize_task(self):
       """Return object data in easily serializeable format"""
       patient = Patient.query.get(self.patient_id)
       return {
           'id': self.id,
           'description': self.description,
           'patient': {'id': patient.id, 'name': patient.name, 'birthYear' : patient.birth_year,'phoneNumber': patient.phone_number,'photoFilename': patient.photo_filename},
           'providerId': self.provider_id,
           'createdAt': dump_datetime(self.created_at),
           'updatedAt': dump_datetime(self.updated_at),
           'status': self.status,
           'priority': self.priority
       }

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    content = Column(Text, nullable=True)
    
    task = relationship("Task")

# class User(Base, UserMixin):
#     __tablename__ = "users" 
#     id = Column(Integer, primary_key=True)
#     email = Column(String(64), nullable=False)
#     password = Column(String(64), nullable=False)
#     salt = Column(String(64), nullable=False)
# 
#     posts = relationship("Post", uselist=True)
# 
#     def set_password(self, password):
#         self.salt = bcrypt.gensalt()
#         password = password.encode("utf-8")
#         self.password = bcrypt.hashpw(password, self.salt)
# 
#     def authenticate(self, password):
#         password = password.encode("utf-8")
#         return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password
# 
# class Post(Base):
#     __tablename__ = "posts"
#     
#     id = Column(Integer, primary_key=True)
#     title = Column(String(64), nullable=False)
#     body = Column(Text, nullable=False)
#     created_at = Column(DateTime, nullable=False, default=datetime.now)
#     posted_at = Column(DateTime, nullable=True, default=None)
#     user_id = Column(Integer, ForeignKey("users.id"))
# 
#     user = relationship("User")

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")
    
def create_tables():
    Base.metadata.create_all(engine)
    # u = User(email="test@test.com")
    # u.set_password("unicorn")
    # session.add(u)
    # p = Post(title="This is a test post", body="This is the body of a test post.")
    # u.posts.append(p)
    # session.commit()

if __name__ == "__main__":
    create_tables()
