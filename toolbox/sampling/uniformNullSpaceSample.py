def uniformNullSpaceSample(SciPyModel):
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
    # Import required packages
    import numpy

    # Initialize ParameterSets array
    SciPyModel.SimulationData.Sensitivity.Global.ParameterSets = numpy.zeros([
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity
    ])

    # Get minimum bound of Michaelis constants
    MinimumEBound = SciPyModel.Parameters.MinimumValue[[
        not KineticFlag for KineticFlag in SciPyModel.Parameters.KineticFlag
    ]]
    # Check if any bounds are zero. If so, make them a small number instead.
    MinimumEBound[(
        MinimumEBound == 0.)] = numpy.ones(sum((MinimumEBound == 0.))) * 1e-6

    # Create the nullspace matrix at the minimum bound.
    MinimumNullSpace = SciPyModel.ToolboxFunctions.NullSpaceFunction(
        MinimumEBound, SciPyModel.Species.Value)

    # Using minimum bound of kinetic rate constants solve Ng=k
    MinimumGBound = numpy.linalg.lstsq(
        MinimumNullSpace, SciPyModel.Parameters.MinimumValue[
            SciPyModel.Parameters.KineticFlag])[0]

    # Get maximum bound of Michaelis constants
    MaximumEBound = SciPyModel.Parameters.MaximumValue[[
        not KineticFlag for KineticFlag in SciPyModel.Parameters.KineticFlag
    ]]
    # Check if any bounds are zero. If so, make them a small number instead.
    MaximumEBound[(
        MaximumEBound == 0.)] = numpy.ones(sum((MaximumEBound == 0.))) * 1e-6

    # Create the nullspace matrix at the maximum bound.
    MaximumNullSpace = SciPyModel.ToolboxFunctions.NullSpaceFunction(
        MaximumEBound, SciPyModel.Species.Value)

    # Using maximum bound of kinetic rate constants solve Ng=k
    MaximumGBound = numpy.linalg.lstsq(
        MaximumNullSpace, SciPyModel.Parameters.MaximumValue[
            SciPyModel.Parameters.KineticFlag])[0]

    # Initialize sample space boundary
    MinimumBound = numpy.concatenate([MinimumGBound, MinimumEBound])
    MaximumBound = numpy.concatenate([MaximumGBound, MaximumEBound])

    # Uniform random sample array
    RanSet = numpy.random.uniform(0, 1, [
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity - sum(SciPyModel.Parameters.KineticFlag)
        + SciPyModel.Parameters.NullSpaceDimension
    ])

    # Initialization of sample array
    PreParameterSets = numpy.zeros([
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity - sum(SciPyModel.Parameters.KineticFlag)
        + SciPyModel.Parameters.NullSpaceDimension
    ])

    # For loop to divide sample space and ensure conditions are met
    for x_idx in range(SciPyModel.Parameters.Quantity -
                       sum(SciPyModel.Parameters.KineticFlag) +
                       SciPyModel.Parameters.NullSpaceDimension):
        idx = numpy.random.permutation(
            SciPyModel.SimulationData.Sensitivity.Global.NumSamples) + 1
        P = (numpy.transpose(idx) - RanSet[:, x_idx]
             ) / SciPyModel.SimulationData.Sensitivity.Global.NumSamples
        PreParameterSets[:, x_idx] = (
            MinimumBound[x_idx] + P *
            (MaximumBound[x_idx] - MinimumBound[x_idx]))

    # Initialize colelction array
    SciPyModel.SimulationData.Sensitivity.Global.ParameterSets = (numpy.empty([
        SciPyModel.SimulationData.Sensitivity.Global.NumSamples,
        SciPyModel.Parameters.Quantity
    ]))

    # Loop over each sample
    for i in range(SciPyModel.SimulationData.Sensitivity.Global.NumSamples):

        # Calculate kinetic rate constants based on current sample
        KSample = SciPyModel.ToolboxFunctions.NullSpaceFunction(
            list(PreParameterSets[i,
                                  SciPyModel.Parameters.NullSpaceDimension:]),
            list(SciPyModel.Species.Value)).dot(
                list(PreParameterSets[
                    i, :SciPyModel.Parameters.NullSpaceDimension]))

        # Check if kinetic rate constant
        if ((KSample < SciPyModel.Parameters.
             MinimumValue[SciPyModel.Parameters.KineticFlag]).any()
                or (KSample > SciPyModel.Parameters.
                    MaximumValue[SciPyModel.Parameters.KineticFlag]).any()):
            pass

        SciPyModel.SimulationData.Sensitivity.Global.ParameterSets[i, :] = (
            numpy.concatenate([
                KSample.tolist()[0], PreParameterSets[
                    i, SciPyModel.Parameters.NullSpaceDimension:].tolist()
            ]))
    return SciPyModel
