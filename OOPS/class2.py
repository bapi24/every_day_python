class Song:
    
    def __init__(self, lyrics):
        self.lyrics= lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)
    

happy_bday = Song(["hola hola hola...chico chico chico", 'hey chinna, chinna chinna!!!'])

happy_bday.sing_me_a_song()