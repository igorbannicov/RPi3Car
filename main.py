#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main program file.
"""

import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.image import Image
from kivy.config import Config, ConfigParser
from kivy.clock import Clock
from tinytag import TinyTag
from libs.utils import is_true
from configs.settingsjson import media_settings_json, obd2_settings_json
from libs.constants import BAUDS, PROTOCOLS_MAP, WRONG_CHARS
from libs.audio.songlayout import CurrentSongLabel, OtherSongLabel
from random import shuffle

os.environ['KIVY_HOME'] = os.getcwd()
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
Config.write()


class CarApp(App):
    """
    Main application class.
    Draws the interface and creates instances of Player and OBD2 listener with graphs.
    """
    cp = ConfigParser()
    player = None
    obd2 = None
    need_obd = False

    def __init__(self, **kwargs):
        super().__init__()

    def build(self):
        """
        Function is called when CarApp object is created.
        """
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = True
        self.init_player()
        self.init_obd2()
        Clock.schedule_interval(self.update, 0.5)
        Clock.schedule_once(self.kostyli)

    def update(self, _):
        """
        Function used as a callback for timer.
        """
        try:
            if self.player:
                if self.player.p.get_init():
                    volume = self.player.get_volume()
                    self.root.ids.volumeSlider.value = volume
                    tag = TinyTag.get(self.player.playlist[self.player.current_song])
                    self.root.ids.songSlider.max = tag.duration * 1000
                    self.root.ids.songSlider.value = self.player.p.music.get_pos()
        except Exception as exceptn:
            print("Exception in update: " + str(exceptn))

    def init_player(self):
        """
        Initialise the music player.
        """
        extensions = list()
        playlist = list()
        from libs.audio.player import Player
        fpath = self.get_running_app().config.get('Media', 'path')
        if is_true(self.get_running_app().config.get('Media', 'mp3')):
            extensions.append('mp3')
        if is_true(self.get_running_app().config.get('Media', 'flac')):
            extensions.append('flac')
        if is_true(self.get_running_app().config.get('Media', 'm4a')):
            extensions.append('m4a')
        i = 1
        for root, _, files in os.walk(fpath):
            if files != []:
                for file in files:
                    for ext in extensions:
                        if file.endswith(ext):
                            fullpath = str(os.path.join(root, file))
                            playlist.append(fullpath)
                            i += 1
                self.player = Player(current_song=1,
                                     playlist=playlist,
                                     parent=self)
                if is_true(self.get_running_app().config.get('Media', 'shuffle')):
                    self.shuffle()
                self.root.ids.volumeSlider.bind(value=self.player.set_volume)
                self.view_song()
                print('Music player initialized.')
            

    def shuffle(self):
        """
        Shuffle the playlist
        """
        print("Shuffling")
        shuffle(self.player.playlist)

    def init_obd2(self):
        """
        Initialise the OBD2 listener and graphs.
        """
        need_obd = is_true(self.get_running_app().config.get('OBD2', 'enable'))
        if need_obd:
            from libs.obd2.obd2 import OBD2
            self.obd2 = None
            obd_pass = self.get_running_app().config.get('OBD2', 'password')
            obd_baud = self.get_running_app().config.get('OBD2', 'baud')
            obd_protocol = PROTOCOLS_MAP[self.get_running_app().config.get('OBD2', 'protocol')]
            vef = self.get_running_app().config.get('OBD2', 'vef')
            eds = self.get_running_app().config.get('OBD2', 'eds')
            my_time = self.get_running_app().config.get('OBD2', 'time')
            self.obd2 = OBD2(passkey=obd_pass,
                             baud=obd_baud,
                             protocol=obd_protocol,
                             vef=vef,
                             eds=eds,
                             time=my_time,
                             parent=self)
            try:
                self.root.ids.graphScreen.clear_widgets()
                for pid in self.obd2.pids:
                    self.root.ids.graphScreen.add_widget(self.obd2.pids[pid]['gauge'].graph)
                print('OBD2 initialized')
            except Exception as exceptn:
                print("Exception occured: " + str(exceptn))

    def kostyli(self, *args):
        """
        Will take this off once.
        It's for changing the play/pause button icon.
        """
        self.root.ids.togglebtn.clear_widgets()
        img = Image(source='images/play.png',
                    pos=(self.root.ids.togglebtn.x,
                         self.root.ids.togglebtn.y),
                    size=(75, 75))
        self.root.ids.togglebtn.add_widget(img)

    def view_song(self):
        """
        Adds song to playlist (UI).
        :param id:
        """
        self.root.ids.songlist.clear_widgets()

        # Display previous song
        tag = TinyTag.get(self.player.playlist[self.player.get_previous()])
        if (bool(set(WRONG_CHARS) & set(str(tag.title)))):
            tag.title = tag.title.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.album)))):
            tag.album = tag.album.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.artist)))):
            tag.artist = tag.artist.encode('latin1').decode('cp1251')
        line = str(tag.title)[0:20] + "/" + str(tag.artist)[0:20] + "/" + str(tag.album)[0:20]
        label = OtherSongLabel(text=line, root=self)
        self.root.ids.songlist.add_widget(label)

        # Display current song
        tag = TinyTag.get(self.player.playlist[self.player.current_song])
        if (bool(set(WRONG_CHARS) & set(str(tag.title)))):
            tag.title = tag.title.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.album)))):
            tag.album = tag.album.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.artist)))):
            tag.artist = tag.artist.encode('latin1').decode('cp1251')
        line = str(tag.title)[0:20] + "/" + str(tag.artist)[0:20] + "/" + str(tag.album)[0:20] + "/" + str(tag.genre)
        label = CurrentSongLabel(text=line, root=self)
        self.root.ids.songlist.add_widget(label)

        # Display next song
        tag = TinyTag.get(self.player.playlist[self.player.get_next()])
        if (bool(set(WRONG_CHARS) & set(str(tag.title)))):
            tag.title = tag.title.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.album)))):
            tag.album = tag.album.encode('latin1').decode('cp1251')
        if (bool(set(WRONG_CHARS) & set(str(tag.artist)))):
            tag.artist = tag.artist.encode('latin1').decode('cp1251')
        line = str(tag.title)[0:20] + "/" + str(tag.artist)[0:20] + "/" + str(tag.album)[0:20]
        label = OtherSongLabel(text=line, root=self)
        self.root.ids.songlist.add_widget(label)

    def update_volume(self, volume):
        """
        Sets the volume according to volume slider.
        :param volume:
        """
        self.player.set_volume(volume)

    def build_config(self, config):
        """
        Creates config if not found. Initialise the default config values.
        :param config:
        """
        config.setdefaults('Media', {
            'path': '~/Music',
            'shuffle': True,
            'mp3': True,
            'm4a': True,
            'flac': True
        })
        config.setdefaults('OBD2', {
            'enable': False,
            'password': '1234',
            'baud': '38400',
            'protocol': 'AUTO, ISO 9141-2',
            'vef': 87.68,
            'eds': 1.4,
            'time': 0.3
        })

    def build_settings(self, settings):
        """
        Adding config settings from JSON.
        :param settings:
        """
        settings.add_json_panel('Media', self.config, data=media_settings_json)
        settings.add_json_panel('OBD2', self.config, data=obd2_settings_json)

    def on_config_change(self, config, section, key, value):
        """
        Callback, executed when configuration is changed.
        :param config:
        :param section:
        :param key:
        :param value:
        """
        print("Config changed! Section " + str(section))
        self.cp.write()
        if section == "Media":
            self.init_player()
        if section == "OBD2":
            self.init_obd2()


if __name__ == '__main__':
    CarApp().run()
