# -*- coding: utf-8 -*-
"""
Graphs UI classes
"""
from kivy.garden.graph import Graph, SmoothLinePlot
from kivy.uix.label import Label


class GaugeLabel:
    """
    Label data presentation
    """
    def __init__(self, **kwargs):
        self.name = kwargs['name'].upper()
        self.parent = kwargs['parent']
        self.color = list(map(float, kwargs['color']))
        self.gtype = kwargs['gtype']
        self.value = 0
        self.text = "[b]" + str(self.name) + "[/b]"
        self.graph = Label(halign='center',
                           valign='middle',
                           color=self.color,
                           markup=True,
                           text=self.text)

    def update(self):
        """
        Method to update the label text
        :return:
        """
        value = self.parent.pids[self.name.upper()]['value']
        self.text = "[b]" + str(self.name) + "\n[size=32]" + str(value) +"[/size][/b]"
        self.graph.text = self.text


class GaugeGraph:
    """
    Graph data presentation
    """
    def __init__(self, **kwargs):
        self.grid = True or kwargs['grid']
        self.color = kwargs['color']
        self.name = kwargs['name'].upper()
        self.label = kwargs['name']
        self.parent = kwargs['parent']
        self.gtype = kwargs['gtype']
        self.graph = Graph(ylabel=self.label,
                           x_ticks_minor=1,
                           x_ticks_major=5,
                           y_ticks_major=20,
                           x_grid_label=True,
                           y_grid_label=True,
                           padding=5,
                           x_grid=self.grid,
                           y_grid=self.grid,
                           xmin=0,
                           xmax=50,
                           ymin=0,
                           ymax=20)
        self.plot = SmoothLinePlot(color=self.color)
        self.plot.points = []
        self.graph.add_plot(self.plot)

    def update(self):
        """
        Method to update the graph
        :return:
        """
        try:
            values = list(map(int, self.parent.pids[self.name]['values']))
            if len(values) > 1:
                y_max = max(values)
                y_min = min(values)
                self.graph.ymin = y_min
                self.graph.ymax = y_max
                if y_max > 10:
                    self.graph.y_ticks_minor = int(y_max / 10)
                    self.graph.y_ticks_major = int(y_max / 5)
                else:
                    self.graph.y_ticks_minor = 1
                    self.graph.y_ticks_major = 5
            self.plot.points = []
            i = 0
            while i < len(values):
                self.plot.points.append([i, values[i]])
                i += 1
            self.graph.add_plot(self.plot)

        except Exception as exceptn:
            print("Exception in graph update occured: " + str(exceptn))
