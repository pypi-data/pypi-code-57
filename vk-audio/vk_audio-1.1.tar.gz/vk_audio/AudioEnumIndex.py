import re
class AudioEnumIndex(object):
    def __init__(self,header_object,vk):
        self.__vk = vk;
        children = header_object.getchildren();
        for i in children:
            if(i.tag!="script" or 'src' not in i.attrib):continue
            src =i.attrib['src']
            if(re.search('common\.[a-z0-9]+?\.js',src)):
                self.__get_script_from_url(src)
                break;
    def __get_script_from_url(self,src:str):
        resp = self.__vk.http.get("https://vk.com"+src if src.startswith("/") else src);
        text = resp.text;
        match = re.search('\{(AUDIO_ITEM_INDEX_ID:.+?)\}',text).groups()[0]      
        for i in match.split(','):
            i=i.split(':')
            if(len(i)!=2):continue;
            val = i[1].lstrip(' ').rstrip(' ');
            if(not val.isdigit()):continue
            val = int(val)
            if(i[0]=='AUDIO_ITEM_INDEX_ID'):self.AUDIO_ITEM_INDEX_ID=val
            elif(i[0]=='AUDIO_ITEM_INDEX_OWNER_ID'):self.AUDIO_ITEM_INDEX_OWNER_ID=val
            elif(i[0]=='AUDIO_ITEM_INDEX_URL'):self.AUDIO_ITEM_INDEX_URL=val
            elif(i[0]=='AUDIO_ITEM_INDEX_PERFORMER'):self.AUDIO_ITEM_INDEX_ARTIST=val
            elif(i[0]=='AUDIO_ITEM_INDEX_TITLE'):self.AUDIO_ITEM_INDEX_TITLE=val
            elif(i[0]=='AUDIO_ITEM_INDEX_DURATION'):self.AUDIO_ITEM_INDEX_DURATION=val
            elif(i[0]=='AUDIO_ITEM_INDEX_ALBUM_ID'):self.AUDIO_ITEM_INDEX_ALBUM_ID=val
            elif(i[0]=='AUDIO_ITEM_INDEX_AUTHOR_LINK'):self.AUDIO_ITEM_INDEX_AUTHOR_LINK=val
            elif(i[0]=='AUDIO_ITEM_INDEX_LYRICS'):self.AUDIO_ITEM_INDEX_LYRICS=val
            elif(i[0]=='AUDIO_ITEM_INDEX_COVER_URL'):self.AUDIO_ITEM_INDEX_COVER_URL=val
            elif(i[0]=='AUDIO_ITEM_INDEX_MAIN_ARTISTS'):self.AUDIO_ITEM_INDEX_MAIN_ARTISTS=val
            elif(i[0]=='AUDIO_ITEM_INDEX_HASHES'):self.AUDIO_ITEM_INDEX_HASHES=val
            elif(i[0]=='AUDIO_ITEM_INDEX_TRACK_CODE'):self.AUDIO_ITEM_INDEX_TRACK_CODE=val;
        s =self.__get_hash(text,'actionHash');g =s.groups()[0]if s else None;
        self.AUDIO_ACTION_HASH_INDEX=int(g) if g.isdigit() else 2;
        #чтобы поиск шёл быстрее, обрезаем строку 
        if(s):
            text = text[s.start()-1000:-1 if len(text)>s.start()+4000 else (s.start()+4000)]
        s = self.__get_hash(text,'urlHash');g = s.groups()[0]if s else None;
        self.AUDIO_URL_HASH_INDEX=int(g) if g.isdigit() else 5;
        s=self.__get_hash(text,'editHash');g = s.groups()[0]if s else None;
        self.AUDIO_EDIT_HASH_INDEX=int(g) if g.isdigit() else 1;
        s=self.__get_hash(text,'restoreHash');g = s.groups()[0]if s else None;
        self.AUDIO_RESTORE_HASH_INDEX=int(g) if g.isdigit() else 6;
        s=self.__get_hash(text,'deleteHash');g = s.groups()[0]if s else None;
        self.AUDIO_DELETE_HASH_INDEX=int(g) if g.isdigit() else 3;

    def __get_hash(self,where,title):
        return re.search(title+':[a-z]+?\[(\d+?)\]',where)