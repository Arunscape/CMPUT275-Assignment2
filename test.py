import bitio
import huffman
import util

with open("simple.txt", 'wb') as file:
    writer = bitio.BitWriter(file)

    tree = huffman.TreeBranch(huffman.TreeBranch(huffman.TreeLeaf(ord('A')),huffman.TreeLeaf(None)),huffman.TreeLeaf(ord('B')))
    util.write_tree(tree, writer)
    writer.flush()

with open("simple.txt", 'rb') as file:
    reader = bitio.BitReader(file)
    new_tree = util.read_tree(reader)

with open("simple.txt", 'wb') as file:
    writer = bitio.BitWriter(file)

    print("Hey bitch")
    util.write_tree(new_tree, writer)
    writer.flush()

#==============================================================================
#==============================================================================
with open("simple.txt",'wb') as f:
    f.write(b'00')
with open("simple.txt", 'rb') as file:
    reader = bitio.BitReader(file)
    tree = huffman.TreeBranch(huffman.TreeBranch(huffman.TreeLeaf(ord('A')),huffman.TreeLeaf(None)),huffman.TreeLeaf(ord('B')))
    print(util.decode_byte(tree,reader))
