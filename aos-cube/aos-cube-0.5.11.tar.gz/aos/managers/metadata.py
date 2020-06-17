from xml.etree import cElementTree

def ns_cleanup(qn):
    """ Get the tag from string like:
    {http://linux.duke.edu/metadata/repo}revision
    """
    if qn.find('}') == -1: return qn
    return qn.split('}')[1]

class RepoMDError(Exception):
    pass

class RepoData:
    """represents anything beneath a <data> tag"""
    def __init__(self, elem):
        self.type = None
        if elem:
            self.type = elem.attrib.get('type')

        self.location = (None, None)
        self.checksum = (None,None)     # type,value
        self.openchecksum = (None,None) # type,value
        self.timestamp = None
        self.dbversion = None
        self.size      = None
        self.opensize  = None
        self.deltas    = []

        if elem:
            self.parse(elem)

    def parse(self, elem):
        for child in elem:
            child_name = ns_cleanup(child.tag)
            if child_name == 'location':
                relative = child.attrib.get('href')
                base = child.attrib.get('base')
                self.location = (base, relative)
            elif child_name == 'checksum':
                csum_value = child.text
                csum_type = child.attrib.get('type')
                self.checksum = (csum_type,csum_value)
            elif child_name == 'open-checksum':
                csum_value = child.text
                csum_type = child.attrib.get('type')
                self.openchecksum = (csum_type, csum_value)
            elif child_name == 'timestamp':
                self.timestamp = child.text
            elif child_name == 'database_version':
                self.dbversion = child.text
            elif child_name == 'size':
                self.size = child.text
            elif child_name == 'open-size':
                self.opensize = child.text
            elif child_name == 'delta':
                delta = RepoData(child)
                delta.type = self.type
                self.deltas.append(delta)


class RepoMD():
    """represents the repomd xml file"""
    def __init__(self, repomd_xml):
        self.timestamp = 0
        self.repoData  = {}
        self.checksums = {}
        self.length    = 0
        self.revision  = None
        self.tags      = {'content' : set(), 'distro' : {}, 'repo': set()}

        if repomd_xml:
            self.parse(repomd_xml)

    def parse(self, repomd_xml):
        with open(repomd_xml, "r") as f:
            parser = cElementTree.iterparse(f)
            try:
                for event, elem in parser:
                    elem_name = ns_cleanup(elem.tag)
                    if elem_name == "data":
                        thisdata = RepoData(elem=elem)
                        self.repoData[thisdata.type] = thisdata
                    elif elem_name == "revision":
                        self.revision = elem.text
                    elif elem_name == "tags":
                        for child in elem:
                            child_name = ns_cleanup(child.tag)
                            if child_name == 'content':
                                self.tags['content'].add(child.text)
                            if child_name == 'distro':
                                cpeid = child.attrib.get('cpeid', '')
                                distro = self.tags['distro'].setdefault(cpeid,set())
                                distro.add(child.text)
            except SyntaxError as e:
                raise RepoMDError("Damaged repomd.xml file")

    def getData(self, type):
        if type in self.repoData:
            return self.repoData[type]
        else:
            raise RepoMDError("Requested datatype %s not available" % type)
