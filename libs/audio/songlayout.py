from kivy.uix.label import Label


class CurrentSongLabel(Label):

    def __init__(self, **kwargs):
        super().__init__()
        self.halign = 'left'
        self.valign = 'middle'
        self.font_size = 32
        self.text = kwargs['text']
        self.root = kwargs['root']
        self.width = self.root.root.ids.songlist.width
        self.background_color = (0.5, 0.5, 0.5, 1)
        self.color = (1, 1, 1, 1)

class OtherSongLabel(Label):

    def __init__(self, **kwargs):
        super().__init__()
        self.halign = 'left'
        self.valign = 'middle'
        self.font_size = 24
        self.text = kwargs['text']
        self.root = kwargs['root']
        self.width = self.root.root.ids.songlist.width
        self.background_color = (1, 1, 1, 1)
        self.color = (0.25, 0.25, 0.25, 0.1)
