def simplePlot(SciPyModel):
    ''' 
        Creates a single plot of all the species in the model.
        
        Useful for preliminary visualization and prototyping
        of model structure.

        To Do
        -----
        1. Devise method for allowing user to select which
           species to display. Method would be useful for
           the GUI implementation.

        Parameters
        ----------
        SciPyModel : internal object instance
            
            The SciPyModel instance must contain data from 
            a deterministic integration.
        
        Returns
        -------
        
            
        See Also
        --------
        
        
        Notes
        -----
        
    '''
    # Import required packages
    from matplotlib import pyplot

    # Close previously opened figures
    pyplot.close()

    # Plot all state variables
    PlotHandles = pyplot.plot(SciPyModel.SimulationData.Deterministic.TimeVector,
                              SciPyModel.SimulationData.Deterministic.Data)

    # Title plot with model name
    pyplot.title(SciPyModel.MetaData.FilePath.split('/')[-1].split('.')[0])

    # Add grid to the plot
    pyplot.grid()

    # Add legend to plot
    pyplot.legend(
        PlotHandles,
        SciPyModel.Species.Names,
        bbox_to_anchor=(0., -.1, 1., 0),
        ncol=3,
        mode="expand",
        borderaxespad=0.)

    # Display the plot to user
    pyplot.show()