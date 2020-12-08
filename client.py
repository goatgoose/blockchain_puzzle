import random
import json
from blockchain import Blockchain, Block
from bitlist import Bitlist


class Client:
    def __init__(self):
        self.blockchain = Blockchain()

        self.words = json.load(open("words.json", "r"))

        self.id = None
        self.unique_seed = None

    def start(self):
        self._setup()
        puzzle_seed = self.unique_seed.shuffled

        nibbles = [Bitlist(puzzle_seed.bits[i:i + 4]) for i in range(0, len(puzzle_seed.bits), 4)]
        words = [self.words[i][nibble.to_int()] for i, nibble in zip(range(len(self.words)), nibbles)]
        encrypted_words = [self.encrypt_word(word, nibbles[3].to_int()) for word in words]
        print(words)
        print(encrypted_words)

    def _setup(self):
        print("Welcome to the Manual Blockchain Puzzle Tournament!\n")
        player_count = int(input("Number of players: "))
        player_bit_length = len(Bitlist.from_int(player_count))

        self.id = int(input("Enter ID: "))

        print(
            f"Would you like to: \n"
            f"\t 1. Generate a seed\n"
            f"\t 2. Enter a seed"
        )
        option = int(input("> "))

        random_bits = None
        random_size = 16 - player_bit_length
        if option == 1:
            random_int = random.getrandbits(random_size)
            random_bits = Bitlist.from_int(random_int, random_size)
            print(f"Random seed: {random_bits}")
        else:
            random_bit_string = input("Enter seed: ").replace(" ", "")
            random_bits = Bitlist.from_str(random_bit_string)
            assert len(random_bits) == random_size
            for bit in random_bits.bits:
                assert bit == 0 or bit == 1

        id_bits = Bitlist.from_int(self.id, player_bit_length)
        self.unique_seed = random_bits + id_bits
        print(f"unique seed: {self.unique_seed}")

    @staticmethod
    def encrypt_word(word, key):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                   "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        letter_numbers = {letter: number for number, letter in enumerate(letters)}
        encrypted_word = ""
        for letter in word:
            encrypted_word += letters[(letter_numbers[letter] + key) % len(letters)]
        return encrypted_word


if __name__ == '__main__':
    Client().start()
