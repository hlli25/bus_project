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

# User class
@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(20), default='')

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    # when user deleted, reviews remain with null user
    reviews: so.Mapped[list['Review']] = relationship(back_populates='user', cascade='save-update, merge')

    # when user deleted, conversations and messages also deleted
    conversations: so.Mapped[list['Conversation']] = relationship(back_populates='user', cascade='all, delete-orphan')
    messages: so.Mapped[list['Message']] = relationship(back_populates='sender', cascade='all, delete-orphan')

    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Admin, Student and Counsellor classes inherit from User
class Admin(User):
    __tablename__ = 'admins'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    admin_level: so.Mapped[int] = so.mapped_column(default=1)

    __mapper_args__ = {
        'polymorphic_identity': 'Admin'
    }

class Student(User):
    __tablename__ = 'students'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    course_enrollments: so.Mapped[list[str]] = so.mapped_column(sa.JSON, default=list)

    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

class Counsellor(User):
    __tablename__ = 'counsellors'
    id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), primary_key=True)
    specialisation: so.Mapped[str] = so.mapped_column(sa.String(128))

    __mapper_args__ = {
        'polymorphic_identity': 'Counsellor'
    }


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


# User 1-n Conversations
class Conversation(db.Model):
    __tablename__ = "conversations"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: so.Mapped[datetime] = so.mapped_column(default=sa.func.now())
    user: so.Mapped["User"] = relationship(back_populates="conversations")
    messages: so.Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")

# User and Conversation have 1-n association with Message
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


class Resource(db.Model):
    __tablename__ = "resources"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    last_updated: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        onupdate=sa.func.now()
    )

    def __repr__(self) -> str:
        return f"<Resource id={self.id} title={self.title!r}>"


class CounsellingSession(db.Model):
    __tablename__ = "counselling_sessions"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    counsellor_id: so.Mapped[int] = so.mapped_column(ForeignKey("counsellors.id", ondelete="CASCADE"))
    date_time: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), default=sa.func.now())
    status: so.Mapped[str] = so.mapped_column(sa.String(32), default="scheduled")

    student: so.Mapped["Student"]    = so.relationship(backref="sessions_as_student")
    counsellor: so.Mapped["Counsellor"] = so.relationship(backref="sessions_as_counsellor")

    def __repr__(self) -> str:
        return f"<Session {self.id} {self.status} {self.date_time:%Y‑%m‑%d %H:%M}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("students.id", ondelete="CASCADE"))
    counsellor_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("counsellors.id", ondelete="SET NULL"))
    status: so.Mapped[str] = so.mapped_column(sa.String(32), default="open")
    # Store chat‑style messages as JSON list of strings for simplicity
    messages: so.Mapped[list[str]] = so.mapped_column(sa.JSON, default=list)

    student: so.Mapped["Student"] = so.relationship(backref="tickets_opened")
    counsellor: so.Mapped[Optional["Counsellor"]] = so.relationship(backref="tickets_handled")

    def __repr__(self) -> str:
        return f"<Ticket {self.id} status={self.status}>"



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
