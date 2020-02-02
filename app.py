from flask import Flask, render_template, request, redirect, url_for, jsonify
from gra import *

app: Flask = Flask(__name__)

game = 0
current_player = 0
winner = 0


@app.route('/')
def index():
    global game
    global current_player
    game = SkipBo(2)
    current_player = 1
    change_player()
    return render_template('index.html')


@app.route('/zasady')
def zasady():
    return render_template('zasady.html')


@app.route('/game_over')
def game_over():
    return render_template('game_over.html', winner=winner)


@app.route('/game_view', methods=["GET", "POST"])
def game_view():
    global game
    global current_player
    cards_in_hand = [0, 0, 0, 0, 0]
    if not game.players_stack[current_player]:
        game.players_stack[current_player] = []
        players_stack = 0;
    else:
        players_stack = game.players_stack[current_player][-1]
    len_players_stack = len(game.players_stack[current_player])
    cards_in_gs = [0, 0, 0, 0]
    cards_in_discard = [0, 0, 0, 0]

    for i in range(0, 4):
        if game.discard_pile[current_player][i]:
            cards_in_discard[i] = game.discard_pile[current_player][i][-1]
        if game.game_stacks[i]:
            cards_in_gs[i] = game.game_stacks[i][-1]

    for i in range(0, len(game.players_hand[current_player])):
        cards_in_hand[i] = game.players_hand[current_player][i]

    print()
    return render_template('game_view.html', cards_in_hand=cards_in_hand,
                           cards_in_gs=cards_in_gs, players_stack=players_stack, cards_in_discard=cards_in_discard,
                           len_players_stack=len_players_stack, current_player=current_player)


@app.route('/move', methods=["POST"])
def move():
    # Obsluga post - sprawdzamy co sie stało
    # zmieniamy stan gry w obiekcie game tak aby odzwiercidlic zmiane zadana przez uzytkownika albo jego kolegow
    # jak juz zmienimy stan gry to po prostu robimy redirect do game_view
    global game
    global current_player
    global winner
    card = request.form.getlist("card")[0]
    target = request.form.getlist("target")[0]

    if target[0:2] == 'gs':
        place = Place.STACK
        place_id = int(target[-1])
    else:
        place = Place.DISCARD
        place_id = int(target[-1])

    # move_from_hand: stack or discard
    if card[0:4] == 'hand':
        card_index = int(card[-1])
        ret = game.move_from_hand(place, game.players_hand[current_player][card_index], place_id, current_player)

    # move_from_players_stack
    if card == 'ps':
        ret = game.move_from_players(game.players_stack[current_player][-1], place_id, current_player)
        # is this the end?
        if len(game.players_stack[current_player]) == 0:
            winner = current_player
            return jsonify(dict(redirect=url_for('game_over')))

    # move_from_discard
    if card[0:11] == 'discardcard':
        card_index = int(card[-1])
        discard_pile_id = int(card[-1])
        ret = game.move_from_discard(game.discard_pile[current_player][card_index][-1], place_id, discard_pile_id,
                                     current_player)

    # This sounds fancy but it's just a redirect
    return jsonify(dict(redirect=url_for('game_view')))


@app.route('/changeplayer', methods=["POST"])
def change_player():
    global game
    global current_player
    if current_player == 0:
        current_player = 1
    else:
        current_player = 0
    game.fill_hand(current_player)

    return game_view()


if __name__ == '__main__':
    app.run(debug=True)
