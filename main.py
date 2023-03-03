import flask
import requests
import json
import sqlite3
f = open('settings.json')
SETTINGS = json.load(f)
app = flask.Flask(__name__)
DISCORD_ENDPOINT = 'https://discord.com/api/v10/'

print(SETTINGS['CLIENTID'])
print(SETTINGS['CLIENTSECRET'])

@app.route('/')
def index():
    user = None
    #do discord exchange and get user information
    if flask.request.args:
        code = flask.request.args['code']
        
        data = {
            'client_id': int(SETTINGS['CLIENTID']),
            'client_secret': SETTINGS['CLIENTSECRET'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://127.0.0.1:5000/'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(f'{DISCORD_ENDPOINT}oauth2/token', data=data, headers=headers)
        clientdata = r.json()
        
        accesstoken = clientdata['access_token']

        r = requests.get(f"{DISCORD_ENDPOINT}users/@me", headers={'Authorization': f'Bearer {accesstoken}'})
        userdata = r.json()
        icondata = userdata['avatar']
        userid = userdata['id']
        avatar = f'https://cdn.discordapp.com/avatars/{userid}/{icondata}.png?size=512'
        response = flask.make_response(flask.redirect('/')) 
        response.set_cookie('access_token', accesstoken)
        return response
    #check if a cookie is set
    token = flask.request.cookies.get('access_token')
    
    if token:
        r = requests.get(f"{DISCORD_ENDPOINT}users/@me", headers={'Authorization': f'Bearer {token}'})
        userdata = r.json()
        icondata = userdata['avatar']
        userid = userdata['id']
        avatar = f'https://cdn.discordapp.com/avatars/{userid}/{icondata}.png?size=512'
        user = userdata['username']
        return flask.render_template('base.html', user=user, avatar=avatar, discriminator=userdata['discriminator'])
    print(user)
    return flask.render_template('base.html', user=user)
        
    

@app.route('/login')
def login():
    return flask.redirect('https://discord.com/api/oauth2/authorize?client_id=817049551843229736&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2F&response_type=code&scope=identify%20guilds%20email%20guilds.join')

@app.route('/logout')
def logout():
    token = flask.request.cookies.get('access_token')
    if token:
        response = flask.make_response(flask.redirect('/'))
        response.set_cookie('access_token', '', expires=0)
        return response
    return flask.redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    #check if logged in
    #im going to redo the cookies, where I set the username, avatar, refresh token, and regular token all in cookies, so I dont have to make stupid request
    user = None
    if user:
        return flask.render_template('dashboard.html')
    else:
        return flask.redirect('/login')
    


app.run()