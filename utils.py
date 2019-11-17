# As in add-on 413416269
from .config import getUserOption
from anki.utils import intTime

def getRelationsFromNote(note):
    relations = set()
    for relation in note.tags:
        for prefix in getUserOption("tag prefixes", ["relation_"]):
            if relation.startswith(prefix):
                relations.add(relation)
                break
    return relations

def createRelationTag():
    return f"""{getUserOption("current tag prefix", "relation_")}{intTime(1000)}"""
