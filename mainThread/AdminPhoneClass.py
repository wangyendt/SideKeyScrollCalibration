# coding: utf-8

import AdbToolsClass

class AdminPhone:
    def __init__(self):
        self.adb = AdbToolsClass.AdbTools()
        self.set_admin()

    def set_admin(self):
        self.adb.execute('adb root')
        self.adb.execute('adb remount')
        self.adb.execute('adb shell chmod 777 /dev/ndt')
        self.adb.execute('adb shell setenforce 0')

    def export_data(self):
        self.adb.execute('adb pull /sdcard/NDT/EdgeSensorDemo/')

    def clear_data(self):
        pass_word = input('Input password if you want to delete:')
        if pass_word == 'wangye':
            self.adb.execute('adb shell rm /sdcard/NDT/EdgeSensorDemo/*')
        else:
            print('Deleting is not allowed.')
