import json
from .processor import getSSP, getASP, SSP_Path, ASP_Path


class SSP(object):
    def __init__(self,name = "SSP"):
        self.name = name
        self.mySSP = None

    @getSSP
    def getSSP(self):
        """
        Read SSP file prepared by default in humo.

        input
        ======
        None

        output
        ======
        default SSP file [json]
        """
        with open("{}.json".format(self.name)) as f:
            b = json.load(f)
        #a = open("{}.json".format(self.name))
        #b = json.load(a)
        return b

    @SSP_Path
    def overwriteSSP(self,defaultfile):
        print("Do you want to save your default SSP file?")
        answer = input("y / n ? : ")
        if (answer.lower() == "y") or (answer.lower() == "yes"):
            with open("{}.json".format(self.name), "w") as f:
                json.dump(defaultfile, f, indent=4)
            #file = open("SSP.json","w")
            #json.dump(defaultfile, file, indent=4)
            print("The SSP file was saved successfully.")
        else:
            print("Saving of SSP file was canceled.")

    def read_mySSP(self, name):
        """
        Read the SSP file set by the individual.

        input
        ======
        name : file name or abs path + file name

        output
        ======
        ssp file [json] : The SSP file set by the individual.

        Note
        ======
        If you do not specify a file with an absolute path,
        navigate to the directory where your SSP file is stored.

        --------------------------------------------------------------------
        [Example]
        import os
        os.chdir("The path of the directory where your SSP file is stored")
        --------------------------------------------------------------------
        """
        with open("{}.json".format(name)) as f:
            b = json.load(f)
        #a = open("{}.json".format(name))
        #b = json.load(a)
        self.mySSP = b

    @SSP_Path
    def save_mySSP(self,filename):
        """
        Save your SSP file read with the readSSP method.

        input
        ======
        filename : str
        Your SSP file name

        output
        ======
        None
        """
        print("Do you want to save your SSP file?")
        answer = input("y / n ? : ")
        if (answer.lower() == "y") or (answer.lower() == "yes"):
            with open("{}.json".format(filename), "w") as f:
                json.dump(self.mySSP, f, indent=4)
            #file = open("{}.json".format(filename),"w")
            #json.dump(self.mySSP, file, indent=4)
            print("The SSP file was saved successfully.")
        else:
            print("Saving of SSP file was canceled.")

class ASP(object):
    def __init__(self,name = "ASP"):
        self.name = name
        self.myASP = None

    @getASP
    def getASP(self):
        """
        Read ASP file prepared by default in humo.

        input
        ======
        None

        output
        ======
        default ASP file [json]
        """
        a = open("{}.json".format(self.name))
        b = json.load(a)
        return b

    @ASP_Path
    def overwritASP(self,defaultfile):
        print("Do you want to save your default ASP file?")
        answer = input("y / n ? : ")
        if (answer.lower() == "y") or (answer.lower() == "yes"):
            file = open("ASP.json","w")
            json.dump(defaultfile, file, indent=4)
            print("The default ASP file was saved successfully.")
        else:
            print("Saving of default ASP file was canceled.")

    def read_myASP(self, name):
        """
        Read the ASP file set by the individual.

        input
        ======
        name : file name or abs path + file name

        output
        ======
        ssp file [json] : The ASP file set by the individual.

        Note
        ======
        If you do not specify a file with an absolute path,
        navigate to the directory where your ASP file is stored.

        --------------------------------------------------------------------
        [Example]
        import os
        os.chdir("The path of the directory where your SSP file is stored")
        --------------------------------------------------------------------
        """
        a = open("{}.json".format(name))
        b = json.load(a)
        self.myASP = b

    @ASP_Path
    def save_myASP(self,filename):
        """
        Save your ASP file read with the readASP method.

        input
        ======
        filename : str
        Your ASP file name

        output
        ======
        None
        """
        print("Do you want to save your ASP file?")
        answer = input("y / n ? : ")
        if (answer.lower() == "y") or (answer.lower() == "yes"):
            file = open("{}.json".format(filename),"w")
            json.dump(self.myASP, file, indent=4)
            print("The ASP file was saved successfully.")
        else:
            print("Saving of ASP file was canceled.")

def settings(SSPname, ASPname):
    ssp, asp = SSP(SSPname), ASP(ASPname)
    return ssp.getSSP(), asp.getASP()

