

s = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. "


x = ""
for i in s:
    if (ord(i) < 97 or ord(i) > 122):
        x += i
    elif (ord(i) > 120):
        x += chr(ord(i)-24)
    else:
        x += chr(ord(i)+2)    
    
print(x)
