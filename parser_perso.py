import requests
import json
import argparse
import datetime

### ajout les coordonnées alphavantage

url = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
apikey = '3PQRLNKE9VP5JH12'
now = datetime.date.today()


# création du parser et ajout arguments à accepter (début, fin, valeur, help):

parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un symbole boursier", conflict_handler='resolve')
parser.add_argument('symbole', type=str, nargs='+', help="Nom du symbole boursier désiré")
parser.add_argument('-d',  '--début', type=str, help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
parser.add_argument('-f','--fin', type=str, help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
parser.add_argument('-v', '--valeur', nargs=1, type=str, default='fermeture', choices=['fermeture','ouverture','min','max','volume'], help="La valeur désirée (par défaut: fermeture)")
args = parser.parse_args()

## fonction pour convertir l'input de la date en datetime.date

def conversion_date(date):
    listedate = date.split('-')
    année = int(listedate[0])
    mois = int(listedate[1])
    jour = int(listedate[2])
    return(datetime.date(année,mois,jour))

## set valeur de début et fin en jours

fin = conversion_date(args.fin)
début = conversion_date(args.début)
val = args.valeur[0]

## si la valeur de args.valeur = f, on veut avoir fermeture dans l'affichage
if val == "f":
    val = 'fermeture'

## si on a pas d'input de début OU fin, on set à la date d'aujourd'hui

if args.début == None or args.fin == None:
    début = datetime.time.today()
    fin = début

## fonction du calcul boursier

def calcul_boursier(symbole):
    size = 'compact'
    tdelta = fin - début

    ## on set tdelta à la différence entre la fin et le début

    if tdelta > datetime.timedelta(days=100):
        size = 'full'

    ## plusieurs if statements pour les différents input de -v

    if val == 'ouverture':
        v = '1. open'
    elif val == 'min':
        v = '3. low'
    elif val == 'max':
        v = '2. high'
    elif val == 'volume':
        v = '5. volume'
    else:
        v = '4. close'

    ## on fait une loop si jamais on a plus d'un symbole à évaluer

    for symbol in symbole:

        params = {
            'function': function,
            'symbol': symbol,
            'apikey': apikey,
            'outputsize': size,
        }
        ## connection serveur
        response = requests.get(url=url, params=params)  # type: object
        response = json.loads(response.text)
        ## renvoi de message d'erreur si impossible de se connecter à Alphavantage
        try:
            tuple1 = (str(début), response['Time Series (Daily)'][str(début)][str(v)])
            tuple2 = (str(fin), response['Time Series (Daily)'][str(fin)][str(v)])
        except KeyError:
            print("Difficultés à se connecter à AlphaVantage, veuillez réessayer plus tard")
            break
        else:
            print('{}({}, {}, {})'.format(symbol, val, str(début), str(fin)))
            print([tuple1, tuple2])



if __name__ == '__main__':
    ## on éxécute la fonction calcul_boursier à l'appel du programme dans le terminal
    calcul_boursier(args.symbole)
