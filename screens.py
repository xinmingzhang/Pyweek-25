from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.gesture import GestureDatabase, Gesture
from kivy.properties import ObjectProperty,NumericProperty,StringProperty
from components import GameOver,Piece
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
import json
from time import strftime
from kivy.app import App

Builder.load_file('screens.kv')

gesture_strings = {
    'bottom_to_top_line': 'eNq1l81u2zAMx+96kebSgBS/pBforgP6AEM/jDRo0RhJuq1vP4nOnKrLtoNgXwxQ5J+mfhIlr7bP2+/v681wOL7th/Dl9B4hrB5HDLdXh+N+9zwcrsIYw+plpLC6GHHrbmHkGiclbtxtX481TGuY/SXsa/UKY6pRuUS9lwCEcHMNa2FKkpUzxpiALRxur37WYSzDuAaVhIxAyoACNFwjh8P93T/zYPSyKGxOSTglAoZMohYFy8hh05XA60c5J6BonIQSIGrmXnl1eVtK3jlgnuUpopJx1AwgSUA7E0RfVhGXS+CAIy2XwAFHWS6BI45nxFEVEiZDYoFouVffGccz44ggUQnFUmbtlScnTLiUvPOlM18UzgamEIkyWuzVd7wki+k7XTrThZwZJQKrJVIA603geCkvloAdMJ8BQ9OnSxvqTeCImZZL4Iz5xLjo19YpGbQ207KBuXuKHDLbnMDPFlbM9bTp/nwnzHkZdXG8gr/Vfc4N0KbjWHo3sDhdocX0pwvIDBfrqo9i5PtAuzewOFuxxfSdrsx0ve0kjElrI6LUy1edr858Y+nKRprY+7Rot77zVVpM3/nqzNcPxRwpWz0mWXr3rjpftcX0na/OfLneGtiy+D0i594LqDlfw8X0na/NfFkUGUggmWHJ8n/5co0/POyH4XX+QzD2XwQJqxtKti66UeIaPj4UjqNpuGs88sfHqoc1HlxexZgao1wIy42HeViCxpja79HqgY1HnsLiR6PCZKTGiBe0uPGIU5g0RpqM+snYlMPVo5kFlSmsmQXVyZg/Gf/Qys0saPKw3BSuU+G5KdymwjNdMpZap3XwY/t4fCoLIIsfZPUP77h7GfZ3rw9DNat32Go+LcZv4373+PZwrINWFNfK5WZWWrCVHlxOQam+T8N28+QuKdygfeZ9uF//Arrd4HI=',
    'top_to_bottom_line': 'eNqtlktu2zAQQPe8iL2pMf8hL+BuC/gART6GY6SIBctpm9uXHKW2laQfAfJGwGjmgfOGprjcP+6/v6x22/70fNymz6/PDtLyvsO0WfSn4+Fx2y9SR2n5reO0/LBiE2mpk1anta477J9Orcxamf+h7EvLSl1uVaVWvdQChLSGlZIxqucizpazpn6z+NneYnsLqb+9+SsSKTrgtBt4Yi6FyAAMC0nqd/9Nip5QzyTIZtkZTAGNwaewLFg+CyusYfnNYilZlACJMxedQKKYNuEMpLBOZ+tUEAjNMZPV9iahQjvpHKiwTmfrxIQlo5CgZCOZYp3COpU5WBze+ewdndnFkAEYAZWnsMI88yysUM9n9YiiipBZC1YqTGKFe/ZZWOGez+5B1clVBb2oG5QJLAn3grOwwr28uv9US4ChaHGN3YHFcAot7IteaNYYCmJS/40mNgUW+sXngYV/KWcYErgwsIQ90SltagxAcR5YTEAvE2hTNFPjdu5nlSnHhQ4fMZ0HFgPQywDiTAUolL1+h2zKl0jDv5Y5WBb67aKfihOyEbWDFmVSkxb6jeeBhX676Gc1YEdFB/J2I5gCC/3m88DCv138x5kPlrGdasIyBeYxAMd5YDEAvwwgbk1CCHGPwjf+612qvztut0/nW5pLXNM0LddUtGatRag+Tp1burkK4hD0UbCdeFc/axn5OoPLUFZGwRzBDKOgrcr1T1oGvsmIMhoFdQjyKCjv15VllMFDmY6CQ+N51DjDB+vyNxlRNmqcygdLGFmgwUIZWSAfgqPGaWi8jBoneb+uwv/MqBaGffBjf396qBugXvOG3bFZnA7ftsebp7ttC1t8tFv4ded97Y6H++e7U3vpaU0r03r4ZKo3xnrb4Eh92O53D5GR0xp9rKCehf3t6hdWSVuU',
    'left_to_right_line': 'eNq1l0luGzEQRfd9EWsTgTVXXcDZBvABAg+CLSSwG5Kc4fZhF52BQJLmpleCPlm/+flKFHt3/HT88n3/eDhfXk+H6f3b51ym3cMM083V+XJ6+XQ4X00zTrvPM027v1bc5LRp5qVOat38cny+LGW6lNk/yj4ss6bZl6qoVd9rAZTp+l3ZFwoiY2PAUswLT+ebq2/LOOS4IBgFUGFis9DpfHf734cAZiaaHv/9hMc38zfR0UGMEGTdPZPXiSPuqFKgkECoOtu6uaa5jZiTuTuEm5gpGQ4sPbcfYht3zFZCaO7V/OeucnhocPE/3AlQMShCXDx83TyZIm1jnkhRRszRSZk8kCiEkQb2JZmibeSeTDGG3EkLsjMbFg6OVXNKpDSEFNy5iIVBAWbR9WanZEq0kXtCpSGowLX71eqeOFJ4bbZV94RKQ1BLEKhZAVciKTaw9oRKsY07J1UeolpYhF1rLzJTIVrfGU6qvE51GcJiv86gegg5rdsnVpat7JMr24g9h3owlwiyAFk/ZzixcoyYh1Fxdtdl2VHWVy5JVWAb84QqI1DrzzPQhBSp/miV17dF2l1iBCkECqs4udS+r2jXzROo2DbmCVRGgCIXUFEC1ggHWt8WTaA6AhTdzFktikdBH/BOnkqbeCdOHcFZDywu9XKhVny5f6z/3Wni1BGc5FQQzZjQAGXAO2lqbOFtCdNGYNZzVhkcIVjBMAbMk6aN0GRz1OIaooK4XPjubut1+3x/Ohyef13ljfMuL9Puuh4U+2oqUG2ny2w63S5idKKlmN9+i95E6MRoIjYRUvTSROpEaCJ3IjZROpGaqJ3ITbROlCZ6J7ZEEJ3YEmHpxJYIoRNbIuwSRUuEXaJoibBLFC0RdomiJcIuUbRE2CWKlgi7RNESYZco7G9iTdQa4Ovx4fJUyUdM1xmwapeXz4fT7fP9Id/VsrNg0d+a8ON8enl4vb/kaG0u3Gt9YagnGwfVG5rUVqmTnw7Hx6c2B6frdL7b/wBF3Mpg',
    'right_to_left_line': 'eNq1l8+OmzAQh+9+keSyyPb8sf0C2WulPECVJihBu0oQsG337WsP2Qaq7sJl5oI0md/nwBeC2TYvzc/36lz3w1tXm+f7sbVme2qd2W/6obu91P3GtN5sX1sw2/8m9jJmWiw5yrn21lyHEuMSC5/EvpUp08aSSjn1ngPOmp2rQmAgjpDQWk+W6idHpt9vfpcJZ3a2IorwKALT/zh8uYrzclJgzl8tcb7THU8q0DJdTj0T1tCB7KRydJHOQg9KdBHgkg7dy4/JOyW6WPWgRBerfp1V72lG98t40eqDFl68+qSEBxELTgsvZmGN2Sdb2RnfAi3fsiBygfQWEL0Q9BYQwZDUFkBRjE5vAZGMepJRJKOeZBTJqCcZRTKulcyzwuXnIoljcmp8UUwrFfuA6VGRl/HjnoO08KKXghZe5FJSwrO4ZaeFF7WspZZFLa9Ui3ZWsIIvbjmo8UUuJy1+ELvBqfFFb1ipF3G6Z0aWf7a8Ze+PXV1f/74QBJQ3AjLbnedUZTBEnw9DG9gcSjPOmmFs4qwZx6abNZM0Cas0rfCYiPZjYhKLTpqYv8rs8kwm/DjBsxiMTfo8hosTZA7jNfrVnIZLvjj5pth5+PcE8sBwe627w/VYl6FQNlSutO/evrfd7fR2HMqHMRMqTgzxoxKW0UvdnC8ykUrcZjvVH8xWrBo='}

gestures = GestureDatabase()
for name, gesture_string in gesture_strings.items():
    gesture = gestures.str_to_gesture(gesture_string)
    gesture.name = name
    gestures.add_gesture(gesture)


class Game(Screen):
    time = StringProperty('')
    date = StringProperty('')
    board1 = ObjectProperty(None)
    n_piece_1 = ObjectProperty(None)
    board2 = ObjectProperty(None)
    n_piece_2 = ObjectProperty(None)
    level = NumericProperty(1)
    piece_1 = ObjectProperty(None)
    piece_2 = ObjectProperty(None)
    high_score = NumericProperty(0)
    score = NumericProperty(0)
    lines = NumericProperty(0)

    def __init__(self, **kwargs):
        for name in gesture_strings:
            self.register_event_type('on_{}'.format(name))
        super(Game, self).__init__(**kwargs)

    def on_enter(self, *args):
        with open('record.json', 'r') as f:
            self.high_score = json.load(f)
        self.score = 0
        self.level = 1
        self.lines = 0
        self.gameover = GameOver()
        self.n_piece_1.update_grids()
        self.n_piece_1.clear_blocks()
        self.board1.update_grids()
        self.board1.clear_blocks()
        self.n_piece_2.update_grids()
        self.n_piece_2.clear_blocks()
        self.board2.update_grids()
        self.board2.clear_blocks()
        if self.piece_1:
            self.piece_1.clear_widgets()
        elif self.piece_2:
            self.piece_2.clear_widgets()
        self.next_piece_1 = Piece(0, 0)
        self.next_piece_2 = Piece(0,0)
        self.add_piece_1()
        self.add_piece_2()
        self.falling_1 = Clock.schedule_interval(self.piece_1_falling, 1.0 / self.level)
        self.falling_2 = Clock.schedule_interval(self.piece_2_falling, 1.0 / self.level)
        Clock.schedule_interval(self.update_time, 0)
        Window.bind(on_key_down=self._keydown)

    def _keydown(self,instance, key, scancode=None, codepoint=None, modifier=None):
        if key in (119,273):
            self.on_bottom_to_top_line()
        elif key in (115,274):
            self.on_top_to_bottom_line()
        elif key in (97,276):
            self.on_right_to_left_line()
        elif key in (100,275):
            self.on_left_to_right_line()


    def on_score(self,*args):
        if self.score > self.high_score:
            self.high_score = self.score

    def update_time(self,*args):
        self.time = strftime('%H:%M')
        self.date = strftime('%b %d')

    def on_leave(self, *args):
        self.n_piece_1.clear_blocks()
        self.board1.clear_blocks()
        self.n_piece_2.clear_blocks()
        self.board2.clear_blocks()
        if self.piece_1:
            self.piece_1.clear_widgets()
        if self.piece_2:
            self.piece_2.clear_widgets()


    def on_level(self, *args):
        self.falling_1.cancel()
        self.falling_2.cancel()
        self.falling_1 = Clock.schedule_interval(self.piece_1_falling, 1.0 / self.level)
        self.falling_2 = Clock.schedule_interval(self.piece_2_falling, 1.0 / self.level)

    def on_lines(self, *args):
        self.level = self.lines // 40 + 1

    def piece_1_move_left(self, *args):
        stop = False
        for child in self.piece_1.children:
            if child.co_x == 0:
                stop = True
            elif self.board1.grids[child.co_x - 1, child.co_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_1.co_x -= 1
            self.piece_1.rotation_center[0] -= 1
            for child in self.piece_1.children:
                child.co_x -= 1

    def piece_2_move_left(self, *args):
        stop = False
        for child in self.piece_2.children:
            if child.co_x == 0:
                stop = True
            elif self.board2.grids[child.co_x - 1, child.co_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_2.co_x -= 1
            self.piece_2.rotation_center[0] -= 1
            for child in self.piece_2.children:
                child.co_x -= 1

    def piece_1_move_right(self, *args):
        stop = False
        for child in self.piece_1.children:
            if child.co_x == 9:
                stop = True
            elif self.board1.grids[child.co_x + 1, child.co_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_1.co_x += 1
            self.piece_1.rotation_center[0] += 1
            for child in self.piece_1.children:
                child.co_x += 1

    def piece_2_move_right(self, *args):
        stop = False
        for child in self.piece_2.children:
            if child.co_x == 9:
                stop = True
            elif self.board2.grids[child.co_x + 1, child.co_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_2.co_x += 1
            self.piece_2.rotation_center[0] += 1
            for child in self.piece_2.children:
                child.co_x += 1

    def piece_1_rotate(self, *args):
        stop = False
        for child in self.piece_1.children:
            dest_x = int(self.piece_1.rotation_center[0] + child.co_y - self.piece_1.rotation_center[1])
            dest_y = int(self.piece_1.rotation_center[0] - child.co_x + self.piece_1.rotation_center[1])
            if dest_x < 0 or dest_x > 9:
                stop = True
            elif self.board1.grids[dest_x, dest_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_1.rotate()

    def piece_2_rotate(self, *args):
        stop = False
        for child in self.piece_2.children:
            dest_x = int(self.piece_2.rotation_center[0] + child.co_y - self.piece_2.rotation_center[1])
            dest_y = int(self.piece_2.rotation_center[0] - child.co_x + self.piece_2.rotation_center[1])
            if dest_x < 0 or dest_x > 9:
                stop = True
            elif self.board2.grids[dest_x, dest_y].active:
                stop = True
        if stop:
            pass
        else:
            self.piece_2.rotate()

    def piece_1_hard_drop(self, *args):
        n = [self.get_p1_falling_distance(block) for block in self.piece_1.children]
        n.sort()
        d = n[0]
        self.piece_1.co_y -= d
        self.piece_1.rotation_center[1] -= d
        for child in self.piece_1.children:
            child.co_y -= d

    def piece_2_hard_drop(self, *args):
        n = [self.get_p2_falling_distance(block) for block in self.piece_2.children]
        n.sort()
        d = n[0]
        self.piece_2.co_y -= d
        self.piece_2.rotation_center[1] -= d
        for child in self.piece_2.children:
            child.co_y -= d


    def on_left_to_right_line(self):
        self.piece_1_move_right()
        self.piece_2_move_right()

    def on_right_to_left_line(self):
        self.piece_1_move_left()
        self.piece_2_move_left()

    def on_bottom_to_top_line(self):
        self.piece_1_rotate()
        self.piece_2_rotate()

    def on_top_to_bottom_line(self):
        self.piece_1_hard_drop()
        self.piece_2_hard_drop()

    def get_p1_falling_distance(self, block):
        d = block.co_y
        for j in range(d):
            if self.board1.grids[block.co_x, j].active == True:
                d = block.co_y - j - 1
        return d

    def get_p2_falling_distance(self, block):
        d = block.co_y
        for j in range(d):
            if self.board2.grids[block.co_x, j].active == True:
                d = block.co_y - j - 1
        return d

    def on_touch_down(self, touch):
        if touch.is_triple_tap:
            pass
        touch.ud['gesture_path'] = [(touch.x, touch.y)]
        super(Game, self).on_touch_down(touch)


    def on_touch_move(self, touch):
        touch.ud['gesture_path'].append((touch.x, touch.y))
        super(Game, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'gesture_path' in touch.ud:
            gesture = Gesture()
            gesture.add_stroke(touch.ud['gesture_path'])
            gesture.normalize()
            match = gestures.find(gesture, minscore=0.60)
            if match:
                self.dispatch('on_{}'.format(match[1].name))
        super(Game, self).on_touch_up(touch)

    def add_piece_1(self, *args):
        self.check_failure()
        for child in self.next_piece_1.children:
            child.co_x += 3
            child.co_y += 19
        self.piece_1 = self.next_piece_1
        self.piece_1.rotation_center = [self.piece_1.rotation_center[0] + 3, self.piece_1.rotation_center[1] + 19]
        self.board1.add_widget(self.piece_1)
        self.next_piece_1 = Piece(0, 0)
        self.n_piece_1.update(self.next_piece_1)

    def add_piece_2(self, *args):
        self.check_failure()
        for child in self.next_piece_2.children:
            child.co_x += 3
            child.co_y += 19
        self.piece_2 = self.next_piece_2
        for child in self.piece_2.children:
            child.x_scale = 1
            child.y_scale = 1
        self.piece_2.rotation_center = [self.piece_2.rotation_center[0] + 3, self.piece_2.rotation_center[1] + 19]
        self.board2.add_widget(self.piece_2)
        self.next_piece_2 = Piece(0, 0)
        self.n_piece_2.update(self.next_piece_2)

    def check_failure(self, *args):
        if True in self.board1.grids_state[:][20]:
            self.falling_1.cancel()
            self.falling_2.cancel()
            self.gameover.open()

            with open('record.json', 'w') as f:
                json.dump(self.high_score, f)
        elif True in self.board2.grids_state[:][20]:
            self.falling_1.cancel()
            self.falling_2.cancel()
            self.gameover.open()
            with open('record.json', 'w') as f:
                json.dump(self.high_score, f)

    def piece_1_falling(self, *args):
        self.check_piece_1_stop()
        self.piece_1.co_y -= 1
        self.piece_1.rotation_center[1] -= 1
        for child in self.piece_1.children:
            child.co_y -= 1

    def piece_2_falling(self, *args):
        self.check_piece_2_stop()
        self.piece_2.co_y -= 1
        self.piece_2.rotation_center[1] -= 1
        for child in self.piece_2.children:
            child.co_y -= 1

    def check_piece_1_stop(self, *args):

        stop = False
        for child in self.piece_1.children:
            if child.co_y == 0:
                stop = True
            elif self.board1.grids[child.co_x, child.co_y - 1].active:
                stop = True
        if stop:
            self.add_piece_1_to_grids()

    def check_piece_2_stop(self, *args):

        stop = False
        for child in self.piece_2.children:
            if child.co_y == 0:
                stop = True
            elif self.board2.grids[child.co_x, child.co_y - 1].active:
                stop = True
        if stop:
            self.add_piece_2_to_grids()

    def on_score(self, *args):
        if self.score >= self.high_score:
            self.high_score = self.score

    def add_piece_1_to_grids(self, *args):
        for child in self.piece_1.children:
            i, j = child.co_x, child.co_y
            self.board1.grids[i, j].active = True
            self.board1.grids[i,j].x_scale = 1
            self.board1.grids[i,j].y_scale = 1
        self.clear_p1_line()
        self.board1.remove_widget(self.piece_1)
        self.add_piece_1()

    def add_piece_2_to_grids(self, *args):
        for child in self.piece_2.children:
            i, j = child.co_x, child.co_y
            self.board2.grids[i, j].active = True
        self.clear_p2_line()
        self.board2.remove_widget(self.piece_2)
        self.add_piece_2()

    def clear_p1_line(self, *args):
        lines = set([block.co_y for block in self.piece_1.children])
        delete_lines = []

        for line in lines:
            if False not in self.board1.grids_state[:][line]:
                delete_lines.append(line)
        delete_lines.sort()
        n = len(delete_lines)
        if n == 1:
            self.lines += 1
            self.score += 40 * self.level
            for j in range(22):
                for i in range(10):
                    if j == delete_lines[0]:
                        self.board1.grids[i, j].active = False
                    elif j > delete_lines[0] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 1].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board2.grids[i,j].active == True:
                        self.board2.grids[i,j].active = False
                        self.board2.grids[i,j+1].active = True
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board2.grids[i,0].active = True
        elif n == 2:
            self.lines += 2
            self.score += 100 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1]):
                        self.board1.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 1].active = True
                    elif delete_lines[1] < j and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 2].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board2.grids[i,j].active == True:
                        self.board2.grids[i,j].active = False
                        self.board2.grids[i,j+2].active = True
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board2.grids[i,0].active = True
                    self.board2.grids[i, 1].active = True
        elif n == 3:
            self.lines += 3
            self.score += 300 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1], delete_lines[2]):
                        self.board1.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 1].active = True
                    elif delete_lines[1] < j < delete_lines[2] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 2].active = True
                    elif delete_lines[2] < j and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 3].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board2.grids[i,j].active == True:
                        self.board2.grids[i,j].active = False
                        self.board2.grids[i,j+3].active = True
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board2.grids[i,0].active = True
                    self.board2.grids[i, 1].active = True
                    self.board2.grids[i, 2].active = True
        elif n == 4:
            self.lines += 4
            self.score += 1200 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1], delete_lines[2], delete_lines[3]):
                        self.board1.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 1].active = True
                    elif delete_lines[1] < j < delete_lines[2] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 2].active = True
                    elif delete_lines[2] < j < delete_lines[3] and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 3].active = True
                    elif delete_lines[3] < j and self.board1.grids[i, j].active == True:
                        self.board1.grids[i, j].active = False
                        self.board1.grids[i, j - 4].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board2.grids[i,j].active == True:
                        self.board2.grids[i,j].active = False
                        self.board2.grids[i,j+4].active = True
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board2.grids[i,0].active = True
                    self.board2.grids[i, 1].active = True
                    self.board2.grids[i, 2].active = True
                    self.board2.grids[i, 3].active = True

    def clear_p2_line(self, *args):
        lines = set([block.co_y for block in self.piece_2.children])
        delete_lines = []
        for line in lines:
            if False not in self.board2.grids_state[:][line]:
                delete_lines.append(line)
        delete_lines.sort()
        n = len(delete_lines)
        if n == 1:
            self.lines += 1
            self.score += 40 * self.level
            for j in range(22):
                for i in range(10):
                    if j == delete_lines[0]:
                        self.board2.grids[i, j].active = False
                    elif j > delete_lines[0] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 1].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board1.grids[i,j].active == True:
                        self.board1.grids[i,j].active = False
                        self.board1.grids[i,j+1].active = True
                        self.board1.grids[i,j+1].x_scale = 1
                        self.board1.grids[i,j+1].y_scale = 1
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board1.grids[i,0].active = True
                    self.board1.grids[i,0].x_scale = 1
                    self.board1.grids[i,0].y_scale = 1
        elif n == 2:
            self.lines += 2
            self.score += 100 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1]):
                        self.board2.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 1].active = True
                    elif delete_lines[1] < j and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 2].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board1.grids[i,j].active == True:
                        self.board1.grids[i,j].active = False
                        self.board1.grids[i,j+2].active = True
                        self.board1.grids[i,j+2].x_scale = 1
                        self.board1.grids[i,j+2].y_scale = 1
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board1.grids[i,0].active = True
                    self.board1.grids[i,0].x_scale = 1
                    self.board1.grids[i,0].y_scale = 1
                    self.board1.grids[i, 1].active = True
                    self.board1.grids[i,1].x_scale = 1
                    self.board1.grids[i,1].y_scale = 1
        elif n == 3:
            self.lines += 3
            self.score += 300 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1], delete_lines[2]):
                        self.board2.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 1].active = True
                    elif delete_lines[1] < j < delete_lines[2] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 2].active = True
                    elif delete_lines[2] < j and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 3].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board1.grids[i,j].active == True:
                        self.board1.grids[i,j].active = False
                        self.board1.grids[i,j+3].active = True
                        self.board1.grids[i,j+3].x_scale = 1
                        self.board1.grids[i,j+3].y_scale = 1
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board1.grids[i,0].active = True
                    self.board1.grids[i,0].x_scale = 1
                    self.board1.grids[i,0].y_scale = 1
                    self.board1.grids[i, 1].active = True
                    self.board1.grids[i,1].x_scale = 1
                    self.board1.grids[i,1].y_scale = 1
                    self.board1.grids[i, 2].active = True
                    self.board1.grids[i,2].x_scale = 1
                    self.board1.grids[i,2].y_scale = 1
        elif n == 4:
            self.lines += 4
            self.score += 1200 * self.level
            for j in range(22):
                for i in range(10):
                    if j in (delete_lines[0], delete_lines[1], delete_lines[2], delete_lines[3]):
                        self.board2.grids[i, j].active = False
                    elif delete_lines[0] < j < delete_lines[1] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 1].active = True
                    elif delete_lines[1] < j < delete_lines[2] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 2].active = True
                    elif delete_lines[2] < j < delete_lines[3] and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 3].active = True
                    elif delete_lines[3] < j and self.board2.grids[i, j].active == True:
                        self.board2.grids[i, j].active = False
                        self.board2.grids[i, j - 4].active = True
            for j in range(21,-1,-1):
                for i in range(9,-1,-1):
                    if self.board1.grids[i,j].active == True:
                        self.board1.grids[i,j].active = False
                        self.board1.grids[i,j+4].active = True
                        self.board1.grids[i,j+4].x_scale = 1
                        self.board1.grids[i,j+4].y_scale = 1
            seed = int(self.time[-1])
            for i in range(9,-1,-1):
                if i != seed:
                    self.board1.grids[i,0].active = True
                    self.board1.grids[i,0].x_scale = 1
                    self.board1.grids[i,0].y_scale = 1
                    self.board1.grids[i, 1].active = True
                    self.board1.grids[i,1].x_scale = 1
                    self.board1.grids[i,1].y_scale = 1
                    self.board1.grids[i, 2].active = True
                    self.board1.grids[i,2].x_scale = 1
                    self.board1.grids[i,2].y_scale = 1
                    self.board1.grids[i, 3].active = True
                    self.board1.grids[i,3].x_scale = 1
                    self.board1.grids[i,3].y_scale = 1


class Title(Screen):
    password = StringProperty('')
    psw =StringProperty( '_ _ _ _ _ _ ')

    def __init__(self,**kwargs):
        super(Title,self).__init__(**kwargs)
        self.texture = Texture.create(size=(2, 7), colorfmt='rgba')
        p1_color = [255, 0,0, 200]
        p2_color = [255, 165, 0, 200]
        p3_color = [255, 255, 0, 200]
        p4_color = [0, 255, 0, 200]
        p5_color = [0,127, 255,200]
        p6_color = [0, 0, 255, 200]
        p7_color = [139, 0, 255, 200]

        p = p1_color*2 + p2_color*2 + p3_color*2 + p4_color*2 +p5_color*2+p6_color*2+p7_color*2

        buf = bytes(p)
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.texture.wrap = 'repeat'
        with self.canvas.before:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)

        self._trig = t = Clock.create_trigger(self._update_rect)
        self.bind(pos=t, size=t)

        Clock.schedule_interval(self._update_texture, 0)


    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


    def _update_texture(self, *args):
        a = Clock.get_boottime() * 0.1
        self.rect.tex_coords = 0,a,1,a,1,1+a,0,1+a

    def on_enter(self, *args):
        self.password = ''
        Clock.schedule_interval(self.update_time, 0)

    def update_time(self,*args):
        pass


    def on_password(self,*args):
        a = len(self.password)
        b = 6 - a
        self.psw = '* '* a + '_ '*b
        if a == 6 and self.password == '799335':
            app = App.get_running_app()
            app.root.current = 'game'
        if a == 6 and self.password != '799335':
            self.password = ''