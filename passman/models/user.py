from sqlalchemy.orm import mapped_column, Mapped, relationship

from passman.models import Base
from passman.models.password import Password




class User(Base):
    __tablename__ = 'users'
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    passwords: Mapped[list["Password"]] = relationship('Password', lazy="joined", cascade="all, delete")
    is_admin: Mapped[bool] = mapped_column(default=False)
