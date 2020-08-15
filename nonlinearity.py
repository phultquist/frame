top = 256

def compensate(original):
    return int((original * original) / top)