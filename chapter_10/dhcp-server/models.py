from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime


class BaseTable(DeclarativeBase):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserLease(BaseTable):
    __tablename__ = "user_lease"
    id = Column(Integer, primary_key=True)
    ip_addr = Column(String(50), nullable=False)
    mac_address = Column(String(50))


class WhiteListLease(BaseTable):
    __tablename__ = "white_list_lease"
    id = Column(Integer, primary_key=True)
    mac_address = Column(String(50), unique=True)


class ArpRecord(BaseTable):
    __tablename__ = "arp_record"
    id = Column(Integer, primary_key=True)
    ip_addr = Column(String(50), nullable=False)
    mac_address = Column(String(50), unique=True)
