class Character:
    def __init__(self, max_hp=100, max_mp=100, texture=None, cols=1, rows=1, portrait=None):
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.texture = texture
        self.cols = cols
        self.rows = rows
        self.portrait = portrait or texture

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        print(f"{self.__class__.__name__} colpito! HP: {self.hp}/{self.max_hp}")

    def use_magic(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            print(f"Magia usata! MP: {self.mp}/{self.max_mp}")
            return True
        return False

    def restore_mp(self, amount):
        self.mp = min(self.max_mp, self.mp + amount)

class Adventurer(Character):
    def __init__(self):
        # adventurer-Sheet.png: 350 x 407. fw=50, fh=37 -> 7 cols x 11 rows.
        # Wait, the review says I swapped them.
        # 350 / 7 = 50. 407 / 11 = 37. So 7 cols, 11 rows is correct for 50x37 frames.
        # 350 / 11 = 31.8. 407 / 7 = 58.
        # Actually 407 / 11 = 37. 350 / 7 = 50.
        # If frames are 50x37, then cols=7, rows=11.
        # The user's prompt says: "7 cols × 11 rows".
        super().__init__(
            max_hp=120,
            max_mp=60,
            texture='assets/adventurer-Sheet.png',
            cols=7,
            rows=11
        )

class Warrior(Character):
    def __init__(self):
        # Warrior_Sheet-Effect.png: 414 x 748. 9 cols x 11 rows.
        # 414 / 9 = 46. 748 / 11 = 68. Correct.
        super().__init__(
            max_hp=200,
            max_mp=30,
            texture='assets/Warrior_Sheet-Effect.png',
            cols=9,
            rows=11
        )

class Mage(Character):
    def __init__(self):
        # tsyr_sheet.png (SPRITE_SHEET.png): 320 x 352. 8 cols x 8 rows.
        # 320 / 8 = 40. 352 / 8 = 44. Correct.
        super().__init__(
            max_hp=80,
            max_mp=150,
            texture='assets/SPRITE_SHEET.png',
            cols=8,
            rows=8,
            portrait='assets/SPRITE_PORTRAIT.png'
        )

# For backward compatibility or as a default
class Player(Adventurer):
    pass
