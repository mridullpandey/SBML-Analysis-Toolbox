def calculateLocalSensitivities( SciPyModel ):
    ''' 
        Caclulate local sensitivity coefficents for the
        model. Sensitivities are calulated by way of the
        centered difference approximation for the derivative
        dx/dp. The approximation is then normalized by the
        parameter value and species value for the base
        simulation at each given time point.

        To Do
        -----
        1. Enable parallelization of the loop to calculate
           sensitivities.
        2. Provide a way to pause the loop and continue
           execution from the last position.
           

        Parameters
        ----------
        SciPyModel : internal object instance
        
            SciPyModel object with basic model information
            specified as well as the PercentVary field
            specified.
        
        Returns
        -------
        SciPyModel : internal object instance
        
            SciPyModel object with local sensitivity coefficients
            along time vector and 
            
        See Also
        --------
        calculateGlobalSensitivities
        
        Notes
        -----
        The local sensitivity analysis information is limited
        in its ability to properly guide the modeler to
        full understanding of the model. This information
        is only valid within the neighborhood around
        the nominal parameterization specified in the model
        when this function is called.
    '''
    # Import required packages
    import os, sys, numpy
    NotebookDirectory = os.path.split(os.getcwd())[0]
    if NotebookDirectory not in sys.path:
        sys.path.append(NotebookDirectory)
    import toolbox
    
    # Integrate Base Simulation
    SciPyModel = toolbox.simulation.integrateODEFunction(SciPyModel)
    BaseSimulation = SciPyModel.SimulationData.Deterministic.Data[:, :]

    # Create Holder for Base Parameterization
    BaseParameters = SciPyModel.Parameters.Value[:]

    # Set Local Sensitivity Parameters
    SciPyModel.SimulationData.Sensitivity.Local.PercentVary = 0.10

    # Initialize Sensitivity Capture Array
    SciPyModel.SimulationData.Sensitivity.Local.Data = numpy.empty(
        (SciPyModel.Parameters.Quantity, SciPyModel.SimulationData.DataPoints,
         SciPyModel.Species.Quantity))

    for i in range(SciPyModel.Parameters.Quantity):
        # Reset Parameter Values
        SciPyModel.Parameters.Value = BaseParameters

        # High Parameter Simulation
        SciPyModel.Parameters.Value[i] = BaseParameters[i] * (
            1 + SciPyModel.SimulationData.Sensitivity.Local.PercentVary)
        SciPyModel = toolbox.simulation.integrateODEFunction(SciPyModel)
        HiSimulation = SciPyModel.SimulationData.Deterministic.Data[:, :]

        # Low Parameter Simulation
        SciPyModel.Parameters.Value[i] = BaseParameters[i] * (
            1 - SciPyModel.SimulationData.Sensitivity.Local.PercentVary)
        SciPyModel = toolbox.simulation.integrateODEFunction(SciPyModel)
        LoSimulation = SciPyModel.SimulationData.Deterministic.Data[:, :]

        # Calculate Sensitivities
        SciPyModel.SimulationData.Sensitivity.Local.Data[i, :, :] = (
            HiSimulation - LoSimulation) / (2 * BaseSimulation[
                i] * SciPyModel.SimulationData.Sensitivity.Local.PercentVary)
        
    return SciPyModel