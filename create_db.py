from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Integer, String, Date, DateTime, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Float

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

    cadastrejour = Column(Integer, nullable=True)
    renove = Column(Integer, nullable=True)
    profondeur = Column(String, nullable=True)
    cadastrematrice = Column(Integer, nullable=True)
    idlots_cad = Column(String, nullable=True)
    frontage = Column(String, nullable=True)
    cadastrehisto = Column(Integer, nullable=True)
    idlots = Column(Integer, nullable=True)
    superficie = Column(String, nullable=True)
    idlots_his = Column(String, nullable=True)
    nolot = Column(String, nullable=True)


class InfoGenerale(Base):

    __tablename__ = 'infogenerale'

    info_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    yearconstruction = Column(String, nullable=True)
    etages = Column(Integer, nullable=True)
    profondeur = Column(Float, nullable=True)
    voisinage = Column(String, nullable=True)
    frontage = Column(Float, nullable=True)
    nblocaux = Column(Float, nullable=True)
    superficie = Column(Float, nullable=True)
    nblogements = Column(Float, nullable=True)
    codeutilisation = Column(String, nullable=True)
    utilisation = Column(String, nullable=True)


class Proprietaires(Base):

    __tablename__ = 'proprietaires'

    proprio_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    adresse = Column(String, nullable=True)
    codepostal = Column(String, nullable=True)
    city = Column(String, nullable=True)
    dateinscription = Column(Date, nullable=True)
    nom = Column(String, nullable=True)


class Adresses(Base):

    __tablename__ = 'adresses'

    adress_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    x = Column(Float, nullable=True)
    adresse = Column(String, nullable=True)
    y = Column(Float, nullable=True)
    statut = Column(String, nullable=True)
    fmat18 = Column(String, nullable=True)
    codegenerique = Column(String, nullable=True)
    matricule = Column(String, nullable=True)
    lien = Column(String, nullable=True)
    voie = Column(String, nullable=True)
    matricule18 = Column(String, nullable=True)
    numcivique = Column(String, nullable=True)
    source = Column(String, nullable=True)
    isadresseprincipale = Column(Integer, nullable=True)
    fmat = Column(String, nullable=True)


class ValeurRole(Base):

    __tablename__ = 'valeurrole'

    value_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    pull_id = Column(Integer, ForeignKey('lotpull.pull_id'))

    t_anterieur = Column(Float, nullable=True)
    t_actuelle = Column(Float, nullable=True)
    yearRole = Column(String, nullable=True)
    i_anterieur = Column(Float, nullable=True)
    b_anterieur = Column(Float, nullable=True)
    t_next = Column(String, nullable=True)
    i_actuelle = Column(Float, nullable=True)
    b_actuelle = Column(Float, nullable=True)


# class Croquis(Base):

#     __tablename__ = 'croquis'

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
#     trade_date = Column(DateTime, nullable=False)
#     tid = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)
#     amount = Column(Float, nullable=False)
#     side = Column(String, nullable=False)


# class Zonage(Base):

#     __tablename__ = 'zonage'

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
#     trade_date = Column(DateTime, nullable=False)
#     tid = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)
#     amount = Column(Float, nullable=False)
#     side = Column(String, nullable=False)


# class Photos(Base):

#     __tablename__ = 'photos'

#     id = Column(Integer, autoincrement=True, primary_key=True)
#     transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
#     trade_date = Column(DateTime, nullable=False)
#     tid = Column(Integer, nullable=False)
#     price = Column(Float, nullable=False)
#     amount = Column(Float, nullable=False)
#     side = Column(String, nullable=False)


if __name__ == '__main__':
    engine = create_engine(DB_PATH, echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
