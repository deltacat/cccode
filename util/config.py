import json
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
        rawPrjs = re.split(r"[,\s]+", walkerItems.get("projects") or "")
        projects = [s for s in rawPrjs if s]
        if len(projects) == 0:
            projects = list(pathItems.keys())

        extensions = json.loads(walkerItems.get("extension"))
        excludeDirs = json.loads(walkerItems.get("exclude_dir"))
        excludeNames = json.loads(walkerItems.get("exclude_name"))

        self.projects = projects
        self.extensions = set(ext.lower() for ext in extensions)
        self.excludeDirs = [ex.lower() for ex in excludeDirs]
        self.excludeNames = [ex.lower() for ex in excludeNames]
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
