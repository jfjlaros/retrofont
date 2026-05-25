from yaml import safe_load


test_yaml_font = safe_load(open('data/test_font.yaml'))

test_glyph = b'\x01\x32\x18\x0c\x00\xe7\xa7\xe7'
test_text_glyph = test_yaml_font[2][0]['data']

test_empty = b'\x00\x00\x00\x00\x00\x00\x00\x00'
