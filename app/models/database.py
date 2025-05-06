from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker,
from sqlalchemy.dialects.postgresql import insert as pg_insert  # for UPSERT in PostgreSQL
from models import *
from more_itertools import chunked
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Db:
    def __init__(self, engine):
        self.engine = engine
        self.SessionLocal = sessionmaker(bind=self.engine)

    def connect(self):
        print("[DB] Creating tables...")
        Base.metadata.create_all(bind=self.engine)
        self._add_stores()
        self._add_regions()
        print("[DB] Save tables...")

    def _add_stores(self):
        stores = [
            {"id": 1, "name": "Ашан", "code": "ashan"},
            {"id": 2, "name": "Магнит", "code": "magnit"},
        ]
        with self.SessionLocal() as session:
            for store in stores:
                exists = session.query(Store).filter_by(id=store["id"]).first()
                if not exists:
                    session.add(Store(**store))
            session.commit()

    def _add_regions(self):
        regions = [
            {"id": 77, "name": "Москва"},
            {"id": 78, "name": "Санкт-Петербург"},
            {"id": 59, "name": "Пермь"},
        ]
        with self.SessionLocal() as session:
            for region in regions:
                exists = session.query(Region).filter_by(id=region["id"]).first()
                if not exists:
                    session.add(Region(**region))
            session.commit()

    def add_products(self, products: list[dict], batch_size: int):
        with self.SessionLocal() as session:
            for batch in chunked(products, batch_size):
                stmt = pg_insert(Product).values(batch)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['product_id'],
                    set_={"price": stmt.excluded.price}
                )
                session.execute(stmt)
            session.commit()
