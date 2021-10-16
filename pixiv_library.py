from pixivpy3 import *
import json

class PixivLibrary(AppPixivAPI):
    def __init__(self):
        super().__init__()
        self.pixiv_ids = json.load(open("pixiv_ids.json"))
        self.auth(refresh_token=self.pixiv_ids['REFRESH_TOKEN'])