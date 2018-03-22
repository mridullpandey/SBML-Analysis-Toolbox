from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import design
import os
import libsbml
from utils import SBML2SciPy2
# For debugging, ensures latest GUI design is used during execution
os.system('pyuic4 design.ui -o design.py')


class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
	def __init__(self, parent=None):
		super(ExampleApp,self).__init__(parent)
		self.setupUi(self)
		
		# Enable switching of stackedWidget pages via treeWidget interface
		self.treeWidget.currentItemChanged.connect(self.updatePageWidget)
		
		# Enable opening of SBML model files via menubar
		self.actionOpen.triggered.connect(self.openModelFile)
		
		
		
	# Open file dialog and upacking data from SBML files
	def openModelFile(self):
		# Get SBMLModelPath from user input
		self.SBMLModelPath = str(QtGui.QFileDialog.getOpenFileName(filter = '*.xml'))
		
		# Read in SBML model file into SBML Document variable
		SBMLDoc = libsbml.readSBMLFromFile( self.SBMLModelPath )
    
		# Check if any major errors in reading SBML model
		# e.g. Filepath does not exist
		if SBMLDoc.getNumErrors() > 0:
			print('ERROR: File reading errors.')
			print(SBMLDoc.getErrorLog().toString())

		# Make all parameters of the model global parameters.
		# Enables all parameters to be vectorized.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('promoteLocalParameters', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			print('ERROR: Unable to convert parameters to global.')
			print(SBMLDoc.getErrorLog().toString())

		# Write out all reaction-specific function definitions.
		# Enables all variables in reactions to be swapped with vectorized
		# versions.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('expandFunctionDefinitions', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			print('ERROR: Unable to expand internal function usage.')
			print(SBMLDoc.getErrorLog().toString())
	
		# Write out all state variable and parameter initializations.
		# Enables this data to be placed into required SciPyModel object
		# places.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('expandInitialAssignments', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			print('ERROR: Unable to expand initial assignments.')
			print(SBMLDoc.getErrorLog().toString())
        
		# Extract SBML Model object from SBML Document object.
		self.SBMLModel = SBMLDoc.getModel()
    
		# Extract MetaData data from SBML model
		# -- Name, VolumeUnits, SubstanceUnits, TimeUnits
		self.lineEditModelName.setText(self.SBMLModel.getName())
		self.lineEditVolumeUnits.setText(self.SBMLModel.getVolumeUnits())
		self.lineEditQuantityUnits.setText(self.SBMLModel.getSubstanceUnits())
		
		print self.SBMLModel.getSubstanceUnits()
		
		self.lineEditTimeUnits.setText(self.SBMLModel.getTimeUnits())
    
		# Extract Compartment data from SBML model
		# -- Quantity, Names, VectorIndex
		self.tableCompartments.setRowCount(self.SBMLModel.getNumCompartments())
		for i in range(self.tableCompartments.rowCount()):
			CurCompartment = self.SBMLModel.getCompartment(i)
			self.tableCompartments.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableCompartments.setItem(i, 1, QtGui.QTableWidgetItem(str(CurCompartment.name)))
			self.tableCompartments.setItem(i, 2, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
			self.tableCompartments.setItem(i, 3, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
		
		# Extract Species data from SBML Model
		# -- Quanity, Names, Value, VectorIndex, BoundaryValue
		self.tableSpecies.setRowCount(self.SBMLModel.getNumSpecies())
		for i in range(self.tableSpecies.rowCount()):
			CurSpecies = self.SBMLModel.getSpecies(i)
			self.tableSpecies.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableSpecies.setItem(i, 1, QtGui.QTableWidgetItem(str(CurSpecies.name)))
			self.tableSpecies.setItem(i, 2, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 3, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 4, QtGui.QTableWidgetItem(str(CurSpecies.boundary_condition)))
	
		# Extract Parameter data from SBML Model
		# -- Quantity, Names, Value, VectorIndex
		self.tableParameters.setRowCount(self.SBMLModel.getNumParameters())
		for i in range(self.tableParameters.rowCount()):
			CurParameter = self.SBMLModel.getParameter(i)
			self.tableParameters.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableParameters.setItem(i, 1, QtGui.QTableWidgetItem(str(CurParameter.name)))
			self.tableParameters.setItem(i, 2, QtGui.QTableWidgetItem(str(CurParameter.value)))
			self.tableParameters.setItem(i, 3, QtGui.QTableWidgetItem(str(True)))
		
	
	
	
	
	# Interpret highlighted treeWidgetItem name as stackedWidget index
	def updatePageWidget(self):
		
		# Dictionary to convert name of treeWidget items to index of stackedWidget
		nameIndexDictionary = {'Model':0,'Compartments':1,'Species':2,
		'Parameters':3,'Reactions':4,'Matrices':5,'Layout':6,
		'Simulation':7,'Time Course':8,'Local Sensitivity Analaysis':9,
		'Global Sensitivity Analysis':10}
		
		# Change current page to treeWidget selection.
		try:
			self.stackedWidget.setCurrentIndex(
			nameIndexDictionary[str(self.treeWidget.currentItem().text(0))]
			)
		except:
			print 'ERROR: Unable to register treeWidget selection.'
			
	
		
def main():
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()
	
if __name__ == '__main__':
	main()
