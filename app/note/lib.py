# -*- coding: utf-8 -*-
from app.note.models import NoteID
def getnextseq():
    if NoteID.objects(name="noteid").count() == 0:
        NoteID(name="noteid",seq=0).save()

    now_seq = NoteID.objects(name="noteid").first()
    next_seq = now_seq.seq + 1
    now_seq.seq = next_seq
    now_seq.save()

    return next_seq