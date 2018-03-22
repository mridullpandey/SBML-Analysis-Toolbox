def importSBMLFile( SciPyModel, Provided_FilePath=None ):
    ''' Reads an SBML model from a given file and unpacks the
        SBML model into the provided SciPyModel object structure.  
    
        Parameters
        ----------
        SciPyModel : object instance
            Description needed.
        Provided_FilePath : string, optional
            Description needed.
        
        Returns
        -------
        SciPyModel : object instance
            Initial SciPyModel object with relevant edits in
            structure as dictated by the SBML model file.
            
        See Also
        --------
        createSciPyModel
        
        Notes
        -----
        If no file path is provided or if the provided file
        encounters error, then the function returns an unmodified
        SciPyModel object.
    '''
    
    # Specify imports required by the function.
    import libsbml, numpy, Tkinter, tkFileDialog
    
    # Conditional check for provided filepath, if None then open
    # Tkinter dialogue box.
    if Provided_FilePath == None:
        Tkinter.Tk().withdraw()
        SciPyModel.MetaData.FilePath = tkFileDialog.askopenfilename()
    elif type(Provided_FilePath) == str:
        SciPyModel.MetaData.FilePath = Provided_FilePath[0]
    else:
        print 'ERROR: Unable to parse provided filepath.'
        return SciPyModel
    
    # Read in SBML model file into SBML Document variable
    SBMLDoc = libsbml.readSBMLFromFile( SciPyModel.MetaData.FilePath )

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
    SBMLModel = SBMLDoc.getModel()
    
    # Extract MetaData data from SBML model
    # -- Name, VolumeUnits, SubstanceUnits, TimeUnits
    SciPyModel.MetaData.Name = SBMLModel.getName()
    SciPyModel.MetaData.VolumeUnits = SBMLModel.getVolumeUnits()
    SciPyModel.MetaData.SubstanceUnits = SBMLModel.getSubstanceUnits()
    SciPyModel.MetaData.TimeUnits = SBMLModel.getTimeUnits()
    
    # Extract Compartment data from SBML model
    # -- Quantity, Names, VectorIndex
    SciPyModel.Compartments.Quantity = SBMLModel.getNumCompartments()
    for i in range(SBMLModel.getNumCompartments()):
        current_compartment = SBMLModel.getCompartment(i)
        SciPyModel.Compartments.Names.append(current_compartment.name)
        SciPyModel.Compartments.VectorIndex.append(i)

    # Extract Species data from SBML Model
    # -- Quanity, Names, Value, VectorIndex, BoundaryValue
    SciPyModel.Species.Quantity = SBMLModel.getNumSpecies()
    for i in range(SBMLModel.getNumSpecies()):
        current_species = SBMLModel.getSpecies(i)
        SciPyModel.Species.Names.append(current_species.name)
        SciPyModel.Species.Value.append(current_species.initial_amount)
        SciPyModel.Species.VectorIndex.append(i)
        SciPyModel.Species.BoundaryValue.append(
            current_species.boundary_condition)

    # Extract Parameter data from SBML Model
    # -- Quantity, Names, Value, VectorIndex
    SciPyModel.Parameters.Kinetic.Quantity = SBMLModel.getNumParameters()
    for i in range(SBMLModel.getNumParameters()):
        current_parameter = SBMLModel.getParameter(i)
        SciPyModel.Parameters.Kinetic.Names.append(current_parameter.name)
        SciPyModel.Parameters.Kinetic.Value.append(current_parameter.value)
        SciPyModel.Parameters.Kinetic.VectorIndex.append(i)

    # Extract Reaction data from SBML Model
    # -- Names, Formulas, Stoichiometry
    SciPyModel.Reactions.Stoichiometry = numpy.zeros( [SBMLModel.getNumSpecies(),
                                                       SBMLModel.getNumReactions() ] )
    SciPyModel.Reactions.Quantity = SBMLModel.getNumReactions()
    for i in range(SBMLModel.getNumReactions()):
        current_reaction = SBMLModel.getReaction(i)
        SciPyModel.Reactions.Names.append(current_reaction.name)
        SciPyModel.Reactions.Formulas.append(
            current_reaction.getKineticLaw().getFormula())

        for r in current_reaction.getListOfReactants():
            SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                r.getSpecies()), i] -= r.getStoichiometry()

        for p in current_reaction.getListOfProducts():
            SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                p.getSpecies()), i] += p.getStoichiometry()

    return SciPyModel

def createSciPyModel( ):
    ''' Construct an empty SciPyModel object to pass into 
        the other functions of the SBML-Sensitivity-Toolbox.

        To-Do
        -----
        1. Allow users to pass in arguments to variables within
           the SciPyModel structure.
           
        2. Implement an "UpdateModel" method into the SciPyModel
           object itself. Will ensure errors due to mismatching 
           are mitigated.
           
        3. Implement a "ValidateModel" method into the SciPyModel
           object itself. Will help users to mitigate import 
           errors.

        Parameters
        ----------
        None
        
        Returns
        -------
        SciPyModel : internal object instance
            Empty SciPyModel object.
            
        See Also
        --------
        
        Notes
        -----
        The SciPyModel object structure is as follows:

        -Model
        |-MetaData
        |--FilePath, Name, VolumeUnits, SubstanceUnits 
        |--TimeUnits
        |-Species
        |--Quantity, Names, VectorIndex, Value
        |--BoundaryCondition
        |-Parameters
        |--Kinetic
        |---Quantity, Names, VectorIndex, Value
        |--Other
        |---Quantity, Names, VectorIndex, Value
        |-Compartments
        |--Quantity, Names, VectorIndex, Value
        |-Reactions
        |--Quantity, Names, Formulas
        |--Stoichiometry
        |-SimulationData
        |--TimeStart
        |--TimeEnd
        |--DataPoints
        |--Deterministic
        |-ToolboxFunctions
        |--DerivativeFunction
    '''
    
    # Class to create SciPyModel object
    class Model:
        def __init__(self):
            self.MetaData = MetaData()
            self.Species = Species()
            self.Parameters = Parameters()
            self.Compartments = Compartments()
            self.Reactions = Reactions()
            self.SimulationData = SimulationData()
            self.ToolboxFunctions = ToolboxFunctions()
    
    # Class to organize SciPyModel metadata information
    class MetaData:
        def __init__(self):
            self.FilePath = None
            self.Name = None
            self.VolumeUnits = None
            self.SubstanceUnits = None
            self.TimeUnits = None

        def UpdateModel(self):
            self.Species.Quantity = len(self.Species.Names)
            self.Parameters.Kinetic.Quantity = len(
                             self.Parameters.Kinetic.Names)
            self.Parameters.Other.Quantity = len(
                               self.Parameters.Other.Names)
            self.Compartments.Quantity = len(
                                   self.Compartments.Names)
            self.Reactions.Quantity = len(
                                      self.Reactions.Names)
            
    # Class to organize SciPyModel species information
    class Species:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            self.BoundaryValue = []

    # Class to organize SciPyModel parameter information
    class Parameters:
        def __init__(self):
            self.Kinetic = Kinetic()
            self.Other = Other()

    # Class to organize SciPyModel kinetic parameter information
    class Kinetic:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            
    # Class to organize SciPyModel non-kinetic parameter information
    class Other:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            
    # Class to organize SciPyModel compartment information
    class Compartments:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []

    # Class to organize SciPyModel reaction information
    class Reactions:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.Formulas = []
            self.Stoichiometry = []
    
    # Class to organize SciPyModel simulation data
    class SimulationData:
        def __init__(self):
            self.TimeStart = None
            self.TimeEnd = None
            self.DataPoints = None
            self.Deterministic = Deterministic()
    
    class Deterministic:
        def __init__(self):
            self.Data = None
    
    # Class to organize SciPyModel toolbox-specific function information
    class ToolboxFunctions:
        def __init__(self):
            self.DerivativeFunction = None
    
    # Call Model class to return empty SciPyModel
    return Model()



def writeODEFunction( SciPyModel ):
    ''' Create a derivative function from the provided 
        SciPyModel as a basis for other internal packaged
        methods. The derivative function is stored as a 
        bytearray and written to a file when needed to be
        called by each internal method.

        To Do
        -----
        1. Implement a method to check if SciPyModel 
           structure is of proper form, i.e. there are
           sufficent state variables and parameters as
           needed by highest vector indecies in rxns.

        Parameters
        ----------
        SciPyModel : internal object instance
        
        Returns
        -------
        SciPyModel : internal object instance
            SciPyModel object with derivative function as
            specified by reaction declarations.
            
        See Also
        --------
        
        
        Notes
        -----
        
    '''
    
    # Write header information for the derivative function file.
    generated_code = bytearray('')
    generated_code.extend('from __future__ import division \n')
    generated_code.extend('import numpy \n')
    generated_code.extend('\n')
    generated_code.extend('def ode_fun( y, t, p ): \n')
    generated_code.extend('\n')
    generated_code.extend(
        '    rxn = numpy.zeros([' + str(SciPyModel.Reactions.Quantity) + ']) \n')
    
    # Loop over each reaction within the SciPyModel object.
    for rxn_ix in range(SciPyModel.Reactions.Quantity):

        # Get information about the current reaction
        Formula = SciPyModel.Reactions.Formulas[rxn_ix]

        # Removes usage of compartments from reaction equations.
        for j in reversed(range(SciPyModel.Compartments.Quantity)):
            Formula = Formula.replace(SciPyModel.Compartments.Names[j] + ' * ',
                                      '')
            Formula = Formula.replace(' * ' + SciPyModel.Compartments.Names[j],
                                      '')
            Formula = Formula.replace(' / ' + SciPyModel.Compartments.Names[j],
                                      '')

        # Replace parameter names with index of vectorized parameter array.
        # Iterates through parameter names sorted by length of name.
        for key in sorted(
                SciPyModel.Parameters.Kinetic.Names, key=len, reverse=True):
            Formula = Formula.replace(
                key,
                'p[' + str(SciPyModel.Parameters.Kinetic.Names.index(key)) + ']')

        # Replace species names with index of species parameter array.
        for key in sorted(SciPyModel.Species.Names, key=len, reverse=True):
            Formula = Formula.replace(
                key, 'y[' + str(SciPyModel.Species.Names.index(key)) + ']')

        # Reset formula declaration in SciPyModel class
        SciPyModel.Reactions.Formulas[rxn_ix] = Formula

        # Append each formula declaration to the growing output bytearray.
        generated_code.extend(
            '    # ' + SciPyModel.Reactions.Names[rxn_ix] + '\n')
        generated_code.extend('    rxn[' + str(rxn_ix) + '] = ' + Formula + '\n')
    
    # Write out footer information for the derivative function file
    generated_code.extend('\n')
    generated_code.extend('    S = numpy.' + repr(SciPyModel.Reactions.Stoichiometry) 
                          + '\n')
    generated_code.extend('    \n')
    generated_code.extend('    dy = S.dot(rxn) \n')
    generated_code.extend('    return dy \n')
    
    # Place generated bytearray code into the derivative function
    SciPyModel.ToolboxFunctions.DerivativeFunction = generated_code
    
    return SciPyModel





def integrateODEFunction(SciPyModel):
    ''' Integrate the derivative function from the provided
        SciPyModel deterministically between the specified 
        bounds. The resulting data is stored within the 
        SciPyModel structure for further analysis,
        visualization, and exporting to file.
        
        The function uses the SciPy.integrate method odeint
        to perform the integration. The method is robust
        for both stiff and non-stiff models.

        To Do
        -----
        

        Parameters
        ----------
        SciPyModel : internal object instance
        
        Returns
        -------
        SciPyModel : internal object instance
            SciPyModel object with deterministic integration
            between time bounds performed.
            
        See Also
        --------
        scipy.integrate.odeint
        
        Notes
        -----
        
    '''
    # Import NumPy, SciPy.integrate, pand packages.
    from scipy import integrate
    import numpy, pandas, os

    # Write derivative function to file.
    open('temp.py', 'w+').write(SciPyModel.ToolboxFunctions.DerivativeFunction)

    # Import derivative function from temporary file.
    from temp import ode_fun

    # Check if time vector data is specified
    try:
        # Create time vector.
        tempTimeVector = numpy.linspace(
            SciPyModel.SimulationData.TimeStart,
            SciPyModel.SimulationData.TimeEnd,
            SciPyModel.SimulationData.DataPoints)
    except TypeError:
        print "ERROR: Check time data values in SciPyModel object."
        return

    # Integrate using odeint method. Store as a Pandas dataframe within SciPyModel object.
    SciPyModel.SimulationData.Deterministic.Data = integrate.odeint(
                ode_fun, SciPyModel.Species.Value, tempTimeVector, 
                args=(SciPyModel.Parameters.Kinetic.Value,) 
                )

    # Delete temporary file
    os.remove('temp.py')
    
    return SciPyModel
