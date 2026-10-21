def add_zeros(date):
    """
    Adds zeros to a date, to match the format DD-MM-YYYY
    """
    elts = ['']
    compteur = 0
    for i in range(len(date)):
        if date[i] in '-/':
            compteur +=1
            elts.append('')
        else:
            elts[compteur] += date[i]
    if len(elts[0]) > len(elts[2]):
        elts[0], elts[2] = elts[2], elts[0]
    intlen = [2,2,4]
    for i in range(3):
        if len(elts[i]) < intlen[i]:
            elts[i] = '0' * (intlen[i] - len(elts[i])) + elts[i]
    return elts[2] + '/' + elts[1] + '/' + elts[0]

def get_duree_rdv(heure1, heure2):
    heure1 = heure1.split(":")
    heure2 = heure2.split(':')
    multiplicateurs = [60,1,1/60]
    for i in range(3):
        heure1[i] = int(heure1[i]) * multiplicateurs[i]
        heure2[i] = int(heure2[i]) * multiplicateurs[i]
    return (sum(heure2) - sum(heure1))/60

def date_number_to_char(date):
    mois = ["", " Janvier ", " Février ", " Mars ", " Avril ", " Mai ", " Juin ", " Août ", " Septembre ", " Octobre ", " Novembre ", " Décembre "]
    date = date.split('-')
    return date[2] + mois[int(date[1])] + date[0]

if __name__ == '__main__':    
    print(get_duree_rdv('09:15:00', '11:30:00'))