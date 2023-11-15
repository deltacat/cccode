import os
import string
from datetime import datetime


def _genOutFilename(base: string, name: string):
    suffix = datetime.now().strftime(r"-%Y%m%d%H%M%S.src.txt")
    return os.path.join(base, name + suffix)


class Project:
    def __init__(self, name: string, srcDir: string, outDir: string):
        self.name = name
        self.srcDir = srcDir
        self.outFile = _genOutFilename(outDir, name)

    def _setSets(self, key, coms: [], prjs: []):
        hasPrjCfg = prjs and len(prjs)
        prjSet = set(prjs) if hasPrjCfg else set()
        comSet = set(coms) if (coms and len(coms)) else set()
        self.__dict__[key] = comSet.union(prjSet)
        if (hasPrjCfg):
            print('{}: {} {}'.format(self.name, key, self.__dict__[key]))
        return self

    def setExtensions(self, comExts: [], prjExts: []):
        return self._setSets("extensions", comExts, prjExts)

    def setExcludeNames(self, comExclNames: [], prjExclNames: []):
        return self._setSets("excludeNames", comExclNames, prjExclNames)

    def setExcludeDirs(self, comExclDirs: [], prjExclDirs: []):
        return self._setSets("excludeDirs", comExclDirs, prjExclDirs)

    def walk(self):
        rootPath = self.srcDir
        if not os.path.isabs(rootPath):
            rootPath = os.path.abspath(rootPath)
        for top, _, fs in os.walk(rootPath):
            # cfs = [x.lower() for x in top.split(os.path.sep) if x]
            if self._validDir(top):
                for file in filter(lambda f: self._validFile(f), fs):
                    fullpath = os.path.join(top, file)
                    cfs = [x for x in top.split(os.path.sep) if x]
                    if len(cfs) > 3:
                        cfs = cfs[-3:].copy()
                    title = os.path.join(*cfs, file)
                    yield fullpath, title

    def _validDir(self, path: string):
        # 由于 os.walk 并非递归访问，无法仅判断“本级”文件夹，需对整个路径进行检查。对性能有一定影响。
        if path.find(os.path.sep + ".") > -1:
            return False
        if any(path.lower().find(x) > -1 for x in self.excludeDirs):
            return False
        return True

    def _validFile(self, filename: str):
        name, ext = os.path.splitext(filename)
        ext = ext.replace(".", "")

        # 排除 . 开头文件（一般为隐藏文件）
        if name.startswith("."):
            return False

        # 排除配置中需排除的文件
        for en in self.excludeNames:
            finding = en.lower()
            lName = filename.lower()
            if lName.find(finding) > -1:
                return False

        # 排除不包含的文件类型
        if ext.lower() not in self.extensions:
            return False

        return True
