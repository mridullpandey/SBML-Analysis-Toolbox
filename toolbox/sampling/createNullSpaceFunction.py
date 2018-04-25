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