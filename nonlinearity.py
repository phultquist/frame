top = 256

def compensate(original):
    # print(original)
    original = int(original)
    if original == 0:
        return 0
    return int((original * original) / top)