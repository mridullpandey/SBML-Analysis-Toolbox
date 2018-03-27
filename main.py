from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import sys
import design
import os
import libsbml
import numpy
import re

from string import ascii_letters

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
		self.actionOpen.triggered.connect(self.loadModelFile)
		
		# Enable creation of new SBML model files via menubar
		self.actionNew.triggered.connect(self.newModelFile)
		
		# Initialize error log bytearray and display to user
		self.ErrorLog = QtCore.QString('')
		self.SpeciesErrors = QtCore.QString('')
		self.ParameterErrors = QtCore.QString('')
		
		# Initialize species table
		self.tableSpecies.setItem(0, 0, QtGui.QTableWidgetItem('s[0]'))
		self.tableSpecies.setItem(0, 1, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setItem(0, 2, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setItem(0, 3, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setCellWidget(0, 4, QtGui.QSpinBox())
		self.tableSpecies.setCellWidget(0, 5, QtGui.QCheckBox())
		self.tableSpecies.setItem(0, 6, QtGui.QTableWidgetItem('s[0]'))
		
		# Initialize parameter table
		self.tableParameters.setItem(0, 0, QtGui.QTableWidgetItem('p[0]'))
		self.tableParameters.setItem(0, 1, QtGui.QTableWidgetItem(''))
		self.tableParameters.setItem(0, 2, QtGui.QTableWidgetItem(''))
		self.tableParameters.setCellWidget(0, 3, QtGui.QCheckBox())
		self.tableParameters.setItem(0, 4, QtGui.QTableWidgetItem('p[0]'))
		
		# Connect auto extending functionality of datatables
		self.tableSpecies.itemChanged.connect(self.updateTableSpecies)
		self.tableParameters.itemChanged.connect(self.updateTableParameters)
	
	# Function to reinitialize software for a new model
	def newModelFile(self):
		
		# Reset species table to empty state
		self.tableSpecies.setRowCount(0); self.tableSpecies.setRowCount(1)
		self.tableSpecies.setItem(0, 0, QtGui.QTableWidgetItem('s[0]'))
		self.tableSpecies.setItem(0, 1, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setItem(0, 2, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setItem(0, 3, QtGui.QTableWidgetItem(''))
		self.tableSpecies.setCellWidget(0, 4, QtGui.QSpinBox())
		self.tableSpecies.setCellWidget(0, 5, QtGui.QCheckBox())
		self.tableSpecies.setItem(0, 6, QtGui.QTableWidgetItem('s[0]'))
		
		# Reset parameter table to empty state
		self.tableParameters.setRowCount(0); self.tableParameters.setRowCount(1)
		self.tableParameters.setItem(0, 0, QtGui.QTableWidgetItem('p[0]'))
		self.tableParameters.setItem(0, 1, QtGui.QTableWidgetItem(''))
		self.tableParameters.setItem(0, 2, QtGui.QTableWidgetItem(''))
		self.tableParameters.setCellWidget(0, 3, QtGui.QCheckBox())
		self.tableParameters.setItem(0, 4, QtGui.QTableWidgetItem('p[0]'))
	
	# Function to automatically extend parameter table as needed
	def updateTableSpecies(self):
		
		# Reset ParameterErrorLog
		self.SpeciesErrors = QtCore.QString('')
		
		# Get length of table
		FinalRowIndex = self.tableSpecies.rowCount()
		
		# Check if either the name, value or metadata functions have been modified
		# If they have been, extend the table.
		try:
			if (self.tableSpecies.item(FinalRowIndex-1,1).data(0) != QtGui.QTableWidgetItem('').data(0)
		     or self.tableSpecies.item(FinalRowIndex-1,2).data(0) != QtGui.QTableWidgetItem('').data(0)):
				 
					self.tableSpecies.insertRow(FinalRowIndex)
					self.tableSpecies.setItem(FinalRowIndex, 0, QtGui.QTableWidgetItem('s[0]'))
					self.tableSpecies.setItem(FinalRowIndex, 1, QtGui.QTableWidgetItem(''))
					self.tableSpecies.setItem(FinalRowIndex, 2, QtGui.QTableWidgetItem(''))
					self.tableSpecies.setItem(FinalRowIndex, 3, QtGui.QTableWidgetItem(''))
					self.tableSpecies.setCellWidget(FinalRowIndex, 4, QtGui.QSpinBox())
					self.tableSpecies.setCellWidget(FinalRowIndex, 5, QtGui.QCheckBox())
					self.tableSpecies.setItem(FinalRowIndex, 6, QtGui.QTableWidgetItem('s[0]'))
					
			# Highlight errors in index, name, value, and metaid
			for i in range(self.tableSpecies.rowCount()-1):
				if self.tableSpecies.item(i,0).data(0) != QtGui.QTableWidgetItem('s['+str(i)+']').data(0):
					self.tableSpecies.setItem(i,0,QtGui.QTableWidgetItem('s['+str(i)+']'))
					self.SpeciesErrors.append('Illegal index name change attempt in row '+str(i)+'\n')
				else:
					self.tableSpecies.item(i,0).setBackground(QtGui.QColor(255,255,255))
				
				if not (all(ord(char) < 128 for char in str(self.tableSpecies.item(i,1).data(0).toString())) and
				    any(c.isalpha() for c in str(self.tableSpecies.item(i,1).data(0).toString()))):
					self.tableSpecies.item(i,1).setBackground(QtGui.QColor(255,150,150))
					self.SpeciesErrors.append('Name error in row '+str(i)+'\n')
				else:
					self.tableSpecies.item(i,1).setBackground(QtGui.QColor(255,255,255))
				
				try:
					float(str(self.tableSpecies.item(i,2).data(0).toString()))
					self.tableSpecies.item(i,2).setBackground(QtGui.QColor(255,255,255))
				except ValueError:
					self.tableSpecies.item(i,2).setBackground(QtGui.QColor(255,150,150))
					self.SpeciesErrors.append('Value error in row '+str(i)+'\n')
					
		except AttributeError:
			pass
			
		# Display parameter errors for user feedback
		self.speciesErrorLog.clear()
		self.speciesErrorLog.setPlainText(self.SpeciesErrors)
	
	# Function to automatically extend parameter table as needed
	def updateTableParameters(self):
		
		# Reset ParameterErrorLog
		self.ParameterErrors = QtCore.QString('')
		
		# Get length of table
		FinalRowIndex = self.tableParameters.rowCount()
		
		# Check if either the name, value or metadata functions have been modified
		# If they have been, extend the table.
		try:
			if (self.tableParameters.item(FinalRowIndex-1,1).data(0) != QtGui.QTableWidgetItem('').data(0)
		     or self.tableParameters.item(FinalRowIndex-1,2).data(0) != QtGui.QTableWidgetItem('').data(0)
			 or self.tableParameters.item(FinalRowIndex-1,4).data(0) != QtGui.QTableWidgetItem('p['+str(FinalRowIndex-1)+']').data(0)):
					self.tableParameters.insertRow(FinalRowIndex)
					self.tableParameters.setItem(FinalRowIndex, 0, QtGui.QTableWidgetItem('p['+str(FinalRowIndex)+']'))
					self.tableParameters.setItem(FinalRowIndex, 1, QtGui.QTableWidgetItem(''))
					self.tableParameters.setItem(FinalRowIndex, 2, QtGui.QTableWidgetItem(''))
					self.tableParameters.setCellWidget(FinalRowIndex, 3, QtGui.QCheckBox())
					self.tableParameters.setItem(FinalRowIndex, 4, QtGui.QTableWidgetItem('p['+str(FinalRowIndex)+']'))
					
			# Highlight errors in index, name, value, and metaid
			for i in range(self.tableParameters.rowCount()-1):
				if self.tableParameters.item(i,0).data(0) != QtGui.QTableWidgetItem('p['+str(i)+']').data(0):
					self.tableParameters.setItem(i,0,QtGui.QTableWidgetItem('p['+str(i)+']'))
					self.ParameterErrors.append('Illegal index name change attempt in row '+str(i)+'\n')
				else:
					self.tableParameters.item(i,0).setBackground(QtGui.QColor(255,255,255))
				
				if not (all(ord(char) < 128 for char in str(self.tableParameters.item(i,1).data(0).toString())) and
				    any(c.isalpha() for c in str(self.tableParameters.item(i,1).data(0).toString()))):
					self.tableParameters.item(i,1).setBackground(QtGui.QColor(255,150,150))
					self.ParameterErrors.append('Name error in row '+str(i)+'\n')
				else:
					self.tableParameters.item(i,1).setBackground(QtGui.QColor(255,255,255))
				
				try:
					float(str(self.tableParameters.item(i,2).data(0).toString()))
					self.tableParameters.item(i,2).setBackground(QtGui.QColor(255,255,255))
				except ValueError:
					self.tableParameters.item(i,2).setBackground(QtGui.QColor(255,150,150))
					self.ParameterErrors.append('Value error in row '+str(i)+'\n')
					
		except AttributeError:
			pass
			
		# Display parameter errors for user feedback
		self.parameterErrorLog.clear()
		self.parameterErrorLog.setPlainText(self.ParameterErrors)
				
		
				
	
	def syncErrorLog(self):
		self.modelErrorLog.setPlainText(self.ErrorLog)
		
	# Open file dialog and upacking data from SBML files
	def loadModelFile(self):
		
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
			self.tableCompartments.setItem(i, 0, QtGui.QTableWidgetItem('c['+str(i)+']'))
			
			if not str(CurCompartment.getName()):
				self.tableCompartments.setItem(i, 1, 
					QtGui.QTableWidgetItem('default'+str(i)))
				self.tableCompartments.item(i, 1).setBackground(QtGui.QColor(255,255,150))
			else:
				self.tableCompartments.setItem(i, 1, 
					QtGui.QTableWidgetItem(str(CurCompartment.getName())))
			
			self.tableCompartments.setItem(i, 2, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
			self.tableCompartments.setItem(i, 3, QtGui.QTableWidgetItem(str(CurCompartment.volume)))
		self.tableCompartments.resizeColumnsToContents()
		
		# Extract Species data from SBML Model
		self.tableSpecies.setRowCount(self.SBMLModel.getNumSpecies())
		for i in range(self.tableSpecies.rowCount()):
			CurSpecies = self.SBMLModel.getSpecies(i)
			self.tableSpecies.setItem(i, 0, QtGui.QTableWidgetItem('s['+str(i)+']'))
			self.tableSpecies.setItem(i, 1, QtGui.QTableWidgetItem(str(CurSpecies.getName())))
			self.tableSpecies.setItem(i, 2, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 3, QtGui.QTableWidgetItem(str(CurSpecies.initial_amount)))
			self.tableSpecies.setItem(i, 4, QtGui.QTableWidgetItem(str(CurSpecies.compartment)))
			self.tableSpecies.setItem(i, 5, QtGui.QTableWidgetItem(str(CurSpecies.boundary_condition)))
			self.tableSpecies.setItem(i, 6, QtGui.QTableWidgetItem(str(CurSpecies.getMetaId())))
		self.tableSpecies.resizeColumnsToContents()
		
		# Create a vector of Species names for later use
		ListOfSpecies = self.getTableData(self.tableSpecies, 1, 0, 1, 
								self.SBMLModel.getNumSpecies()).flatten()
		
		# Extract Parameter data from SBML Model
		# -- Quantity, Names, Value, VectorIndex
		self.tableParameters.setRowCount(self.SBMLModel.getNumParameters())
		for i in range(self.tableParameters.rowCount()):
			CurParameter = self.SBMLModel.getParameter(i)
			
			# Create vector index for parameter
			self.tableParameters.setItem(i, 0, QtGui.QTableWidgetItem('p['+str(i)+']'))
			
			# Port parameter name data from SBML model
			if not str(CurParameter.getName()):
				self.tableParameters.setItem(i, 1, 
					QtGui.QTableWidgetItem('default_prm'+str(i)))
			else:
				self.tableParameters.setItem(i, 1, 
					QtGui.QTableWidgetItem(str(CurParameter.getName())))
			
			# Get parameter value data from SBML model
			if not str(CurParameter.getValue()):
				self.tableParameters.setItem(i, 2, 
					QtGui.QTableWidgetItem('nan'))
			else:
				self.tableParameters.setItem(i, 2, 
					QtGui.QTableWidgetItem(str(CurParameter.getValue())))
			
			# Initialize parameter variable condtional
			self.tableParameters.setCellWidget(i, 3, QtGui.QCheckBox())
			
			# Get parameter metaid data from SBML model
			if not str(CurParameter.getMetaId()):
				self.tableParameters.setItem(i, 4, 
					QtGui.QTableWidgetItem('default_prmid'+str(i)))
			else:
				self.tableParameters.setItem(i, 4, 
					QtGui.QTableWidgetItem(str(CurParameter.getMetaId())))
					
			
			
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
			
			# Get current reaction from SBML model
			CurReaction = self.SBMLModel.getReaction(i)
			
			# Create reaction vector index
			self.tableReactions.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
			
			# Port name data from SBML model
			if not str(CurReaction.getName()):
				self.tableReactions.setItem(i, 1, 
					QtGui.QTableWidgetItem('default_rxn'+str(i)))
				self.tableReactions.item(i, 1).setBackground(QtGui.QColor(255,255,150))
			else:
				self.tableReactions.setItem(i, 1, 
					QtGui.QTableWidgetItem(str(CurReaction.getName())))
				
			# Get current reaction differential equation
			Formula = str(CurReaction.getKineticLaw().getFormula())
	
			# Replace compartment names with vector index in equation
			for j in reversed(range(self.tableCompartments.rowCount())):
				Formula = Formula.replace( str(self.tableCompartments.item(j,1).data(0).toString()), 
										   str(self.tableCompartments.item(j,0).data(0).toString()) )
		
			# Replace parameter names with vector index in equation
			for j in reversed(range(self.tableParameters.rowCount())):
				Formula = Formula.replace( str(self.tableParameters.item(j,1).data(0).toString()), 
										   str(self.tableParameters.item(j,0).data(0).toString()) )
				Formula = Formula.replace( str(self.tableParameters.item(j,4).data(0).toString()), 
										   str(self.tableParameters.item(j,0).data(0).toString()) )
										   
			# Replace species names with vector index in equation
			for j in reversed(range(self.tableSpecies.rowCount())):
				Formula = Formula.replace( str(self.tableSpecies.item(j,1).data(0).toString()), 
										   str(self.tableSpecies.item(j,0).data(0).toString()) )
				Formula = Formula.replace( str(self.tableSpecies.item(j,6).data(0).toString()), 
										   str(self.tableSpecies.item(j,0).data(0).toString()) )

			# Place differential equation into tableReactions
			self.tableReactions.setItem(i, 2, QtGui.QTableWidgetItem(Formula))
			
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
