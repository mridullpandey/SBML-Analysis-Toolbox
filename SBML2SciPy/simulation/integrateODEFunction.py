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