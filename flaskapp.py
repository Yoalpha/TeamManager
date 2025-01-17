from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import join_room, leave_room, send, SocketIO
import mongomanager
import pymongo
from pymongo import MongoClient
import randomCode
import random
from string import ascii_uppercase

app = Flask(__name__)

SECRET = open("secretKey.txt", "r")
SECRET_KEY = SECRET.readline()
SECRET.close()
MONGO = open('mongoURL.txt', 'r')
MONGO_URL = MONGO.readline()
MONGO.close()

app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY
cluster = MongoClient(MONGO_URL)



socketio = SocketIO(app)
global rooms 
rooms = {}


@app.route("/", methods =["GET", "POST"])
def main():

    return render_template("home.html")



@app.route("/player_register", methods =["GET", "POST"])
def player_register():
    error = ''
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        school = request.form.get("school")
        role = request.form.get("role")
        print(role)
        
        print(mongomanager.checkPlayerUserExists(username, email))
        out = mongomanager.checkPlayerUserExists(username, email)
        if password == confirm_password and role == 'player' and out == '':
            mongomanager.addplayer(name, username , email, password,school)
            return redirect(url_for('player_login'))
        else:
            error = str(out)+' in use'
            
    return render_template('player_register.html', error = error)

@app.route("/coach_register", methods =["GET", "POST"])
def coach_register():
    error = ''
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        school = request.form.get("school")
        role = request.form.get("role")
        print(role)
        
        out = mongomanager.checkPlayerUserExists(username, email)
        print(out)
        if password == confirm_password and role == 'coach'and out == '':
            mongomanager.addcoach(name, username, email, password, school)
            return redirect(url_for('coach_login'))
        else:
            error = str(out)+' in use'
    return render_template('coach_register.html', error = error)


@app.route("/player_login", methods =['GET', 'POST'])
def player_login():
    error = None
    if request.method == 'POST':
        verify = ''
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get('role')

        verify = mongomanager.playerLogin(username, password)


        if verify and role == 'student':
            session['role'] = role
            session["username"] = username
            return redirect(url_for('player_client'))
        
        else:
            error = 'INCORRECT LOGIN DETAILS'
            return render_template('player_login.html', error = error)
        
    return render_template('player_login.html', error = error)
        
@app.route("/coach_login", methods =['GET', 'POST'])
def coach_login():
    error = None
    if request.method == 'POST':
        verify = ''
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get('role')
        
        verify = mongomanager.coachLogin(username, password)
    

        if verify and role == 'coach':
            session['role'] = role
            session["username"] = username
            return redirect(url_for('coach_client'))
        
        else:
            error = 'INCORRECT LOGIN DETAILS'
            return render_template('coach_login.html', error=error)
            

    return render_template('coach_login.html', error=error)

@app.route('/coach_client', methods =["GET", "POST"])
def coach_client():
    if 'username' in session and session['role'] == 'coach':

        result = mongomanager.getCoachTeams(session['username'])
        arr = {}
        result2 = mongomanager.getCoachTournament(session['username'])
        arr2 = {}
    
        for i in result:
            arr[i['team_name']] = i['_id']
        print(arr)  

        for i in result2:
            arr2[i['tournament_name']] = i['_id']
        print(arr)  

        return render_template('coach_client.html', username = session['username'], result = arr, resulttournament = arr2)
    elif 'username' in session and session['role'] == 'student':
        return redirect(url_for('player_client'))
    else:
        return redirect(url_for('coach_login'))
    

@app.route('/player_client', methods =["GET", "POST"])
def player_client():
    if 'username' in session and session['role'] == 'student':

        result = mongomanager.getPlayerTeams(session['username'])
        arr = {}
    
        for i in result:
            arr[i['team_name']] = i['_id']
        print(arr) 

        if request.method == 'POST':
            team_id = request.form.get('team-id')
            coach_name = request.form.get('coach-name')
            print(team_id, coach_name)
            mongomanager.addPlayerToTeam(team_id, coach_name, session['username'])
            



        return render_template('player_client.html', username = session['username'], result = arr)
            
    else:
        return redirect(url_for('player_login'))

@app.route('/create_team', methods =["GET", "POST"])
def create_team():
    if 'username' in session and session['role'] == 'coach':
        if request.method == 'POST':
            team_name = request.form.get('team-name')
            groupcode = randomCode.get_random_string(6)
            mongomanager.createTeam(session['username'], groupcode, team_name)
            rooms[groupcode] = {"members": 1 ,"messages": []}
            return render_template('group.html', groupCode = groupcode, username = session.get('username'))
        return render_template('group.html', username = session.get('username'))
    else:
        return redirect('coach_login')
    
@app.route('/create_tournament', methods = ['GET', 'POST'])
def create_tournament():
    if 'username' in session and session['role'] == 'coach':
        if request.method == 'POST':
            tournament_name = request.form.get('tournament-name')
            tournamentcode = randomCode.get_random_string(6)
            mongomanager.createTournament(session['username'], tournamentcode, tournament_name)
            
            
            return render_template('tornament_create.html', tournamentCode = tournamentcode, username = session.get('username'))
        return render_template('tornament_create.html', username = session.get('username'))
    else:
        return redirect(url_for('coach_login'))


    
@app.route('/team/<team_name>', methods =["GET", "POST"])
def team(team_name):
    if 'username' in session and session['role'] == 'coach':
        
        result = mongomanager.getCoachTeams(session['username'])
        arr = {}
    
        for i in result:
            arr[i['team_name']] = i['_id']

        players = mongomanager.getTeamPlayers(session['username'], team_name)





        #chat room
        team_code = arr[team_name]
        room = str(team_code)
        if room not in rooms:
            rooms[room] = {"members": 1 ,"messages": []}
        session['room'] = room
        
        print('rooms', rooms)





        return render_template('team.html', team_name = team_name, team_code = team_code, players = players, messages = rooms[room]["messages"])
    
    elif 'username' in session and session['role'] == 'student':

        result = mongomanager.getPlayerTeams(session['username'])
        arr = {}
    
        for i in result:
            arr[i['team_name']] = i['_id']
            arr['coachname'] = i['coach_name']
        print('student arr', arr) 
        players = mongomanager.getTeamPlayers(arr['coachname'], team_name)


        #chat room
        team_code = arr[team_name]
        room = str(team_code)
        if room not in rooms:
            rooms[room] = {"members": 1 ,"messages": []}
        session['room'] = room

        print(rooms[room]["messages"])
        return render_template('team.html', team_code = arr[team_name], team_name = team_name, players = players,  messages = rooms[room]["messages"])

    else:
        return redirect('coach_login')


@socketio.on("message")
def message(data):
    print('hahah', session.get('room'))
    room = session.get('room')
    if room not in rooms:
        return
    content  = {
        
        "name": session.get('username'),
        "message": data['data']
    }
    send(content, to=room)
    rooms[room]['messages'].append(content)
    print(rooms[room]['messages'])

@socketio.on('connect')   
def connect():
    room = session['room']
    name = session['username']
    if not room or not name: 
        return
    if room not in rooms:
        return
    
    join_room(room)
    
    print(rooms)
    rooms[room]['members']+=1
    print(name, room)

@socketio.on("disconnect")
def disconnect():
    room = session['room']
    name = session['username']
    #leave_room(room)


@app.route('/delete/<team_code>')
def delete(team_code):
    coach_name = session.get('username')
    mongomanager.deleteTeam(coach_name,team_code)
    return redirect(url_for('coach_client'))

@app.route('/tournament/<tournament_name>')
def tournament(tournament_name):
    if 'username' in session and session['role'] == 'coach': 
        return render_template('Tournament-Home.html', tournament_name = tournament_name)
        return redirect(url_for(coach_login))





@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('player_login'))



if __name__ == "__main__":
    app.run(debug=True)

