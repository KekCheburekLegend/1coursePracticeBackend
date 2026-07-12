from sqids import Sqids

sqids = Sqids(
    min_length=6,
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
)

def encode_url( id: int):
    url_id = id
    return sqids.encode([url_id])


def decode_code(Link: str):
    try:
        decoded = sqids.decode(Link)  
        return decoded[0] if decoded else None
    except:
        return None