class Player:
    def __init__(self, max_hp=100, max_mp=100):
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        print(f"Giocatore colpito! HP: {self.hp}/{self.max_hp}")

    def use_magic(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            print(f"Magia usata! MP: {self.mp}/{self.max_mp}")
            return True
        return False

    def restore_mp(self, amount):
        self.mp = min(self.max_mp, self.mp + amount)
