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
        self._prompt = common.get("prompt", True)
        self.common = common
        self.fileMaxLines = common.get("file_max_lines", 800)
        self.fileSleep = common.get("file_sleep", 0.0005)
        self.outDir = common.get("output_path", "output")
        self._ask()

    def getProjects(self):
        allProjects = self._projects
        useProjects = list(filter(lambda p: p.get("enable", True), allProjects))
        for prjCfg in useProjects:
            name = prjCfg.get("name")
            if not (name and len(name)):
                continue
            prj = Project(name, self.outDir)
            prj.srcDir = prjCfg.get("src")
            prjExts = prjCfg.get("extensions")
            prj.extensions = prjExts if (prjExts and len(prjExts)) else self.common.get("extension")
            prjExclN = prjCfg.get("exclude_name")
            prj.excludeNames = prjExclN if (prjExclN and len(prjExclN)) else self.common.get("exclude_name")
            prjExclD = prjCfg.get("exclude_dir")
            prj.excludeDirs = prjExclD if (prjExclD and len(prjExclD)) else self.common.get("exclude_dir")
            yield prj

    def _show(self):
        print(toml.dumps(self._data))

    def _ask(self):
        msg = "Using customized configuration" if self._customized else "Using default configuration"
        print("\33[1;37m{}\33[00m".format(msg))
        self._show()
        # for key in self.__dict__.keys():
        #     if not key.startswith('_'):
        #         print("{:<16s}{}".format(key+":", self.__dict__.get(key)))
        print("-------")
        self._confirm()

    def _confirm(self):
        if self._prompt:
            choose = input("\33[1;37mConfirm and continue? \33[00m (y/N) ")
            if choose.lower() != "y":
                exit()
