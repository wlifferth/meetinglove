from random import SystemRandom

def generateKey(size=10):
    key = ''.join(SystemRandom().choice(list('abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789')) for _ in range(size))
    return key
