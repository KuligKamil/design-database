import uuid
import re

from sqlalchemy import inspect, create_engine, Column, func, DateTime, String, Integer
from sqlalchemy.orm import declared_attr, declarative_base
from sqlalchemy_utils import create_database

db_url = f'sqlite:///example{uuid.uuid1()}.sqlite'
create_database(db_url)
engine = create_engine(db_url)
ins: inspect = inspect(engine)


def camel_snake(s: str) -> str:
    """
    >>> camel_snake('CamelNotationIsNotCoolUntilItIsSSSnake')
    'camel_notation_is_not_cool_until_it_is_sssnake'
    >>> camel_snake('PartnerCRMNoteType')
    'partner_crmnote_type'
    >>> camel_snake('CRMQuestion')
    'crmquestion'
    """
    return re.sub(r'([a-z])([A-Z])', r'\g<1>_\g<2>', s).lower()


def generate_uuid() -> str:
    return uuid.uuid4().hex


class CustomBase:
    # id = Column(uuid.UUID, primary_key=True, default=generate_uuid)
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return camel_snake(cls.__name__)


Base = declarative_base(cls=CustomBase)


class User(Base):
    name = Column(String(128), nullable=False, unique=True)


Base.metadata.create_all(bind=engine)
