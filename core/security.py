import base64

def encode_id(fid):
    return base64.urlsafe_b64encode(
        str(fid).encode()
    ).decode()


def decode_id(code):
    try:
        return int(
            base64.urlsafe_b64decode(
                code.encode()
            ).decode()
        )
    except:
        return None
