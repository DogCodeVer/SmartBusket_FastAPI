from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code = Column(String)

    products = relationship("Product", back_populates="store")

class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    products = relationship("Product", back_populates="region")

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Text, unique=True)
    store_id = Column(Integer, ForeignKey('store.id'))
    region_id = Column(Integer, ForeignKey('region.id'))
    name = Column(Text)
    code = Column(Text)
    category = Column(String)
    category_code = Column(String)
    price = Column(Float)

    store = relationship("Store", back_populates="products")
    region = relationship("Region", back_populates="products")
