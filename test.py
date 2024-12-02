from urllib.parse import unquote
t = unquote("MrBeast%20en%20EspaÃ%C2%83Â%C2%83Ã%C2%82Â%C2%83Ã%C2%83Â%C2%82Ã%C2%82Â±ol").encode()
t = t\
    .decode('utf-8')\
    .encode('latin1')\
    .decode('utf-8')\
    .encode('latin1')\
    .decode('utf-8')\
    .encode('latin1')\
    .decode('utf-8')\
    .encode('latin1')\
    .decode('utf-8')

print(t)