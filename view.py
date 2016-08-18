# -*- coding:utf-8 -*-

__author__ = 'dong'

import os
import io
import datetime
import hashlib
from PyQt4.QtGui import QMainWindow, QIcon, QFileDialog, QDesktopWidget
from PyQt4.QtCore import pyqtSlot, QThread, Qt, pyqtSignal
from home import Ui_MainWindow

class HomeView(QMainWindow):

    def __init__(self, parent=None):
        super(HomeView, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('MD5')
        # self.setWindowIcon(QIcon('md5.ico'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())

        screen=QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.ui.plainTextEdit_result.setPlainText(u'欢迎使用MD5获取工作！！！\n作者联系方式:850246539@qq.com')


    def set_md5(self, content):
        '''
        写入md5
        :return:
        '''
        self.ui.plainTextEdit_result.setPlainText(os.path.basename(unicode(self.ui.lineEdit_path.text())))
        self.ui.plainTextEdit_result.appendPlainText(content)


    @pyqtSlot()
    def on_pushButton_select_clicked(self):
        '''
        选择
        :return:
        '''
        file_path = QFileDialog.getOpenFileName(self, u'选择文件', '.', '*.*')
        path = unicode(file_path)
        if os.path.isfile(path):
            self.ui.plainTextEdit_result.setPlainText(u'计算中...')
            self.ui.lineEdit_path.setText(path)
            self.m = Md5(path)
            self.m.finishSignal.connect(self.set_md5)
            self.m.start()

    @pyqtSlot()
    def on_pushButton_save_clicked(self):
        '''
        保存
        :return:
        '''
        path = unicode(self.ui.lineEdit_path.text())
        if not path:
            filename = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        else:
            filename = os.path.basename(path).split('.')[-2]
        content = self.ui.plainTextEdit_result.toPlainText()
        with open(filename+'_md5.txt', 'w') as fd:
            fd.write(content+'\n'+str(datetime.datetime.today()))
        self.statusBar().showMessage(filename+ u'_md5.txt 保存成功...')


class Md5(QThread):

    finishSignal = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super(Md5, self).__init__(parent)
        self.file_path = file_path

    def run(self):
        m = hashlib.md5()
        file = io.FileIO(self.file_path, 'r')
        bytes = file.read(10240)
        while (bytes != b''):
            m.update(bytes)
            bytes = file.read(10240)
        file.close()
        self.finishSignal.emit(m.hexdigest())
