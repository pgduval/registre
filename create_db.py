from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Boolean, Integer, String, Date, DateTime, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Float

from setup import DB_PATH

Base = declarative_base()


class LotPull(Base):

    __tablename__ = 'lotpull'

    pull_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    lot_id = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pull_date = Column(Date, nullable=False)


class InfoLots(Base):

    __tablename__ = 'infolots'

    info_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    cadastreJour = Column(Boolean, nullable=False)
    renove = Column(Boolean, nullable=False)
    profondeur = Column(String, nullable=True)
    cadastreMatrice = Column(Boolean, nullable=False)
    idLotS_Cad = Column(String, nullable=True)
    frontage = Column(String, nullable=True)
    cadastreHisto = Column(Boolean, nullable=False)
    idLotS = Column(Integer, nullable=True)
    superficie = Column(String, nullable=True)
    idLotS_His = Column(String, nullable=True)
    noLot = Column(String, nullable=False)


class InfoGenerale(Base):

    __tablename__ = 'infogenerale'

    info_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    yearConstruction = Column(Integer)
    etages = Column(Integer)
    profondeur = Column(Float)
    voisinage = Column(String)
    frontage = Column(Float)
    nbLocaux = Column(Float)
    superficie = Column(Float)
    nbLogements = Column(Float)
    codeUtilisation = Column(String)
    utilisation = Column(String)


class Proprietaires(Base):

    __tablename__ = 'proprietaires'

    price_id = Column(Integer, autoincrement=True, primary_key=True)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    last = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)


class Adresses(Base):

    __tablename__ = 'adresses'

    transact_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)


class ValeurRole(Base):

    __tablename__ = 'valeurrole'

    id = Column(Integer, autoincrement=True, primary_key=True)
    transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
    trade_date = Column(DateTime, nullable=False)
    tid = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


class Croquis(Base):

    __tablename__ = 'croquis'

    id = Column(Integer, autoincrement=True, primary_key=True)
    transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
    trade_date = Column(DateTime, nullable=False)
    tid = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


class Zonage(Base):

    __tablename__ = 'zonage'

    id = Column(Integer, autoincrement=True, primary_key=True)
    transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
    trade_date = Column(DateTime, nullable=False)
    tid = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


class Photos(Base):

    __tablename__ = 'photos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
    trade_date = Column(DateTime, nullable=False)
    tid = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


if __name__ == '__main__':
    engine = create_engine(DB_PATH, echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
