"""parser qui prend les coordonnées alphavantage pour renvoyer des valeurs de bourse"""

import json
import argparse
import datetime
import requests

# ajout les coordonnées alphavantage

URL = 'https://www.alphavantage.co/query'
FUNCTION = 'TIME_SERIES_DAILY'
APIKEY = '3PQRLNKE9VP5JH12'


# création du PARSER et ajout arguments à accepter (début, FIN, valeur, help):

PARSER = argparse.ArgumentParser(description=
                                 "Extraction de valeurs historique pour un symbole boursier",
                                 conflict_handler='resolve')
PARSER.add_argument('symbole', type=str, nargs='+', help="Nom du symbole boursier désiré")
PARSER.add_argument('-d', '--début', type=str, metavar='DATE',
                    help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
PARSER.add_argument('-f', '--FIN', type=str, metavar='DATE',
                    help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
PARSER.add_argument('-v', '--valeur', nargs=1, type=str, default='fermeture',
                    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
                    help="La valeur désirée (par défaut: fermeture)")
ARGS = PARSER.parse_args()

# fonction pour convertir l'input de la date en datetime.date


def conversion_date(date):
    """convertir la date de l'input de l'utilisateur"""
    listedate = date.split('-')
    annee = int(listedate[0])
    mois = int(listedate[1])
    jour = int(listedate[2])
    return datetime.date(annee, mois, jour)

# set valeur de début et FIN en jours


if ARGS.début is None and ARGS.FIN is None:
    DEBUT = datetime.date.today()
    FIN = DEBUT
elif ARGS.FIN is None:
    DEBUT = conversion_date(ARGS.début)
    FIN = datetime.date.today()
elif ARGS.début is None:
    FIN = conversion_date(ARGS.FIN)
    DEBUT = FIN
else:
    DEBUT = conversion_date(ARGS.début)
    FIN = conversion_date(ARGS.FIN)


VAL = ARGS.valeur[0]

"""si la valeur de ARGS.valeur = f, on veut avoir fermeture dans l'affichage"""

if VAL == "f":
    VAL = 'fermeture'

# fonction du calcul boursier


def calcul_boursier(symbole):
    """fonction qui va chercher les données dans le dictionnaire alphavantage"""
    size = 'compact'
    tdelta = FIN - DEBUT

    if tdelta.days*5/7 > 100:
        size = 'full'

    if VAL == 'ouverture':
        variable = '1. open'
    elif VAL == 'min':
        variable = '3. low'
    elif VAL == 'max':
        variable = '2. high'
    elif VAL == 'volume':
        variable = '5. volume'
    else:
        variable = '4. close'

    for symbol in symbole:

        params = {
            'function': FUNCTION,
            'symbol': symbol,
            'apikey': APIKEY,
            'outputsize': size,
        }

        response = requests.get(url=URL, params=params)  # type: object
        response = json.loads(response.text)
        tuple1 = (str(DEBUT), response['Time Series (Daily)'][str(DEBUT)][str(variable)])
        tuple2 = (str(FIN), response['Time Series (Daily)'][str(FIN)][str(variable)])
        print('{}({}, {}, {})'.format(symbol, VAL, str(DEBUT), str(FIN)))
        print([tuple1, tuple2])


if __name__ == '__main__':
    calcul_boursier(ARGS.symbole)
