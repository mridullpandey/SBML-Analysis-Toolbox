def uniformNullSpaceSample( SciPyModel ):
    ''' 
        Create a sample of the parameter space as defined 
        by the MinimumValue and MaximumValue vectors.
        
        Samples are generated using 

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
        sampleLHSU
        
        Notes
        -----
        
    '''
        
    
    
    return SciPyModel