"""
动态加载ui文件
"""



from PyQt5.QtWidgets import QApplication, QMainWindow

import os
from PyQt5 import uic
import sys
class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.the_front_ui()

    def the_front_ui(self):
        self.ui1 = uic.loadUi("./the_front_ui.ui")
        self.division_set = self.ui1.horizontalSlider_3
        self.part_set = self.ui1.horizontalSlider_2
        self.division_browser = self.ui1.textBrowser
        self.part_browser = self.ui1.textBrowser_2
        self.address = self.ui1.lineEdit
        self.start_fov = self.ui1.pushButton




        self.division_set.valueChanged.connect(self.division_change)
        self.part_set.valueChanged.connect(self.part_change)
        self.start_fov.clicked.connect(self.fov_start)

    def division_change(self):
        self.d_level = self.division_set.value()
        self.division_browser.clear()
        self.division_browser.append("%d" %self.d_level)


    #have some problems
    def part_change(self):
        self.p_level = self.part_set.value()
        self.part_browser.clear()
        self.part_browser.append("%d" %self.p_level)



    def fov_start(self):
        #self.transp_level = self.p_level
        #self.tansd_level = self.d_level
        os.system("python ./FoV_Test.py")

        #FoV_Test()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    front1 = MyWindow()
    # 展示窗口
    front1.ui1.show()

    app.exec()