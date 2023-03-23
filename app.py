from flask import Flask, render_template, request, redirect, url_for, session
from database import database as db
import json
from passlib.hash import sha256_crypt
import openrouteservice as ors
import requests
import folium
import random
import string

apiKey = '5b3ce3597851110001cf6248d3e48705c5a74e9685b9a73396eff621'

app = Flask(__name__, static_url_path='/templates')

app.secret_key = "pA7EM7NC6RvlWIGY0fLO" #random string

@app.route("/")
def index():
    db.main()
    return render_template('index.html')

@app.route("/logout", methods=['get', 'post'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/forgot", methods=['get', 'post'])
def forgot():
    if 'username' in session:
        return redirect(url_for('getroute'))
    if request.method == 'POST':
        if 'resetEmail' in request.form:
            if db.emailExists(request.form['resetEmail']):
                sendResetCode(request.form['resetEmail'])
                return "success"
            else:
                return("<div class='alert alert-danger'>Email does not exist</div>")
    return render_template('forgot.html')


@app.route("/login", methods=['get', 'post'])
def login():
    if 'username' in session:
        return redirect(url_for('getroute'))
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            if db.authenticate(username, password):
                session['username'] = username
                return "success"
            else:
                return("<div class='alert alert-danger'>Login Unsuccessful</div>")
        return("<div class='alert alert-danger'>Please populate all fields</div>")
    return render_template('login.html')

@app.route("/register", methods=['get','post'])
def register():
    if 'username' in session:
        return redirect(url_for('getroute'))
    if request.method == 'POST':
        if request.form['username'] and request.form['password'] and request.form['email'] and request.form['firstName']:
            if(db.noUsernameExists(request.form['username'])):
                username = request.form['username']
                password = sha256_crypt.encrypt(request.form['password'])
                email = request.form['email']
                firstName = request.form['firstName']
                registrationData = (username, password, email, firstName)
                db.addUser(registrationData)
                return "success" 
            else:
                return("<div class='alert alert-danger'>Username already exists</div>") 
        else:
            return("<div class='alert alert-danger'>Please fill in all fields</div>") 
    else:
        return render_template('register.html')

@app.route("/profile", methods=['get','post'])
def profile():
    if ('username' in session and request.method == 'POST' and "changeusername" in request.form):
        if db.noUsernameExists(request.form['changeusername']):
            if (db.updateUsername(request.form['changeusername'], session['username'])):
                session['username'] = request.form['changeusername']
                return "success"
            else:
                return("<div class='alert alert-danger'>Username change failed</div>")
        else:
            return("<div class='alert alert-danger'>Username already exists!</div>")
        
    if 'username' in session and request.method == 'POST' and ("oldpassword" in request.form and "newpassword" in request.form):
        username = session['username']
        password = request.form['oldpassword']
        if db.authenticate(username, password):
            if (db.updatePassword(request.form['newpassword'], session['username'])):
                return "success"
            else:
                return "<div class='alert alert-danger'>Password change failed</div>"
        else:
            return "<div class='alert alert-danger'>Old password does not match saved password</div>"
    if 'username' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route("/savejourney", methods=['post'])
def savejourney():
    if db.newJourney(request.form['journeyName']):
        userId = db.getUserId(session['username'])
        checkBoxStatus = 0
        if (db.newAddress(request.form['start'], userId)):
            if 'startfavourite' in request.form and request.form['startfavourite']=="on":
                checkBoxStatus = 1
            coordinates = geocode(request.form['start'],request.form['postcode'])
            data = (request.form['start'],request.form['postcode'],request.form['startname'],coordinates[1],coordinates[0],checkBoxStatus,userId)
            checkBoxStatus = 0
            db.addAddress(data)

        if (db.newAddress(request.form['end'], userId)):
            if 'endfavourite' in request.form and request.form['endfavourite']=="on":
                checkBoxStatus = 1
            coordinates = geocode(request.form['end'],request.form['endpostcode'])
            data = (request.form['end'],request.form['endpostcode'],request.form['endname'],coordinates[1],coordinates[0],checkBoxStatus,userId)
            checkBoxStatus = 0
            db.addAddress(data)

        startId = db.getAddressId(request.form['start'], session['username'])
        endId = db.getAddressId(request.form['end'], session['username'])
        data = (startId,endId,request.form['journeyName'],0,0,userId)
        db.addJourney(data)

        return "success"
    else:
        return "notUniqueJourneyName"

@app.route("/journey", methods=['get', 'post'])
def journeyoption():
    if 'username' in session:
        if request.method == 'POST':
            return redirect(url_for('getroute'))
        journeylist = db.getJourneyNames(db.getUserId(session['username']))
        return render_template('journeyoption.html', journeylist=journeylist)
    else:
        return redirect(url_for('login'))

@app.route("/deletejourney", methods=['get', 'post'])
def deleteJourney():
    if 'journeyid' in request.form and request.method == 'POST':
        db.deleteJourney(request.form['journeyid'])
        return "success"
    return

@app.route("/getroute", methods=['get', 'post'])
def getroute():
    if 'username' in session:

        client = ors.Client(key=apiKey)
        begin = geocode("Wilmslow High School", "SK9 1LZ")
        m = folium.Map(location=list(reversed(begin)), zoom_start=16)

        addressautofill = db.getAddresses(session['username'])

        if request.method == 'POST':
            if 'loadjourney' in request.form:
                if request.form['loadjourney'] == 'yes':
                    coords = []
                    startCoord = request.form['start']
                    endCoord = request.form['end']
                    startSplit = startCoord.split(',')
                    endSplit = endCoord.split(',')

                    startSplit = [ float(i) for i in startSplit ]
                    endSplit = [ float(i) for i in endSplit ]

                    coords.append(startSplit)
                    coords.append(endSplit)
                    
                    m = folium.Map(location=list(reversed(coords[0])), zoom_start=16)
                    route = client.directions(coordinates=coords, profile='foot-walking', format='geojson')

                    folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']], color="blue").add_to(m)
                    folium.Marker(location=list(reversed(coords[0])), popup=request.form['startaddress']).add_to(m)
                    folium.Marker(location=list(reversed(coords[1])), popup=request.form['endaddress']).add_to(m)
                    m.save('templates/map.html')
                    
            else:
                if request.form['start'] and request.form['end'] and request.form['postcode'] and request.form['endpostcode']:
                    coords = []
                    coords.append(geocode(request.form['start'], request.form['postcode']))
                    coords.append(geocode(request.form['end'], request.form['endpostcode']))

                    m = folium.Map(location=list(reversed(coords[0])), zoom_start=16)
                    route = client.directions(coordinates=coords,profile='foot-walking',format='geojson')

                    folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']], color="blue").add_to(m)
                    folium.Marker(location=list(reversed(coords[0])), popup=request.form['start']).add_to(m)
                    folium.Marker(location=list(reversed(coords[1])), popup=request.form['end']).add_to(m)
                    m.save('templates/map.html')
                    return "success"  
                
        m.save('templates/map.html')
        return render_template('getroute.html', addressautofill=addressautofill)
    else:
        return redirect(url_for('login'))

@app.route("/showmap", methods=['get'])
def showmap():
    return render_template('map.html')

@app.route("/accessibility", methods=['get', 'post'])
def accessibility():
    return render_template('access.html')

def sendResetCode(email):
    newPassword = ( ''.join(random.choice(string.ascii_uppercase) for i in range(5)) ) 
    newPassword += str( ''.join(random.choice(string.digits) for i in range(3)) )
    print(newPassword) # this would be sent by email.
    username = db.getUsername(email)
    db.updatePassword(newPassword, username)

def geocode(address, postcode):
    headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            }
    call = requests.get('https://api.openrouteservice.org/geocode/search/structured?api_key='+apiKey+'&address='+address+'&postalcode='+postcode+'&country=UK', headers=headers)
    long = json.loads(call.text)
    lat = long["features"][0]["geometry"]["coordinates"][1]
    long = long["features"][0]["geometry"]["coordinates"][0]
    return [long, lat]

if __name__ == "__main__":
    app.run()