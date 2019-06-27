# -*- coding: utf-8 -*-
"""
Player implementation for Linux.
ALSA - based.
"""

from kivy.uix.image import Image
from pygame import mixer
from threading import Thread, Event


class Player(Thread):
    """
    Player class
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.playlist = kwargs['playlist']
        self.current_song = kwargs['current_song']
        self.parent = kwargs['parent']
        self.is_paused = True
        self.p = mixer
        self.p.init()
        self.daemon = True
        self.start()
        self._stop_event = Event()

    def _draw_toggle_button(self, btn):
        img = 'images/' + str(btn) + '.png'
        btnImage = Image(source=img,
                    pos=(self.parent.root.ids.togglebtn.x, self.parent.root.ids.togglebtn.y),
                    size=(75, 75))            
        self.parent.root.ids.togglebtn.clear_widgets()
        self.parent.root.ids.togglebtn.add_widget(btnImage)

    def _continue(self):
        p = self.is_paused
        if self.p.get_init():
            self.stop()
        if p == False:
            self.toggle()

    def toggle(self):
        """
        Pause playback
        :return:
        """
        self.parent.root.ids.togglebtn.clear_widgets()
        if not self.p.get_init():
            print("Starting playback.")
            self.is_paused = False
            self.p.init()
            self.p.music.load(self.playlist[self.current_song])
            self.p.music.play()
            self._draw_toggle_button('pause')
        elif self.is_paused == True:
            print("Unpausing playback.")
            self.is_paused = False
            self.p.music.unpause()
            self._draw_toggle_button('pause')
        else:
            print("Pausing playback.")
            self.is_paused = True
            self.p.music.pause()
            self._draw_toggle_button('play')

    def stop(self):
        """
        Stop playback
        :return:
        """
        print("Stopping playback.")
        if self.p.get_init():
            self.p.music.stop()
            self.p.quit()
        self.is_paused = None
        self._draw_toggle_button('play')
        self.parent.root.ids.songSlider.value = 0

    def get_volume(self):
        """
        Get current audio volume
        :return:
        """
        if self.p.get_init():
            return self.p.music.get_volume()
        else:
            return 0

    def set_volume(self, _, value):
        """
        Set audio volume
        :param value:
        :return:
        """
        if self.p.get_init():
            self.p.music.set_volume(value)

    def get_previous(self):
        """
        Switch to previous song in playlist
        :return:
        """
        print("Going to previous song")
        if self.current_song > 0:
            return self.current_song - 1
        else:
            return len(self.playlist) - 1

    def set_previous(self):
        self.current_song = self.get_previous()
        self.parent.view_song()
        self._continue()

    def get_next(self):
        """
        Switch to next song in playlist
        :return:
        """
        print("Going to next song")
        if self.current_song < (len(self.playlist) - 1):
            return self.current_song + 1
        else:
            return 0

    def set_next(self):
        self.current_song = self.get_next()
        self.parent.view_song()
        self._continue()
