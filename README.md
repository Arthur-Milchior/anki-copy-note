# anki-copy-note
An add-on to copy anki's note

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
