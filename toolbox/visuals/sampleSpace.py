def sampleSpace(SciPyModel):
    ''' 
        Plots the parameter samples on a series of 1-D
        numberlines.
        
        Useful for understanding the representation of the
        desired sample space in the currently drawn sample.

        To Do
        -----
        1. Devise method for allowing user to select which
           plots to display. Method would be relevant for
           visualizing any samples from the null spac.


        Parameters
        ----------
        SciPyModel : internal object instance
            
            The SciPyModel instance must contain a sample
            set within the ParameterSets field. 
        
        Returns
        -------
        
            
        See Also
        --------
        
        
        Notes
        -----
        
    '''

    # Import required packages
    from matplotlib import pyplot

    # Initialize subplots, create more as needed.
    pyplot.figure(figsize=(10, 3 * SciPyModel.Parameters.Quantity))

    # Loop over each parameter
    for i in range(SciPyModel.Parameters.Quantity):
        
        # Select current subplot
        pyplot.subplot(SciPyModel.Parameters.Quantity, 1, i + 1)

        # Create black horizontal line between parameter bounds
        pyplot.hlines(1, SciPyModel.Parameters.MinimumValue[i],
                      SciPyModel.Parameters.MaximumValue[i])

        # Plot vertical lines at every set value of current parameter
        pyplot.eventplot(
            SciPyModel.SimulationData.Sensitivity.Global.ParameterSets[:, i],
            orientation='horizontal',
            colors='b')
        
        # Remove background axis for clarity
        pyplot.axis('off')
        
        # Title plot using current parameter name
        pyplot.title(SciPyModel.Parameters.Names[i])

    # Display plot to user
    pyplot.show()
