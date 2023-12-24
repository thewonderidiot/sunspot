import array
import os

bank25_bit16 = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1]

bank30_bit16 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

def calc_parity(w):
    p = 1
    for i in range(15):
        if i == 14:
            i += 1

        if (w & (1 << i)):
            p ^= 1

    return p

def add(x, y):
    x = ((x & 0o40000) << 1) | x
    y = ((y & 0o40000) << 1) | y
    u = x + y
    if u & 0o200000:
        u = (u & 0o177777) + 1
    if (u & 0o140000) == 0o040000:
        u += 1
    elif (u & 0o140000) == 0o100000:
        u -= 1

    u = ((u & 0o100000) >> 1) | (u & 0o37777)
    return u

fn = '1003733-251.bin'
data = array.array('H')
with open(fn, 'rb') as f:
    data.fromfile(f, int(os.path.getsize(fn)/2))
    data.byteswap()

bs = 0
bsing = False
bank_idx = 0
banks = [0o10, 0o05, 0o30, 0o25]
bank = banks[0]
for i,w in enumerate(data):
    if (i % 1024) == 0:
        bs = 0
        bsing = True
        addr = 0o5777
        bank = banks[bank_idx]
        bank_idx += 1

    addr += 1

    actual = (w >> 14) & 1
    expected = calc_parity(w)

    if (bank in [0o5,0o10] and addr < 0o6400) and (actual != expected):
        w ^= 0o100000
    elif (bank in [0o5,0o10] and addr >= 0o6400 and addr < 0o7000) and (actual != expected):
        w ^= 0o4000
    elif (bank in [0o5,0o10] and addr >= 0o7000 and addr < 0o7400) and (actual != expected):
        w ^= 0o100000
    elif (bank in [0o25,0o30] and addr >= 0o6000 and addr < 0o6400) and (actual != expected):
        w ^= 0o4000
    elif (bank in [0o25,0o30] and addr >= 0o7400) and (actual != expected):
        w ^= 0o10000

    if (bank == 0o25 and addr >= 0o7000 and addr < 0o7400):
        if bank25_bit16[addr - 0o7000]:
            w |= 0o100000
        else:
            w &= ~0o100000
        expected = calc_parity(w)
        if actual != expected:
            w ^= 0o10

    if (bank == 0o30 and addr >= 0o7000 and addr < 0o7400):
        if bank30_bit16[addr - 0o7000]:
            w |= 0o100000
        else:
            w &= ~0o100000
        expected = calc_parity(w)
        if actual != expected:
            w ^= 0o10

    if bank == 0o25 and addr >= 0o7772:
        w = 0
    if bank == 0o30 and addr >= 0o7751:
        w = 0

    if bsing:
        if w == 0:
            print('Banksum = %05o' % bs)
            bsing = False
        bs = add(bs, ((w & 0o100000) >> 1) | (w & 0o37777))

    print('%02o,%04o  %05o %o' % (bank,addr,((w & 0o100000) >> 1) | (w & 0o37777),actual),end='')

    if actual != expected:
        if bsing:
            print('  !')
        elif w != 0:
            print('  !')
        else:
            print('')
    else:
        print('')

    data[i] = w

data.byteswap()
with open(fn.replace('.bin','_fixed.bin'), 'wb') as f:
    data.tofile(f)
