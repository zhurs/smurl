symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
base = len(symbols)
n2s = dict(enumerate(symbols))
s2n = dict( [(b,a) for (a,b) in n2s.items()] )

def smurl_encode(num):
    ret = ''
    while num > 0:
        num, digit = divmod(num, base)
        ret = n2s[digit] + ret
    if ret == '':
        ret = n2s[0]
    return ret

def smurl_decode(str):
    ret = 0;
    for i in str:
        if i in s2n:
            ret = ret * base + s2n[i]
    return ret
