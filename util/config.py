import re
import string
from configparser import ConfigParser


class Config:

    def __init__(self):
        """
        初始化配置类
        """

        defaultFile = "config.ini"
        userFile = "config.custom.ini"

        parser = ConfigParser()
        if parser.read(userFile, encoding="utf-8"):
            self._customized = True
        else:
            self._customized = False
            parser.read(defaultFile, encoding="utf-8")

        walkerItems = dict(parser.items("walker"))
        self._prompt = bool(walkerItems.get("prompt"))
        self._pathItems = pathItems = dict(parser.items("project-path"))
        projects = self._getCfg2Arr(walkerItems, "projects")

        self.projects = list(pathItems.keys()) if len(projects) == 0 else projects
        self.extensions = self._getCfg2Arr(walkerItems, "extension", True)
        self.excludeDirs = self._getCfg2Arr(walkerItems, "exclude_dir", True)
        self.excludeNames = self._getCfg2Arr(walkerItems, "exclude_name", True)
        self.fileSleep = float(walkerItems.get("file_sleep"))
        self.fileMaxLines = int(walkerItems.get("file_max_lines"))

        self._ask()

    def getProjectPath(self, project: string):
        return self._pathItems.get(project)

    def _ask(self):
        msg = "Using customized configuration" if self._customized else "Using default configuration"
        print("\33[1;37m{}\33[00m".format(msg))
        for key in self.__dict__.keys():
            if not key.startswith('_'):
                print("{:<16s}{}".format(key+":", self.__dict__.get(key)))
        print("-------")
        self._confirm()

    def _confirm(self):
        if self._prompt:
            choose = input("\33[1;37mConfirm and continue? \33[00m (y/N) ")
            if choose.lower() != 'y':
                exit()

    def _getCfg2Arr(self, items, key, toLower=False):
        rawVals = re.split(r"[,\s]+", items.get(key) or "")
        if toLower:
            return [s.lower() for s in rawVals if s]
        else:
            return [s for s in rawVals if s]
