
class Player:
    player_count = 1

    def __init__(self, color, name="Player"):
        self.color = color
        self.name = f"{name} {self.player_count}"
        self.card_names = []
        self.player_count += 1
        self.has_won = False

    def set_new_cards(self, new_cards):
        self.card_names = new_cards

    def replace_card(self, new_card, card_index):
        old_card = self.card_names[card_index]
        self.card_names[card_index] = new_card
        return old_card

    def __repr__(self):
        return f'The {self.color} player has {"won" if self.has_won else "not won"}'
