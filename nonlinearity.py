top = 256
gamma = 1.5

def compensate(original):
    # print(original)
    original = int(original)
    if original == 0:
        return 0
    return int((original ** gamma) * (top ** (1 - gamma)))
