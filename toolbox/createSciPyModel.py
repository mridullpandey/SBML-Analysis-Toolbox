def createSciPyModel():
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
           
        4. Begin process of switching from custom class structure
           to Qt4 class structure for easier implementations.

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
            self.Parameters.Quantity = len(self.Parameters.Names)
            self.Parameters.Other.Quantity = len(self.Parameters.Other.Names)
            self.Compartments.Quantity = len(self.Compartments.Names)
            self.Reactions.Quantity = len(self.Reactions.Names)

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
            self.MinimumValue = []
            self.MaximumValue = []
            self.NullSpaceDimension = None

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
            self.Sensitivity = Sensitivity()

    class Deterministic:
        def __init__(self):
            self.Data = None
            self.TimeVector = None

    class Sensitivity:
        def __init__(self):
            self.Global = Global()
            self.Local = Local()

    class Global:
        def __init__(self):
            self.NumSamples = None
            self.Data = None
            self.ParameterSets = None

    class Local:
        def __init__(self):
            self.Data = None

    # Class to organize SciPyModel toolbox-specific function information
    class ToolboxFunctions:
        def __init__(self):
            self.DerivativeFunction = None
            self.NullSpace = None

    # Call Model class to return empty SciPyModel
    return Model()
