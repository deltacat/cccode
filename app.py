#!/usr/bin/python
import os
import string
from time import sleep

from util.config import Config
from util.project import Project


def process(prj: Project, fileMaxLines: int, fileSleep: float):
    filesNum = 0
    totalLines = 0
    print("\r\n\33[3;33m▷ processing {}\33[00m".format(prj.name))
    with open(prj.outFile, "w") as dest:
        maxLinesFile = ["", 0]
        for file, title in prj.walk():
            filesNum += 1
            dest.write("\r\n/*** " + title + " ***/\r\n")
            lines, linesNum = processFile(file)
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


def processFile(file: string):
    with open(file, "r") as src:
        lines = list(filter(_filterLine, src.readlines()))
        return lines, len(lines)


def _filterLine(line: string):
    content = line.lstrip()
    if len(content) == 0 or content.startswith("*") or content.startswith("/") or content.startswith("#"):
        return False
    return True


def main():
    cc = Config()
    outDir = cc.outDir
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    results = [process(p, cc.fileMaxLines, cc.fileSleep) for p in cc.getProjects()]
    print("\r\n-------")
    tmpl = "\33[0;33m{:20s} \33[00m\33[0;32m{:>8,d}\33[00m files \33[0;32m{:>8,d}\33[00m lines"
    totalFiles = 0
    totalLines = 0
    for result in results:
        print(tmpl.format(result[0][:20], result[1], result[2]))
        totalFiles += result[1]
        totalLines += result[2]
    print("-------")
    print("total {} projects, {:,d} files, {:,d} lines".format(len(results), totalFiles, totalLines))


if __name__ == "__main__":
    main()
