import math
import requests
import json
import argparse

### ajout les coordonnées alphavantage

url = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
apikey = '3PQRLNKE9VP5JH12'

# création du parser et ajout arguments à accepter (début, fin, valeur, help)

parser = argparse.ArgumentParser(description="entrer nom compagnie pour informations sur les prix bourse")
parser.add_argument('-d', '--début', type='int', metavar='', help="Date initiale du prix de l'action" )
parser.add_argument('-f', '--fin', type='int', metavar='', help="Date finale du prix de l'action" )
parser.add_argument('symbol', type='str', metavar='', help="" )
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--valeur', action='store_true', nargs=1, default='fermeture', metavar='', help="valeur désirée de l'action")
args = parser.parse_args()


## fonction à call

def parser_bourse(symbol, début, fin):
    ## loop pour demander compacte ou full
    while True:
        size = str(input('compact ou full? c/f'))
        if size.lower() == 'c' or size.lower() == 'compact':
            params = {
            'function': function,
            'symbol': symbol,
            'apikey': apikey,
            'outputsize': compact,
            }
            break
        elif size.lower() == 'f' or size.lower() == 'full':
            params = {
            'function': function,
            'symbol': symbol,
            'apikey': apikey,
            'outputsize': full,
            }
            break
        else:
            print('Désolé, veuillez entrer une commande valide. Compact ou Full(c/f)?')
            continue

    response = requests.get(url=url, params=params)
    response = json.loads(response.text)

    ## ajouter le truc pour valeur




if __name__ == '__main__':
    print('allo')
