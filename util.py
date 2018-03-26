# The functions in this file are to be implemented by students.

import bitio
import huffman

def read_tree(bitreader):
    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeLeaf that is None (the special "end of message" character)
          is represented by the two bits 00.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
    '''

    while True:
        try:
            bit = bitreader.readbit()
            if bit == 1: # branch is indicated by a 1
                left = read_tree(bitreader)
                right = read_tree(bitreader)
                tree_part = huffman.TreeBranch(left, right)
            elif bit == 0: # leaf is indicated by a 0
                bit = bitreader.readbit()
                if bit == 1: # 01 is a 'symbol'
                    symbol = bitreader.readbits(8)
                    tree_part = huffman.TreeLeaf(symbol)
                elif bit == 0: # 00 is the EOF symbol
                    tree_part = huffman.TreeLeaf(None)

            return tree_part
        except:
            break


def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leave is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    #read bits from the bit reader

    current = tree

    while True:
        try:
            bit = bitreader.readbit()
            # print(bit)
        except EOFError:
            raise Exception("SOMETHING BROKE")
            break

        if bit:
            #go right
            # print('going right')
            current = current.right
        else:
            #go left
            # print('going left')
            current = current.left
        if type(current) == type(huffman.TreeLeaf(0)):
            break

    return current.value

    # #traverse the tree based on bits
    # while type(tree_part)=="TreeBranch"#not at a leaf:
    #     if not bit: #bit==0
    #         pass
    #         #go left
    #     elif bit: #bit=1
    #         pass
    #     bit = bitreader.bit()
    #
    #     if type(tree_part)=="TreeLeaf": #at a leaf
    #         return tree_part.value



def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.

    '''

    bitreader = bitio.BitReader(compressed)
    bitwriter = bitio.BitWriter(uncompressed)

    # read the tree from the compressed stream
    tree = read_tree(bitreader)

    # keep decoding bytes and writing to the uncompressed stream until the
    # EOF symbol is reached
    while True:
        decoded = decode_byte(tree, bitreader)
        if decoded == None:
            break
        bitwriter.writebits(decoded,8)


def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''

    if type(tree)==type(huffman.TreeBranch(0,0)):
        # tree branch bit code is 1
        bitwriter.writebit(True)
        # write the bits for the children
        write_tree(tree.left, bitwriter)
        write_tree(tree.right, bitwriter)
    elif type(tree) == type(huffman.TreeLeaf(0)):
        if tree.value == None:
            # EOF bit code is 00
            bitwriter.writebit(False)
            bitwriter.writebit(False)
        else:
            # code for a leaf is 01 followed by the 8 bit leaf symbol
            bitwriter.writebit(False)
            bitwriter.writebit(True)
            symbol = tree.value
            bitwriter.writebits(symbol,8)



def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''

    bitwriter = bitio.BitWriter(compressed)
    bitreader = bitio.BitReader(uncompressed)

    # table maps the byte of a leaf node to a tuple containiing the bit sequence
    table = huffman.make_encoding_table(tree)

    write_tree(tree, bitwriter)

    # holds the bits written to the compressed stream
    bit_count = 0

    # read bits from the uncompressed stream until there are none left
    while True:
        try:
            symbol = bitreader.readbits(8)
        except:
            break

        # write the bit sequence for the symbol read
        encoded = table[symbol]
        for bit in encoded:
            bit_count += 1
            bitwriter.writebit(bit)

    # write the end of file message
    for bit in table[None]:
        bit_count += 1
        bitwriter.writebit(bit)

    # pad with zeros if there are partial bytes
    remaining = bit_count % 8
    if remaining != 0:
        for i in range(remaining):
            bitwriter.writebit(False)

    bitwriter.flush()
