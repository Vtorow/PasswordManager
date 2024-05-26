from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from passman.models import Base





class Password(Base):
    __tablename__ = 'passwords'
    description: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))