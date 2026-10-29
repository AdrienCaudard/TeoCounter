from datetime import date

def lire_ics(file):
    return  # Not defined yet, has to transform the ICS data into an array that I can use


def add_zeros(date):
    """
    Adds zeros to a date, to match the format DD-MM-YYYY
    """
    elts = ['']
    compteur = 0
    for i in range(len(date)):          # Splits the date manually for any separator in the string below on line 8
        if date[i] in '-/':
            compteur +=1
            elts.append('')
        else:
            elts[compteur] += date[i]
            
    if len(elts[0]) > len(elts[2]):     # Reverses the date From YYYY MM DD to DD MM YYYY
        elts[0], elts[2] = elts[2], elts[0]
    intlen = [2,2,4]
    for i in range(3):
        if len(elts[i]) < intlen[i]:
            elts[i] = '0' * (intlen[i] - len(elts[i])) + elts[i]
    return elts[2] + '/' + elts[1] + '/' + elts[0]


def delta_date(jr1, jr2):
    jr1 = jr1.split('/')
    jr2 = jr2.split("/")
    if len(jr1[0]) > len(jr1[2]):
        jr1[0], jr1[2] = jr1[2], jr1[0]
    if len(jr2[0]) > len(jr2[2]):
        jr2[0], jr2[2] = jr2[2], jr2[0]
    for i in range(3):
        jr1[i] = int(jr1[i])
        jr2[i] = int(jr2[i])
    jr1 = date(jr1[2], jr1[1], jr1[0])
    jr2 = date(jr2[2], jr2[1], jr2[0])
    res = jr2 - jr1
    return res.days


def get_duree_rdv(heure1, heure2, jr1 = "12/12/1212", jr2 = "12/12/1212"):
    heure1 = heure1.split(":")
    heure2 = heure2.split(':')
    multiplicateurs = [60,1,1/60]   # In order to get a data in minutes
    for i in range(3):
        heure1[i] = round(int(heure1[i]) * multiplicateurs[i])
        heure2[i] = round(int(heure2[i]) * multiplicateurs[i])
    res = [((sum(heure2) - sum(heure1))/60), 24 * delta_date(jr1, jr2)]
    return sum(res)

def date_number_to_char(date):
    '''
    Splits DD MM YYYY date to DD Month YYYY
    '''
    
    mois = ["", " Janvier ", " Février ", " Mars ", " Avril ", " Mai ", " Juin ", "Juillet", " Août ", " Septembre ", " Octobre ", " Novembre ", " Décembre "]

    date = date.split('-')
    return date[2] + mois[int(date[1])] + date[0]

def tri_data(data):
    """
    Sorts the data by alphabetical order given its intitulate / title / whatever you call it
    """
    for i in range(len(data)):
        idx_min = i
        for j in range(i + 1, len(data)):
            if data[j][0].lower() < data[idx_min][0].lower():
                idx_min = j
        data[i], data[idx_min] = data[idx_min], data[i]
    return data
            
def get_time_minutes(time):
    '''
    Transforms raw time data (1.66h) into a readable format -> 1H 40min for example.
    The data in parameter is a float or an int.
    '''
    return str(round(time // 1)) + "h " + str(round((time - time//1) * 60)) + "min"
        
if __name__ == '__main__':    
    print(get_duree_rdv('09:15:00', '11:30:00'))
    print(get_time_minutes(1.66))