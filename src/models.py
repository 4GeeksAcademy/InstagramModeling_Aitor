import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

#from flask import Flask
#from flask_sqlalchemy imoport SQLALchemy

#= Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
#db = SQLAlchemy(app)

Base = declarative_base()


#User TABLA PRINCIPAL------------------------------------------------------

class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key = True) #llave primaria
    userName = Column(String(250))
    firstName = Column(String(250))
    lastName = Column(String(250))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def serialize(self): #devuelve la información en formato diccionario. Esto es lo que va a recibir el front. Se ponen solo los valores que se quieren enviar
        return {
            "id": self.id,
            "userName": self.userName,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }


#Post ------------------------------------------------------

class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='posts')

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id
        }

    

#Comment ------------------------------------------------------

class Comments(Base):
    __tablename__="comments"
    id = Column(Integer, primary_key = True)
    commenText = Column(String(250))
    authorId = Column(Integer)
    postId = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Posts', backref='Comments')
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='Comments')

    def to_dict(self): #devuelve la información en formato diccionario. Esto es lo que va a recibir el front. Se ponen solo los valores que se quieren enviar
        return {
            "id": self.id,
            "commenText": self.commenText,
            "authorId": self.authorId,
            "postId": self.postId
        }

#Follower ------------------------------------------------------

class Followers(Base):
    __tablename__="followers"
    userFromId = Column(Integer, primary_key = True)
    userToId = Column(Integer)
    from_id = Column(Integer, ForeignKey('users.id'))
    from_user = Column(Integer, ForeignKey('users.id'))
    to_id = relationship('Users', foreign_keys=[from_id], backref='followers')
    to_user = relationship('Users', foreign_keys=[from_id], backref='following')

    def to_dict(self): #devuelve la información en formato diccionario. Esto es lo que va a recibir el front. Se ponen solo los valores que se quieren enviar
        return {
            "userFromId": self.userFromId,
            "userToId": self.userToId
        }

#Media ------------------------------------------------------

class Media(Base):
    __tablename__="media"
    id = Column(Integer, primary_key = True)
    type = Column(Integer)
    url = Column(String(250))
    postId = Column(Integer)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Posts', backref='media')

    def to_dict(self): #devuelve la información en formato diccionario. Esto es lo que va a recibir el front. Se ponen solo los valores que se quieren enviar
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "postId": self.postId
        }
    


# ----------------------------------------------------------------



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
