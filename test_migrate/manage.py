#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='.', url='mysql://root:jvb1l0Iwata@db02.wsl.mind.meiji.ac.jp/test1?charset=utf8', debug='False')
