from database.files import (
    get_by_unique,
    insert_file
)

from core.utils import clean_filename
from config import CHANNEL_ID

async def index_file(client, msg):

    file = msg.document or msg.video or msg.audio

    if not file:
        return ("NO_FILE", None)

    unique_id = file.file_unique_id

    name = clean_filename(
        file.file_name
    )

    existing = get_by_unique(unique_id)

    if existing:
        return ("EXISTS", existing[0])

    # Already in source channel
    if msg.chat.id == CHANNEL_ID:

        insert_file(
            CHANNEL_ID,
            msg.id,
            name,
            unique_id
        )

        return ("INDEXED_CHANNEL", None)

    # Upload to source channel
    sent = await client.send_document(
        CHANNEL_ID,
        file.file_id
    )

    insert_file(
        CHANNEL_ID,
        sent.id,
        name,
        unique_id
    )

    return ("UPLOADED", None)
