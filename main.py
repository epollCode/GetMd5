# -*- coding:utf-8 -*-

__author__ = 'dong'


import sys
from PyQt4.QtGui import QApplication
from view import HomeView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = HomeView()
    home.show()
    sys.exit(app.exec_())