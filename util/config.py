import toml

from util.project import Project


def _merge(c1, c2):
    for key in c2.keys():
        if (key not in c1.keys()) or (not isinstance(c2[key], dict)):
            c1[key] = c2[key]
        else:
            _merge(c1[key], c2[key])


class Config:
    def __init__(self):
        """
        初始化配置类
        """
        data = toml.load("config.toml")
        try:
            ccUser = toml.load("config.custom.toml")
            _merge(data, ccUser)
            self._customized = True
        except:
            self._customized = False
        common = data.get("common", {})
        self._data = data
        self._projects = data.get("projects", [])
        self.prompt = common.get("prompt", True)
        self.common = common
        self.fileMaxLines = common.get("file_max_lines", 800)
        self.fileSleep = common.get("file_sleep", 0.0005)
        self.outDir = common.get("output_path", "output")
        self.comExts = self.common.get("extension")
        self.comExclDirs = self.common.get("exclude_dir")
        self.comExclNames = self.common.get("exclude_name")
        self.validPrjCfgs = list(self._getValidPrjCfgs())

    def _getValidPrjCfgs(self):
        for prjCfg in self._projects:
            enabled = prjCfg.get("enable", True)
            name = prjCfg.get("name")
            if enabled and name and len(name):
                yield prjCfg

    def buildProject(self, prjCfg):
        prj = Project(prjCfg.get("name"), prjCfg.get("src"), self.outDir)
        prj.setExtensions(self.comExts, prjCfg.get("extensions"))
        prj.setExcludeDirs(self.comExclDirs, prjCfg.get("exclude_dir"))
        prj.setExcludeNames(self.comExclNames, prjCfg.get("exclude_name"))
        return prj

    def getProjects(self):
        for prjCfg in self.validPrjCfgs:
            yield self.buildProject(prjCfg)

    def show(self):
        msg = "Using customized configuration" if self._customized else "Using default configuration"
        print("\33[1;37m{}\33[00m".format(msg))
        print(toml.dumps(self.common))
        print(toml.dumps({"projects": self.validPrjCfgs}))
