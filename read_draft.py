import sqlite3

with open('./data/draft_results2024.txt', 'r') as draft_results:
	draft_data = draft_results.read()

with open('./data/player_prices2023.txt', 'r') as draft_results2023:
    draft_data2023 = draft_results2023.read()

def read_draft(draft_data):
    players = []

    for line in draft_data.split('\n'):
        player = []
        name = ''
        first_tab = False
        # get the player names from the draft data
        for item in line:
            if item == '\t':
                first_tab = True
            elif first_tab:
                if item == '(':
                    name = name[:-1]
                    break
                name += item

        # get the players drafted team from the draft data
        team = ''
        ct = 0
        second_tab = False
        for item in line:
            if item == '\t':
                ct+=1
            elif ct == 2:
                second_tab = True
            elif second_tab:
                if item == '\n':
                    break
                team += item

        # get the players value from the draft data
        price = ''
        dollar_sign = False
        for item in line:
            if item == '$':
                dollar_sign = True
            elif dollar_sign:
                if item == '\t':
                    break
                price += item

        player.append(name)
        player.append(team)
        player.append(price)
        players.append(player)
    return players

def add_to_database(players):
    connection = sqlite3.connect("player_base.db")
    cursor = connection.cursor()

    for player in players:
        if player.__len__() == 4:
            cursor.execute('''
            INSERT INTO players (name, price_2023, price_2024, team)
            VALUES (?, ?, ?, ?)
            ''', (player[0], player[3], player[2], player[1]))
        else: 
            cursor.execute('''
            INSERT INTO players (name, price_2024, team)
            VALUES (?, ?, ?)
            ''', (player[0], player[2], player[1]))

    connection.commit()
    connection.close()

def get_2023_price(draft_data2023, players):
    line_ct = 0
    for line in draft_data2023.split('\n'):
        line_ct += 1
        name = ""
        price = ""
        if line_ct % 2 == 1:
            for item in line:
                if item == '\t':
                    break
                name += item
            for item in line:
                if item.isdigit() or item == '-':
                    if item == '-':
                        price = '1'
                    else:
                        price += item
        for player in players:
            if player[0] == name:
                player.append(price)
                break
        

    
players = read_draft(draft_data)
get_2023_price(draft_data2023, players)
add_to_database(players)