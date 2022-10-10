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
            print("使用自定义配置：")
        else:
            parser.read(defaultFile, encoding="utf-8")
            print("使用默认配置：")

        walkerItems = dict(parser.items("walker"))
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
        for key in self.__dict__.keys():
            if not key.startswith('_'):
                print("\33[1;37m{:<16s}\33[00m{}".format(
                    key+":", self.__dict__.get(key)))
        # self._confirm()

    def _confirm(self):
        choose = input("\33[0;33m确认配置无误并继续? \33[00m (y/N) ")
        if choose.lower() != 'y':
            exit()

    def _getCfg2Arr(self, items, key, toLower = False):
        rawVals = re.split(r"[,\s]+", items.get(key) or "")
        if toLower:
            return [s.lower() for s in rawVals if s]
        else:
            return [s for s in rawVals if s]
