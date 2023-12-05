from .decorators import *
import base64

import uuid
def generate_unique_id(digit):
    return str(int(str(uuid.uuid4().int)[:digit]))


def encoding_string(string_data):
    encoded_bytes = base64.b64encode(string_data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_string(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
