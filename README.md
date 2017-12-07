# -*- coding: utf-8 -*-
# Copyright: Arthur Milchior arthur@milchior.fr
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Select any number of cards in the card browser and create exact copies of each card in the deck
# Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-copy-note
# Anki's add-on number: 1566928056

#This add-ons is heavily based on Kealan Hobelmann's addon 396494452


1) Open the card browser
2) Select the desired notes (at least one card by note)
3) Go to "Edit > Copy Notes in place" or "Edit > Full note copy"

Both option consider the note you did select, and create a new note with the same content. (Fields and tags)
Both option add the card of the copied note to the deck in which the original card is (this is the main difference with addon 396494452)

"Copy notes in place" create  cards which are new. Empty card's are not copied.
"Full note copy" also copy the reviews paramater (number of reviews,  of leeches, easiness, due date...). Empty card's are copied. 

Recall that an «empty cards» is a card that should be deleted by
«check empty card».
