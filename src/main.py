from ursina import *
from src.player import Player
from src.hud import CurvedBar

app = Ursina()
player = Player()

# Caricamento asset
# Player nel mondo (usa il primo frame dello sheet)
player_sprite = Entity(model='quad', texture='assets/SPRITE_SHEET.png', scale=3, position=(0,0,0))
player_sprite.texture.filtering = False # Per pixel art nitida

# HUD: Portrait e Barre in alto a sinistra
hud_group = Entity(parent=camera.ui, position=(-0.75, 0.35))
player_portrait = Entity(parent=hud_group, model='quad', texture='assets/SPRITE_PORTRAIT.png', scale=0.15)
player_portrait.texture.filtering = False

hp_bar = CurvedBar(radius=0.3, thickness=0.03, start_angle=-30, max_angle=240, bar_color=color.green, parent=hud_group)
mp_bar = CurvedBar(radius=0.26, thickness=0.02, start_angle=-30, max_angle=240, bar_color=color.blue, parent=hud_group)

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
