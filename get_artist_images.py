import os
from pixiv_library import PixivLibrary
from time import sleep

ARTIST = 21380191

PATH = './pixiv_images/'

class ArtistLibrary(PixivLibrary):
    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path

    def get_artist_illusts(self, artist):
        self.json_data = self.user_illusts(artist)
        save_path = os.path.join(self.save_path,self.json_data.illusts[0].user.name)

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        for illust in self.json_data.illusts:
            self.download(illust.image_urls.large, path=save_path)
        else:
            next_qs = self.parse_qs(self.json_data.next_url)
            if next_qs != None:
                self.json_data = self.user_illusts(**next_qs)
                self.get_artist_illusts(artist)
                sleep(1)

app = ArtistLibrary(PATH)
app.get_artist_illusts(ARTIST)