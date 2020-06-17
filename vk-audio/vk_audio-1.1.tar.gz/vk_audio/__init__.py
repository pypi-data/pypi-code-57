import vk_api,re,datetime,json,zlib,os,base64,time
from .AudioList import *
from .UrlDecoder import *;
from .Playlist import *
from .AudioObj import *
from .Audio import *
from .AudioEnumIndex import *
import json as json_parser
class VkAudio(object):
    __enum_p=None
    
    def __init__(this,vk=None,login=None,password=None):
        "Модуль аудио вк. vk - vk_api.VkApi или login и пароль"
        if vk is None:vk=vk_api.VkApi(login,password);vk.auth()
        this.vk=vk;
        this.uid = this.vk.method("users.get")[0]["id"]
        this.decode=UrlDecoder(this.uid);
        return
    def load(this,owner_id=None,count_audios_to_get_url=10):
        """
        :param owner_id: id страницы, у которой хотите получить аудио
        :type owner_id: int or NoneType
        :param count_audios_to_get_url: У скольких аудиозаписей получать ссылку за один раз
        :param count_audios_to_get_url: int
        """
        if(owner_id is None):owner_id=this.uid
        audio_to_return:Audio=Audio(this, owner_id);
        this._getPlaylists(audio_to_return,count_audios_to_get_url);
        this._getAudios(audio_to_return,len(audio_to_return.Audios),count_audios_to_get_url);   
        audio_to_return.Count=len(audio_to_return.Audios)
        return audio_to_return
    def get_only_audios(self,owner_id=None,offset=0,count=None,need_list=False):
        if(not self.__enum_p):self.__enum_p=AudioEnumIndex(html.fromstring(self.vk.http.get('https://vk.com/dev/')).getchildren()[0],self.vk)
        if(need_list):
            return list(self.get_only_audios(owner_id,offset,count))
        self.vk.http.headers['X-Requested-With']='XMLHttpRequest'
        resp = self.vk.http.post(
           "https://m.vk.com/audios"+str(owner_id if owner_id is not None else self.uid),data={
            '_ajax': 1,
            'offset': offset    
           }
        ).json();
        del  self.vk.http.headers['X-Requested-With'];
        if(not resp['data']):return False;
        audios = [];
        for c, key in enumerate(resp['data'][0]):
            if(count is not None and count-c<=0):break
            value =  AudioObj(resp['data'][0][key][1],self,audios,None);
            if(c%10==9):
                audios=[]
            else:
                audios.append(value)
            yield value 
        if(count is None or count-c>=0):
            audios=self.get_only_audios(owner_id,offset+c,None if count is None else count-c)
            if(audios):
                for i in audios:
                    yield i
    def _getPlaylists(self,audio:Audio,c):
        html_text = self.vk.http.get('https://vk.com/audios'+str(audio.owner_id),allow_redirects=False).text;
        tree:list = html.fromstring(html_text)
        body:html.Element = tree.getchildren()[1];

        if(not self.__enum_p):self.__enum_p=AudioEnumIndex(tree.getchildren()[0],self.vk)

        script_with_info = self.__get_last(body.getchildren())
        self.__parse_info_from_script(script_with_info.text,audio,c);
    def _getAudios(self,audio:Audio,offset=30,c=10):     
        params = {'access_hash': '',
            'act': 'load_section',
            'al': 1,
            'claim': 0,
            'offset': offset,
            'owner_id': audio.owner_id,
            'playlist_id': -1,
            'track_type': 'default',
            'type': 'playlist'}
        self.vk.http.headers['X-Requested-With']='XMLHttpRequest'
        resp = self.vk.http.post('https://vk.com/al_audio.php',data=params);
        del self.vk.http.headers['X-Requested-With'];
        audios_json = json.loads(resp.text.lstrip('<!--'))
        audios = audios_json['payload'][1][0]['list']
        self.__load_audios_from_js(audios,audio,c)
    def __parse_info_from_script(self,text:str,audio:Audio,c=10):
        #получаем данные аудио в json
        text = text[text.find('new AudioPage'):-1]
        text = text[text.find('{'):re.search('"listenedHash"\:"[a-z0-9]+?"\}\);', text).span()[1]-2]
        json = json_parser.loads(text);
        audio._Audio__newPlaylistHash=json['newPlaylistHash'];
        audio._Audio__audiosReorderHash=json['audiosReorderHash'];
        audio._Audio__playlistsReorderHash=json['reorderHash'];
        audio._Audio__listenedHash=json['listenedHash'];
        self.__load_playlists_from_js(json['playlists'],audio);
        if json['sectionData']['all']['playlist'] and json['sectionData']['all']['playlist']['list']:
            self.__load_audios_from_js(json['sectionData']['all']['playlist']['list'],audio,c);
        else:audio.Count=0;
        #self.__load_audios_from_js(json['playlists'],audio,c);
        #audio.Count=json['sectionData']['all']['playlistData']['totalCount']
        return;
    def __load_playlists_from_js(self,json,audio:Audio):
        for i in json:
            audio.Playlists.append(Playlist(i,audio._Audio__audiosReorderHash,self.vk))
    def __load_audios_from_js(self,json:dict,audio:Audio,c:int):
        audios = [];
        for i in json:
            a=AudioObj(i,self,audios,audio._Audio__audiosReorderHash)
            audio.Audios.append(a)
            audios.append(a);
            if(len(audios)>=c):audios=[]
    def __get_last(self,q):
        return q[len(q)-1]
if __name__=="__main__":
    vk = vk_api.VkApi(input("введите логин:","введите пароль"));
    vk._auth_cookies();
    a = VkAudio(vk)
    t = time.time()
    audios = a.load(owner_id=100);
    print("Получение аудои заняло "+str(time.time()-t)+" секунд")
    iterator =  a.get_only_audios();
    for i in iterator:
        print(i.url)
    #z=a.get()