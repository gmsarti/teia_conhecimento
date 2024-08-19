import json
import os
import random


class Oraculo:
    def __init__(self):
        self.decks_folder = "/Users/gustavosarti/Documents/code/meus_projetos/teia_conhecimento/src/tarot/baralhos"
        self.available_decks = self.get_available_decks()
        self.current_deck = None
        self.deck = []

    def get_available_decks(self):
        try:
            if not os.path.exists(self.decks_folder):
                print(f"Error: The folder {self.decks_folder} does not exist.")
                return []

            decks = [f for f in os.listdir(self.decks_folder) if f.endswith(".json")]

            if not decks:
                print(f"No deck files found in {self.decks_folder}")
                print("Contents of the folder:")
                print(os.listdir(self.decks_folder))

            return [
                os.path.splitext(deck)[0] for deck in decks
            ]  # Remove .json extension
        except Exception as e:
            print(f"An error occurred while getting available decks: {str(e)}")
            return []

    def choose_deck(self, deck_name):
        if deck_name not in self.available_decks:
            raise ValueError(
                f"Deck '{deck_name}' not found. Available decks: {', '.join(self.available_decks)}"
            )
        self.current_deck = deck_name
        self.deck = self.load_deck()
        random.shuffle(self.deck)

    def load_deck(self):
        deck_path = os.path.join(self.decks_folder, f"{self.current_deck}.json")
        with open(deck_path, "r") as file:
            deck_data = json.load(file)
            return deck_data[
                self.current_deck
            ]  # Assuming the deck name is the first key

    def draw_card(self):
        if not self.current_deck:
            raise ValueError("No deck selected. Use choose_deck() to select a deck.")
        if not self.deck:
            self.deck = self.load_deck()
            random.shuffle(self.deck)
        return self.deck.pop()

    def three_card_reading(self):
        return [self.draw_card() for _ in range(3)]

    def celtic_cross(self):
        return [self.draw_card() for _ in range(10)]

    def interpret_card(self, card):
        return card.get("interpretation", "This card's meaning is a mystery.")

    def perform_reading(self, spread="three_card"):
        if not self.current_deck:
            raise ValueError("No deck selected. Use choose_deck() to select a deck.")

        if spread == "three_card":
            cards = self.three_card_reading()
            positions = ["Past", "Present", "Future"]
        elif spread == "celtic_cross":
            cards = self.celtic_cross()
            positions = [
                "Current Situation",
                "Challenge",
                "Distant Past",
                "Recent Past",
                "Best Outcome",
                "Immediate Future",
                "Factors Affecting the Situation",
                "External Influences",
                "Hopes and Fears",
                "Final Outcome",
            ]
        else:
            raise ValueError(
                "Invalid spread type. Choose 'three_card' or 'celtic_cross'."
            )

        reading = []
        for position, card in zip(positions, cards):
            card_name = card.get("nome", "Unnamed Card")
            taro_card = card.get("carta_taro", "N/A")
            card_meaning = card.get("significado", "N/A")
            reading.append(f"{position}: {card_name}\n{taro_card}: {card_meaning}\n")

        return "\n".join(reading)


# Example usage
if __name__ == "__main__":
    oraculo = Oraculo()
    print("Available decks:", ", ".join(oraculo.available_decks))

    if not oraculo.available_decks:
        print("No decks available. Please check the baralhos folder.")
    else:
        deck_choice = input("Choose a deck: ")
        oraculo.choose_deck(deck_choice)

        spread_choice = input("Choose a spread (three_card or celtic_cross): ")
        print(f"\n{spread_choice.capitalize()} Reading with {deck_choice} deck:\n")
        print(oraculo.perform_reading(spread_choice))
