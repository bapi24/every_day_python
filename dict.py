players = {
    'kobe': 'lakers',
    'jordan': 'bulls',
    'magic': 'lakers',
    'irving': 'celtics'
}

cities = {
    'lakers': 'los angeles',
    'celtics': 'boston',
    'bulls': 'chicago'
}

#add more players
players['dirk'] = 'mavs'
players['curry'] = 'warriors'

#add more teams
cities['mavs'] = 'dallas'
cities['warriors'] = 'golden state'

#print player names
print("==" * 15)
for player in players.keys():
    print(player)

#print team names
print("==" * 15)
for team in players.values():
    print(team)

#print some players and their teams
print("=-"*15)
for player, team in players.items():
    print(f"{player} plays for {team}!!")

#test print
print(list(players.items()))