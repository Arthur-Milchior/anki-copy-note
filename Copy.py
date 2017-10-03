# -*- coding: utf-8 -*-

"""Copyright: Arthur Milchior arthur@milchior.fr
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Select any number of cards in the card browser and create exact copies of each card in the deck

This add-ons is heavily based on Kealan Hobelmann's addon 396494452

To use:

1) Open the card browser
2) Select the desired notes (at least one card by note)
3) Go to "Edit > Copy Notes in place" or press ctrl+c

A couple notes:

- The copied cards should look exactly like the originals
- Tags are preserved in the copied cards
- Review history is NOT copied to the new cards (they appear as new cards)
- The cards will be marked as duplicates (because they are!)

Note that this add-on copy notes and not cards. Cards you have not
selected may also be copied. This is due to the fact that a cards
depends on note and templates. They could not be created or deleted
independtly of the note and templates which generate them.

Note that «empty cards» (i.e. cards that should be deleted by «check
empty card») are not copied. If you need empty card to be copied (I
don't see how it could be a feature, but who knows...), contact me and
I may edit the add-on. 

This leads to the following strange action. If you select an empty
card in the browser and click on «Copy Notes in place», the other
note's cards will be copied but not the selected one. This is not a
bug.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip
from anki.utils import timestampID
import anki.notes

def copyCards(nids):
    mw.checkpoint("Copy Notes")
    mw.progress.start()
    
    
    # Copy notes
    for nid in nids:
        print "Found note: %s" % (nid)
        note = mw.col.getNote(nid)
        model = note._model
        
        # Create new note
        note_copy = anki.notes.Note(mw.col,model=model)
        # Copy tags and fields (all model fields) from original note
        note_copy.tags = note.tags
        note_copy.fields = note.fields

        # Refresh note and add to database
        note_copy.flush()
        mw.col.addNote(note_copy)

        cards_copy= note_copy.cards()
        cards= note.cards()
        for card_copy in cards_copy:
            ord = card_copy.ord
            (cid, ) = mw.col.db.first("select id from cards where nid = ? and ord = ?",nid, ord)
            card = mw.col.getCard(cid)
            did =  card.odid or card.did
            card_copy.did=did
            card_copy.flush()
            

    # Reset collection and main window
    mw.col.reset()
    mw.reset()
        
    # Reset collection and main window
    mw.col.reset()
    mw.reset()
    tooltip(_("""Cards copied."""))
    
    
def setupMenu(browser):
    a = QAction("Copy Notes in place", browser)
    a.setShortcut(QKeySequence("Ctrl+C")) # Shortcut for convenience. Added by Didi
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onCopyCards(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onCopyCards(browser):
    copyCards(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
