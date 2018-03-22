import bitio
import util

with open("simple.txt", 'rb') as file:
    reader = bitio.BitReader(file)
    tree = util.read_tree(reader)
    print(type(tree))
