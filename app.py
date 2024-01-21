from flask import *
import random

app = Flask(__name__)

games = [
    {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""},
    {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""},
    {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""},
    {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""},
    {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""}
]

deck = [i + '_' + j for i in ["red", "blue", "yellow", "green"] for j in ([str(k) for k in range(10)]*2 + ["swap", "skip", "plus two"])]*2 + ["plus four", "wild"]*4

def redirect(url='../../../'):
    return "<meta http-equiv=\"refresh\" content=\"0; URL=" + url + "\" />"

@app.route("/")
def game_choice():																															
    return "<div style=\"font-family: Arial\"><label for=\"gamenum\">Join: </label><select id=\"gamenum\"><option value=\"1\">Game 1</option><option value=\"2\">Game 2</option><option value=\"3\">Game 3</option><option value=\"4\">Game 4</option><option value=\"5\">Game 5</option></select><br /><label for=\"username\">Username: </label><input id=\"username\" type=\"username\"><button onclick=\"submit()\">Submit</button></div><script>function submit() { var j = document.getElementById('gamenum').value; var k = document.getElementById('username').value; if (k === '' || k === ' ') { return 0; }; window.location.replace('/choose_game/' + j + '/' + k); }</script>"

@app.route("/choose_game/<gamenum>/<username>")
def set_game(gamenum, username):
    global games
    if username in games[int(gamenum)]["players"]:
        return redirect()
    else: 
        games[int(gamenum)-1]["players"].append(username)
        print("[INFO]: Player '" + username + "' connected to Game #" + gamenum + '.')
        print("[DEBUG]: Game #" + gamenum + ": " + str(games[int(gamenum)-1]))
        return redirect('../../../play_game/' + gamenum + '/' + username)

def get_card_color(card):
    if 'blue' in card:
        return 'blue'
    elif 'green' in card:
        return 'green'
    elif 'yellow' in card:
        return 'yellow'
    elif 'red' in card:
        return 'red'
    elif ('wild' in card) or ('plus four' in card):
        return 'black'

game_over = [None, 0, 0, 0, 0]

@app.route("/play_game/<gamenum>/<username>")
def play_game(gamenum, username):
    if (games[int(gamenum)-1]["confirmations"] == games[int(gamenum)-1]["players"]) and len(games[int(gamenum)-1]["players"]) > 1:
        if not username in games[int(gamenum)-1]["data"]:
            games[int(gamenum)-1]["data"][username] = [random.choice(deck) for _ in range(7)]
        games[int(gamenum)-1]["started"] = True
        if games[int(gamenum)-1]["turn"] == "":
            games[int(gamenum)-1]["turn"] = random.choice(games[int(gamenum)-1]["players"])
        if games[int(gamenum)-1]["curcard"] == "":
            games[int(gamenum)-1]["curcard"] = random.choice(deck)
            while ("plus two" in games[int(gamenum)-1]["curcard"]) or ("plus four" in games[int(gamenum)-1]["curcard"]) or ("wild" in games[int(gamenum)-1]["curcard"]) or ("swap" in games[int(gamenum)-1]["curcard"]) or ("skip" in games[int(gamenum)-1]["curcard"]):
                games[int(gamenum)-1]["curcard"] = random.choice(deck)
        print("[DEBUG]: '" + username + "' cards: " + str(games[int(gamenum)-1]["data"][username]))
        if game_over[int(gamenum)] == 1:
            games[int(gamenum)-1] = {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""}
            game_over[int(gamenum)] = 0
            return "<h1>You lost.</h1><br /><button onclick=\"home()\">Play Again</button><script>function home() { window.location.replace('/'); }</script>"
        return f"<meta http-equiv=\"refresh\" content=\"3; URL=../../../play_game/{gamenum}/{username}\" />" + """<div style=\"font-family: Arial\"><button onclick="window.location.replace('/')">Return to Home Page</button><button onclick="window.location.replace('/play_card/{}/{}/pass')">Draw Card and Skip Turn</button><br /><p style="font-size: 13px">Turn: {}</p><p>{}</p>""".format(username, gamenum, games[int(gamenum)-1]["turn"], games[int(gamenum)-1]["curcard"].replace('_', ' ').title()) + ''.join([f"<button style=\"padding: 5px 3px 5px 3px; background-color: " + {'red': '#d60000', 'green': '#00c20d', 'blue': '#005eff', 'yellow': '#ffee00', 'black': '#000000'}[get_card_color(card)] + f"; color: " + {'red': '#FFFFFF', 'green': '#FFFFFF', 'blue': '#FFFFFF', 'yellow': '#000000', 'black': '#FFFFFF'}[get_card_color(card)] + f"\" onclick=\"window.location.replace('/play_card/{username}/{gamenum}/{card}')\">{card.replace('_', ' ').title()}</button>" for card in games[int(gamenum)-1]["data"][username]]) + '</div>'
    return f"<meta http-equiv=\"refresh\" content=\"3; URL=../../../play_game/{gamenum}/{username}\" />" + f"""<div style="font-family: Arial"><button onclick="window.location.replace('/')">Return to Home Page</button><br /><button onclick="window.location.replace('/confirm_game/{gamenum}/{username}')">Confirm Game</button></div>"""

@app.route("/confirm_game/<gamenum>/<username>")
def confirm_game(gamenum, username):
    if not username in games[int(gamenum)-1]["confirmations"]:
        games[int(gamenum)-1]["confirmations"].append(username)
    print("[DEBUG]: " + str(games[int(gamenum)-1]))
    return redirect(f"/play_game/{gamenum}/{username}")

# @app.route("/delete_user/<username>/<gamenum>")
# def delete_user(username, gamenum):
#     if input(f"Delete '{username}' from game #{gamenum}? (y/N): ").lower() == "y":
#         games[int(gamenum)-1]["data"].remove(username)
#         games[int(gamenum)-1]["players"].remove(username)
#         games[int(gamenum)-1]["confirmations"].remove(username)
#     return redirect()



@app.route("/play_card/<username>/<gamenum>/<card>")
def play_card(username, gamenum, card):
    if games[int(gamenum)-1]["turn"] != username:
        return redirect(f'../../../../play_game/{gamenum}/{username}')
    if card == "pass":
        games[int(gamenum)-1]["data"][username].append(random.choice(deck))
        games[int(gamenum)-1]["turn"] = games[int(gamenum)-1]["players"][[1,0][games[int(gamenum)-1]["players"].index(username)]]
        return redirect(f'../../../../play_game/{gamenum}/{username}')
    if card in games[int(gamenum)-1]["data"][username]:
        curcard = games[int(gamenum)-1]["curcard"].split("_")
        cardlist = card.split("_")
        if len(cardlist) == 1:
            cardlist.append('')
        if len(curcard) == 1:
            curcard.append('')
        if ([card] == games[int(gamenum)-1]["data"][username]) and ((curcard[0] == cardlist[0]) or (curcard[1] == cardlist[1])): #if the card being played is the last card in the player's hand
            games[int(gamenum)-1]["data"][username].remove(card)
            game_over[int(gamenum)] = 1
            games[int(gamenum)-1] = {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""}
            return "<h1>You've won!</h1><br /><button onclick=\"home()\">Play Again</button><script>function home() { window.location.replace('/'); }</script>"
        elif card == "plus four":
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["data"][games[int(gamenum)-1]["players"][[1, 0][games[int(gamenum)-1]["players"].index(username)]]] += [random.choice(deck) for _ in range(4)]
            if (games[int(gamenum)-1]["curcard"] == "plus four") and (games[int(gamenum)-1]["curcard"] in games[int(gamenum)-1]["data"][username]):
                return """<label for="colorchoose">Choose Color: </label><select id="colorchoose"><option value="blue">Blue</option><option value="red">Red</option><option value="yellow">Yellow</option><option value="green">Green</option></select><button type="button" onclick="submit()">Submit</button><script>function submit() { window.location.replace('../../../../color_choose/""" + gamenum + '/' + username + """/' + document.getElementById("colorchoose").value + '/""" + card + """'); }</script>"""
        elif ((cardlist[1] == 'plus two') and (curcard[1] == 'plus two')) or ((cardlist[1] == 'plus two') and (curcard[0] == cardlist[0])):
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["data"][username].remove(card)
            games[int(gamenum)-1]["data"][games[int(gamenum)-1]["players"][[1, 0][games[int(gamenum)-1]["players"].index(username)]]] += [random.choice(deck) for _ in range(2)]
            games[int(gamenum)-1]["turn"] = games[int(gamenum)-1]["players"][[1, 0][games[int(gamenum)-1]["players"].index(username)]]
        elif card == "wild":
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["turn"] = games[int(gamenum)-1]["players"][[1, 0][games[int(gamenum)-1]["players"].index(username)]]
            if (games[int(gamenum)-1]["curcard"] == "wild") and (games[int(gamenum)-1]["curcard"] in games[int(gamenum)-1]["data"][username]):
                return """<label for="colorchoose">Choose Color: </label><select id="colorchoose"><option value="blue">Blue</option><option value="red">Red</option><option value="yellow">Yellow</option><option value="green">Green</option></select><button type="button" onclick="submit()">Submit</button><script>function submit() { window.location.replace('../../../../color_choose/""" + gamenum + '/' + username + """/' + document.getElementById("colorchoose").value + '/""" + card + """'); }</script>"""
        elif ((cardlist[1] == 'skip') and (curcard[1] == 'skip')) or ((cardlist[1] == 'skip') and (curcard[0] == cardlist[0])):
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["data"][username].remove(card)
        elif ((cardlist[1] == 'swap') and (curcard[1] == 'swap')) or ((cardlist[1] == 'swap') and (curcard[0] == cardlist[0])):
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["data"][username].remove(card)
        elif (cardlist[0] == curcard[0]) or (cardlist[1] == curcard[1]):
            games[int(gamenum)-1]["curcard"] = card
            games[int(gamenum)-1]["data"][username].remove(card)
            games[int(gamenum)-1]["turn"] = games[int(gamenum)-1]["players"][[1, 0][games[int(gamenum)-1]["players"].index(username)]]
    return redirect(f'../../../../play_game/{gamenum}/{username}')

@app.route("/reset_players/<gamenum>")
def reset_players(gamenum):
    games[int(gamenum)-1] = {"players": [], "started": False, "confirmations": [], "data": {}, "curcard": "", "turn": ""}
    game_over[int(gamenum)] = 0
    return redirect("../../")

@app.route('/color_choose/<gamenum>/<username>/<color>/<card>')
def choose_color(gamenum, username, color, card):
    if card in games[int(gamenum)-1]["data"][username]:
        games[int(gamenum)-1]["curcard"] = color
        games[int(gamenum)-1]["data"][username].remove(card)
    return redirect(f"../../../../../play_game/{gamenum}/{username}")
