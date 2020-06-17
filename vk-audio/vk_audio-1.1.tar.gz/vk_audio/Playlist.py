from lxml import html
class Playlist(object):
    def __init__(this,js:dict,r_h,vk):
        this.__reorder_hash=r_h
        this.owner_id=js['owner_id']
        this.id=js['id'];
        this.raw_id=js['raw_id']
        this.title=js['title']
        this.description=js['description']
        auth=html.fromstring(js['author_line'])
        this.author =auth.text
        this.author_href=auth.attrib['href']
        this.listens = js['listens']
        this.thumb=js['thumb'];
        this.audios_count=js['size']
        this.edit_hash=js['edit_hash']
        this.__vk=vk;