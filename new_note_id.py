from typing import Optional
from aqt import mw

from .time import timestampID

def add_note_with_id(id: Optional[int]= None):
    """Add a note, in the db with unique guid, and id as close as id possible, (now if id=None), without card."""
    note = mw.col.newNote()
    mw.col.add_note(note, 1)
    new_id = timestampID(note.col.db, "notes", id)
    cards_for_new_note = note.cards()
    mw.col.db.execute("""
    update notes
    set id=?
    where id=?
    """, new_id, note.id)
    for c in cards_for_new_note:
        c.nid = new_id
        c.usn = mw.col.usn()
        c.flush()
    note.id = new_id
    return note, cards_for_new_note
