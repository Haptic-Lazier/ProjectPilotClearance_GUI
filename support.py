import requests
from bs4 import BeautifulSoup

def metar_get(aic):
    url = "https://www.aviationweather.gov/metar/data?ids=" + aic + "&format=raw&date=&hours=0"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="awc_main_content_wrap")

    rawmetar = results.find("code")
    metar = str(rawmetar)[6:]
    metar = str(metar)[:-7]

    if metar == '':
        metar = 'nullbyte1'
    print(metar)
    return metar

def metar_dict(aic):
    metar = aic.split()
    clouds = []
    if metar[0] == 'nullbyte1':
        information = {'time': '', 'wind': '', 'vis': '', 'clouds': '', 'baro': '', 'temp': '', 'dew': ''}
    else:
        information = {'time': metar[1], 'wind': '', 'vis': '', 'clouds': '', 'baro': '', 'temp': '', 'dew': ''}

    for a in metar:
        if 'KT' in a:
            information.update({'wind': a})
        if 'SM' in a:
            if '1/4' in a:
                b = '1.25SM'
                information.update({'vis': b})
            elif '1/2' in a:
                b = '1.5SM'
                information.update({'vis': b})
            elif '3/4' in a:
                b = '1.75SM'
                information.update({'vis': b})
            else:
                information.update({'vis': a})

        if 'CLR' in a or 'FEW' in a or 'SCT' in a or 'OVC' in a or 'BKN' in a:
            clouds.append(a)
        if 'A' in a:
            if a[1] == '2' or a[1] == '3':
                information.update({'baro': a})
        if '/' in a:
            tempcounter = 0
            tempmax = len(a)
            tempmid = 0
            if len(a) <= 7 and len(a) >= 5:
                for i in a:
                    if i == '/':
                        tempmid = tempcounter
                    tempcounter += 1
                information.update({'temp': a[:tempmid]})
                information.update({'dew': a[tempmid + 1:]})

        elif 'nullbyte1' in a:
            information.update({'time' : 'Null'})
            information.update({'wind' : 'Null'})
            information.update({'vis': 'Null'})
            information.update({'clouds': 'Null'})
            information.update({'baro': 'Null'})
            information.update({'temp': 'Null'})
            information.update({'dew': 'Null'})
            return information

    information.update({'clouds': clouds})
    print(information)
    return information


def densityalt(baro, temp, alt=0):
    if baro == 'Null':
        return 'Null'
    if temp[0].isalpha() == True:
        temp = temp.replace('M', '')
        temp = temp.replace('C', '')
        temp = temp.replace('*', '')


    baro = baro[1:]
    baroa = baro[0] + baro[1] + '.' + baro[2] + baro[3]
    baro = 1000 * (29.92 - float(baroa))
    baroa = int(alt) - int(baro)
    isa = (18 + (-2 * (alt // 1000)))

    denalt = baroa + (120 * (int(temp) - isa))

    if denalt >= 0:
        return (f'+{denalt}')
    else:
        return denalt

def Condition(clouds, vis, glvl=11):
    if clouds == 'Null':
        return 'Null'
    #print(clouds)
    if clouds[0] == 'CLR':
        clouds = 12000
    elif str(clouds[0][3]) == '0':
        clouds = clouds[0][4:]
    else:
        clouds = clouds[0][3:]
    if float(vis[:-2]) < 3 or (int(clouds) - glvl) < 10:
        return ("IFR")
    else:
        return ("VFR")
#dict = metar_dict(metar_get('KCHA'))
#print(Condition(dict['clouds'], dict['vis']))