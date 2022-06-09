from tear.colours import Colour, ColourRange, lst2colours


def read_colour_transition(s):
    ran = s.split('->')
    rc = ran[1].split('*')
    from_c = read_single_colour(ran[0])
    to_c = read_single_colour(rc[0])
    count = int(rc[1])
    return ColourRange.fromranges(from_c, to_c, count)


def read_single_colour(s):
    if '->' in s:
        return read_colour_transition(s)
    if ',' in s:
        lst = s.split(',')
        return ColourRange(lst2colours(lst))
    if ':' in s:
        lst = s.split(':')
        if '/' in lst[-1]:
            lst2 = lst[-1].split('/')
            lst[-1] = lst2[0]
            count = int(lst2[1])
            return ColourRange.fromlist(lst2colours(lst), count)
        return ColourRange(lst2colours(lst))
    return Colour.fromstr(s)


def read_colour_list(lst):
    r = ColourRange([])
    for cs in lst:
        c = read_single_colour(cs)
        if isinstance(c, ColourRange):
            r.extend(c)
        else:
            r.range.append(c)
    return r
