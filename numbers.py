#!c:\python\python.exe

import random
import struct

########################################################################################################################
class bit_field (object):
    '''

    @alias: bits
    '''

    BIG_ENDIAN    = 0
    LITTLE_ENDIAN = 1

    ####################################################################################################################
    def __init__ (self, width, value=0, max_num=None, static=False):
        self.defaultval = value # this assignment will be persistent via fuzzing ('cause we edit in memory)
        self.width      = width
        self.max_num    = max_num
        self.value      = value
        self.endian     = self.LITTLE_ENDIAN
        self.static     = static

        if self.max_num == None:
            self.max_num = self.to_decimal("1" * width)


    ####################################################################################################################
    def flatten (self):
        '''
        Convert

        @rtype:  Raw Bytes
        @return: Raw byte representation
        '''

        if not type(self.value) == int:
            # xxx - this has to be changed to have no knowledge of inherited classes.
            if isinstance(self, byte):
                self.value = struct.unpack("B", self.value)
                self.value = self.value[0]
            elif isinstance(self, word):
                self.value = struct.unpack("i", self.value)
                self.value = self.value[0]
            elif isinstance(self, dword):
                self.value = struct.unpack("l", self.value)
                self.value = self.value[0]
            elif isinstance(self, qword):
                self.value = struct.unpack("q", self.value)
                self.value = self.value[0]

        # pad the bit stream to the next byte boundary.
        bit_stream = ""

        if self.width % 8 == 0:
            bit_stream += self.to_binary()
        else:
            bit_stream  = "0" * (8 - (self.width % 8))
            bit_stream += self.to_binary()


        flattened = ""

        # convert the bit stream from a string of bits into raw bytes.
        for i in xrange(len(bit_stream) / 8):
            chunk = bit_stream[8*i:8*i+8]
            flattened += struct.pack("B", self.to_decimal(chunk))

        # if necessary, convert the endianess of the raw bytes.
        if self.endian == self.LITTLE_ENDIAN:
            flattened = list(flattened)
            flattened.reverse()
            flattened = "".join(flattened)

        return flattened

    ####################################################################################################################
    def to_binary (self, number=None, bit_count=None):
        '''
        description

        @type number:     Integer
        @param number:    (Optional, def=self.value) Number to convert
        @type bit_count:  Integer
        @param bit_count: (Optional, def=self.width) Width of bit string

        @rtype:  String
        @return: Bit string
        '''

        if number == None:
            number = self.value

        if bit_count == None:
            bit_count = self.width

        return "".join(map(lambda x:str((number >> x) & 1), range(bit_count -1, -1, -1)))


    ####################################################################################################################
    def to_decimal (self, binary):
        return int(binary, 2)

    ####################################################################################################################
    def fuzz (self):
        cases = \
        [
            self.max_num,
            self.max_num / 2,
            self.max_num / 4,
        ]

        if isinstance(self, byte):
            self.value = struct.pack("B", self.max_num)
        elif isinstance(self, word):
            self.value = struct.pack("I", self.max_num)
        elif isinstance(self, dword):
            self.value = struct.pack("L", self.max_num)
        elif isinstance(self, qword):
            self.value = struct.pack("Q", self.max_num)

    ####################################################################################################################
    def reset (self):
        self.value = self.defaultval

########################################################################################################################
class byte (bit_field):
    def __init__ (self, value=0, max_num=None, static=False):
        bit_field.__init__(self, 8, value=struct.pack("B", value), max_num=max_num, static=static)


########################################################################################################################
class word (bit_field):
    def __init__ (self, value=0, max_num=None, static=False):
        bit_field.__init__(self, 16, value=struct.pack("i", value), max_num=max_num, static=static)


########################################################################################################################
class dword (bit_field):
    def __init__ (self, value=0, max_num=None, static=False):
        bit_field.__init__(self, 32, value=struct.pack("l", value), max_num=max_num, static=static)


########################################################################################################################
class qword (bit_field):
    def __init__ (self, value=0, max_num=None, static=False):
        bit_field.__init__(self, 64, value=struct.pack("q", value), max_num=max_num, static=static)


########################################################################################################################


# class aliases
bits   = bit_field
char   = byte
short  = word
long   = dword
double = qword