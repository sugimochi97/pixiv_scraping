from pixiv_library import PixivLibrary
import json
import os
from pprint import pprint
import time

CATEGORY = []

PATH = './MyBookmark_images'
ids = json.load(open('pixiv_ids.json'))
USER_ID = ids['USER_ID']

class MyBookmark(PixivLibrary):
    def __init__(self, path, user_id):
        super().__init__()
        self.json_data = self.user_bookmarks_illust(user_id, restrict='public')
        time.sleep(1)
        self.path = path

    def get_bookmark_tag(self, tag):
        save_path = './Mybookmark_tag'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        save_path = os.path.join(save_path, tag)

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        file_list = os.listdir(save_path)

        for illust in self.json_data.illusts:
            detail_data = self.illust_bookmark_detail(illust.id)
            time.sleep(1)
            try:
                tags = detail_data.bookmark_detail.tags
            except:
                pprint(detail_data.bookmark_detail)
            try:
                tags = [{t.name:t.is_registered} for t in tags if t.is_registered]
            except:
                print(tags)
            print(tags)
            for t in tags:
                if list(t.keys())[0] == tag:
                    if illust.meta_pages:
                        for illust_meta in illust.meta_pages:
                            if illust_meta.image_urls.original.split('/')[-1] in file_list:
                                continue
                            
                            self.download(illust_meta.image_urls.original, path=save_path)
                            time.sleep(1)
                    else:
                        if illust.meta_single_page.original_image_url.split('/')[-1] in file_list:
                            continue
                        self.download(illust.meta_single_page.original_image_url, path=save_path)
                        time.sleep(1)
        else:
            next_qs = self.parse_qs(self.json_data.next_url)
            if next_qs != None:
                self.json_data = self.user_bookmarks_illust(**next_qs)
                time.sleep(1)
                self.get_bookmark_tag(tag)


    def get_bookmark_keyword(self, keyword):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        save_path = os.path.join(self.path, keyword)

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        file_list = os.listdir(save_path)

        for illust in self.json_data.illusts:
            tags = [tag.name for tag in illust.tags]
            print(tags)
            if keyword in tags:
                if illust.meta_pages:
                    for illust_meta in illust.meta_pages:
                        if illust_meta.image_urls.original.split('/')[-1] in file_list:
                            continue
                        self.download(illust_meta.image_urls.original, path=save_path)
                        time.sleep(1)
                else:
                    if illust.meta_single_page.original_image_url.split('/')[-1] in file_list:
                        continue
                    self.download(illust.meta_single_page.original_image_url, path=save_path)
                    time.sleep(1)
        else:
            next_qs = self.parse_qs(self.json_data.next_url)
            if next_qs != None:
                self.json_data = self.user_bookmarks_illust(**next_qs)
                time.sleep(1)
                self.get_bookmark_keyword(keyword)

    def get_my_bookmark(self):
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        for illust in self.json_data.illusts:
            save_path = self.save_path
            if '/' not in illust['user']['name']:
                save_path += "/"+illust['user']['name']
            else:
                name = illust['user']['name'].split('/')[0]
                save_path += '/'+name
            
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            if illust.meta_pages:
                for i in illust.meta_pages:
                    self.download(i.image_urls.original, path=save_path)
            else:
                self.download(illust.meta_single_page.original_image_url, path=save_path)
        else:
            next_qs = self.parse_qs(self.json_data.next_url)
            if next_qs != None:
                self.json_data = self.user_bookmarks_illust(**next_qs)
                self.get_my_bookmark()


app = MyBookmark(PATH, USER_ID)
app.get_bookmark_keyword('tag')