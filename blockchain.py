
class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def last_block(self):
        if len(self.blocks) == 0:
            return None
        return self.blocks[-1]


class Block:
    def __init__(self, solution):
        self.solution = solution

