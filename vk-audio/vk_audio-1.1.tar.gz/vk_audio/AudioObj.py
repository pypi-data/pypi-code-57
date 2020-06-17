import json as json_parser
class AudioObj(object):
    __decoded = False;
    def __init__(this,json,vk_audio,audios_to_send_with=None,audiosReorderHash=None):
        if(audios_to_send_with is None):audios_to_send_with=[]
        enum = vk_audio._VkAudio__enum_p;
        this.id=json[enum.AUDIO_ITEM_INDEX_ID];
        this.owner_id=json[enum.AUDIO_ITEM_INDEX_OWNER_ID];
        this.title=json[enum.AUDIO_ITEM_INDEX_TITLE];
        this.artist=json[enum.AUDIO_ITEM_INDEX_ARTIST]
        this.duration=json[enum.AUDIO_ITEM_INDEX_DURATION]
        this.text=json[enum.AUDIO_ITEM_INDEX_LYRICS]
        this.image=json[enum.AUDIO_ITEM_INDEX_COVER_URL]
        this.artists_info = json[enum.AUDIO_ITEM_INDEX_MAIN_ARTISTS]
        this.__url = json[enum.AUDIO_ITEM_INDEX_URL]

        __hashes=json[enum.AUDIO_ITEM_INDEX_HASHES].split("/");

        this.hash = f"{this.owner_id}_{this.id}_{__hashes[enum.AUDIO_ACTION_HASH_INDEX]}_{__hashes[enum.AUDIO_URL_HASH_INDEX]}";
        this.__edit_hash = __hashes[enum.AUDIO_EDIT_HASH_INDEX];
        this.__delete_hash=__hashes[enum.AUDIO_DELETE_HASH_INDEX];
        this.__restore_hash=__hashes[enum.AUDIO_RESTORE_HASH_INDEX];
        this.__track_code_hash=json[enum.AUDIO_ITEM_INDEX_TRACK_CODE];
        this.__reorder_hash=audiosReorderHash;

        this.can_edit=True if this.__edit_hash else False
        this.can_delete = True if this.__delete_hash else False 
        this.deleted=False;

        this.__vk_audio=vk_audio;
        this.get_url_with=audios_to_send_with;
    def __str__(self):
       return  str(self.toArray());
    def __getitem__(self,name:str):
        return self.toArray()[name];
    def __repr__(self):
        return self.__str__();
    def toArray(self):
        return { "owner_id":self.owner_id,
            "id":self.id,
            "title":self.title,
            "artist":self.artist,
            "duration":self.duration,
            "image":self.image,
            "url":self.url,
            "artists_info":self.artists_info }
    @property
    def url(self):
        if not self.__url:
            string=','.join(i.hash for i in self.get_url_with)
            json = AudioObj.get_json_from_ids(self.__vk_audio.vk,string);
            for i,item in enumerate(json):
                if(len(item)<=self.__vk_audio._VkAudio__enum_p.AUDIO_ITEM_INDEX_URL or not item[self.__vk_audio._VkAudio__enum_p.AUDIO_ITEM_INDEX_URL]):continue
                self.get_url_with[i]._AudioObj__url = item[self.__vk_audio._VkAudio__enum_p.AUDIO_ITEM_INDEX_URL];
        if not self.__decoded and self.__url:
            self.__decoded=True
            self.__url=self.__vk_audio.decode.decode(self.__url)
        return self.__url
    #region vk_methods
    def edit(self,title=None,artist=None,text=None):
        if(not self.can_edit):raise PermissionError("you can not edit this audio")
        if(text is None):text=self.text;
        if(artist is None):artist=self.artist;
        if(title is None):title=self.title;
        ans= json_parser.loads(self.__vk_audio.vk.http.post('https://vk.com/al_audio.php',data={'act': 'edit_audio',
            'aid': self.id,
            'oid': self.owner_id,
            'al': 1,
            'force_edit_hash':'', 
            #genre: 18
            'hash': self.__edit_hash,
            'title':title,
            'performer': artist,
            'privacy': 0,
            'text': text
        }).text.lstrip('<!--'))
        if(ans and 'payload' in ans and len(ans['payload'])>=2 and len(ans['payload'][1])!=0):
            self.text=text;
            self.artist=artist;
            self.title=title;
            return True
        else:
            return ans;
    def move(self,insert_before_index:int=None,insert_after_index:int=None):
        '''
        Передвигает аудио. Использовать только 1 из параметров.
        insert_before_index -> id аудио или AudioObj перед которым надо вставить эту аудиозапись
        insert_after_index  -> id аудио или AudioObj после которого надо вставить эту аудиозапись
        '''
        params = {"owner_id":self.owner_id,"audio_id":self.id}
        if(insert_before_index is not None):
            if(isinstanse(insert_before_index,Audio_obj)):
                 params['before']=insert_before_index.id;
            else:
                 params['before']=insert_before_index;
        elif(insert_after_index is not None):
            if(isinstanse(insert_after_index,Audio_obj)):
                params['after']=insert_after_index.id;
            else:
                params['after']=insert_after_index;
        else:raise ValueError("введите insert_before_index или insert_after_index");
        return self.__vk.method("audio.reorder",params)
    def delete(self):
        if(not self.can_delete):raise PermissionError("You can not delete this audio")
        elif(self.deleted):raise PermissionError("This audio have alredy deleted")
        ans = json_parser.loads(self.__vk_audio.vk.http.post('https://vk.com/al_audio.php',data={
            'act': 'delete_audio',
            'aid': self.id,
            'al': 1,
            'hash': self.__delete_hash,
            'oid': self.owner_id,
            'restore': 1,
            'track_code': self.__track_code_hash
        }).text.lstrip('<!--'));
        if(ans and 'payload' in ans and len(ans['payload'])>=2 and len(ans['payload'][1])!=0):
            self.deleted=True;
            return True;
        return ans;
    def restore(self):
        if(not self.deleted):
            raise PermissionError("Your audio is not deleted yet");
        ans = json_parser.loads(self.__vk_audio.vk.http.post('https://vk.com/al_audio.php',data={
            'act': 'restore_audio',
            'aid': self.id,
            'al': 1,
            'hash': self.__restore_hash,
            'oid': self.owner_id,
            'track_code': self.__track_code_hash
        }).text.lstrip('<!--'));
        if(ans and 'payload' in ans and len(ans['payload'])>=2 and len(ans['payload'][1])!=0):
            self.deleted=False;
            return True;
        return ans
    def reorder(self,move_after_id):
        '''
        Передвигает аудио.
        move_after_id  -> id аудио или AudioObj ПОСЛЕ которого надо вставить данную аудиозапись
        '''
        if(not self.__reorder_hash):raise PermissionError("you can not move this audio");
        if isinstance( move_after_id,AudioObj):
            if(move_after_id.owner_id!=self.owner_id):raise ValueError("{0}\nowner_id is not equals\n{1}\nowner_id".format(repr(self),repr(move_after_id)));
            move_after_id=move_after_id.id
        resp = json_parser.loads(self.__vk_audio.vk.http.post('https://vk.com/al_audio.php',{
            'act': 'reorder_audios',
            'al': 1,
            'audio_id': self.id,
            'hash': self.__reorder_hash,
            'next_audio_id':move_after_id,
            'owner_id': self.owner_id
            } ).text.lstrip('<!--'));
        if(resp and 'payload' in resp and len(resp['payload'])>=2):
            return True;
        return resp
    #endregion
    @staticmethod
    def get_audio_from_hash(hash:str,vk_audio):
        json=AudioObj.get_json_from_ids(vk_audio,hash)
        answer = [];
        for i in json:
            answer.append(AudioObj(i,vk_audio));
        return answer
    @staticmethod 
    def get_json_from_ids(vk,ids):
        resp = vk.http.post('https://vk.com/al_audio.php?act=reload_audio',data={
            "al":1,
            "ids":ids
            })
        try:
            json=json_parser.loads(resp.text.lstrip('<!--'))
            if('payload' in json and len(json['payload'])==2 and json['payload'][1][0]=='no_audios'):raise ValueError('');
        except ValueError as e:
            raise ValueError("hash is invalid!")
        json = json['payload'][1][0]
        return json