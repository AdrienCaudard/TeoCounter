import csv
import algos
import os
import datetime

filtres = ['repos']


def csv_to_array(file, simplify = True):
    """
    Transformms a CSV file from Outlook classic into an array
    """
    extension = os.path.splitext(file)[1].lower()
    if extension == '.ics':
        return lire_ics(file)
    results = []
    with open(file, encoding="utf-8-sig", newline="") as fichier: # Reads every row of the CSV file and sends it into my array
        reader = csv.reader(fichier, quoting = csv.QUOTE_ALL)
        for row in reader:
            results.append(row)
    i = 0
    while i < len(results):                     # Removes the rows whose title matches one of the filters line 6
        if results[i][0].lower() in filtres:
            results.pop(i)
        else:
            i += 1
    if simplify == True:
        return simplify_data(results)
    return results


def simplify_data(data):
    """
    Removes the empty columns from my array given the filter of columns filtre_colonnes
    """
    filtre_colonnes = [5,6,9,10,11,12,13,14,15,16,18,19,20,21]
    filtre_colonnes.reverse()   # Reverses to avoid the index errors while popping some columns out of my array
    l_filtre = len(filtre_colonnes)

    data.pop(0)    
    for e in data:
        for i in range(l_filtre):
            e.pop(filtre_colonnes[i])
    
    for e in data:              # Replaces the empty places of work of the CSV file to undetermined (in french Non renseigné).
        if e[-1] == '':
            e[-1] = "Non renseigné"

    return data


def filter_dates(data, date_dbt, date_fin):
    """
    Removes every line out of the range from date_dbt to date_fin
    """
    date_dbt = algos.add_zeros(date_dbt)
    date_fin = algos.add_zeros(date_fin)
    dates_concernees = []
    for e in data:
        e[1] = algos.add_zeros(e[1])
        if e[1] < date_dbt or e[1] > date_fin:     # We can compare dates like that only because they are in the format YYYY MM DD
            continue
        else:
            dates_concernees.append(e)
    return dates_concernees



def get_poportions(data):
    if len(data) == 0:
        return {'cat':{}, 'Lieu':{}}
    results = {'cat':{}, 'Lieu':{}}
    
    for e in data:                                  # Counting the occurency of every meeting category or every place of work.
        if e[0] not in results['cat'].keys():
            results['cat'][e[0]] = 0
        if e[-1] not in results['Lieu'].keys():
            results['Lieu'][e[-1]] = 0
        duree = algos.get_duree_rdv(e[2], e[4])
        results['cat'][e[0]] += duree               # Adding the time of the meeting into the dict              
        results['Lieu'][e[-1]] += duree
    
    for cle, elts in results.items():
        for cat, cptr in elts.items():
            prct = str(round((cptr / get_totaux(data)*100))) + '%'
            if prct == '0%':
                prct = "<1%"
            results[cle][cat] = (prct, algos.get_time_minutes(cptr))
    return results

def get_totaux(data):
    """
    Returns the amount of hours in the given data
    """
    ttal = 0
    for rv in data:
        ttal += algos.get_duree_rdv(rv[2], rv[4])
    return ttal

def get_data(file, jour1, jour2):
    data = filter_dates(csv_to_array(file), jour1, jour2)
    return (algos.tri_data(data), algos.get_time_minutes(get_totaux(data)), get_poportions(data))
