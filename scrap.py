# scrap.py

import os,sys
import requests
import shelve
# class ImportFixer(object):
#     def __init__(self, mname):
#         self.mname = mname

#     def find_module(self, name, path=None):
#         if name == self.mname:
#             return self
#         return None

#     def load_module(self, name):
#         import _htmlparser as module
#         module.__name__ = name
#         return module
# sys.meta_path = [ImportFixer('bs4.builder._htmlparser')]
from bs4 import BeautifulSoup



def download_webpage(url):
    try:
        res = requests.get(url)
        res.raise_for_status()

        get_soup_text = BeautifulSoup(res.text, features='html.parser')

        # download the image
        print("Downloading")
        download_details(get_soup_text)
    except Exception as e:
        print(e)


def download_details(soup_text):
    anime_title = soup_text.select('.anime_info_episodes > h2')[0].getText()
    # print('Anime:', anime_title)

    episodes = soup_text.select('.anime_video_body ul li .active')[0].get('ep_end')
    # print('Episodes', episodes)

    completed = True if soup_text.find(title = 'Completed Anime') != None else False
    # print('Completed',completed)

    ongoing = True if soup_text.find(title = 'Ongoing Anime') != None else False
    # print('Ongoing', ongoing)


   


    image_elements = soup_text.select('.anime_info_body_bg img')

    


    if image_elements == []:
        pass
    else:
        image_url = image_elements[0].get('src')

        image = requests.get(image_url)
        image.raise_for_status()


    ## Save details to shelve file
    with shelve.open(f'./save_files/mydata') as shelf_file:

        file_name = os.path.basename(image_url)

        shelf_file[anime_title] = {
            'episodes': episodes,
            'completed': completed,
            'ongoing': ongoing,
            'image': file_name
            }
    
    

    # save the image
    if os.path.exists(f'./images/{file_name}') != True:
        image_file = open(os.path.join('images', file_name), 'wb')
        for chuck in image.iter_content(100000):
            image_file.write(chuck)
        image_file.close()

    else:
        pass



# download_webpage('https://gogoanime.vc/category/meikyuu-black-company')