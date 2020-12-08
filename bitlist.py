
class Bitlist:
    def __init__(self, bits=None):
        if bits:
            self.bits = bits.copy()
        else:
            self.bits = []

        self.shuffle_shift_amount = 5

    @staticmethod
    def from_int(i, n=0):
        return Bitlist(Bitlist._to_binary(i, n))

    @staticmethod
    def from_hex(hex_list):
        bitlist = Bitlist()
        for hex_ in hex_list:
            bitlist += Bitlist.from_int(int(hex_, 16), 4)
        return bitlist

    @staticmethod
    def from_str(string):
        return Bitlist([int(i) for i in string])

    @staticmethod
    def from_list(list_):
        bitlist = Bitlist()
        bitlist.bits = list_
        return bitlist

    @staticmethod
    def from_bitlist(bitlist):
        new_bitlist = Bitlist()
        new_bitlist.bits = bitlist.bits.copy()
        return new_bitlist

    def shuffle(self):
        flipped = [1 if bit == 0 else 0 for bit in self.bits]
        shift_amount = self.shuffle_shift_amount

        shifted = []
        for i in range(len(flipped)):
            shifted.append(flipped[(i + shift_amount) % len(flipped)])

        reverse_shifted = list(reversed(shifted))

        shuffled_bitlist = Bitlist.from_list(reverse_shifted)
        return shuffled_bitlist

    def unshuffle(self):
        reverse = list(reversed(self.bits))

        shift_amount = self.shuffle_shift_amount
        shifted = []
        for i in range(len(reverse)):
            shifted.append(reverse[(i - shift_amount) % len(reverse)])

        flipped = [1 if bit == 0 else 0 for bit in shifted]

        unshuffled_bitlist = Bitlist.from_list(flipped)
        return unshuffled_bitlist

    @staticmethod
    def readable_str(bits):
        bit_string = ""
        for i, bit in enumerate(bits):
            bit_string += str(bit)
            if (i + 1) % 4 == 0 and i < len(bits) - 1:
                bit_string += " "
        return bit_string

    def to_int(self):
        total = 0
        for i, bit in enumerate(reversed(self.bits)):
            total += bit * 2 ** i
        return total

    def __str__(self):
        return self.readable_str(self.bits)

    def __repr__(self):
        return self.readable_str(self.bits)

    def __add__(self, other):
        return Bitlist.from_list(self.bits + other.bits)

    def __len__(self):
        return len(self.bits)

    def __eq__(self, other):
        if len(self.bits) != len(other.bits):
            return False

        for bit1, bit2 in zip(self.bits, other.bits):
            if bit1 != bit2:
                return False

        return True

    @staticmethod
    def _to_binary(x, n=0):
        return [int(i) for i in "{0:b}".format(x).zfill(n)]
