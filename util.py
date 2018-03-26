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
            if bit == 1:
                left = read_tree(bitreader)
                right = read_tree(bitreader)
                tree_part = huffman.TreeBranch(left, right)
            elif bit == 0:
                bit = bitreader.readbit()
                if bit == 1:
                    symbol = bitreader.readbits(8)
                    tree_part = huffman.TreeLeaf(symbol)
                elif bit == 0:
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
            current = tree.right
        else:
            #go left
            # print('going left')
            current = tree.left
        if type(current) == type(huffman.TreeLeaf(0)): break
    return chr(current.value)

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
    pass
    #probably definitely wrong but I'm just writing
    #what I'm thinking at to moment to try to make sense of this

    #should be the compressed info from the bitstream I think
    cmptree = read_tree(compressed)

    #while
    #rest of input stream
    decoded= decode_byte(tree)
    #add decoded byte to uncompressed tree
    #end while

    #finally, write the tree
    write_tree(uncompressed)

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
        # print(1)
        bitwriter.writebit(True)
        write_tree(tree.left, bitwriter)
        write_tree(tree.right, bitwriter)
    elif type(tree) == type(huffman.TreeLeaf(0)):
        if tree.value == None:
            bitwriter.writebit(False)
            bitwriter.writebit(False)
            # print(0)
            # print(0)

        else:
            bitwriter.writebit(False)
            bitwriter.writebit(True)
            # print(0)
            # print(1)
            symbol = tree.value
            # print(symbol)
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

    write_tree(tree, compressed)


    #flush bitwriter
    pass
