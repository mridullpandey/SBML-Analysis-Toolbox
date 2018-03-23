from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import design
import os
import libsbml
import numpy

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
		
		# Initialize error log bytearray and display to user
		self.ErrorLog = QtCore.QString('')
		
		
	def syncErrorLog(self):
		self.modelErrorLog.setPlainText(self.ErrorLog)
		
	# Open file dialog and upacking data from SBML files
	def openModelFile(self):
		
		# Get SBMLModelPath from user input
		self.SBMLModelPath = str(QtGui.QFileDialog.getOpenFileName(filter = '*.xml'))
		
		# Read in SBML model file into SBML Document variable
		SBMLDoc = libsbml.readSBMLFromFile( self.SBMLModelPath )
    
		# Check if any major errors in reading SBML model
		# e.g. Filepath does not exist
		if SBMLDoc.getNumErrors() > 0:
			self.ErrorLog.append('ERROR: File reading errors.\n')
			self.ErrorLog.append(SBMLDoc.getErrorLog().toString()+'\n')

		# Make all parameters of the model global parameters.
		# Enables all parameters to be vectorized.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('promoteLocalParameters', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			self.ErrorLog.append('ERROR: Unable to convert parameters to global.\n')
			self.ErrorLog.append(SBMLDoc.getErrorLog().toString()+'\n')

		# Write out all reaction-specific function definitions.
		# Enables all variables in reactions to be swapped with vectorized
		# versions.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('expandFunctionDefinitions', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			self.ErrorLog.append('ERROR: Unable to expand internal function usage.\n')
			self.ErrorLog.append(SBMLDoc.getErrorLog().toString()+'\n')
	
		# Write out all state variable and parameter initializations.
		# Enables this data to be placed into required SciPyModel object
		# places.
		Properties = libsbml.ConversionProperties()
		Properties.addOption('expandInitialAssignments', True)
		if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
			self.ErrorLog.append('ERROR: Unable to expand initial assignments.\n')
			self.ErrorLog.append(SBMLDoc.getErrorLog().toString()+'\n')
        
		# Extract SBML Model object from SBML Document object.
		self.SBMLModel = SBMLDoc.getModel()
    
		# Extract MetaData data from SBML model object
		self.lineEditModelName.setText(str(self.SBMLModel.getName()))
		self.lineEditVolumeUnits.setText(str(self.SBMLModel.getVolumeUnits()))
		self.lineEditQuantityUnits.setText(str(self.SBMLModel.getSubstanceUnits()))	
		self.lineEditTimeUnits.setText(str(self.SBMLModel.getTimeUnits()))
    
		# Extract Compartment data from SBML model
		self.tableCompartments.setRowCount(self.SBMLModel.getNumCompartments())
		for i in range(self.tableCompartments.rowCount()):
			CurCompartment = self.SBMLModel.getCompartment(i)
			self.tableCompartments.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableCompartments.setItem(i, 1, QtGui.QTableWidgetItem(str(CurCompartment.name)))
			self.tableCompartments.setItem(i, 2, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
			self.tableCompartments.setItem(i, 3, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
		self.tableCompartments.resizeColumnsToContents()
		
		# Extract Species data from SBML Model
		self.tableSpecies.setRowCount(self.SBMLModel.getNumSpecies())
		for i in range(self.tableSpecies.rowCount()):
			CurSpecies = self.SBMLModel.getSpecies(i)
			self.tableSpecies.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableSpecies.setItem(i, 1, QtGui.QTableWidgetItem(str(CurSpecies.name)))
			self.tableSpecies.setItem(i, 2, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 3, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 4, QtGui.QTableWidgetItem(str(CurSpecies.boundary_condition)))
		self.tableSpecies.resizeColumnsToContents()
		
		# Create a vector of Species names for later use
		ListOfSpecies = self.getTableData(self.tableSpecies, 1, 0, 1, 
								self.SBMLModel.getNumSpecies()).flatten()
		
		# Extract Parameter data from SBML Model
		# -- Quantity, Names, Value, VectorIndex
		self.tableParameters.setRowCount(self.SBMLModel.getNumParameters())
		for i in range(self.tableParameters.rowCount()):
			CurParameter = self.SBMLModel.getParameter(i)
			self.tableParameters.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableParameters.setItem(i, 1, QtGui.QTableWidgetItem(str(CurParameter.name)))
			self.tableParameters.setItem(i, 2, QtGui.QTableWidgetItem(str(CurParameter.value)))
			self.tableParameters.setItem(i, 3, QtGui.QTableWidgetItem(str(True)))
		self.tableParameters.resizeColumnsToContents()
	
		# Extract Reaction data from SBML Model
		self.tableReactions.setRowCount(self.SBMLModel.getNumReactions())
		
		# Construct Stoichiometric Matrix from SBML Model
		# Expand Stoichiometric table to correct dimensions
		self.tableStoichMatrix.setRowCount(self.SBMLModel.getNumSpecies())
		self.tableStoichMatrix.setColumnCount(self.SBMLModel.getNumReactions())
		
		# Place Species names on vertical header for identification
		self.tableStoichMatrix.setVerticalHeaderLabels(ListOfSpecies)
		
		# Create empty numpy array of correct dimension for later use
		StoichMatrix = numpy.empty([self.SBMLModel.getNumSpecies(), 
										self.SBMLModel.getNumReactions()])
		
		for i in range(self.tableReactions.rowCount()):
			
			# Grab current reaction
			CurReaction = self.SBMLModel.getReaction(i)
			self.tableReactions.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			self.tableReactions.setItem(i, 1, QtGui.QTableWidgetItem(str(CurReaction.name)))
			self.tableReactions.setItem(i, 2, QtGui.QTableWidgetItem(str(CurReaction.getKineticLaw().getFormula())))
			
			# Assemeble stoichiometric matrix into a numpy array.
			for r in CurReaction.getListOfReactants():
				StoichMatrix[numpy.where(ListOfSpecies == r.getSpecies()), i] -= r.getStoichiometry()
			for p in CurReaction.getListOfProducts():
				StoichMatrix[numpy.where(ListOfSpecies == p.getSpecies()), i] += p.getStoichiometry()
	
			# Assemble list of reaction modifiers for clarity
			ListOfModifiers = []
			for m in CurReaction.getListOfModifiers():
				ListOfModifiers.append(str(m.getSpecies()))
			
			# Clean string for clarity and display in table
			ListOfModifiers = str(ListOfModifiers).replace('[', '').replace(']', '').replace('\'', '')
			self.tableReactions.setItem(i, 3, QtGui.QTableWidgetItem(ListOfModifiers))
			
			# Print compartment where reaction occurs
			self.tableReactions.setItem(i, 4, QtGui.QTableWidgetItem(CurReaction.getCompartment()))
			
		for i in range(self.tableStoichMatrix.rowCount()):
			for j in range(self.tableStoichMatrix.columnCount()):
				self.tableStoichMatrix.setItem(i,j,QtGui.QTableWidgetItem(str(StoichMatrix[i,j])))
	
		self.tableStoichMatrix.setHorizontalHeaderLabels(
				self.getTableData(self.tableReactions, 1, 0, 1, self.SBMLModel.getNumReactions()).flatten())
		
		# Update error log for user feedback on issues
		self.modelErrorLog.setPlainText(self.ErrorLog)
		
	
	# Interpret highlighted treeWidgetItem name as stackedWidget index
	def updatePageWidget(self):
		
		# Dictionary to convert name of treeWidget items to index of stackedWidget
		nameIndexDictionary = {'Model':0,'Compartments':1,'Species':2,
		'Parameters':3,'Reactions':4,'Matrices':5,'Code':6,
		'Simulation':7,'Time Course':8,'Local Sensitivity Analysis':9,
		'Global Sensitivity Analysis':10}
		
		# Change current page to treeWidget selection.
		try:
			self.stackedWidget.setCurrentIndex(
			nameIndexDictionary[str(self.treeWidget.currentItem().text(0))]
			)
		except:
			print 'ERROR: Unable to register treeWidget selection.'
		
		return None
	
	# Assemble data from QTableWidget into numpy array datatype	
	def getTableData(self, QTableWidget, MinColIndex=0, MinRowIndex=0, MaxColIndex=0, MaxRowIndex=0):
		
		RowRange = range(MaxRowIndex-MinRowIndex)
		ColRange = range(MaxColIndex-MinColIndex)
		
		if RowRange == []:
			RowRange = [0]
		if ColRange == []:
			ColRange = [0]
		
		# Initialize empty numpy array
		ReturnArray = numpy.empty([len(RowRange), len(ColRange)], dtype=object)
				
		# Iterate over columns and rows to populate NumPy array
		for i in RowRange:
			for j in ColRange:
				ReturnArray[i,j] = str(QTableWidget.item(i+MinRowIndex,j+MinColIndex).data(0).toString()) # This line may be an error bc of datatypes
				
		return ReturnArray
		
		
def main():
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()
	
if __name__ == '__main__':
	main()
