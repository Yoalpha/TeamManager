import pymongo
from pymongo import MongoClient

MONGO = open('mongoURL.txt', 'r')
MONGO_URL = MONGO.readline()
MONGO.close()

cluster = MongoClient(MONGO_URL)

logindb = cluster["login"]
coachesteamsdb = cluster["coachesteams"]
playerteamsdb = cluster["playerteams"]
coachestournamentdb = cluster["coachestournament"]

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

def createTournament(CoachUsername, tournamentID, tournament_name):
    CoachUsername = coachestournamentdb[str(CoachUsername)]
    post={'_id': tournamentID, 'tournament_name':tournament_name, 'teams': [str(CoachUsername)]}
    CoachUsername.insert_one(post)
    

def checkPlayerUserExists(username, email):
    temp = []
    temp2 = []
   
    result_username = players.find({'username': username})
    result_email = players.find({'email': email})
    for i in result_username:
        temp.append(i)
    for j in result_email:
        temp2.append(j)

    if temp != []:
        return 'Username'
    elif temp2 != []:
        return 'E-Mail'
    else:
        return''
    
def checkCoachUserExists(username, email):
    temp = []
    temp2 = []
    
    result_username = coaches.find({'username': username})
    result_email = coaches.find({'email': email})
    for i in result_username:
        temp.append(i)
    for j in result_email:
        temp2.append(j)
    
    print(temp)
    if temp != []:
        return 'Username'
    elif temp2 != []:
        return 'E-Mail'
    else:
        return''
    
def playerLogin(username, password):
    result = players.find_one({'username': username})
    print(result)
    if result == None:
        return
    elif password == result['password']:
        return True
    else:
        return False
    
def coachLogin(username, password):
    result = coaches.find_one({'username': username})

    if result == None:
        return
    elif password == result['password']:
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

def addTeamToTournament(tournament_id, coach_name, username):
    collect = coachestournamentdb[str(coach_name)]
    result = collect.find_one({'_id': tournament_id})
    print(result)
    arr = result['teams']
    tournament_name = result['tournament_name']
    arr.append(username)
    CoachUsername = coachesteamsdb[str(username)]
    post={'_id': tournament_id, 'tournament_name': tournament_name, 'coach_name': coach_name}
    CoachUsername.insert_one(post)
    collect.update_one({"_id":str(tournament_id)},{"$set":{"teams":arr}})

def getCoachTeams(coach_name):
    collect = coachesteamsdb[str(coach_name)]
    result = collect.find()
    
    
    return result

def getCoachTournament(coach_name):
    collect = coachestournamentdb[str(coach_name)]
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


def deleteTeam(coach_name, team_id):
    # getting the collection of the coach name from the coaches teams database
    collection = coachesteamsdb[str(coach_name)]
    query = {"_id": team_id}
    collection.delete_one(query)
    # names of the collections
    names = playerteamsdb.list_collection_names()
    # looping throught the players in the db
    for i in names:
        # defining the collection of one player
        collection2 = playerteamsdb[i]
        query2 = {"_id": team_id}
        # deleting the team for every player with that name thats why the loop
        collection2.delete_one(query2)

# def test(coach_name, team_id):


def deleteplayer(team_id, player_name, coach_name):
    collect = coachesteamsdb[str(coach_name)]
    result = collect.find_one({'_id': team_id})
    arr = result['players']
    arr.remove(player_name)
    collect.update_one({"_id":str(team_id)},{"$set":{"players":arr}})
    collect2 = playerteamsdb[player_name]
    query2 = {"_id": team_id}
    collect2.delete_one(query2)





