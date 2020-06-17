from .sales_inv_utils import SalesInvBase
from . import GetInstance

class NotesCollection(SalesInvBase):

    ext_fields = ['finish_week','item_type','notes','soft_delete','parent_path','path']
    COLLECTION_NAME = 'application_data'

    def __init__(self,fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.item_type = kwargs.get('item_type','')
        self.notes = kwargs.get('notes',None)
        self.finish_week = kwargs.get('finish_week','')
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self._loaded_notes = {}
        super(NotesCollection,self).__init__(fsClient, **kwargs)

        if self.notes is not None:
            note_itemnames = self.notes.keys()
            for item_name in note_itemnames:
                item_notes = self.notes[item_name]
                for item_note in item_notes:
                    item_note['_noteCollection'] = self
                    item_note['_growWeekParent'] = self._growWeekParent
                    item_note['item_type'] = self.item_type
                    note = ItemWeekNotes(self._fsClient,**item_note)
                    self._loaded_notes[note.id] = note

    def base_path(self):
        return self.parent_path+'/Notes'

    @property
    def id(self):
        return self.item_type

    @classmethod
    def getInstance(cls,docRef,gwParent):
        ref,snap = NotesCollection.getDocuments(docRef)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        docDict['_growWeekParent'] = gwParent
        return NotesCollection(NotesCollection.get_firestore_client(),**docDict)
    
    @classmethod
    def getOrCreateInstance(cls,docRef,gwParent):
        col = cls.getInstance(docRef,gwParent)
        if not col.exists:
            col.update_ndb(True)
        return col

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(self.parent_path)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent

    def getNotesByItemName(self,item_name):
        return [note for note in list(self._loaded_notes.values()) if note.item_name == item_name]

    def create_note(self, item_name, note):
        note_id = self._get_doc_id('Notes')
        item_note = {'note':note,'finish_week':self.finish_week,'id':note_id}
        item_note['_growWeekParent'] = self._growWeekParent
        item_note['_noteCollection'] = self
        item_note['_growWeekParent'] = self._growWeekParent
        item_note['item_type'] = self.item_type
        item_note['item_name'] = item_name
        note = ItemWeekNotes(self._fsClient,**item_note)
        self._loaded_notes[note.id] = note
        note._set_add_entries()
        note._set_update_entries()
        self.update_ndb()
        return note

    def delete_note(self, note_id):
        del self._loaded_notes[note_id]
        return self.update_ndb()
        
    def update_ndb(self, doCreate=False):
        self.notes = {}
        note_ids = self._loaded_notes.keys()
        for note_id in note_ids:
            note = self._loaded_notes[note_id]
            notes_array = self.notes.get(note.item_name,[])
            notes_array.append(note.get_dict())
            self.notes[note.item_name] = notes_array

        return super(NotesCollection,self).update_ndb(doCreate)

class ItemWeekNotes(SalesInvBase):

    ext_fields = ['note','id','item_name','item_type','finish_week','soft_delete']
    COLLECTION_NAME = 'application_data'
    _active_plants = []
    
    """ Represents a Week where we can have reserve orders """

    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.note = kwargs.get('note','') 
        self.note_id = kwargs.get('id',ItemWeekNotes.GetNextDNL('Notes'))
        self.item_name = kwargs.get('item_name','')
        self.item_type = kwargs.get('item_type')
        self.finish_week = kwargs.get('finish_week','')
        self._growWeekParent = kwargs.get('_growWeekParent',None)
        self._noteCollection = kwargs.get('_noteCollection',None)
        super(ItemWeekNotes, self).__init__(fsClient, **kwargs)

    def base_path(self):
        return self._noteCollection.path
    
    @classmethod
    def get_active(cls):
        return ItemWeekNotes.GetActive('ItemWeekNotes',ItemWeekNotes)
    
    @property
    def id(self):
        return self.note_id
    
    @property
    def path(self):
        return self._noteCollection.path

    @property
    def parent_path(self):
        return self._noteCollection.parent_path

    def get_schema(self):
        schema = self.get_bq_schema()
        schema['fields'].append({'field_name':'note','field_type':'string'})
        schema['fields'].append({'field_name':'plant_name','field_type':'string','field_required':True})
        schema['fields'].append({'field_name':'finish_week','field_type':'string','field_required':True})
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        values['note'] = self.note
        values['item_name'] = self.item_name
        values['finish_week'] = self.finish_week
        return values

    def get_api_summary(self):
        note = {'noteId':self.id,'note':self.note,'added_by':self.added_by,'added_date':self.timestamp}
        return note

    def update_ndb(self,doCreate=True):
        if doCreate:
            self._set_add_entries()
        self._set_update_entries()
        self._noteCollection._loaded_notes[self.id] = self
        return self._noteCollection.update_ndb(doCreate)

    def delete_resp(self):
        if self._noteCollection._loaded_notes.get(self.id,None) is not None:
            del self._noteCollection._loaded_notes[self.id]
        
        self._noteCollection.update_ndb()