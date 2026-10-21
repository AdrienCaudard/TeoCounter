import csv
import algos
import os
import datetime

filtres = ['repos']


def csv_to_array(file, simplify = True):
    extension = os.path.splitext(file)[1].lower()
    if extension == '.ics':
        return lire_ics(file)
    results = []
    with open(file, encoding="utf-8-sig", newline="") as fichier:
        reader = csv.reader(fichier, quoting = csv.QUOTE_ALL)
        for row in reader:
            results.append(row)
    print("Données simplifiées")
    i = 0
    while i < len(results): 
        print(results[i][0].lower(), filtres)
        if results[i][0].lower() in filtres:
            results.pop(i)
            print("Ca degage")
        else:
            print(results[i], i)
            i += 1
        print()
    print("Repos viré")
    if simplify == True:
        return simplify_data(results)
    return results


def simplify_data(data):
    filtre_colonnes = [5,6,9,10,11,12,13,14,15,16,18,19,20,21]
    filtre_colonnes.reverse()
    l_filtre = len(filtre_colonnes)

    data.pop(0)    
    for e in data:
        for i in range(l_filtre):
            e.pop(filtre_colonnes[i])
    
    for e in data:
        if e[-1] == '':
            e[-1] = "Non renseigné"

    return data

def filter_dates(data, date_dbt, date_fin):
    date_dbt = algos.add_zeros(date_dbt)
    date_fin = algos.add_zeros(date_fin)
    dates_concernees = []
    for e in data:
        e[1] = algos.add_zeros(e[1])
        if e[1] < date_dbt or e[1] > date_fin:
            continue
        else:
            dates_concernees.append(e)
    return dates_concernees



def get_poportions(data):
    if len(data) == 0:
        return {'cat':{}, 'Lieu':{}}
    results = {'cat':{}, 'Lieu':{}}
    for e in data:
        if e[0] not in results['cat'].keys():
            results['cat'][e[0]] = 0
        if e[-1] not in results['Lieu'].keys():
            results['Lieu'][e[-1]] = 0
        results['cat'][e[0]] += 1
        results['Lieu'][e[-1]] += 1
    for cle, elts in results.items():
        for cat, cptr in elts.items():
            results[cle][cat] = (str(round((cptr / len(data))*100)) + '%', cptr)
            if results[cle][cat] == '0%':
                results[cle][cat] = "<1%"
    return results

def get_totaux(data):
    ttal = 0
    for rv in data:
        ttal += algos.get_duree_rdv(rv[2], rv[4])
    return ttal

def get_data(file, jour1, jour2):
    data = filter_dates(csv_to_array(file), jour1, jour2)
    return (data, get_totaux(data), get_poportions(data))
