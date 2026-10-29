import os
import csv

nbs = '0123456789/'

def get_dico_base():
        return {'BEGIN':'',"DTSTAMP":'',"PEOPLE":'', "UID":'',"DTSTART":'',"DTEND":'',"SUMMARY":"","DESCRIPTION":'',"LOCATION":'',"END":''}

def dic_to_array(dict):
    debut, fin = dict['DTSTART'], dict['DTEND']
    return [
        dict['SUMMARY'],
        debut[6:8] + "/" + debut[4:6] + "/" + debut[0:4],
        debut[9:11] + ":" + debut[11:13] + ":00",
        fin[6:8] + "/" + fin[4:6] + "/" + fin[0:4],
        fin[9:11] + ":" + fin[11:13] + ":00",
        '01/01/9999', '23:59:00',
        dict['LOCATION']
    ]

def formater_row(row):
        if row != []:
            a = row[0].split(':')
            return a
        return ['Erreur']

def lire_ics(file):
    results = []
    debut = False


    with open(file, encoding="utf-8-sig", newline="") as fichier: # Reads every row of the CSV file and sends it into my array
        reader = csv.reader(fichier, quoting = csv.QUOTE_ALL)
        dico = get_dico_base()
        for row in reader:
            row = formater_row(row)
            if row == ['BEGIN', 'VEVENT']:
                debut = True
            if debut == True:
                if len(row) == 1:
                    row = ["PEOPLE", row]                
                dico[row[0]] = row[1]
                if row == ['END', 'VEVENT']:
                    res = dic_to_array(dico)
                    if res[0].strip() != "" and not res[0].startswith("ANNULE"):
                        results.append(res)
                    dico = get_dico_base()      # hors du if
                    debut = False
    return results

if __name__ == '__main__':
    print(lire_ics('file.ics'))