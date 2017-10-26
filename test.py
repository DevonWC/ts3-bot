from ts3 import TS3Server
from time import sleep
import time
import tibia


# ----------------------- CONFIGURAÇÃO ---------------------------------

#lista teste de players para checar novas mortes, ['nome+do+jogador', 'ultimamorte] (criar banco de dados)
playerlist = [['Deku Panzon', ''], ['Mouzsack', '2017-10-21 01:20:58.000000'], ['Binus+Belis', '2017-10-21 00:40:01.000000'], ['Old Bodybuilder', ''],
              ['Biger', '2017-10-21 00:37:20.000000'], ['Brisadus', ''], ['Edio Lavis', ''], ['Jazir', ''], ['Floki Svein', ''],
              ['Kolerah', ''], ['Zikiz Surf', ''], ['Garrero Tank', ''], ['Lady Lufty', ''], ['Adethor ade', ''], ['Leozin Aguerrido', ''],
              ['Shaymin Prasete', ''], ['Hintz Mixall', ''], ['Pedrox da Ricaria', ''], ['Angoro', ''], ['Dgzin Feat', ''], ['Wix da Ricaria', ''],
              ['Arroto de bolovo', ''], ['Wesilei+On+Honbra', ''], ['Ohnivek', ''], ['Mage+Brisa', '']]

#lista de makers mage
maker_list = ['roque healer', 'king feliipe', 'wizard solo', 'soster mito', 'brax pierce', 'combatente de satan', 'miguel felomenal', 'foxx boladao', 'mexxtre dos magos']

token = 'wdskUKgDKf1bxXUjApjgqBc2wiJiEb1+bLSd6y+a' #token de privilegio ADM
t_makerCheck = 1200 #tempo para cada masspoke de makers online, em segundos
t_connection = 300 #tempo para reconectar ao servidor ts3
makerCheck = time.time() #varivel usada para contar o tempo entre masspoke de makers
previousOnline = 0 #usado para guardar ultima qualidade de makers online
c_renew_time = time.time() #usado para contar tempo usado para renovar conexão com o ts3

# ---------------- FIM DA CONFIGURAÇÂO ---------------------------------

server = TS3Server('127.0.0.1', 10011, 1)
if server.login('serveradmin', 'pKEZF0Ct'):
    print('Server connection initilized...')

clients = server.clientlist()

def massPoke(msg, client):
    for i in clients:
        server.clientpoke(client.get(i)['clid'], msg)


while True:
    
    makers = tibia.checkOnlineMakers(maker_list)

#renova a conexão com o ts3 a cada 5 minutos...
    if (time.time() - c_renew_time) > t_connection:
        server = TS3Server('127.0.0.1', 10011, 1)
        if server.login('serveradmin', 'pKEZF0Ct'):
            clients = server.clientlist()
            c_renew_time = time.time()
            print('Server connection stable...')

#Verifica makers online, apenas atualiza a cada 5 minutos, excento quanto o algum outro maker entra no jogo.
#exemplo, ultimo poke aconteceu a 2 minutos com 5 makers, proximo poke so verificaria em 5 minutos, porem se entrou mais 1 player
#o poke será feito para 6 makers (configuravel, pode-se adicionar incrementos maiores)
#como elif (makers > (previousOnline+2) ) para apenas avisar quando entrar +3 makers, baseado no numero que havia online antes.
    since = time.time() - makerCheck
    if (makers > 3) and (since > t_makerCheck):
        makerCheck = time.time()
        massPoke("[color=red][b]{0} MAKERS ONLINE[/b][/color]".format(makers), clients)
        previousOnline = makers
    elif (makers > previousOnline):
        massPoke("[color=red][b]{0} MAKERS ONLINE[/b][/color]".format(makers), clients)
        previousOnline = makers


#Esse bloco constantemente verifica os players definidos em uma lista ou banco de dados.
#constando aqui todas as suas mortes, e realizando um massPoke()
#pode ser adicionado filtros, para evitar pokes de inimigos que morrem para monstros de arena pvp. (Pit Reaver, Pit Blackling, Death, etc)

    for k, i  in enumerate(playerlist):
        lastDeath = tibia.checkLastDeath(i[0])
        if tibia.checkNewDeath(i) and int(lastDeath['level']) > 5:
            print("ENEMY MORTO: {0} {1} at level {2}".format(i[0].replace("+", " "), lastDeath['reason'], lastDeath['level']))
            clients = server.clientlist()
            massPoke("[color=red]ENEMY MORTO: {0} at level {1}[/color]".format(i[0].replace("+", " "), lastDeath['level']), clients)
            playerlist[k][1] = lastDeath['date']['date']