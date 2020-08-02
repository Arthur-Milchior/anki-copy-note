# Copy notes

Copy cards, either as new cards, or preserving
intervals, ease, etc., from the original card.

To copy a note:
1. Open the card browser
2. Select at least one note.
3. Go to `Edit > Note Copy`. 
   The keyboard shortcut is configurable;
   the default is `Ctrl+C`.

The copy preserves fields, tags, and decks.

## Warnings

### Bug in previous version
Before the 26th of September 2019, there was a bug in this
add-on. Because of this bug, if you shared and imported a deck 
containing either:
* a note and a copy of this note
* two notes originally copied from the same note
then importing this deck will fail. Only one of the multiple notes will
be imported; the other will be detected as copy by anki, even if they
have quite different content.

This add-on does two things to correct this bug.
##### Correcting your collection
The first time you open a profile with this add-on installed, it'll
check whether your collection contains the bug. In this case it'll ask
whether you want to correct it or not. It won't check again the next time
you open it; indeed, this bug should not appear again. (Unless you use
an old version of this add-on on another computer which is
synchronized with the same collection. But normally, in this case,
it'll be corrected when you update this add-on on the other computer).

##### Correcting imports with this bug
Anki will try to detect when this bug exists in a deck you import. In
this case, it'll correct it and tell you to tell to the deck's author
to update this deck. Since this changes the importer, a
part of anki which should not be touched by an add-on whose purpose is
only to copy notes, you can deactivate it in the configuration.


### Empty cards
There is a potential caveat, which should not occur often nor have
real consequences. You should note that empty cards are not copied. If
you don't know what this means, you probably don't need to worry about
it.


### Incompatibilites
This add-on is currently incompatible with:
* add-on [Show duplicates](https://ankiweb.net/shared/info/865767531)


## Configuration
Using the add-on configuration, you can:
* change the shortcut.
* decide whether to keep the original creation time or set it to the current time.
* decide whether to keep interval, due date, number of lapses, etc...

### Relate card
Add-on [413416269](https://ankiweb.net/shared/info/413416269) allows the user
to relate notes, so that cards of related notes are buried as siblings
during reviews (only on Anki desktop). Relations are created using tags.
You can configure this add-on to automatically relate a note
and its copy by ensuring that they share a tag. More precisely, if
they already have a relation tag, then the same one will be used in
the new copied note. Otherwise, a new tag will be added to both.

### All Configuration Options
* **Copy log** *(Default = True)*: Whether to also copy the review log of the selected cards
* **Preserve creation time** *(Default = True)*: The original card and note's creation time are preserved. Otherwise, it is set to the time of the copy.
* **Preserve ease, due, interval...** *(Default = True)*: Preserve all information not related to creation date
* **Shortcut: copy** *(Default = `Ctrl+C`)*: set a custom keyboard shortcut
* **correct import** *(Default = True)*: Whether to correct bugs in imported decks created by an old version of this add-on. You should set it to False if it interferes with other add-ons; otherwise, keeping it set to True should be all right.
* **current tag prefix** *(Default = relation_)*: the prefix of the tag used to relate notes, as in [Bury related notes add-on](https://ankiweb.net/shared/info/413416269)
* **relate copies** *(Default = True)*: Add a tag to relate the original note and its copy for the [Bury related notes add-on](https://ankiweb.net/shared/info/413416269)
* **tag prefixes** *(Default = ['relation_'])*: if a copied note's tag contain a prefix in this list, no prefix will be added. As in the [Bury related notes add-on](https://ankiweb.net/shared/info/413416269)
* **tag for copies** *(Default = 'copy')*: A tag added to the new notes, copied from another note.

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   |Arthur Milchior <arthur@milchior.fr>
Based on    |Kealan Hobelmann's addon 396494452 (for anki 2.0)
Based on    |Anki code by Damien Elmes <anki@ichi2.net>
License     |GNU AGPL, version 3 or later; http|//www.gnu.org/licenses/agpl.html
Source in   |https://github.com/Arthur-Milchior/anki-copy-note
Addon number| [1566928056](https://ankiweb.net/shared/info/1566928056)
