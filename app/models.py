from typing import Optional, Literal
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")
    # when user deleted, reviews remain with null user
    reviews: so.Mapped[list['Review']] = relationship(back_populates='user', cascade='save-update, merge')

    conversations: so.Mapped[list['Conversation']] = relationship(back_populates='user', cascade='all, delete-orphan')
    messages: so.Mapped[list['Message']] = relationship(back_populates='sender', cascade='all, delete-orphan')


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User 1-n Review relationship
class Review(db.Model):
    __tablename__ = 'reviews'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    feature: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    text: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    stars: so.Mapped[int] = so.mapped_column()
    user_id: so.Mapped[Optional[int]]  = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    user: so.Mapped[Optional['User']] = relationship(back_populates='reviews')

    def __repr__(self):
        return f'Review(stars={self.stars}, text="{self.text}", user_id={self.user_id})'

# User 1-n Conversation 1-n Message
class Conversation(db.Model):
    __tablename__ = "conversations"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: so.Mapped[datetime] = so.mapped_column(default=sa.func.now())
    user: so.Mapped["User"] = relationship(back_populates="conversations")
    messages: so.Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")

class Message(db.Model):
    __tablename__ = "messages"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    conversation_id: so.Mapped[int] = so.mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"))
    sender_id: so.Mapped[Optional[int]] = so.mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role: so.Mapped[Literal["user", "bot"]] = so.mapped_column(sa.Enum("user", "bot", name="msg_role", native_enum=False), nullable=False,)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), default=sa.func.now())
    conversation: so.Mapped["Conversation"] = relationship(back_populates="messages")
    sender: so.Mapped[Optional["User"]] = relationship(back_populates="messages")

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
