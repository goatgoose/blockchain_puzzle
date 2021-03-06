import random
import json
from blockchain import Blockchain, Block
from bitlist import Bitlist
from terminaltables import AsciiTable
import time


class Client:
    def __init__(self, verbose=False):
        self.verbose = verbose

        self.blockchain = Blockchain()

        self.words = json.load(open("words.json", "r"))
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        self.id = None
        self.unique_seed = None
        self.is_finished = False
        self.player_bit_length = None

        self.shared_random = None

        ciphers = list(range(1, 17))
        random.shuffle(ciphers)
        self.ciphers_map = {i: j for i, j in zip(list(range(16)), ciphers)}

    def start(self):
        self.is_finished = False
        self._setup()
        self._game_loop()
        self._game_end()

    def encrypt_word(self, word, key):
        letter_numbers = {letter: number for number, letter in enumerate(self.letters)}
        encrypted_word = ""
        for letter in word:
            encrypted_word += self.letters[(letter_numbers[letter] + key) % len(self.letters)]
        return encrypted_word

    def next_seed(self, last_seed):
        random.seed(last_seed.to_int())
        random_int = random.getrandbits(16 - self.player_bit_length)
        random_bits = Bitlist.from_int(random_int, 16 - self.player_bit_length)
        id_bits = Bitlist.from_int(self.id, self.player_bit_length)
        return random_bits + id_bits

    def _setup(self):
        print("Welcome to the Manual Blockchain Puzzle Tournament!\n")
        player_count = int(input("Number of players: "))
        self.player_bit_length = len(Bitlist.from_int(player_count - 1))

        self.id = int(input("Enter ID: "))

        print(
            f"Would you like to: \n"
            f"\t 1. Generate a seed\n"
            f"\t 2. Enter a seed"
        )
        option = int(input("> ").strip())

        random_bits = None
        random_size = 16 - self.player_bit_length
        if option == 1:
            random_int = random.getrandbits(random_size)
            random_bits = Bitlist.from_int(random_int, random_size)
            print(f"Generated seed: {random_bits}")
        else:
            random_bit_string = input("Enter seed: ").replace(" ", "")
            random_bits = Bitlist.from_str(random_bit_string)
            assert len(random_bits) == random_size
            for bit in random_bits.bits:
                assert bit == 0 or bit == 1

        id_bits = Bitlist.from_int(self.id, self.player_bit_length)
        self.unique_seed = random_bits + id_bits

        random.seed(random_bits.to_int())
        self.shared_random = random.getrandbits(16)

    def _game_loop(self):
        puzzle_seed = self.unique_seed
        random_size = 16 - self.player_bit_length

        while True:
            self.__log(f"puzzle seed: {puzzle_seed}")

            shuffled_seed = puzzle_seed.shuffle(self.shared_random)
            nibbles = [Bitlist(shuffled_seed.bits[i:i + 4]) for i in range(0, len(shuffled_seed.bits), 4)]
            words = [self.words[i][nibble.to_int()] for i, nibble in zip(range(len(self.words)), nibbles)]
            cipher = self.ciphers_map[nibbles[3].to_int()]
            encrypted_words = [self.encrypt_word(word, cipher) for word in words]
            self.__log(f"cypher: {cipher}")
            self.__log(f"original words: {words}")

            table_data = [["#1", "#2", "#3", "Hex"]]
            for row in range(len(self.words[0])):
                row_offset = self.ciphers_map[row]
                table_data.append([f"{hex(row)[2:]}: {self.words[i][row]}" for i in range(len(self.words))] + [f"{hex(row)[2:]}: {row_offset}"])
            table = AsciiTable(table_data, title="Reference Sheet")
            print(table.table)

            print(AsciiTable([
                self.letters,
                list(range(len(self.letters)))
            ], title="Alphabet").table)
            print()

            print(f"Decipher the following puzzle:")
            print(f"\t {' '.join(encrypted_words)}\n")

            while True:
                print("Enter a proof code, or 'exit':")
                command = input("> ").strip().lower()
                if command == "exit":
                    self.is_finished = True
                    return

                input_bitlist = Bitlist.from_hex(command)
                self.__log(f"input: {input_bitlist}")
                self.__log(f"shuffled puzzle seed: {shuffled_seed}")

                unshuffled_input = input_bitlist.unshuffle(self.shared_random)
                self.__log(f"unshuffled input: {unshuffled_input}")
                self.__log(f"original seed: {puzzle_seed}")

                if unshuffled_input.bits[:-1 * self.player_bit_length] == puzzle_seed.bits[:-1 * self.player_bit_length]:
                    self.__log(f"valid solution.")
                    self.blockchain.add_block(Block(unshuffled_input))
                    puzzle_seed = self.next_seed(self.blockchain.last_block().solution)

                    random.seed(Bitlist.from_list(puzzle_seed.bits[:-4]).to_int())
                    self.shared_random = random.getrandbits(random_size)
                    break
                else:
                    print(f"Invalid solution.  Keep trying to solve!")

    def _game_end(self):
        points = {}

        for block in self.blockchain.blocks:
            solution = block.solution
            id_ = Bitlist.from_list(solution.bits[-1 * self.player_bit_length:]).to_int()

            if id_ not in points:
                points[id_] = 0
            points[id_] += 1

        print("---------------------------")
        print("points:")
        for id_ in points:
            print(f"\t player {id_}: {points[id_]}")

    def __log(self, message):
        if self.verbose:
            print(f"[verbose] {message}")


if __name__ == '__main__':
    Client(verbose=True).start()
