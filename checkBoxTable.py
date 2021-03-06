# 2015, T.Moreau
# Tested on OpenSuse, Python2 and Python3
# 
# Display a table with checkbox on the left and custom list model
# CheckBox on the header to check all / check none (if list partially checked, header box set to uncheck)
#
# Subclass QHeaderView and QAbstractTableModel

import sys
import signal
from PyQt4 import QtCore,QtGui

#---------------------------------------------------------------------------------------------------------
# Custom checkbox header
#---------------------------------------------------------------------------------------------------------
#Draw a CheckBox to the left of the first column
#Emit clicked when checked/unchecked
class CheckBoxHeader(QtGui.QHeaderView):
	clicked=QtCore.pyqtSignal(bool)
	_x_offset = 3
	_y_offset = 0 #value calculated later
	_width = 20
	_height = 20
	
	def __init__(self,orientation=QtCore.Qt.Horizontal,parent=None):
		super(CheckBoxHeader,self).__init__(orientation,parent)
		self.setResizeMode(QtGui.QHeaderView.Stretch)
		self.resizeSection(0,20)
		self.isChecked=0
		
	def paintSection(self,painter,rect,logicalIndex):
		painter.save()
		super(CheckBoxHeader,self).paintSection(painter,rect,logicalIndex)
		painter.restore()
		if logicalIndex==0:
			self._y_offset=int((rect.height()-self._width)/2)
			option=QtGui.QStyleOptionButton()
			option.rect= QtCore.QRect(rect.x()+self._x_offset,rect.y()+self._y_offset, self._width,self._height)
			option.state=QtGui.QStyle.State_Enabled | QtGui.QStyle.State_Active
			if self.isChecked==2:
				option.state|=QtGui.QStyle.State_NoChange
			elif self.isChecked==1:
				option.state|=QtGui.QStyle.State_On
			else:
				option.state|=QtGui.QStyle.State_Off
				
			self.style().drawControl(QtGui.QStyle.CE_CheckBox,option,painter)
			
	def updateCheckState(self,state):
		self.isChecked=state
		self.viewport().update()
		
	def mousePressEvent(self,event):
		index=self.logicalIndexAt(event.pos())
		if 0<=index<self.count():
			x = self.sectionPosition(index)
			condX=x + self._x_offset < event.pos().x() < x + self._x_offset + self._width
			condY=self._y_offset < event.pos().y() < self._y_offset + self._height
			if condX and condY:
				if self.isChecked:
					self.isChecked=False
				else:
					self.isChecked=True
				self.clicked.emit(self.isChecked)
				self.viewport().update()
				return
		super(CheckBoxHeader, self).mousePressEvent(event)

#---------------------------------------------------------------------------------------------------------
# Table Model, with checkBoxed on the left
#---------------------------------------------------------------------------------------------------------
#On row in the table
class RowObject(object):
	def __init__(self):
		self.col0="column 0"
		self.col1="column 1"

class Model(QtCore.QAbstractTableModel):
	changeChecked=QtCore.pyqtSignal(int)  #emit when one or more rows are checked/unchecked
	
	def __init__(self,parent=None):
		super(Model,self).__init__(parent)
		#Model= list of object
		self.myList=[RowObject(),RowObject()]
		#Keep track of which object are checked
		self.checkList=[]
		#custom header
		self.header=CheckBoxHeader()
		self.header.clicked.connect(self.headerClick)
		
	def rowCount(self,QModelIndex):
		return len(self.myList)
	
	def columnCount(self,QModelIndex):
		return 2
	
	def addOneRow(self,rowObject):
		frow=len(self.myList)
		self.beginInsertRows(QtCore.QModelIndex(),row,row)
		self.myList.append(rowObject)
		self.endInsertRows()
		
	def data(self,index,role):
		row=index.row()
		col=index.column()
		if role==QtCore.Qt.DisplayRole:
			if col==0:
				return self.myList[row].col0
			if col==1:
				return self.myList[row].col1
		elif role==QtCore.Qt.CheckStateRole:
			if col==0:
				if self.myList[row] in self.checkList:
					return QtCore.Qt.Checked
				else:
					return QtCore.Qt.Unchecked
		#Color in grey if checked
		elif role==QtCore.Qt.BackgroundRole:
			if self.myList[row] in self.checkList:
				color=QtGui.QBrush(QtCore.Qt.lightGray)
				return color
		
	def setData(self,index,value,role):
		row=index.row()
		col=index.column()
		if role==QtCore.Qt.CheckStateRole and col==0:
			rowObject=self.myList[row]
			if rowObject in self.checkList:
				self.checkList.remove(rowObject)
			else:
				self.checkList.append(rowObject)
			#we changed the color of the whole line, not just this cell
			lastIndex=self.index(row,col+1)
			self.dataChanged.emit(index,lastIndex)  
			#number of row checked
			nbChecked=len(self.checkList)
			self.changeChecked.emit(nbChecked)
			self.updateHeader(nbChecked)
		return True
	
	def flags(self,index):
		if index.column()==0:
			return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
		return QtCore.Qt.ItemIsEnabled
	
	def headerData(self,section,orientation,role):
		if role==QtCore.Qt.DisplayRole:
			if orientation==QtCore.Qt.Horizontal:
				if section==0:
					return "Title 1"
				elif section==1:
					return "Title 2"
				
	def headerClick(self,isCheck):
		self.beginResetModel()
		if isCheck:
			self.checkList=self.myList[:]
		else:
			self.checkList=[]
		self.changeChecked.emit(len(self.checkList))
		self.endResetModel()
		
	def updateHeader(self,nbChecked):
		if nbChecked==0:
			self.header.updateCheckState(0)
		elif nbChecked==len(self.myList):
			self.header.updateCheckState(1)
		else:
			self.header.updateCheckState(2)
	

if __name__=='__main__':
	app=QtGui.QApplication(sys.argv)
	
	#to be able to close with ctrl+c
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	tableView=QtGui.QTableView()
	model=Model(parent=tableView)
	tableView.setModel(model)
	tableView.setHorizontalHeader(model.header)
	tableView.show()

	sys.exit(app.exec_())