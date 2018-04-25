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