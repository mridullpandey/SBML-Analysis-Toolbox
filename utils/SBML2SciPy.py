
           











def integrateODEFunction(SciPyModel):
    ''' 
        Integrate the derivative function from the provided
        SciPyModel deterministically between the specified 
        bounds. The resulting data is stored within the 
        SciPyModel structure for further analysis,
        visualization, and exporting to file.
        
        The function uses the SciPy.integrate method odeint
        to perform the integration. The method is robust
        for both stiff and non-stiff models (LSODA).

        To Do
        -----
        1. Possibly switch from odeint to ode in order to allow
           user choice in integrator.
        2. Check issues with deleting temp file.

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

    SciPyModel.SimulationData.Deterministic.TimeVector = tempTimeVector
    
    # Delete temporary file
#     try:
#         os.remove(TempName)
#     except OSError:
#         print 'ERROR: Temporary file has already been deleted.'
#     else:
#         print 'ERROR: Unknown error. Unable to remove '+TempName
    
    return SciPyModel


def createNullSpaceFunction( SciPyModel ):
    ''' 
        Generate the NullSpace of the kinetic parameters
        (parameters which enter the derivative matrix
        linearly). The nullspace in this case can be used
        to solve the system for the steady-state condition.
        
        This operation happens using the SymPy module to
        solve the homogenous equation A*x = 0.

        To Do
        -----
        1. Implement a method for manually setting 
           parameters to be considered kinetic parameters.
        2. Investigate method for sampling using restriction
           given by N*g = k > 0.

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
        The anonymous function can be called as follows:
        
        NullSpaceFunction( E, X )
        
        This produces a SymPy matrix of the nullspace 
        given the desired steady state condition as specified
        by the user choice in E and X.
        
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
    SciPyModel.Parameters.NullSpaceDimension = len( NullBasis )
    
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



def sampleLHSU(SciPyModel):
    ''' 
        Create a uniform Latin-Hypercube sample of the parameter 
        space as defined by the MinimumValue and MaximumValue
        vectors.

        To Do
        -----
        1. Add conditional check to inform user if required
           inputs are not specified in SciPyModel.

        Parameters
        ----------
        SciPyModel : internal object instance
            Requires that 
        
        Returns
        -------
        SciPyModel : internal object instance
            Places the generated parameter set into the field
            SciPyModel.SimulationData.Sensitivity.Global.ParameterSets
            
        See Also
        --------
        sampleNullSpace
        
        Notes
        -----
        Be advised the resulting parameterization will not
        remain at the desired steady state condition.
    '''

    import numpy

    # Uniform random sample array
    RanSet = numpy.random.uniform(0, 1, [
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity
    ])

    # Initialization of sample array
    SciPyModel.SimulationData.Sensitivity.Global.ParameterSets = numpy.zeros([
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity
    ])

    # For loop to divide sample space and ensure conditions are met
    for x_idx in range(SciPyModel.Parameters.Quantity):
        idx = numpy.random.permutation(
            SciPyModel.SimulationData.Sensitivity.Global.NumSamples) + 1
        P = (numpy.transpose(idx) - RanSet[:, x_idx]
             ) / SciPyModel.SimulationData.Sensitivity.Global.NumSamples
        SciPyModel.SimulationData.Sensitivity.Global.ParameterSets[:, x_idx] = (
            SciPyModel.Parameters.MinimumValue[x_idx] + P *
            (SciPyModel.Parameters.MaximumValue[x_idx] -
             SciPyModel.Parameters.MinimumValue[x_idx]))

    return SciPyModel


def sampleNullSpace( SciPyModel ):
    ''' 
        Create a sample of the parameter space as defined 
        by the MinimumValue and MaximumValue vectors.
        
        Samples are generated randomly in a one-at-a-time
        approach which does not guarantee good representation
        of the sample space.

        To Do
        -----
        1. Add conditional check to inform user if required
           inputs are not specified in SciPyModel.
           
        2. Implement a method to divide the shape parameter
           sample space for better representation of the sample
           space.

        Parameters
        ----------
        SciPyModel : internal object instance
            Requires that 
        
        Returns
        -------
        SciPyModel : internal object instance
            Places the generated parameter set into the field
            SciPyModel.SimulationData.Sensitivity.Global.ParameterSets
            
        See Also
        --------
        sampleLHSU
        
        Notes
        -----
        
    '''
        
    
    
    return SciPyModel