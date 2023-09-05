# Author: Marco Simoes
# Adapted from Java's implementation of Rui Pedro Paiva
# Teoria da Informacao, LEI, 2022

import sys
from huffmantree import HuffmanTree
import os

class GZIPHeader:
    """ class for reading and storing GZIP header fields """

    ID1 = ID2 = CM = FLG = XFL = OS = 0
    MTIME = []
    lenMTIME = 4
    mTime = 0

    # bits 0, 1, 2, 3 and 4, respectively (remaining 3 bits: reserved)
    FLG_FTEXT = FLG_FHCRC = FLG_FEXTRA = FLG_FNAME = FLG_FCOMMENT = 0

    # FLG_FTEXT --> ignored (usually 0)
    # if FLG_FEXTRA == 1
    XLEN, extraField = [], []
    lenXLEN = 2

    # if FLG_FNAME == 1
    fName = ''  # ends when a byte with value 0 is read

    # if FLG_FCOMMENT == 1
    fComment = ''  # ends when a byte with value 0 is read

    # if FLG_HCRC == 1
    HCRC = []

    def read(self, f):
        """ reads and processes the Huffman header from file. Returns 0 if no error, -1 otherwise """

        # ID 1 and 2: fixed values
        self.ID1 = f.read(1)[0]
        if self.ID1 != 0x1f: return -1  # error in the header

        self.ID2 = f.read(1)[0]
        if self.ID2 != 0x8b: return -1  # error in the header

        # CM - Compression Method: must be the value 8 for deflate
        self.CM = f.read(1)[0]
        if self.CM != 0x08: return -1  # error in the header

        # Flags
        self.FLG = f.read(1)[0]

        # MTIME
        self.MTIME = [0] * self.lenMTIME
        self.mTime = 0
        for i in range(self.lenMTIME):
            self.MTIME[i] = f.read(1)[0]
            self.mTime += self.MTIME[i] << (8 * i)

        # XFL (not processed...)
        self.XFL = f.read(1)[0]

        # OS (not processed...)
        self.OS = f.read(1)[0]

        # --- Check Flags
        self.FLG_FTEXT = self.FLG & 0x01
        self.FLG_FHCRC = (self.FLG & 0x02) >> 1
        self.FLG_FEXTRA = (self.FLG & 0x04) >> 2
        self.FLG_FNAME = (self.FLG & 0x08) >> 3
        self.FLG_FCOMMENT = (self.FLG & 0x10) >> 4

        # FLG_EXTRA
        if self.FLG_FEXTRA == 1:
            # read 2 bytes XLEN + XLEN bytes de extra field
            # 1st byte: LSB, 2nd: MSB
            self.XLEN = [0] * self.lenXLEN
            self.XLEN[0] = f.read(1)[0]
            self.XLEN[1] = f.read(1)[0]
            self.xlen = self.XLEN[1] << 8 + self.XLEN[0]

            # read extraField and ignore its values
            self.extraField = f.read(self.xlen)

        def read_str_until_0(f):
            s = ''
            while True:
                c = f.read(1)[0]
                if c == 0:
                    return s
                s += chr(c)

        # FLG_FNAME
        if self.FLG_FNAME == 1:
            self.fName = read_str_until_0(f)

        # FLG_FCOMMENT
        if self.FLG_FCOMMENT == 1:
            self.fComment = read_str_until_0(f)

        # FLG_FHCRC (not processed...)
        if self.FLG_FHCRC == 1:
            self.HCRC = f.read(2)

        return 0


class GZIP:
    ''' class for GZIP decompressing file (if compressed with deflate) '''

    gzh = None
    gzFile = ''
    fileSize = origFileSize = -1
    numBlocks = 0
    f = None

    bits_buffer = 0
    available_bits = 0

    def __init__(self, filename):
        self.gzFile = filename
        self.f = open(filename, 'rb')
        self.f.seek(0, 2)
        self.fileSize = self.f.tell()
        self.f.seek(0)

    def decompress(self):
        ''' main function for decompressing the gzip file with deflate algorithm '''

        numBlocks = 0

        # get original file size: size of file before compression
        origFileSize = self.getOrigFileSize()
        print(origFileSize)

        # read GZIP header
        error = self.getHeader()
        if error != 0:
            print('Formato invalido!')
            return

        # show filename read from GZIP header
        print(self.gzh.fName)

        # MAIN LOOP - decode block by block
        BFINAL = 0
        final = open(self.getFinalFileName(), "wb+")
        output_buffer = []
        while not BFINAL == 1:

            BFINAL = self.readBits(1)
            BTYPE = self.readBits(2)
            if BTYPE != 2:
                print('Error: Block %d not coded with Huffman Dynamic coding' % (numBlocks + 1))
                return

            H_LIT, H_DIST, H_CLEN = self.getConstants()
            symbol_order = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
            # Obter os dados acerca do comprimento dos símbolos do alfabeto (comprimentos, valores e criar a árvore)
            HCLEN_lens = self.getCodeLEN(symbol_order, H_CLEN + 4)
            HCLEN_values = self.getValues(HCLEN_lens)
            HCLEN_tree = self.createHuffmanTree(HCLEN_lens, HCLEN_values)

            # Obter os dados dos literais (comprimentos, valores e criar a árvore)
            HLIT_lens = self.getLengths(HCLEN_tree, H_LIT + 257)
            HLIT_values = self.getValues(HLIT_lens)
            HLIT_tree = self.createHuffmanTree(HLIT_lens, HLIT_values)

            # Obter os dados das distâncias (comprimentos, valores e criar a árvore)
            HDIST_lens = self.getLengths(HCLEN_tree, H_DIST + 1)
            HDIST_values = self.getValues(HDIST_lens)
            HDIST_tree = self.createHuffmanTree(HDIST_lens, HDIST_values)

            # Criar tabela de descodificação para o tamanho
            codigo_lengths = [i for i in range(257, 285)]
            lengths_range = [[3, 3]]
            lengths_increase_index = [8, 12, 16, 20, 24]
            length_alphabet = self.createAlphabet(codigo_lengths, lengths_range, lengths_increase_index)
            length_alphabet[285] = (0, (285, 285))

            # Criar tabela de descodificação para a distância
            codigo_dist = [i for i in range(30)]
            dist_range = [[1, 1]]
            dist_increase_index = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
            dist_alphabet = self.createAlphabet(codigo_dist, dist_range, dist_increase_index)

            # Verificar valores
            # print("LEN \n",HCLEN_lens,"\n",HCLEN_values)
            # print("LIT \n", HLIT_lens, "\n", HLIT_values,"\n")
            # print("DIST \n", HDIST_lens, "\n", HDIST_values,"\n")
            # print("Tabela Length\n",length_alphabet)
            # print("Tabela distance\n",dist_alphabet)

            # Ler e interpretar os dados
            output_buffer.extend(self.getData(HLIT_tree, HDIST_tree, length_alphabet, dist_alphabet))
            # update number of blocks read
            numBlocks += 1
        final.write(bytes(output_buffer))
        self.f.close()
        final.close()

    print("End: %d block(s) analyzed." % numBlocks)

    def getOrigFileSize(self):
        ''' reads file size of original file (before compression) - ISIZE '''

        # saves current position of file pointer
        fp = self.f.tell()

        # jumps to end-4 position
        self.f.seek(self.fileSize - 4)

        # reads the last 4 bytes (LITTLE ENDIAN)
        sz = 0
        for i in range(4):
            sz += self.f.read(1)[0] << (8 * i)

        # restores file pointer to its original position
        self.f.seek(fp)

        return sz

    def getHeader(self):
        ''' reads GZIP header'''

        self.gzh = GZIPHeader()
        header_error = self.gzh.read(self.f)
        return header_error

    def readBits(self, n, keep=False):
        ''' reads n bits from bits_buffer. if keep = True, leaves bits in the buffer for future accesses '''

        while n > self.available_bits:
            self.bits_buffer = self.f.read(1)[0] << self.available_bits | self.bits_buffer
            self.available_bits += 8

        mask = (2 ** n) - 1
        value = self.bits_buffer & mask

        if not keep:
            self.bits_buffer >>= n
            self.available_bits -= n

        return value

    def getFinalFileName(self):
        original = self.gzh.fName
        i = 2
        nome= original
        while (os.path.exists("./" + nome)):
            nome = original[:-4] + ' ' + str(i) + original[-4:]
            i += 1
        return nome

    def getConstants(self):
        H_LIT = self.readBits(5)
        H_DIST = self.readBits(5)
        H_CLEN = self.readBits(4)
        return H_LIT, H_DIST, H_CLEN

    def getCodeLEN(self, symbol_order, search_limit):
        CLEN_lens = [0] * len(symbol_order)
        for i in range(search_limit):
            CLEN_lens[symbol_order[i]] = self.readBits(3)
        return CLEN_lens

    def getLengths(self, CODE_tree, search_limit):
        lengths_array = []
        pastNumber = 0
        i = 0
        while (i < search_limit):
            val = -1
            while val < 0:
                bit = str(self.readBits(1))
                val = CODE_tree.nextNode(bit)

            CODE_tree.resetCurNode()

            if (val == 16):
                repeat = self.readBits(2)
                repeatInt = 3 + repeat
                for k in range(repeatInt):
                    lengths_array.append(pastNumber)
                i += repeatInt
            elif (val == 17):
                repeat = self.readBits(3)
                repeatInt = 3 + repeat
                for k in range(repeatInt):
                    lengths_array.append(0)
                i += repeatInt
            elif (val == 18):
                repeat = self.readBits(7)
                repeatInt = 11 + repeat
                for k in range(repeatInt):
                    lengths_array.append(0)
                i += repeatInt
            else:
                pastNumber = val
                lengths_array.append(val)
                i += 1
        return lengths_array

    def getValues(self, length_array):
        MAX_BITS = max(length_array)
        MAX_CODE = len(length_array)
        blCount = [0] * MAX_CODE
        nextCode = [0] * MAX_CODE
        code = 0
        values_array = [0] * MAX_CODE
        for i in length_array:
            blCount[i] += 1
        blCount[0] = 0
        for bits in range(1, MAX_BITS + 1):
            code = (code + blCount[bits - 1]) << 1
            nextCode[bits] = code
        for i in range(MAX_CODE):
            length = length_array[i]
            if length:
                values_array[i] = nextCode[length]
                nextCode[length] += 1
        return values_array

    def createHuffmanTree(self, lengths_array, values_array):
        tree = HuffmanTree()
        for i in range(len(lengths_array)):
            if lengths_array[i]:
                bin_n = format(values_array[i], '0' + str(lengths_array[i]) + 'b')
                tree.addNode(bin_n, i)
        return tree

    def createAlphabet(self, codigo, values_range, increase_index):
        extra_bit = 0
        bits_to_read = [0]
        for i in range(1, len(codigo)):
            if i in increase_index:
                extra_bit += 1
            bits_to_read.append(extra_bit)
            temporary_list = [values_range[i - 1][1] + 1, values_range[i - 1][1] + (2 ** extra_bit)]
            values_range.append(temporary_list)
        alphabet_dict = dict(zip(codigo, zip(bits_to_read, values_range)))
        return alphabet_dict

    def decodeDist(self, HDIST_tree, dist_alphabet):
        extra_dist = 0
        val = -1
        while (val < 0):
            bit1 = str(self.readBits(1))
            val = HDIST_tree.nextNode(bit1)
        HDIST_tree.resetCurNode()

        if (dist_alphabet[val][0] > 0):
            extra_dist = self.readBits(dist_alphabet[val][0])

        return dist_alphabet[val][1][0] + extra_dist

    def decodeLength(self, val, length_alphabet):
        if (val > 256):
            extra_length = 0
            if length_alphabet[val][0] != 0:
                extra_length = self.readBits(length_alphabet[val][0])
            length = length_alphabet[val][1][0] + extra_length
            return length

    def getData(self, HLIT_tree, HDIST_tree, length_alphabet, dist_alphabet):
        val = 0
        output_buffer = []
        while val != 256:
            val = -1
            while val < 0:
                bit = str(self.readBits(1))
                val = HLIT_tree.nextNode(bit)
            HLIT_tree.resetCurNode()
            if val <= 255:
                output_buffer.append(val)
            elif val > 256:
                length = self.decodeLength(val, length_alphabet)
                dist = self.decodeDist(HDIST_tree, dist_alphabet)
                indice = (len(output_buffer) - dist)
                split = output_buffer[indice: indice + length]
                if (length > dist):
                    for i in range((int)(length / dist)):
                        output_buffer.extend(split)
                else:
                    output_buffer.extend(split)
        return output_buffer


if __name__ == '__main__':

    # gets filename from command line if provided
    fileName = "FAQ.txt.gz"
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

    # decompress file
    gz = GZIP(fileName)
    gz.decompress()
