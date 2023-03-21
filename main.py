import flask
import requests
import json
import sqlite3
import time
import discord

f = open('settings.json')
SETTINGS = json.load(f)
app = flask.Flask(__name__)
DISCORD_ENDPOINT = 'https://discord.com/api/v10/'


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
        #get the exchange data and set it as cookies
        clientdata = r.json()
        accesstoken = clientdata['access_token']

        r = requests.get(f"{DISCORD_ENDPOINT}users/@me", headers={'Authorization': f'Bearer {accesstoken}'})
        #get user data aswell and set it as cookies
        userdata = r.json()
        expiration = time.time() + int(clientdata['expires_in'])
        avatar = f'https://cdn.discordapp.com/avatars/{userdata["id"]}/{userdata["avatar"]}.png?size=512'
        response = flask.make_response(flask.redirect('/')) 
        response.set_cookie('access_token', accesstoken, expires=expiration)
        response.set_cookie('refresh_token', clientdata['refresh_token'] )
        response.set_cookie("avatar", avatar)
        response.set_cookie("username", f'{userdata["username"]}#{userdata["discriminator"]}')
        return response
    #check if a cookie is set
    token = flask.request.cookies.get('access_token')
    
    if token:
        
        return flask.render_template('base.html', user=flask.request.cookies.get('username'), avatar=flask.request.cookies.get('avatar'))
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


def abbreviate(string:str):
    abbreviation = ''
    for i, letter in enumerate(string):
        if i == 0:
            abbreviation = letter
        if letter == ' ':
            abbreviation = f'{abbreviation}{string[i+1]}'
    return abbreviation
        


@app.route('/dashboard', methods=['GET', 'POST'])
def serverpage():
    #check if logged in
    token = flask.request.cookies.get('access_token')
    if token:
        #get a list of all the servers the user is in
        r = requests.get(f'{DISCORD_ENDPOINT}users/@me/guilds', headers={'Authorization': f'Bearer {token}'})
        data = r.json()
        servers = []
        for server in data:
            perms = discord.Permissions(int(server['permissions']))
            if perms.manage_guild:
                if server['icon'] != None:
                    icon = f"https://cdn.discordapp.com/icons/{server['id']}/{server['icon']}.png"
                    serverobj = {'name': server['name'], 'icon':icon, 'id':server['id']}
                else:
                    alt = abbreviate(server['name'])
                    serverobj = {'name': server['name'], 'icon':None, 'id':server['id'], 'altname':alt}
                
                servers.append(serverobj)
            
        return flask.render_template('serverpage.html', user=flask.request.cookies.get('username'), avatar=flask.request.cookies.get('avatar'), servers=servers)
    else:
        return flask.redirect('/login')
    
@app.route('/dashboard/<serverid>', methods=['GET', 'POST'])
def dashboard(serverid):
    if flask.request.method == 'GET':
        token = flask.request.cookies.get('access_token')
        if not token:
            return flask.redirect('/login')
        #this is where we would load server information
        #check if the bot is in the server, if not, invite it
        r = requests.get(f'{DISCORD_ENDPOINT}guilds/{serverid}', headers={'Authorization': f'Bot {SETTINGS["TOKEN"]}'})
        if r.status_code == 404:
            return flask.redirect('https://discord.com/api/oauth2/authorize?client_id=817049551843229736&permissions=8&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fdashboard&response_type=code&scope=bot%20identify%20applications.commands')
        if r.status_code == 200:
            r = requests.get(f'{DISCORD_ENDPOINT}guilds/{serverid}/channels', headers={'Authorization': f'Bot {SETTINGS["TOKEN"]}'})
            channelobjs = r.json()
            return flask.render_template('dashboard.html', user=flask.request.cookies.get('username'), avatar=flask.request.cookies.get('avatar'),channels=channelobjs)
    elif flask.request.method == 'POST':
        #save the users data here
        #I havent done this yet obviouisly
        print(flask.request.json)
        r = requests.get(f'{DISCORD_ENDPOINT}guilds/{serverid}/channels', headers={'Authorization': f'Bot {SETTINGS["TOKEN"]}'})
        channelobjs = r.json()
        return flask.render_template('dashboard.html', user=flask.request.cookies.get('username'), avatar=flask.request.cookies.get('avatar'),channels=channelobjs)

app.run()



