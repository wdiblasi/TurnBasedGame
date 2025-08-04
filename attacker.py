from player_char import Player_Char

attacker_max_health = 100
attacker_timer_cap = 200

class Attacker(Player_Char):
    def __init__(self, position):
        super().__init__(attacker_max_health, attacker_timer_cap, position)
        self.special_move_name = "Charge (increase attack modifier)"
        self.attack_modifier = 1.0
