# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
# from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem, ThreeLineAvatarIconListItem, ImageLeftWidget
import shelve
# from kivy.clock import Clock
from scrap import download_webpage
import os
# from kivy.resources import resource_add_path, resource_find
from threading import Thread

# path = os.getcwd().a




#----------------Custom widgets------------------------#

class CustomListItem(OneLineAvatarIconListItem):
    def delete_item(self, text):
        """Delete list item and remove item from the shelve file"""

        with shelve.open('./save_files/mydata')as shelf_file:

            url_list = shelf_file['url_list']
            url_list.remove(str(text))
            shelf_file['url_list'] = url_list

        self.parent.remove_widget(self)









#------------------Screens-------------------------------#

class ScreenManagement(ScreenManager):
    pass


class MainWindow(MDScreen):
    def refresh_callback(self, *args):
        print("Refreshing...")

        def refresh_callback(interval):
            self.ids.box.clear_widgets()
            
            self.get_anime_info()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0

        # Clock.schedule_once(refresh_callback, 1)
        anime_thread = Thread(target=refresh_callback, args=(1,))
        anime_thread.start()

    def get_anime_info(self):
        with shelve.open('./save_files/mydata') as shelf_file:
            url_list = shelf_file['url_list']

        for url in url_list:
            download_webpage(url)



        with shelve.open('./save_files/mydata') as shelf_file:
            for key in shelf_file.keys():
                if key != 'url_list':
                    print(key)
                    anime = shelf_file[key]
                    episodes = anime['episodes']
                    completed = anime['completed']
                    # ongoing = anime['ongoing']
                    image = anime['image']

                    anime_complete = 'completed' if completed else 'ongoing'

                    list_item = ThreeLineAvatarIconListItem(text=key, secondary_text=f"[b]Status:[/b] {anime_complete}", tertiary_text=f"[b]Episodes:[/b] {episodes}")
                    list_item.add_widget(ImageLeftWidget(source=f"./images/{image}"))

                    self.ids.box.add_widget(list_item)
            


class AddUrlScreen(MDScreen):
    def add_url(self, text):
        """Add the url to list and save the url in shelve file"""
        self.ids.linklist.add_widget(CustomListItem(text=text))
        self.ids.linkinput.focus = True
        self.ids.linkinput.text = ''

        # saving to shelve file
        with shelve.open('./save_files/mydata') as shelf_file:
            url_list = shelf_file['url_list']
            url_list.append(str(text))
            shelf_file['url_list'] = url_list
        

    def on_pre_enter(self):
        try:
            with shelve.open('./save_files/mydata') as shelf_file:
                self.ids.linklist.clear_widgets()
                for item in shelf_file['url_list']:
                    self.ids.linklist.add_widget(CustomListItem(text=item))


        except KeyError:
            with shelve.open('./save_files/mydata') as shelf_file:
                shelf_file['url_list'] = []













#-----------------Main App-------------------#

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.root.transition= CardTransition()


    def on_start(self):
        try:
            os.mkdir('images')
            os.mkdir('save_files')
        except:
            pass



    def open_settings_screen(self):
        """open setting window"""
        self.root.current = 'addurl'
        self.root.transition.direction = 'down'

    def return_to_main_window(self):
        self.root.current = 'mainscreen'
        self.root.transition.direction = 'up'



if __name__ == '__main__':
    MainApp().run()
