'''
From my stackoverflow answer http://stackoverflow.com/a/34159455/4720935
Table with a column of buttons
Method to know which button was clicked
'''
import sys
from PyQt4 import QtGui,QtCore

class myTable(QtGui.QTableWidget):
	
	def __init__(self,parent=None):
		super(myTable,self).__init__(parent)
		self.setColumnCount(2)
		
	def add_item(self,name):
		#new row
		row=self.rowCount()
		self.insertRow(row)
		
		#button in column 0
		button=QtGui.QPushButton(name)
		button.setProperty("name",name)
		button.setProperty("row",row)
		button.clicked.connect(self.on_click)
		self.setCellWidget(row,0,button)
		
		#text in column 1
		self.setItem(row,1,QtGui.QTableWidgetItem(name))

	def on_click(self):
		# find the item with the same name to get the row
		text=self.sender().property("name")
		row=self.sender().property("row")
		item=self.findItems(text,QtCore.Qt.MatchExactly)[0]
		print("Button click at row:",item.row(),row)
		# row property could be use if the rows are fixed
		# here it does not work because the table was sorted

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	
	widget = myTable()
	widget.add_item("unicorn")
	widget.add_item("kitten")
	widget.sortItems(1)
	widget.show()

	sys.exit(app.exec_())
