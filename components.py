from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.properties import OptionProperty,BooleanProperty,NumericProperty,DictProperty,ListProperty
from kivy.lang import Builder
from random import choice,uniform
from kivy.uix.popup import Popup
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label


Builder.load_file('components.kv')

class Block(Widget):
    co_x = NumericProperty(0)
    co_y = NumericProperty(0)
    x_scale = NumericProperty(1)
    y_scale = NumericProperty(1)
    active = BooleanProperty(False)
    color = ListProperty([0.75,0.75,0.75,1])

    def __init__(self, co_x, co_y, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.co_x = co_x
        self.co_y = co_y
        self.rescale()

    def rescale(self, *args):
        self.x_scale = uniform(0.5, 1.5)
        self.y_scale = uniform(0.5, 1.5)



class Board(RelativeLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.update_grids()

    def update_grids(self, *args):
        self.grids = {}
        for i in range(10):
            for j in range(25):
                self.grids[i, j] = Block(i, j, active=False)
                self.add_widget(self.grids[i, j])

    @property
    def grids_state(self):
        return [[self.grids[i, j].active for i in range(10)] for j in range(25)]

    def clear_blocks(self, *args):
        self.clear_widgets()
        self.update_grids()



class NPiece(RelativeLayout):
    def __init__(self, **kwargs):
        super(NPiece, self).__init__(**kwargs)
        self.update_grids()

    def update_grids(self, *args):
        self.grids = {}
        for i in range(4):
            for j in range(4):
                block = Block(i, j, active=False)
                block.x_scale = 1
                block.y_scale = 1
                self.grids[i, j] = block
                self.add_widget(self.grids[i, j])

    def update(self, new_piece):
        colors = {'I':[0,1,1,1],
                  'O':[1,1,0,1],
                  'T':[0.63,0.13,0.94,1],
                  'S':[0,1,0,1],
                  'Z':[1,0,0,1],
                  'J':[0,0,1,1],
                  'L':[1,0.65,0,1]}
        color = colors[new_piece.style]
        for i in range(4):
            for j in range(4):
                self.grids[i, j].active = False
        for child in new_piece.children:
            i, j = child.co_x, child.co_y
            self.grids[i,j].color = color
            self.grids[i, j].active = True

    def clear_blocks(self, *args):
        self.clear_widgets()
        self.update_grids()

class Piece(RelativeLayout):
    grids = DictProperty({})
    style = OptionProperty('I', options=('I', 'O', 'T', 'S', 'Z', 'J', 'L'))
    co_x = NumericProperty(0)
    co_y = NumericProperty(0)

    def __init__(self, co_x, co_y, **kwargs):
        super(Piece, self).__init__(**kwargs)
        self.co_x = co_x
        self.co_y = co_y
        self.creat()

    def creat(self, *args):
        self.style = choice(Piece.style.options)
        styles = {'I': [(0, 2), (1, 2), (2, 2), (3, 2)],
                  'O': [(1, 1), (1, 2), (2, 1), (2, 2)],
                  'T': [(0, 1), (1, 1), (2, 1), (1, 2)],
                  'S': [(0, 1), (1, 1), (1, 2), (2, 2)],
                  'Z': [(0, 2), (1, 2), (1, 1), (2, 1)],
                  'J': [(0, 1), (1, 1), (2, 1), (2, 2)],
                  'L': [(0, 2), (0, 1), (1, 1), (2, 1)]}
        colors = {'I':[0,1,1,1],
                  'O':[1,1,0,1],
                  'T':[0.63,0.13,0.94,1],
                  'S':[0,1,0,1],
                  'Z':[1,0,0,1],
                  'J':[0,0,1,1],
                  'L':[1,0.65,0,1]}

        for pos in styles[self.style]:
            block = Block(self.co_x + pos[0], self.co_y + pos[1], active=True)
            block.color = colors[self.style]
            self.add_widget(block)
        if self.style in ('I', 'O'):
            self.rotation_center = [self.co_x + 1.5, self.co_y + 1.5]
        else:
            self.rotation_center = [self.co_x + 1, self.co_y + 1]

    def rotate(self, *args):
        for child in self.children:
            dest_x = int(self.rotation_center[0] + child.co_y - self.rotation_center[1])
            dest_y = int(self.rotation_center[0] - child.co_x + self.rotation_center[1])
            child.co_x, child.co_y = dest_x, dest_y
            child.rescale()

class Margin(BoxLayout):
    pass


class Pause(Popup):
    pass


class GameOver(Popup):
    pass


class NumKey(ButtonBehavior,Label):
    pass

