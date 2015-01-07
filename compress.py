'''
Created on 07.01.2015

@author: dddsnn
'''

import bitstring as bs

def order_enc(bits, sample_len):
    if len(bits) % sample_len:
        raise ValueError('Input not divisible by sample length')
    res = bs.BitStream()
    num_samples = len(bits) // sample_len
    for i in range(sample_len):
        for s in range(num_samples):
            pos = s * sample_len + i
            res += bits[pos:pos + 1]
    return res

def order_dec(bits, sample_len):
    if len(bits) % sample_len:
        raise ValueError('Input not divisible by sample length')
    res = bs.BitStream()
    num_samples = len(bits) // sample_len
    for s in range(num_samples):
        for i in range(sample_len):
            pos = i * num_samples + s
            res += bits[pos:pos + 1]
    return res

def mtf_enc(bits):
    res = bs.BitStream()
    last = False
    for b in bits:
        if b == last:
            res += bs.Bits('0b0')
        else:
            res += bs.Bits('0b1')
            last = b
    return res

def mtf_dec(bits):
    res = bs.BitStream()
    last = bs.BitStream('0b0')
    for b in bits:
        if b == True:
            last.invert()
        res += last
    return res

def rl_enc(bits):
    def write_zeros():
        nonlocal res
        res += bs.Bits('0b0')
        x = bs.Bits(ue=zero_count)
        res += x
    res = bs.BitStream()
    zero_count = 0
    for b in bits:
        if b:
            # write zeros first
            if zero_count:
                write_zeros()
                zero_count = 0
            # just write 1's normally, they're rare
            res += bs.Bits('0b1')
        else:
            zero_count += 1
    # write any remaining zeros
    if zero_count:
        write_zeros()
    return res

def rl_dec(bits):
    res = bs.BitStream()
    while bits.pos != bits.len:
        b = bits.read('bits:1')
        if b[0]:
            res += b
        else:
            num_zeros = bits.read('ue')
            res += bs.Bits(num_zeros)
    return res

def compress(bits, sample_len):
    reordered = order_enc(bits, sample_len)
    mtfed = mtf_enc(reordered)
    return rl_enc(mtfed)

def decompress(bits, sample_len):
    rl_decoded = rl_dec(bits)
    un_mtfed = mtf_dec(rl_decoded)
    return order_dec(un_mtfed, sample_len)

if __name__ == '__main__':
    # sample size 1
    test1 = bs.Bits('0b00011111111111111000111111111111110010001111111111111111111111100010000000000000')
    # sample size 13
    test2 = bs.Bits('0b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000100000000000010000000000001000000000000100000000000010000000000001000000000000100000000000010100000000001010000000000101000000000010100000000001000000000000100000000000010000000000001010000000000100000000000010000000000001001000000000100100000000010000000000001000000000000101000000000010100000000001000000000000100000000000010000000000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001010010000000101001000000010000000000001000000000000100100000000010010000000001010010000000101001000000010000100000001001010000000100101000000010100100000001010010000000100001000000010000100000001000000000001100000000000110000000000001000000000000100000000000010000000000001000010000000100001000000010000100000001000010000001100001000000110000100000011000010000001100001000000010000100000001000010000000100001000000010000000000001000000000000100000000000010000000000001000000000000100000000000010000000000001000000000000100000000100010000000010001000000000000100000000000010000000000001100000000000110000000000011000000000001000000000000100000000000010000000000001000000000000100100000000010010000000001000000000000100000000000010000000000001000000000000100000000000010100000000001000000000000100000000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000100001000000010000100000001000010000000101001000000010100000000001010000000000100000000000010010000000001001000000000100000100000000000010000000010001000000001000100000010010010000001001001000000100100100000010000010000001000001000000100000100000010100010000001010001000000100000000000010000001000001000000100000100000010000000000011000000000001000000000000100000000000010000000000001000000100000100000010000000000001000000100000100000010000010000001000001000000100000100001010000010000101000001000010100000100001010000010000101000001000000100000100000010000010000001000001000100100000100010010000010001001000001000000100000100000010000010000001000001000000100000100000010000010000001000001000000100000100000010000010000001000001000000100000000000110000000000011000000000001100000000000110000010000001000001000000100000100000010000010000001000001000')
    print(len(test2))
    print(len(compress(test2, 13)))
    print(decompress(compress(test2, 13), 13) == test2)
#     print(mtf_dec(mtf_enc(test2)) == test2)
#     print(test2)
#     print(order_enc(test2, 13))