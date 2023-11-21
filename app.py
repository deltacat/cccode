#!/usr/bin/python
import os
import string
from time import sleep

from util.config import Config
from util.project import Project
from util.processor import Processor


def ask(cfg: Config):
    cfg.show()
    if cfg.prompt:
        print("-------")
        choose = input("\33[1;37mConfirm and continue? \33[00m (y/N) ")
        if choose.lower() != "y":
            exit()


def main():
    cc = Config()
    ask(cc)
    results = Processor(cc).processAll()
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
