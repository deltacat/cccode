import os
import string
from time import sleep
from util.config import Config
from util.project import Project


def _processFile(file: string):
    with open(file, "r") as src:
        lines = list(filter(_filterLine, src.readlines()))
        return lines, len(lines)


def _filterLine(line: string):
    content = line.lstrip()
    if len(content) == 0 or content.startswith("*") or content.startswith("/") or content.startswith("#"):
        return False
    return True


class Processor:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.projects = [cfg.buildProject(p) for p in cfg.validPrjCfgs]

    def processAll(self):
        outDir = self.cfg.outDir
        if not os.path.exists(outDir):
            os.mkdir(outDir)
        return [self.process(p) for p in self.projects]

    def process(self, prj: Project):
        filesNum = 0
        totalLines = 0
        fileMaxLines = self.cfg.fileMaxLines
        fileSleep = self.cfg.fileSleep
        print("\r\n\33[3;33m▷ processing {}\33[00m".format(prj.name))
        with open(prj.outFile, "w") as dest:
            maxLinesFile = ["", 0]
            for file, title in prj.walk():
                filesNum += 1
                dest.write("\r\n/*** " + title + " ***/\r\n")
                lines, linesNum = _processFile(file)
                dest.writelines(lines)
                totalLines += linesNum
                print("\r{:<4d} files".format(filesNum, linesNum), end="", flush=True)
                if linesNum > maxLinesFile[1]:
                    maxLinesFile = [title, linesNum]
                if linesNum > fileMaxLines:
                    dLen = 60
                    dTitle = title if len(title) <= dLen else ("…" + title[-dLen + 1 :])
                    print("\r{:60s} \33[0;35m{:>8,d}\33[00m lines".format(dTitle, linesNum), flush=True)
                sleep(fileSleep)
            print("\r☞ {} files. max lines {:,d}: {}".format(filesNum, maxLinesFile[1], maxLinesFile[0]), flush=True)
        return prj.name, filesNum, totalLines
