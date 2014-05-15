keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def getCharSafe(strin, index, func, oth):
    try:
        return func(strin[index])
    except Exception:
        pass
    return oth


def decodeString(to_dec):
    output = ""
    i = 0
    while i < len(to_dec):

        enc1 = getCharSafe(to_dec, i, keyStr.find, 0)
        i += 1
        enc2 = getCharSafe(to_dec, i, keyStr.find, 0)
        i += 1
        enc3 = getCharSafe(to_dec, i, keyStr.find, 0)
        i += 1
        enc4 = getCharSafe(to_dec, i, keyStr.find, 0)
        i += 1
        
        chr1 = (enc1 << 2) | (enc2 >> 4)
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
        chr3 = ((enc3 & 3) << 6) | enc4

        output = output + chr(chr1)
        
        if enc3 != 64:
            output = output + chr(chr2)

        if enc4 != 64:
            output = output + chr(chr3)
    return output


def encodeString(to_enc):
    output = ""
    i = 0
    while i < len(to_enc):
        chr1 = getCharSafe(to_enc, i, ord, 0)
        i += 1
        chr2 = getCharSafe(to_enc, i, ord, 0)
        i += 1
        chr3 = getCharSafe(to_enc, i, ord, 0)
        i += 1

        enc1 = chr1 >> 2
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
        enc4 = chr3 & 63

        if chr2 == 0:
            enc3 = 64
            enc4 = 64
        elif chr3 == 0:
            enc4 = 64

        output = output + keyStr[enc1] + keyStr[enc2] + keyStr[enc3] + keyStr[enc4]
    return output
