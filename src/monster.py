from ursina import *
from src.player import Character

class Monster(Entity, Character):
    def __init__(self, target=None, **kwargs):
        Entity.__init__(self, model='quad', scale=3, **kwargs)
        Character.__init__(self, max_hp=50)
        self.target = target
        self.speed = 1
        self.attack_range = 1.5
        self.attack_cooldown = 2.0
        self.timer = 0

        self.anim = None
        self.current_state = 'idle'
        # Skeleton sprites are 600x150, 4 frames -> 150x150 each.
        self.idle_cols = 4
        self.walk_cols = 4
        # Attack.png is 1200x150, 8 frames -> 150x150 each.
        self.attack_cols = 8
        self.set_animation('assets/Idle.png', self.idle_cols)

    def set_animation(self, texture, cols):
        if self.anim:
            # Safely destroy animation
            if hasattr(self.anim, 'animations'):
                self.anim.animations = []
            destroy(self.anim)
            self.anim = None

        self.anim = SpriteSheetAnimation(
            texture,
            parent=self,
            tileset_size=(cols, 1),
            fps=8,
            animations={
                'loop': ((0, 0), (cols - 1, 0)),
            }
        )
        if self.anim.texture:
            self.anim.texture.filtering = False
        self.anim.play_animation('loop')

    def update(self):
        if not self.target or not hasattr(self.target, 'character_data'):
            return

        dist = distance(self.position, self.target.position)

        if dist > self.attack_range:
            # Move towards target
            direction = (self.target.position - self.position).normalized()
            self.position += direction * self.speed * time.dt

            if self.current_state != 'walk':
                self.set_animation('assets/Walk.png', self.walk_cols)
                self.current_state = 'walk'

            # Flip sprite based on direction
            if self.anim:
                if direction.x > 0:
                    self.anim.scale_x = 1
                elif direction.x < 0:
                    self.anim.scale_x = -1
        else:
            # Attack logic
            self.timer += time.dt
            if self.timer >= self.attack_cooldown:
                if self.target and hasattr(self.target, 'character_data'):
                    print(f"Skeleton attacks {self.target}!")
                    self.target.character_data.take_damage(10)
                self.timer = 0

                # Play attack animation
                self.set_animation('assets/Attack.png', self.attack_cols)
                self.current_state = 'attack'
                invoke(self.reset_to_idle, delay=1.0)

    def reset_to_idle(self):
        if self.current_state == 'attack':
            self.set_animation('assets/Idle.png', self.idle_cols)
            self.current_state = 'idle'

class Skeleton(Monster):
    def __init__(self, target=None, **kwargs):
        super().__init__(target=target, **kwargs)
