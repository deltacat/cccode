#!/usr/bin/python
import os
import string
from datetime import datetime
from time import sleep

from util.config import Config
from util.finder import FileFinder

_OUT_DIR = "output"


def genOutFilename(project: string):
    suffix = datetime.now().strftime(r"-%Y%m%d%H%M%S.src.txt")
    return os.path.join(_OUT_DIR, project + suffix)


def processProject(finder: FileFinder, project: string, fileMaxLines: int, fileSleep: float):
    filesNum = 0
    totalLines = 0
    outfile = genOutFilename(project)
    print("\r\nprocessing", project, "...")
    with open(outfile, "w") as dest:
        maxLinesFile = ['', 0]
        for file, title in finder.walk(project):
            filesNum += 1
            dest.write("\r\n/*** " + title + " ***/\r\n")
            lines, linesNum = processFile(file)
            dest.writelines(lines)
            totalLines += linesNum
            print("\r{:<4d}".format(filesNum, linesNum), end="", flush=True)
            if linesNum > maxLinesFile[1]:
                maxLinesFile = [title, linesNum]
            if linesNum > fileMaxLines:
                print("\r-> {} has {:,d} lines".format(title, linesNum), flush=True)
            sleep(fileSleep)
        print("\r=> {} files. max lines {:,d}: {}"
              .format(filesNum, maxLinesFile[1], maxLinesFile[0]), flush=True)
    return project, filesNum, totalLines


def processFile(file: string):
    with open(file, 'r') as src:
        lines = list(filter(_filterLine, src.readlines()))
        return lines, len(lines)


def _filterLine(line: string):
    content = line.lstrip()
    if len(content) == 0 or content.startswith("*") or content.startswith("/") or content.startswith("#"):
        return False
    return True


def main():
    if not os.path.exists(_OUT_DIR):
        os.mkdir(_OUT_DIR)
    cc = Config()
    finder = FileFinder(cc)
    projects = cc.projects
    results = [processProject(finder, p, cc.fileMaxLines, cc.fileSleep)
               for p in projects]
    print("\r\n-------")
    tmpl = "\33[0;33m{:20s} \33[00m\33[0;32m{:>4,d}\33[00m files \33[0;32m{:>8,d}\33[00m lines"
    totalFiles = 0
    totalLines = 0
    for result in results:
        print(tmpl.format(*result))
        totalFiles += result[1]
        totalLines += result[2]
    print("-------")
    print("total {} projects, {:,d} files, {:,d} lines"
          .format(len(results), totalFiles, totalLines))


if __name__ == '__main__':
    main()
