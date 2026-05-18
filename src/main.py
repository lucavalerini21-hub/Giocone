from ursina import *
from src.player import Player
from src.hud import CurvedBar

app = Ursina()
player = Player()

hp_bar = CurvedBar(radius=0.4, thickness=0.04, start_angle=-30, max_angle=240, bar_color=color.green, parent=camera.ui, position=(0.6, -0.3))
mp_bar = CurvedBar(radius=0.35, thickness=0.03, start_angle=-30, max_angle=240, bar_color=color.blue, parent=camera.ui, position=(0.6, -0.3))

def update():
    hp_bar.set_value(player.hp / player.max_hp)
    mp_bar.set_value(player.mp / player.max_mp)

def input(key):
    if key == 'space': # Simula danno
        player.take_damage(10)
    if key == 'm': # Simula magia
        player.use_magic(20)

if __name__ == '__main__':
    app.run()
