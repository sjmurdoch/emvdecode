from IPython.display import HTML, display
from binascii import a2b_hex, b2a_hex

def to_bin(x, to_list = False):
    '''Convert a byte (as a string) to bits. If to_list is False, returns a string.
    If to_list is True returns a list of characters'''
    x = int(x, 16)
    if x > 0xff or x < 0x00:
        raise Exception("Value will not fit in one byte", x)
    s = format(x, '08b')
    if to_list:
        return list(s)
    else:
        return s

def strip_bytes(s):
    '''Remove whitespace from a string of hex bytes'''
    s = s.lower().split()
    s = "".join(s)
    if len(s) % 2:
        raise Exception("Not a multiple of two characters")
    return "".join(s)

def split_bytes(s):
    '''Remove whitespace from a string and split into pairs of characters'''
    s = strip_bytes(s)
    return " ".join([s[i:i+2] for i in range(0, len(s), 2)])

def len_bytes(s):
    '''Count number of bytes in a hex string'''
    return int(len(strip_bytes(s)) / 2)

def decode_bytes(s):
    return a2b_hex(strip_bytes(s)).decode('iso8859-1', errors='replace')

def format_bytes(x, pattern=[8], do_display=True):
    '''Return an HTML table showing bits in a byte.
    Pattern shows how many bits to show on each row.'''
    if sum(pattern) != 8:
        raise Exception("Pattern must use all 8 bits")
    b = to_bin(x, True)
    header = '<tr>{}{}</tr>'.format(
        "<td>0x{:02x} =</td>".format(int(x, 16)),
        "".join(['<th>b{}</th>'.format(i) for i in range(8,0,-1)]))
    rows = []
    i = 0
    for nbits in pattern:
        cells = []
        cells.append('<td></td>')
        for padding in range(i):
            cells.append('<td>-</td>')
        for col in range(nbits):
            cells.append('<td>{}</td>'.format(b[i]))
            i += 1
        for padding in range(8-i):
            cells.append('<td>-</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    table = "<table>" + header + "\n" + "\n".join(rows) + "</table>"
    if do_display:
        display(HTML(table))
        return None
    else:
        return table

def take(s, count=None, start=0):
    '''Take count bytes from a hex string, starting at position start'''
    s = strip_bytes(s)
    if not count is None:
        s = s[start * 2:start*2 + count*2]
    else:
        s = s[start * 2:]
    return split_bytes(s)
