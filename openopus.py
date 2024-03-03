import requests
import random


# https://github.com/openopus-org/openopus_api/blob/master/USAGE.md
classical_url = "https://api.openopus.org"
piano_composers = ['Adams', 'Bach', 'Bartók', 'Beethoven', 'Berg', 'Borodin', 'Boulez', 'Brahms', 'Britten', 'Bruckner', 'Chopin', 'Copland', 'Couperin', 'Debussy', 'Dvořák', 'Elgar', 'Falla', 'Franck', 'Gershwin', 'Gesualdo', 'Ginastera', 'Glass', 'Grieg', 'Handel', 'Haydn', 'Ives', 'Janacek', 'Ligeti', 'Liszt', 'Lully', 'Lutoslawski', 'Martinů', 'Mendelssohn', 'Messiaen', 'Milhaud', 'Mozart', 'Mussorgsky', 'Nielsen', 'Pärt', 'Poulenc', 'Prokofiev', 'Puccini', 'Purcell', 'Rachmaninoff', 'Rameau', 'Ravel', 'Reich', 'Rimsky-Korsakov', 'Rossini', 'Saint-Saëns', 'Scarlatti', 'Schnittke', 'Schoenberg', 'Schubert', 'Schumann', 'Shostakovich', 'Sibelius', 'Smetana', 'Stravinsky', 'Tchaikovsky', 'Villa-Lobos', 'Vivaldi', 'Wagner', 'Webern']


class OpenOpus:
    def __init__(self):
        self.comp_id = ""
        self.epochs = ["All", "Renaissance", "Baroque", "Classical", "Early Romantic", "Romantic", "Late Romantic", "20th Century", "Post-War", "21st Century"]
        self.works = []
        self.composer = ""

        # find composer info by name
    def composer_by_name(self, name):
        first_letter = name[0].lower()
        response = requests.get(f"{classical_url}/composer/list/name/{first_letter}.json")
        response.raise_for_status()
        data = response.json()["composers"]
        for i in range(len(data)):
            if data[i]["name"] == name:
                self.composer = data[i]
            # UnboundLocalError when composer in lower case or not available
        return self.composer

# list of essential composers (77)
#     def composer_id(self, name):
#         response = requests.get(f"{classical_url}/composer/list/rec.json")
#         response.raise_for_status()
#         data = response.json()['composers']
#         composers = {data[n]['name']: data[n]['id'] for n in range(len(data))}
#         print(composers)
#         self.comp_id = composers[name]
#         return self.comp_id

# list works by composer
    def list_keyboard_works(self, comp_id):
        response = requests.get(f"{classical_url}/work/list/composer/{comp_id}/Keyboard.json")
        response.raise_for_status()
        self.works = response.json()['works']
        return self.works

# get random piece by epoch, piano
    def epoch_random(self, epoch):
        header = {"genre": "Keyboard",
                  "epoch": epoch}
        response = requests.get(f"{classical_url}/dyn/work/random", params=header)
        response.raise_for_status()
        self.works = response.json()["works"]
        # returns list of 40 random works
        return self.works

# get popular works by composer:
    def popular_works(self, comp_id):
        response = requests.get(f"{classical_url}/work/list/composer/{comp_id}/genre/Popular.json")
        response.raise_for_status()
        all_works = response.json()['works']
        for work in all_works:
            if work['genre'] == "Keyboard":
                self.works.append(work)
        return self.works


app = OpenOpus()

# res = requests.get(f"{classical_url}/composer/list/rec.json")
# res.raise_for_status()
# dt = res.json()['composers']
# keyboard_composers = []
# for i in range(len(dt)):
#     try:
#         app.list_keyboard_works(dt[i]['id'])
#         keyboard_composers.append(dt[i]['name'])
#     except KeyError:
#         pass

### NOT WORKING on API end ###
# sample_id = app.composer_by_name("Bach")
# print(sample_id)
# works = app.popular_works(sample_id)
# print(works)







