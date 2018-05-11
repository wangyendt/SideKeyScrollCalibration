# coding: utf-8

import os


class AdbTools:
    def execute(self, cmd):
        info = self.private_execute(cmd)
        if info is not '':
            print(info)

    @staticmethod
    def private_execute(cmd):
        return os.popen(cmd).read()
