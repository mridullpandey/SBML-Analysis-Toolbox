def uniformLatinHypercubeSample(SciPyModel):
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