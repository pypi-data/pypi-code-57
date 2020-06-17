import os
from pyPhases import Project
from pyPhases.util.Optionizable import Optionizable
from pyPhases.Data import Data


class Phase(Optionizable):
    name = ""
    config = {}
    metrics = {}
    summary = {}
    inputs = []
    model = None
    runMethod = "main"
    project: Project = None
    exportData = []
    exportDataStrings = []
    decorators = None
    _prepared = False

    def prepare(self):
        if(self._prepared):
            return
        self.logDebug("Prepare phase: " + self.name)
        self.exportData = list(map(lambda s: Data.create(s, self.project), self.exportData))
        self.exportDataStrings = list(map(lambda data: data.name, self.exportData))
        self._prepared = True

    def getDecorators(self):
        if not self.decorators == None:
            return self.decorators

        self.decorators = []
        for decorator in self.project.decorators:
            if(decorator.filter(self)):
                self.decorators.append(decorator)

        return self.decorators

    def getData(self, name):
        self.run()

    def run(self):
        self.log("RUN phase: " + self.name)

        def methodNotFound():
            self.logError("The current phase needs the following method defined: " +
                      self.runMethod)

        method = getattr(self, self.runMethod, methodNotFound)
        decorators = self.getDecorators()

        for decorator in decorators:
            decorator.before(self)

        method()

        for decorator in decorators:
            decorator.after(self)
