# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior arthur@milchior.fr
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Select any number of cards in the card browser and create exact copies of each card in the deck
# Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-copy-note
# Anki's add-on number: 1566928056

# This add-ons is heavily based on Kealan Hobelmann's addon 396494452

"""To use:

1) Open the card browser
2) Select the desired notes (at least one card by note)
3) Go to "Edit > Copy Notes in place" or "Edit > Full note copy"

Both option consider the note you did select, and create a new note with the same content. (Fields and tags)
Both option add the card of the copied note to the deck in which the original card is (this is the main difference with addon 396494452)

"Copy notes in place" create  cards which are new. Empty card's are not copied.
"Full note copy" also copy the reviews paramater (number of reviews,  of leeches, easiness, due date...). Empty card's are copied.

Recall that an «empty cards» is a card that should be deleted by
«check empty card».
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import anki.notes
from anki.hooks import addHook
from anki.importing.anki2 import Anki2Importer
from anki.lang import _
from anki.utils import guid64
from aqt import mw
from aqt.utils import showWarning, tooltip

from .config import getUserOption
from .utils import createRelationTag, getRelationsFromNote
from .new_note_id import add_note_with_id
from .time import timestampID

#import profile


def copyNotes(browser):
    """
    nids -- id of notes to copy
    """
    nids = browser.selectedNotes()
    mw.checkpoint("Copy Notes")
    mw.progress.start()
    for nid in nids:
        copyNote(nid)
    # Reset collection and main window
    mw.progress.finish()
    mw.col.reset()
    mw.reset()
    browser.onSearchActivated()
    tooltip("""Cards copied.""")


def setupMenu(browser):
    a = QAction("Note Copy", browser)
    # Shortcut for convenience. Added by Didi
    a.setShortcut(QKeySequence(getUserOption("Shortcut: copy", "Ctrl+C")))
    a.triggered.connect(lambda: copyNotes(browser))
    browser.form.menu_Notes.addSeparator()
    browser.form.menu_Notes.addAction(a)


def copyNote(nid):
    note = mw.col.getNote(nid)
    old_cards = note.cards()
    old_cards_sorted = sorted(old_cards, key=lambda x: x.ord) # , reverse=True)
    oid = note.id

    new_note, new_cards = add_note_with_id(note, nid if getUserOption("Preserve creation time", True) else None)
    new_cards_sorted = sorted(new_cards, key=lambda x: x.ord) # , reverse=True)
    
    note.id = new_note.id
    note.guid = new_note.guid


    if getUserOption("relate copies", False):
        if not getRelationsFromNote(note):
            note.addTag(createRelationTag())
            note.flush()
        
    for old, new in zip(old_cards_sorted, new_cards_sorted):
        copyCard(old, new)
    
    
    note.addTag(getUserOption("tag for copies"))
    note.usn = mw.col.usn()
    note.flush()


def copyCard(old_card, new_card):
    oid = old_card.id
    # Setting id to 0 is Card is seen as new; which lead to a different process in backend
    old_card.id = new_card.id
    # new_cid = timestampID(note.col.db, "cards", oid)
    if not getUserOption("Preserve ease, due, interval...", True):
        old_card.type = 0
        old_card.ivl = 0
        old_card.factor = 0
        old_card.reps = 0
        old_card.lapses = 0
        old_card.left = 0
        old_card.odue = 0
    old_card.nid = new_card.nid
    old_card.usn = mw.col.usn()
    old_card.flush()
    # I don't care about the card creation time
    if getUserOption("Copy log", True):
        for data in mw.col.db.all("select * from revlog where cid = ?", oid):
            copyLog(data, old_card.id)


def copyLog(data, newCid):
    id, cid, usn, ease, ivl, lastIvl, factor, time, type = data
    id = timestampID(mw.col.db, "revlog", t=id)
    cid = newCid
    mw.col.db.execute("insert into revlog values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      id, cid, usn, ease, ivl, lastIvl, factor, time, type)


addHook("browser.setupMenus", setupMenu)




firstBug = False
NID = 0
GUID = 1
MID = 2
MOD = 3
# determine if note is a duplicate, and adjust mid and/or guid as required
# returns true if note should be added


def _uniquifyNote(self, note):
    global firstBug
    srcMid = note[MID]
    dstMid = self._mid(srcMid)

    if srcMid != dstMid:
        # differing schemas and note doesn't exist?
        note[MID] = dstMid

    if note[GUID] in self._notes:
        destId, destMod, destMid = self._notes[note[GUID]]
        if note[NID] == destId:  # really a duplicate
            if srcMid != dstMid:  # schema changed and don't import
                self._ignoredGuids[note[GUID]] = True
            return False
        else:  # Probably a copy made by buggy version. Change guid to a new one.
            while note[GUID] in self._notes:
                note[GUID] = guid64()
            if not firstBug:
                firstBug = True
                showWarning("""Hi. Sorry to disturb you. 
The deck you are importing seems to have a bug, created by a version of the add-on 1566928056 before the 26th of september 2019. Can you please tell the author of the imported deck that you were warned of this bug, and that it should update the shared deck to remove the bug ? Please send them the link https://github.com/Arthur-Milchior/anki-copy-note so they can have more informations. And let me know on this link whether there is any trouble. 

Arthur@Milchior.fr""")

            return True
    else:
        return True


if getUserOption("correct import", True):
    Anki2Importer._uniquifyNote = _uniquifyNote


def _importNotes(self):
    # build guid -> (id,mod,mid) hash & map of existing note ids
    self._notes = {}
    existing = {}
    for id, guid, mod, mid in self.dst.db.execute(
            "select id, guid, mod, mid from notes"):
        self._notes[guid] = (id, mod, mid)
        existing[id] = True
    # we may need to rewrite the guid if the model schemas don't match,
    # so we need to keep track of the changes for the card import stage
    self._changedGuids = {}
    # we ignore updates to changed schemas. we need to note the ignored
    # guids, so we avoid importing invalid cards
    self._ignoredGuids = {}
    # iterate over source collection
    add = []
    update = []
    dirty = []
    usn = self.dst.usn()
    dupesIdentical = []
    dupesIgnored = []
    total = 0
    for note in self.src.db.execute(
            "select * from notes"):
        total += 1
        # turn the db result into a mutable list
        note = list(note)
        shouldAdd = self._uniquifyNote(note)
        if shouldAdd:
            # ensure id is unique
            while note[0] in existing:
                note[0] += 999
            existing[note[0]] = True
            # bump usn
            note[4] = usn
            # update media references in case of dupes
            note[6] = self._mungeMedia(note[MID], note[6])
            add.append(note)
            dirty.append(note[0])
            # note we have the added the guid
            self._notes[note[GUID]] = (note[0], note[3], note[MID])
        else:
            # a duplicate or changed schema - safe to update?
            if self.allowUpdate:
                oldNid, oldMod, oldMid = self._notes[note[GUID]]
                # will update if incoming note more recent
                if oldMod < note[MOD]:
                    # safe if note types identical
                    if oldMid == note[MID]:
                        # incoming note should use existing id
                        note[0] = oldNid
                        note[4] = usn
                        note[6] = self._mungeMedia(note[MID], note[6])
                        update.append(note)
                        dirty.append(note[0])
                    else:
                        dupesIgnored.append(note)
                        self._ignoredGuids[note[GUID]] = True
                else:
                    dupesIdentical.append(note)
