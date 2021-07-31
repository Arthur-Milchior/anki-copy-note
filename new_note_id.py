from typing import Optional
from aqt import mw
from .time import timestampID

def add_note_with_id(id: Optional[int]= None):
    """Add a note, in the db with unique guid, and id as close as id possible, (now if id=None), without card."""
    note = mw.col.newNote()
    mw.col.add_note(note, 1)
    mw.col.db.execute("delete from cards where nid = ?", note.id)
    new_id = timestampID(note.col.db, "notes", id)
    mw.col.db.execute("""
    update notes
    set id=?
    where id=?
    """, new_id, note.id)
    note.id = new_id
    return note
    
