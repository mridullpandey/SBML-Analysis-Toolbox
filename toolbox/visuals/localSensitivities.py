def localSensitivities( SciPyModel ):
    ''' 
        Plots the local sensitivity analysis data for
        the time course as well as at the last time.
        
        Useful for drawing conclusions from local sensitivity
        information on model interpretations and development.

        To Do
        -----
        1. Devise method for allowing user to select which
           plots to display. Method would be relevant for
           visualizing any samples from the null spac.
           
        2. Provide user utitlities to better control output
           plots.

        Parameters
        ----------
        SciPyModel : internal object instance
            
            The SciPyModel instance must contain data from
            running Local Sensitivity Analysis.
        
        Returns
        -------
        
            
        See Also
        --------
        
        
        Notes
        -----
        
    '''
    # Import required packages
    from matplotlib import pyplot as plt
    # Close previous figures
    plt.close()
    # Create new figure of required size
    plt.figure(figsize=(15, 5 * SciPyModel.Species.Quantity))
    # Pad the subplots with whitespace for clarity
    plt.subplots_adjust(hspace=1.0)
    # Loop over each species
    for ix in range(SciPyModel.Species.Quantity):
        # Select current left-column subplot
        plt.subplot(SciPyModel.Species.Quantity, 2, 2 * ix + 1)
        # Plot local sensitivities over time
        PlotHandles = plt.plot(
            SciPyModel.SimulationData.Deterministic.TimeVector,
            SciPyModel.SimulationData.Sensitivity.Local.Data[:, :, ix].transpose())
        # Title the plot
        plt.title(
            'Normalized Local Sensitivities for ' + SciPyModel.Species.Names[ix])
        # Lable the axis
        plt.xlabel('Time')
        plt.ylabel('Normalized Sensitivity')
        # Turn the grid on
        plt.grid()
        # Add legend to plot below the xaxis
        plt.legend(
            PlotHandles,
            SciPyModel.Parameters.Names,
            bbox_to_anchor=(0., -.225, 1., 0),
            ncol=3,
            mode="expand",
            borderaxespad=0.)
        # Select the right-column plot
        plt.subplot(SciPyModel.Species.Quantity, 2, 2 * ix + 2)
        # Plot the bargraph of sensitivities at ending time
        plt.bar(
            range(SciPyModel.Parameters.Quantity),
            SciPyModel.SimulationData.Sensitivity.Local.Data[:, -1, ix])
        # Change the xticks to parameter names
        plt.xticks(
            range(SciPyModel.Parameters.Quantity),
            SciPyModel.Parameters.Names,
            rotation=40)
        # Turn grid on for clarity
        plt.grid()
        # Title the plots for clarity
        plt.title('Normalized Local Sensitivities for ' +
                  SciPyModel.Species.Names[ix] + 'at Time ' +
                  str(SciPyModel.SimulationData.Deterministic.TimeVector[-1]))
        # Add ylabel
        plt.ylabel('Normalized Sensitivity')
    # Display the plots
    plt.show()