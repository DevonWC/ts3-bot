import json
import urllib.request as ur
import time

player = "https://api.tibiadata.com/v1/characters/{0}.json"
world = "https://api.tibiadata.com/v1/worlds/Honbra.json"
t1 = time.time()

def getJson(url):
    
    return json.loads((ur.urlopen(url).read()).decode('utf-8'))

def checkLastDeath(name):
    jd = getJson(player.format(name))
    return jd.get('characters')['deaths'][0]

#checa se jogador por novas mortes (atualizar para banco de dados)
def checkNewDeath(plist):
    if checkLastDeath(plist[0])['date']['date'] != plist[1]:
        plist[1] = checkLastDeath(plist[0])['date']['date']
        return True

#retorna o total de makers online, baseado em uma lista.
def checkOnlineMakers(list):
    p_online = getJson(world).get('worlds')['players_online']
    onlineCounter = 0

    for i in p_online:
        if i['name'].lower() in list:
            onlineCounter += 1

    return onlineCounter

t2 = time.time()
print('tempo:', t2-t1)