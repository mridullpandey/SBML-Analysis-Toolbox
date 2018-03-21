from PyQt4 import QtGui
import sys
import design

class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
	def __init__(self, parent=None):
		super(ExampleApp,self).__init__(parent)
		self.setupUi(self)
		
		self.treeWidget.currentItemChanged.connect(self.updatePageWidget)
		
	def updatePageWidget(self):
		nameIndexDictionary = {'Model':1,'Compartments':2}
		
		
		self.treeWidget.currentItem().text(0)
			
	
		
def main():
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()
	
if __name__ == '__main__':
	main()
