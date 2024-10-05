import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://yoyogesh27:LH44isthegoat@cluster0.umivw3g.mongodb.net/?retryWrites=true&w=majority')

logindb = cluster["login"]
coachesteamsdb = cluster["coachesteams"]
playerteamsdb = cluster["playerteams"]

coaches = logindb["coaches"]
players = logindb["players"]


def addcoach(name, username, email, password, school):
    coaches.insert_one({"name": name, "username":username, "email": email, 'password': password, 'school': school})

def addplayer(name, username, email, password, school):
    players.insert_one({"name": name, "username":username, "email": email, 'password': password, 'school': school})

def createTeam(CoachUsername, teamID, team_name):
    CoachUsername = coachesteamsdb[str(CoachUsername)]
    post={'_id': teamID, 'team_name':team_name, 'players': []}
    CoachUsername.insert_one(post)

    

def checkPlayerUserExists(username, email):
    temp = []
   
    result_username = players.find({'username': username})
    result_email = players.find({'email': email})
    for i in result_username:
        temp.append(i)
  

    if temp != []:
        return 'Username'
    else:
        return''
    
def checkCoachUserExists(username, email):
    temp = []
    
    result_username = coaches.find({'username': username})
    result_email = coaches.find({'email': email})
    for i in result_username:
        temp.append(i)
    
    print(temp)
    if temp != []:
        return 'Username'
    
    else:
        return''
    
def playerLogin(username, password):
    result = players.find_one({'username': username})
    print(result)
    if password == result['password']:
        return True
    else:
        return False
    
def coachLogin(username, password):
    result = coaches.find_one({'username': username})

    if password == result['password']:
        return True
    else:
        return False   
    
def addPlayerToTeam(team_id, coach_name, username):
    collect = coachesteamsdb[str(coach_name)]
    result = collect.find_one({'_id': team_id})
    print(result)
    arr = result['players']
    team_name = result['team_name']
    arr.append(username)
    PlayerUsername = playerteamsdb[str(username)]
    post={'_id': team_id, 'team_name': team_name, 'coach_name': coach_name}
    PlayerUsername.insert_one(post)
    collect.update_one({"_id":str(team_id)},{"$set":{"players":arr}})

def getCoachTeams(coach_name):
    collect = coachesteamsdb[str(coach_name)]
    result = collect.find()
    
    
    return result

def getPlayerTeams(player_name):
    collect = playerteamsdb[str(player_name)]
    result = collect.find()
    
    
    return result

def getTeamPlayers(coach_name, team_name):
    
    collect = coachesteamsdb[str(coach_name)]
    result = collect.find({'team_name': team_name})
    for i in result:
        players = i['players']
    return players


    

    
#def deleteplayer(name):



