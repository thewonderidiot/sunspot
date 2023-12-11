import array
import os

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


fn = '1003733-281.bin'
data = array.array('H')
with open(fn, 'rb') as f:
    data.fromfile(f, int(os.path.getsize(fn)/2))
    data.byteswap()

bs = 0
bsing = False
bank_idx = 0
banks = [0o12, 0o13, 0o32, 0o33]
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

    # if (bank in [0o12,0o13] and addr >= 0o6000 and addr < 0o6400) and (actual != expected):
    #     w ^= 0o40

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
