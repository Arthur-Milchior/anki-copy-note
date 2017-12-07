# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior arthur@milchior.fr
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Select any number of cards in the card browser and create exact copies of each card in the deck
# Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-copy-note
# Anki's add-on number: 1566928056

#This add-ons is heavily based on Kealan Hobelmann's addon 396494452

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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip, showWarning
from anki.utils import timestampID
import anki.notes

def copyCards(nids,review):
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
        nid_copy = note_copy.id
        
        cards_copy= note_copy.cards()
        cards= note.cards()
        ord_to_card = {card.ord:card for card in cards}
        ord_to_card_copy = {card.ord:card for card in cards_copy}
        if review:
            for card in cards:
                ord = card.ord
                card_copy = ord_to_card_copy.get(ord)
                if card_copy:
                    card.id=card_copy.id
                    card.nid = nid_copy
                else:
                    tooltip("We copy a card which should not exists.")
                    card.id=timestampID(mw.col.db,"cards")
                    card.nid=nid_copy
                card.flush()
        else:
            for card_copy in cards_copy:
                ord = card_copy.ord
                card = ord_to_card.get(ord)
                if card:
                    card_copy.did=card.odid or card.did
                    card_copy.flush()

    # Reset collection and main window
    mw.col.reset()
    mw.reset()
        
    tooltip(_("""Cards copied."""))
    
    
def setupMenu(browser):
    a = QAction("Note Copy", browser)
    a.setShortcut(QKeySequence("Ctrl+C")) # Shortcut for convenience. Added by Didi
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onCopyCards(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)
    a = QAction("Full Notes Copy", browser)
    a.setShortcut(QKeySequence("Ctrl+Shift+C")) # Shortcut for convenience. Added by Didi
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onCopyCards(e,review=True))
    browser.form.menuEdit.addAction(a)

def onCopyCards(browser, review=False):
    copyCards(browser.selectedNotes(),review)

addHook("browser.setupMenus", setupMenu)
