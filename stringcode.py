keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def decodeString(to_dec):
    output = ""
    i=0
    while i < len(to_dec):

        enc1 = keyStr.find(to_dec[i])
        i+=1
        enc2 = keyStr.find(to_dec[i])
        i+=1
        enc3 = keyStr.find(to_dec[i])
        i+=1
        enc4 = keyStr.find(to_dec[i])
        i+=1
        
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
    pass