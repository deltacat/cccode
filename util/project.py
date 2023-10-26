import os
import string
from datetime import datetime


def _genOutFilename(base: string, name: string):
    suffix = datetime.now().strftime(r"-%Y%m%d%H%M%S.src.txt")
    return os.path.join(base, name + suffix)


class Project:
    def __init__(self, name: string, outDir: string):
        self.name = name
        self.outFile = _genOutFilename(outDir, name)

    def walk(self):
        rootPath = self.srcDir
        if not os.path.isabs(rootPath):
            rootPath = os.path.abspath(rootPath)
        for top, _, fs in os.walk(rootPath):
            # cfs = [x.lower() for x in top.split(os.path.sep) if x]
            if not self._validDir(top):
                continue
            for file in fs:
                if self._validFile(file):
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

        if name.startswith("."):
            return False

        for en in self.excludeNames:
            if name.lower().find(en) > -1:
                return False

        if ext.lower() in self.extensions:
            return True

        return False
