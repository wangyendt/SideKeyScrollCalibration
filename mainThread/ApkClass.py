# coding: utf-8

import AdbToolsClass


class Apk:
    def __init__(self):
        self.adb = AdbToolsClass.AdbTools()

    def install_apk(self, apk_path):
        self.adb.execute(''.join(('adb install ', apk_path)))

    def open_apk(self, apk_package_name, class_name=''):
        self.adb.execute(''.join(('adb shell am start -n ', apk_package_name, '/.', class_name)))

    def close_apk(self, apk_package_name):
        self.adb.execute(''.join(('adb shell am force-stop ', apk_package_name)))
