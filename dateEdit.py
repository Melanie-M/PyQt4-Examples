import sys
from PyQt4 import QtCore,QtGui
'''
subclass QDateEdit to only allow a list of valid day
nb: display by default in format MM/DD/YYYY
'''

class mainWindow(QtGui.QWidget):
	def __init__(self):
		super(mainWindow,self).__init__()

		dateEdit=customDate(self)
		
		layout=QtGui.QVBoxLayout()
		layout.addWidget(dateEdit)
		self.setLayout(layout)


class customDate(QtGui.QDateEdit):
	def __init__(self,parent):
		super(customDate, self).__init__(parent)
		self.dateChanged.connect(self.on_change)
		self.valid=[1,11,21]
		self.match={2:11,10:1,12:21,20:11,22:21}
		
	def on_change(self,date):
		day=date.day()
		if day in self.valid:
			return
		newDay=self.match[day]
		newDate=QtCore.QDate(date.year(),date.month(),newDay)
		self.setDate(newDate)

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	app.setStyle("plastique")
	mw = mainWindow()
	mw.show()
	sys.exit(app.exec_())
