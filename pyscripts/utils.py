def levels(line):
    levels = line.split(' ')[0]
    if levels[-1] == '.':
        return levels[:-1]
    else:
        return levels

def zone_names(line):
    zone_name = line.split('.')[-1]
    zone_name = zone_name.split(" ", 1)[1]
    return zone_name.strip()