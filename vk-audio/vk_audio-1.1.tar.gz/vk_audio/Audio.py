from .AudioList import AudioList
from .AudioEnumIndex import AudioEnumIndex
import vk_api
class Audio(object):
    __newPlaylistHash=None;
    __audiosReorderHash=None;
    __playlistsReorderHash=None;
    __listenedHash=None;
    def __init__(self,vkaudio,owner_id):
        self.owner_id=owner_id;
        self.Audios:AudioList=AudioList(vkaudio);
        self.Playlists=[]
        return


