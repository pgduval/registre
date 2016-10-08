import os
import json
import datetime
import re
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import *
from create_db import *


def store_pull(lot):
    new_item = LotPull()
    new_item.lot_id = lot.strip(".txt")
    new_item.city = CITY
    new_item.pull_date = datetime.datetime.now().date()
    session.add(new_item)
    session.commit()

    pull_id = new_item.pull_id
    return pull_id


def store_infolots(infolots):
    # List info lots
    for info in infolots:

        new_item = InfoLots()
        new_item.pull_id = pull_id

        new_item.cadastrejour = info.get('cadastreJour') * 1
        new_item.renove = info.get('renove') * 1
        new_item.profondeur = float(info.get('profondeur'))
        new_item.cadastrematrice = info.get('cadastreMatrice') * 1
        new_item.idlots_cad = info.get('idLotS_Cad')
        new_item.frontage = float(info.get('frontage'))
        new_item.cadastrehisto = info.get('cadastreHisto') * 1
        new_item.idlots = info.get('idLotS')
        new_item.superficie = float(info.get('superficie'))
        new_item.idlots_his = info.get('idLotS_His')
        new_item.nolot = info.get('noLot')
        session.add(new_item)
        session.commit()


def store_infogeneral(infogeneral):

    # Info Generale
    non_decimal = re.compile(r'[^\d.]+')

    new_item = InfoGenerale()
    new_item.pull_id = pull_id
    new_item.yearconstruction = infogeneral.get('yearConstruction')
    new_item.etages = int(infogeneral.get('etages'))

    p1 = infogeneral.get('profondeur')
    p2 = non_decimal.sub('', p1.replace(",", "."))
    new_item.profondeur = p2

    new_item.voisinage = infogeneral.get('voisinage')

    f1 = infogeneral.get('frontage')
    f2 = non_decimal.sub('', f1.replace(",", "."))
    new_item.frontage = f2

    new_item.nblocaux = infogeneral.get('nbLocaux')

    s1 = infogeneral.get('superficie')
    s2 = non_decimal.sub('', s1.replace(",", "."))
    new_item.superficie = s2

    new_item.nblogements = float(infogeneral.get('nbLogements'))
    new_item.codeutilisation = infogeneral.get('codeUtilisation')
    new_item.utilisation = infogeneral.get('utilisation')

    session.add(new_item)
    session.commit()


def store_proprio(proprio):
    for prop in proprio:

        new_item = Proprietaires()
        new_item.pull_id = pull_id

        new_item.adresse = prop.get('adresse')
        new_item.codepostal = prop.get('codePostal')
        new_item.city = prop.get('city')
        d1 = datetime.datetime.strptime(prop.get('dateInscription'), "%Y-%m-%d")
        new_item.dateinscription = d1.date()
        new_item.nom = prop['nom']

        session.add(new_item)
        session.commit()


def store_adresses(adresses):
    for adress in adresses:
        new_item = Adresses()
        new_item.pull_id = pull_id

        new_item.x = float(adress.get('x'))
        new_item.adresse = adress.get('adresse')
        new_item.y = float(adress.get('y'))
        new_item.statut = adress.get('statut')
        new_item.fmat18 = adress.get('fMat18')
        new_item.codegenerique = adress.get('codeGenerique')
        new_item.matricule = adress.get('matricule')
        new_item.lien = adress.get('lien')
        new_item.voie = adress.get('voie')
        new_item.matricule18 = adress.get('matricule18')
        new_item.numcivique = adress.get('numCivique')
        new_item.source = adress.get('source')
        new_item.isadresseprincipale = adress.get('isAdressePrincipale') * 1
        new_item.fmat = adress.get('fMat')

        session.add(new_item)
        session.commit()


def store_value(valeur):
    new_item = ValeurRole()
    new_item.pull_id = pull_id

    new_item.t_anterieur = float(valeur['t_anterieur'])
    new_item.t_actuelle = float(valeur['t_actuelle'])
    new_item.yearRole = valeur['yearRole']
    new_item.i_anterieur = float(valeur['i_anterieur'])
    new_item.b_anterieur = float(valeur['b_anterieur'])
    new_item.t_next = valeur['t_next']
    new_item.i_actuelle = float(valeur['i_actuelle'])
    new_item.b_actuelle = float(valeur['b_actuelle'])
    session.add(new_item)
    session.commit()


# Main
engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

logging.basicConfig(filename=os.path.join(LOG_PATH, 'store.log'),
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

all_lots = os.listdir(os.path.join(PATH_OUT, 'raw'))

lots_db = session.query(LotPull.lot_id).all()
lots_db = [x[0] + ".txt" for x in lots_db]

lots_to_insert = [x for x in all_lots if x not in lots_db]

print("Total lots:{0} - New lots:{1}".format(len(all_lots), len(lots_to_insert)))

logging.info('--- Start storage session for {0} lots ---'.format(len(lots_to_insert)))

for lot in lots_to_insert:

    print("Starting lot {0}".format(lot))
    try:
        data = json.load(open(os.path.join(PATH_OUT, 'raw', lot)))
        pull_id = store_pull(lot)
        store_infolots(data['infoLots'])
        store_infogeneral(data['infoGenerale'])
        store_proprio(data['proprietaires'])
        store_adresses(data['adresses'])
        store_value(data['valeurRole'])
        print("Done!")
    except:
        logging.warning('Failed storage for lot: {0}'.format(lot))
logging.info('---- End storage session ------')

# END
