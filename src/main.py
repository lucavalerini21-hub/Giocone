from ursina import *
from src.player import Adventurer, Warrior, Mage
from src.hud import CurvedBar
from src.monster import Skeleton
import random
from pathlib import Path

# Set asset folder to project root
application.asset_folder = Path(__file__).parent.parent

app = Ursina()

# Player setup
player_classes = [Adventurer(), Warrior(), Mage()]
current_class_index = 0

# Player Entity
player_entity = Entity(model='quad', scale=3, position=(0,0,0))
player_entity.character_data = player_classes[current_class_index]
player_anim = None
current_anim_state = 'idle'

def update_player_sprite():
    global player_anim, current_anim_state
    if player_anim:
        if hasattr(player_anim, 'animations'):
            player_anim.animations = []
        destroy(player_anim)

    player_anim = SpriteSheetAnimation(
        player_entity.character_data.texture,
        parent=player_entity,
        tileset_size=(player_entity.character_data.cols, player_entity.character_data.rows),
        fps=10,
        animations={
            'idle': ((0, 0), (min(3, player_entity.character_data.cols - 1), 0)),
            'walk': ((0, 1), (min(5, player_entity.character_data.cols - 1), 1)),
        }
    )
    if player_anim.texture:
        player_anim.texture.filtering = False
    player_anim.play_animation('idle')
    current_anim_state = 'idle'

    # Update portrait
    player_portrait.texture = player_entity.character_data.portrait
    if player_portrait.texture:
        player_portrait.texture.filtering = False

# HUD: Portrait e Barre in alto a sinistra
hud_group = Entity(parent=camera.ui, position=(-0.75, 0.35))
player_portrait = Entity(parent=hud_group, model='quad', scale=0.15)

update_player_sprite()

hp_bar = CurvedBar(radius=0.3, thickness=0.03, start_angle=-30, max_angle=240, bar_color=color.green, parent=hud_group)
mp_bar = CurvedBar(radius=0.26, thickness=0.02, start_angle=-30, max_angle=240, bar_color=color.blue, parent=hud_group)

# Monsters
monsters = []

def spawn_skeleton():
    x = random.uniform(-10, 10)
    y = random.uniform(-5, 5)
    s = Skeleton(target=player_entity, position=(x, y, 0))
    monsters.append(s)

# Initial monsters
for _ in range(3):
    spawn_skeleton()

def update():
    global current_anim_state
    hp_bar.set_value(player_entity.character_data.hp / player_entity.character_data.max_hp)
    mp_bar.set_value(player_entity.character_data.mp / player_entity.character_data.max_mp)

    # Simple movement
    move_speed = 5
    dx = held_keys['d'] - held_keys['a']
    dy = held_keys['w'] - held_keys['s']
    player_entity.x += dx * move_speed * time.dt
    player_entity.y += dy * move_speed * time.dt

    if dx != 0:
        player_anim.scale_x = 1 if dx > 0 else -1
        if current_anim_state != 'walk':
            player_anim.play_animation('walk')
            current_anim_state = 'walk'
    elif dy != 0:
        if current_anim_state != 'walk':
            player_anim.play_animation('walk')
            current_anim_state = 'walk'
    else:
        if current_anim_state != 'idle':
            player_anim.play_animation('idle')
            current_anim_state = 'idle'

def input(key):
    global current_class_index

    if key == '1':
        current_class_index = 0
        player_entity.character_data = player_classes[current_class_index]
        update_player_sprite()
    elif key == '2':
        current_class_index = 1
        player_entity.character_data = player_classes[current_class_index]
        update_player_sprite()
    elif key == '3':
        current_class_index = 2
        player_entity.character_data = player_classes[current_class_index]
        update_player_sprite()

    if key == 'space': # Simula danno
        player_entity.character_data.take_damage(10)
    if key == 'm': # Simula magia
        player_entity.character_data.use_magic(20)

    if key == 'k': # Attack
        for m in monsters[:]:
            if distance(player_entity.position, m.position) < 2:
                m.take_damage(20)
                if m.hp <= 0:
                    monsters.remove(m)
                    m.target = None
                    destroy(m)
                    # Respawn a new one
                    spawn_skeleton()

if __name__ == '__main__':
    app.run()
