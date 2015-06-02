# Python implementation of github.com/fabienpn/simple-qt-thread-example
# mutex not implemented
# Tested with Linux OpenSuse, Python3.4 and PyQt4

#QT
import PyQt4.QtCore as PCore
import PyQt4.QtGui as PGui

import sys
import signal
import time


class Worker(PCore.QObject):
	valueChanged=PCore.pyqtSignal(int)   #in Pyside, replace pyqtSignal by Signal
	finished=PCore.pyqtSignal()
	workRequested=PCore.pyqtSignal()
	
	def __init__(self):
		super(Worker,self).__init__()
		self._working=False
		self._abort=False
		self.workRequested.emit()
	
	def requestWork(self):
		print("work requested")
		self._working=True
		self._abort=False
		self.workRequested.emit()

	def doWork(self):
		print("doWork")
		for i in range(10):
			if self._abort:
				break
			time.sleep(1)
			self.valueChanged.emit(i)
		self._working=False
		self.finished.emit()
		
	def abort(self):
		if self._working:
			self._abort=True
			print("abort requested")



class MainWindow(PGui.QWidget):

	def __init__(self):
		super(MainWindow,self).__init__()
		
		#Buttons
		self.button_start=PGui.QPushButton("Start")
		self.button_start.clicked.connect(self.on_start)
		self.button_cancel=PGui.QPushButton("Cancel")
		self.button_cancel.clicked.connect(self.on_cancel)
		self.button_cancel.setEnabled(False)
		
		#layout
		layout=PGui.QVBoxLayout()
		layout.addWidget(self.button_start)
		layout.addWidget(self.button_cancel)
		self.setLayout(layout)
		
		
		#Thread and worker
		self.thread=PCore.QThread()
		self.worker=Worker()
		self.worker.moveToThread(self.thread)
		
		self.worker.valueChanged.connect(self.display_progress)
		self.worker.workRequested.connect(self.thread.start)
		self.thread.started.connect(self.worker.doWork)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.on_finish)
		
		
	def display_progress(self,value):
		print("progress=",value)
		
	def on_start(self):
		self.button_start.setEnabled(False)
		self.button_cancel.setEnabled(True)
		self.worker.requestWork()
		
	def on_cancel(self):
		self.worker.abort()
		
	def on_finish(self):
		print("done")
		self.button_start.setEnabled(True)
		self.button_cancel.setEnabled(False)
		
		

if __name__=='__main__':
	PGui.QApplication.setStyle("cleanlooks")
	app=PGui.QApplication(sys.argv)
	
	#to be able to close wth ctrl+c
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	win=MainWindow()
	win.show()

	sys.exit(app.exec_())
