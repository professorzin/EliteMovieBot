from fastapi import FastAPI
from database.files import get_file

api = FastAPI()

@api.get("/file/{fid}")
def file_api(fid: int):

    f = get_file(fid)

    if not f:
        return {
            "error": "not found"
        }

    return {
        "chat_id": f[0],
        "message_id": f[1],
        "file_name": f[2]
    }
