# Copy notes

The copy can have only new cards. Or they can have exactly the same
intervals, ease, etc... than the original card.

To copy a note:
1. Open the card browser
2. Select the desired notes (at least one card by note)
3. Go to "Edit > Copy and set to new" their shortcut are configurable,
   by default (Ctrl+C)

The copy preserve fields, tags, decks.

## Warning

### Bug in previous version
Before the 26th of september 2019, there was a bug in this
add-on. Because of this bug, if you share and import a deck containing
either:
* a note and a copy of this note
* two notes originally copied from the same note
then importing this deck will bug. Only one of the multiple notes will
be imported; the other will be detected as copy by anki, even if they
have quite different content.

This add-on do two things to correct this bug.
### Correcting your collection
The first time you open a profile with this add-on installed, it'll
check whether your collection contains the bug. In this case it'll ask
whether you want to correct it or not. It won't check again next time
you open it; indeed, this bug should not appear again. (Unless you use
an old version of this add-on on another computer which is
synchronized with the same collection. But normally, in this case,
it'll be corrected when you update this add-on on the other computer).

### Correcting imports with this bug
Anki will try to detect when this bug exists in a deck you import. In
this case, it'll correct it and tell you to tell to the decks' author
that it should update this deck. Since this change the importer, a
part of anki which should not be touched by an add-on whose purpose is
only to copy notes, you can deactivate it in the configurations.


### Empty cards
There is a potential caveat, which should not occur often nor have
real consequences. You should note that empty cards are not copied. If
you don't know what it means, you probably doesn't need to worry about
this.


### Incompatibilites
This add-on is currently incompatible with:
* add-on [Show duplicates](https://ankiweb.net/shared/info/865767531)


## Configuration
Using the add-on configuration, you can:
* change the shortcut.
* decide whether you keep creation time or set it to current time.
* decide whether you keep interval, due date, number of lapse, etc...

## Configuration
"Preserve creation time": as indicated by the name, if it's true, the card and note's creation time are preserved. Otherwise, it is set to the time of the copy.

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   |Arthur Milchior <arthur@milchior.fr>
Based on    |Kealan Hobelmann's addon 396494452 (for anki 2.0)
Based on    |Anki code by Damien Elmes <anki@ichi2.net>
License     |GNU AGPL, version 3 or later; http|//www.gnu.org/licenses/agpl.html
Source in   |https://github.com/Arthur-Milchior/anki-copy-note
Addon number| [1566928056](https://ankiweb.net/shared/info/1566928056)
Support me on| [![Ko-fi](https://ko-fi.com/img/Kofi_Logo_Blue.svg)](Ko-fi.com/arthurmilchior) or [![Patreon](http://www.milchior.fr/patreon.png)](https://www.patreon.com/bePatron?u=146206)
