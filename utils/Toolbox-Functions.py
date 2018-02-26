# This is the collection of "finalized" functions to be imported into the Jupyter Notebook works.

def createSciPyModel():
    ''' Construct an empty SciPyModel object to pass
        into the other functions of the SBML-Sensitivity-
        Toolbox.
        
        The SciPyModel object structure is as follows:
        
        -Model
        |-MetaData
        |--FilePath
        |--Name
        |--VolumeUnits
        |--SubstanceUnits
        |--TimeUnits
        |-Species
        |--Quantity
        |--Names
        |--VectorizedIndex
        |--Value
        |--BoundaryCondition
        |-Parameters
        |--Kinetic
        |---Quantity
        |---Names
        |---VectorizedIndex
        |---Value
        |--Other
        |---Quantity
        |---Names
        |---VectorizedIndex
        |---Value
        |-Compartments
        |--Quantity
        |--Names
        |--VectorizedIndex
        |--Value
        |-Reactions
        |--Quantity
        |--Names
        |--Formulas
        |--Stoichiometry
        |-InternalFunctions
        |--DerivativeFunction
    '''
    
    class Model:
        def __init__(self):
            self.MetaData = MetaData()
            self.Species = Species()
            self.Parameters = Parameters()
            self.Compartments = Compartments()
            self.Reactions = Reactions()
            self.InternalFunctions = InternalFunctions()

    class MetaData:
        def __init__(self):
            self.FilePath = None
            self.Name = None
            self.VolumeUnits = None
            self.SubstanceUnits = None
            self.TimeUnits = None

    class Species:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []
            self.BoundaryCondition = []

    class Parameters:
        def __init__(self):
            self.Quantity = None
            self.Kinetic = Kinetic()
            self.Other = Other()

    class Kinetic:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []

    class Other:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []

    class Compartments:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.VectorIndex = []
            self.Value = []

    class Reactions:
        def __init__(self):
            self.Quantity = None
            self.Names = []
            self.Formulas = []
            self.Stoichiometry = []

    class InternalFunctions:
        def __init__(self):
            self.DerivativeFunction = None

    return Model()