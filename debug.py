from anki.hooks import addHook
from anki.utils import guid64
from aqt import mw
from aqt.utils import askUser

from .config import getUserOption


def check():
    checkedGui = getUserOption("checkedGui", [])
    if mw.pm.name in checkedGui:
        return
    lastGuid = None
    accepted = False
    for guid, nid in mw.col.db.all("select guid, id from notes order by guid, id"):
        if lastGuid == guid:
            if accepted is False:
                accepted = askUser(
                    "A previous version of copy note created a bug. Correcting it will require to do a full sync of your collection. Do you want to correct it now ?")
            if accepted is False:
                return
            mw.col.modSchema(True)
            mw.col.db.execute(
                "update notes set guid = ? where id = ? ", guid64(), nid)
        lastGuid = guid
    checkedGui.append(mw.pm.name)


addHook("profileLoaded", check)
