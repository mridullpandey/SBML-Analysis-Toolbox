def importSBMLFile( SciPyModel ):
    ''' Reads an SBML model from a given file and unpacks the
        SBML model into the provided SciPyModel object structure.
        User may specify SBML model file path within SciPyModel
        manually.
        
        To-Do
        -----
        Difficulty importing Copasi exported SBML models due to
        difference in name/meta_id fields. Specific issue with
        SBML models imported/exported through Copasi.
    
        Parameters
        ----------
        SciPyModel : object instance
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

    # Import required modules
    import libsbml, numpy, Tkinter, tkFileDialog
    
    # Conditional to check if FilePath was specified
    if SciPyModel.MetaData.FilePath == None:
        Tkinter.Tk().withdraw()
        SciPyModel.MetaData.FilePath = tkFileDialog.askopenfilename()
    else:
        pass
    
    # Read in SBML model file into SBML Document variable
    SBMLDoc = libsbml.readSBMLFromFile(SciPyModel.MetaData.FilePath)
    
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
    
    # Extract MetaData
    # -- Name, VolumeUnits, SubstanceUnits, TimeUnits
    SciPyModel.MetaData.Name = SBMLModel.getName()
    SciPyModel.MetaData.VolumeUnits = SBMLModel.getVolumeUnits()
    SciPyModel.MetaData.SubstanceUnits = SBMLModel.getSubstanceUnits()
    SciPyModel.MetaData.TimeUnits = SBMLModel.getTimeUnits()
    
    # Extract Compartment Data
    # -- Quantity, Names, VectorIndex
    SciPyModel.Compartments.Quantity = SBMLModel.getNumCompartments()
    for i in range(SBMLModel.getNumCompartments()):
        current_compartment = SBMLModel.getCompartment(i)
        SciPyModel.Compartments.Names.append(current_compartment.name)
        SciPyModel.Compartments.VectorIndex.append(i)
        SciPyModel.Compartments.MetaID.append(current_compartment.meta_id)
    
    # Extract Species Data
    # -- Quanity, Names, Value, VectorIndex, BoundaryValue
    SciPyModel.Species.Quantity = SBMLModel.getNumSpecies()
    for i in range(SBMLModel.getNumSpecies()):
        current_species = SBMLModel.getSpecies(i)
        SciPyModel.Species.Names.append(current_species.name)
        SciPyModel.Species.Value.append(current_species.initial_amount)
        SciPyModel.Species.VectorIndex.append(i)
        SciPyModel.Species.BoundaryValue.append(current_species.boundary_condition)
        SciPyModel.Species.MetaID.append(current_species.meta_id)
    
    # Extract Parameter Data
    # -- Quantity, Names, Value, VectorIndex, MetaID, KineticFlag
    SciPyModel.Parameters.Quantity = SBMLModel.getNumParameters()
    for i in range(SBMLModel.getNumParameters()):
        current_parameter = SBMLModel.getParameter(i)
        SciPyModel.Parameters.Names.append(current_parameter.name)
        SciPyModel.Parameters.Value.append(current_parameter.value)
        SciPyModel.Parameters.VectorIndex.append(i)
        SciPyModel.Parameters.MetaID.append(current_parameter.meta_id)
    [
    SciPyModel.Parameters.KineticFlag.append(False)
    for i in range(SciPyModel.Parameters.Quantity)
    ]
    
    # Extract Reaction Data
    # -- Names, Formulas, Stoichiometry
    SciPyModel.Reactions.Stoichiometry = numpy.zeros(
        [SBMLModel.getNumSpecies(),
         SBMLModel.getNumReactions()])
    SciPyModel.Reactions.Quantity = SBMLModel.getNumReactions()
    for i in range(SBMLModel.getNumReactions()):
        current_reaction = SBMLModel.getReaction(i)
        SciPyModel.Reactions.Names.append(current_reaction.name)
        SciPyModel.Reactions.Formulas.append(
            current_reaction.getKineticLaw().getFormula())

        # Try-Except in order to see if Names or MetaID are used in the functions
        try:
            for r in current_reaction.getListOfReactants():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                    r.getSpecies()), i] -= r.getStoichiometry()
            for p in current_reaction.getListOfProducts():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                    p.getSpecies()), i] += p.getStoichiometry()
        except ValueError:
            for r in current_reaction.getListOfReactants():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.MetaID.index(
                    r.getSpecies()), i] -= r.getStoichiometry()
            for p in current_reaction.getListOfProducts():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.MetaID.index(
                    p.getSpecies()), i] += p.getStoichiometry()
        else:
            print 'ERROR: Unable to create Stoichiometric Matrix. Check species name/metaid.'

        # Remove Stoichiometry of Boundary State Variables
        for s in range(SciPyModel.Species.Quantity):
            if SciPyModel.Species.BoundaryValue[s]:
                SciPyModel.Reactions.Stoichiometry[s, :] = numpy.zeros(
                    (1, SciPyModel.Reactions.Quantity))

    # Vectorize Functions within SciPyModel object.
    for rxn_ix in range(SciPyModel.Reactions.Quantity):

        # Get information about the current reaction
        Formula = SciPyModel.Reactions.Formulas[rxn_ix]

        # Removes usage of compartments from reaction equations.
        for j in reversed(range(SciPyModel.Compartments.Quantity)):
            if SciPyModel.Compartments.Names[j] != '':  # If name isn't empty
                Formula = Formula.replace(SciPyModel.Compartments.Names[j] + ' * ',
                                          '')
                Formula = Formula.replace(' * ' + SciPyModel.Compartments.Names[j],
                                          '')
                Formula = Formula.replace(' / ' + SciPyModel.Compartments.Names[j],
                                          '')

        # Replace parameter names with index of vectorized parameter array.
        # Iterates through parameter names sorted by length of name.
        for key in sorted(
                SciPyModel.Parameters.Names, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(key, 'p[' + str(
                    SciPyModel.Parameters.Names.index(key)) + ']')

        for key in sorted(
                SciPyModel.Parameters.MetaID, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(key, 'p[' + str(
                    SciPyModel.Parameters.MetaID.index(key)) + ']')

        # Replace species names with index of species parameter array.
        for key in sorted(SciPyModel.Species.Names, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(
                    key, 'y[' + str(SciPyModel.Species.Names.index(key)) + ']')

        for key in sorted(SciPyModel.Species.MetaID, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(
                    key, 'y[' + str(SciPyModel.Species.MetaID.index(key)) + ']')

        # Reset formula declaration in SciPyModel class
        SciPyModel.Reactions.Formulas[rxn_ix] = Formula
    
    # Grab indecies of kinetic rate constant parameters
    ReactionIndex = []
    for rxn_ix in range(SciPyModel.Reactions.Quantity):
        ReactionIndex.append(
            int(SciPyModel.Reactions.Formulas[rxn_ix].split(']')[0].split('[')[
                -1]))

    # Order the parameters and track the internal index ordering
    SortedIndex = [
        i[0] for i in sorted(enumerate(ReactionIndex), key=lambda x: x[1])
    ]

    # Apply the index ordering to order the formula vector
    SciPyModel.Reactions.Formulas = [
        SciPyModel.Reactions.Formulas[i] for i in SortedIndex
    ]

    # Apply the index ordering to order the stoichiometry matrix
    SciPyModel.Reactions.Stoichiometry = numpy.vstack([
        SciPyModel.Reactions.Stoichiometry[:, i] for i in SortedIndex
    ]).transpose()
    
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
        |--BoundaryCondition, MetaID
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
            self.Parameters.Quantity = len(
                             self.Parameters.Names)
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
            self.MetaID = []

    # Class to organize SciPyModel parameter information
    class Parameters:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            self.MetaID = []
            self.KineticFlag = []

    # Class to organize SciPyModel compartment information
    class Compartments:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            self.MetaID = []

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
            self.NullSpace = None
    
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
    # Enable printing of full sized numpy arrays/matrix
    import numpy
    numpy.set_printoptions(threshold=numpy.nan)
    
    # Write header information for the derivative function file.
    generated_code = bytearray('')
    generated_code.extend('from __future__ import division \n')
    generated_code.extend('import numpy, sympy \n')
    generated_code.extend('\n')
    generated_code.extend('def ode_fun( y, t, p ): \n')
    generated_code.extend('\n')
    generated_code.extend(
        '    rxn = numpy.zeros([' + str(SciPyModel.Reactions.Quantity) + ']) \n')
    
    # Loop over each reaction within the SciPyModel object.
    for rxn_ix in range(SciPyModel.Reactions.Quantity):

        # Get information about the current reaction
        Formula = SciPyModel.Reactions.Formulas[rxn_ix]
        
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
    
    
    # Write function definition for reactions -- edit this to isolate shape/kinetic parameters
    generated_code.extend('\n')
    generated_code.extend('\n')
    generated_code.extend('def rxn_fun( y, t, p ): \n')
    generated_code.extend('\n')
    generated_code.extend(
        '    rxn = sympy.zeros(' + str(SciPyModel.Reactions.Quantity) + ',1) \n')
    for rxn_ix in range(SciPyModel.Reactions.Quantity):
        Formula = SciPyModel.Reactions.Formulas[rxn_ix]
        generated_code.extend(
            '    # ' + SciPyModel.Reactions.Names[rxn_ix] + '\n')
        generated_code.extend('    rxn[' + str(rxn_ix) + '] = ' + Formula + '\n')
    generated_code.extend('    return rxn \n')
    
    
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
    from scipy.integrate import odeint
    import numpy, os, datetime

    # Write derivative function to file.
    TempName = (SciPyModel.MetaData.Name
                +datetime.datetime.now().strftime("%I%M%p%B%d%Y")
                +'.py')
    open(TempName, 'w+').write(SciPyModel.ToolboxFunctions.DerivativeFunction)
    
    # Import derivative function from temporary file.
    TempModule = __import__(TempName[:-3])

    # Check if time vector data is specified -   
    try:
        # Create time vector.
        tempTimeVector = numpy.linspace(
            SciPyModel.SimulationData.TimeStart,
            SciPyModel.SimulationData.TimeEnd,
            SciPyModel.SimulationData.DataPoints)
    except TypeError:
        print "ERROR: Check time data values in SciPyModel object."
        return

    # Integrate using odeint method.
    SciPyModel.SimulationData.Deterministic.Data = (odeint(
        TempModule.ode_fun, SciPyModel.Species.Value,
        tempTimeVector, args=(SciPyModel.Parameters.Value, )))

    # Delete temporary file
    try:
        os.remove(TempName)
    except OSError:
        print 'ERROR: Temporary file has already been deleted.'
    else:
        print 'ERROR: Unknown error. Unable to remove '+TempName
    
    return SciPyModel


def createNullSpaceFunction( SciPyModel ):
    ''' Generate the NullSpace of the kinetic parameters
        (parameters which enter the derivative matrix
        linearly). The nullspace in this case can be used
        to solve the system for the steady-state condition.
        
        This operation happens using the SymPy module to
        solve the homogenous equation A*x = 0.

        To Do
        -----
        1. Implement a method for manually setting 
        parameters to be considered kinetic parameters.

        Parameters
        ----------
        SciPyModel : internal object instance
        
        Returns
        -------
        SciPyModel : internal object instance
            SciPyModel with NullSpaceFunction based on
            model parameterization.
            
        See Also
        --------
        
        Notes
        -----
        
    '''

    import sympy, datetime, numpy
    
    # Automatically flag kinetic parameters.
    for rxn in SciPyModel.Reactions.Formulas:
        if SciPyModel.Reactions.Formulas[0][0] == 'p':
            SciPyModel.Parameters.KineticFlag[int(
                rxn.split(']')[0].split('[')[1])] = True
    
    # Write derivative function to file
    TempName = (SciPyModel.MetaData.Name
                +datetime.datetime.now().strftime("%I%M%p%B%d%Y")
                +'.py')
    open(TempName, 'w+').write(SciPyModel.ToolboxFunctions.DerivativeFunction)
    
    # Import derivative function from temporary file.
    TempModule = __import__(TempName[:-3])

    # Create symbolic species and parameter vectors
    y = sympy.symarray('y', len(SciPyModel.Species.Names))
    p = sympy.symarray('p', len(SciPyModel.Parameters.Names))

    # Create symbolic reaction and stoichiometry matrices
    R = sympy.Matrix(TempModule.rxn_fun(y,0,p))
    S = sympy.Matrix(SciPyModel.Reactions.Stoichiometry)
    
    # Create symbolic derivative matrix
    DerivativeMatrix = sympy.Matrix(
    [S[:, i] * R[i] for i in range(len(R))]).reshape(S.shape[1],
                                                     S.shape[0]).transpose()
    
    # Extract kinetic parameters
    M = sympy.Matrix(
    sympy.lambdify((p[SciPyModel.Parameters.KineticFlag]), DerivativeMatrix,
                   'sympy')(*sympy.ones(
                       len(p[SciPyModel.Parameters.KineticFlag]), 1)))
    
    # Obtain basis for nullspace
    NullBasis = M.nullspace()
    
    # Assemble nullspace matrix from basis
    NullSpace = sympy.Matrix([NullBasis[i] for i in range(len(NullBasis))])
    NullSpace = NullSpace.reshape(len(NullBasis),
                                  len(NullSpace) / len(NullBasis)).transpose()
    
    # Create anonymous sampling function
    SciPyModel.ToolboxFunctions.NullSpaceFunction = sympy.lambdify(
        (p[numpy.invert(SciPyModel.Parameters.KineticFlag)],y),
        NullSpace,
        'numpy',
        dummify=False)
    
    return SciPyModel