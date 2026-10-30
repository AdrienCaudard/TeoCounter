import csv
import algos
import os
from lire_ics import lire_ics

filtres = ['repos']


def csv_to_array(file, simplify = True):
    """
    Transformms a CSV file from Outlook classic into an array
    """
    extension = os.path.splitext(file)[1].lower()
    print(f"Type de fichier : fichier {extension}")
    if extension == '.ics':
        results = lire_ics(file)
    else:
        results = []
        with open(file, encoding="utf-8-sig", newline="") as fichier: # Reads every row of the CSV file and sends it into my array
            reader = csv.reader(fichier, quoting = csv.QUOTE_ALL)
            for row in reader:
                results.append(row)
        if simplify == True:
            results = simplify_data(results)
    i = 0
    while i < len(results):                     # Removes the rows whose title matches one of the filters line 6
        if results[i][0].lower() in filtres:
            results.pop(i)
        else:
            i += 1
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
    results = {'cat': {}, 'Lieu': {}}           # Creates a dictionnary in order to iterate the working hours
    if not data:
        return results
    total = get_totaux(data)
    for e in data:
        duree = algos.get_duree_rdv(e[2], e[4], e[1], e[3])             # Gets the length in time for the row selected
        results['cat'][e[0]] = results['cat'].get(e[0], 0) + duree
        results['Lieu'][e[-1]] = results['Lieu'].get(e[-1], 0) + duree
    for cle, elts in results.items():                                   # Selects every category counted
        for cat, cptr in elts.items():                                  # Selects Every type of meeting among the categorys
            prct = f"{round(cptr / total * 100)}%" if total else "0%"
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
        ttal += algos.get_duree_rdv(rv[2], rv[4], rv[1], rv[3])         # Counts the total of hours in the data filtered
    return ttal

def get_data(file, jour1, jour2):
    """
    Returns a tuple (Sorted data , Total of time , proportions for each meeting)
    """
    data = filter_dates(csv_to_array(file), jour1, jour2)
    res = (algos.tri_data(data), algos.get_time_minutes(get_totaux(data)), get_poportions(data))
    return res

if __name__ == "__main__":
    a = csv_to_array("edt_annee.CSV")
    print(get_data("file.ics", "2026-11-02", "2026-11-06")[1])