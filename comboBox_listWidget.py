import sys, signal
from PyQt4 import QtCore, QtGui

class myWidget(QtGui.QWidget):
	def __init__( self, parent=None):
		super(myWidget, self ).__init__( parent )

		self.myDict={"Pet":['Dog','Cat'],"Bird":['Eagle','Jay','Falcon']}

		self.listWidget=QtGui.QListWidget()
		
		self.comboBox=QtGui.QComboBox()
		self.comboBox.addItems(list(self.myDict.keys()))
		#use overload signal: emits the text associated to the index 
		self.comboBox.currentIndexChanged[str].connect(self.on_change)
		#set initial index so the listWidget is not empty
		self.comboBox.setCurrentIndex(1)
		
		layout=QtGui.QVBoxLayout()
		layout.addWidget(self.comboBox)
		layout.addWidget(self.listWidget)
		self.setLayout(layout)
	
	def on_change(self,key):
		#clear everything
		self.listWidget.clear()
		#fill with list of corresponding key
		for name in self.myDict[key]:
			item=QtGui.QListWidgetItem(name)
			item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
			item.setCheckState(QtCore.Qt.Unchecked)
			self.listWidget.addItem(item)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win= myWidget()
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	win.show() 
	sys.exit(app.exec_())
