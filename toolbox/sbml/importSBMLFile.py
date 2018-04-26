def importSBMLFile( SciPyModel ):
    ''' 
        Reads an SBML model file and unpacks the
        SBML model into the provided SciPyModel object structure.
        User may specify SBML model file path within SciPyModel
        manually.
        
        To-Do
        -----
        1. Difficulty importing Copasi exported SBML models due to
           difference in name/meta_id fields. Specific issue with
           SBML models imported/exported through Copasi.
           
        2. Write code to inform user of required fields to be
           filled out. Should be in the form of:
           
           SciPyModel.errorLog()
           
           Which prints a list of potential issues in the model
           for the user to update.
           
        3. Implement conditional to reset SciPyModel to initial
           form if user passes in filled model.
    
        Parameters
        ----------
        SciPyModel : object instance
            
            Can be called on any SciPyModel object.
        
        Returns
        -------
        SciPyModel : object instance
            Initial SciPyModel object with relevant edits in
            structure as dictated by the SBML model file.
            
        See Also
        --------
        createSciPyModel
        
        Notes
        -----
        If no file path is provided or if the provided file
        encounters error, then the function returns an unmodified
        SciPyModel object.
    '''

    # Import required modules
    import libsbml, numpy, Tkinter, tkFileDialog
    
    # Conditional to check if FilePath was specified
    if SciPyModel.MetaData.FilePath == None:
        Tkinter.Tk().withdraw()
        SciPyModel.MetaData.FilePath = tkFileDialog.askopenfilename()
    else:
        pass
    
    # Read in SBML model file into SBML Document variable
    SBMLDoc = libsbml.readSBMLFromFile(SciPyModel.MetaData.FilePath)
    
    # Check if any major errors in reading SBML model
    # e.g. Filepath does not exist
    if SBMLDoc.getNumErrors() > 0:
        print('ERROR: File reading errors.')
        print(SBMLDoc.getErrorLog().toString())
    
    # Make all parameters of the model global parameters.
    # Enables all parameters to be vectorized.
    Properties = libsbml.ConversionProperties()
    Properties.addOption('promoteLocalParameters', True)
    if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print('ERROR: Unable to convert parameters to global.')
        print(SBMLDoc.getErrorLog().toString())
    
    # Write out all reaction-specific function definitions.
    # Enables all variables in reactions to be swapped with vectorized
    # versions.
    Properties = libsbml.ConversionProperties()
    Properties.addOption('expandFunctionDefinitions', True)
    if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print('ERROR: Unable to expand internal function usage.')
        print(SBMLDoc.getErrorLog().toString())
    
    # Write out all state variable and parameter initializations.
    # Enables this data to be placed into required SciPyModel object
    # places.
    Properties = libsbml.ConversionProperties()
    Properties.addOption('expandInitialAssignments', True)
    if SBMLDoc.convert(Properties) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print('ERROR: Unable to expand initial assignments.')
        print(SBMLDoc.getErrorLog().toString())
    
    # Extract SBML Model object from SBML Document object.
    SBMLModel = SBMLDoc.getModel()
    
    # Extract MetaData
    # -- Name, VolumeUnits, SubstanceUnits, TimeUnits
    SciPyModel.MetaData.Name = SBMLModel.getName()
    SciPyModel.MetaData.VolumeUnits = SBMLModel.getVolumeUnits()
    SciPyModel.MetaData.SubstanceUnits = SBMLModel.getSubstanceUnits()
    SciPyModel.MetaData.TimeUnits = SBMLModel.getTimeUnits()
    
    # Extract Compartment Data
    # -- Quantity, Names, VectorIndex
    SciPyModel.Compartments.Quantity = SBMLModel.getNumCompartments()
    for i in range(SBMLModel.getNumCompartments()):
        current_compartment = SBMLModel.getCompartment(i)
        SciPyModel.Compartments.Names.append(current_compartment.name)
        SciPyModel.Compartments.VectorIndex.append(i)
        SciPyModel.Compartments.MetaID.append(current_compartment.meta_id)
    
    # Extract Species Data
    # -- Quanity, Names, Value, VectorIndex, BoundaryValue
    SciPyModel.Species.Quantity = SBMLModel.getNumSpecies()
    for i in range(SBMLModel.getNumSpecies()):
        current_species = SBMLModel.getSpecies(i)
        SciPyModel.Species.Names.append(current_species.name)
        SciPyModel.Species.Value.append(current_species.initial_amount)
        SciPyModel.Species.VectorIndex.append(i)
        SciPyModel.Species.BoundaryValue.append(current_species.boundary_condition)
        SciPyModel.Species.MetaID.append(current_species.meta_id)
    
    # Extract Parameter Data
    # -- Quantity, Names, Value, VectorIndex, MetaID, KineticFlag
    SciPyModel.Parameters.Quantity = SBMLModel.getNumParameters()
    for i in range(SBMLModel.getNumParameters()):
        current_parameter = SBMLModel.getParameter(i)
        SciPyModel.Parameters.Names.append(current_parameter.name)
        SciPyModel.Parameters.Value.append(current_parameter.value)
        SciPyModel.Parameters.VectorIndex.append(i)
        SciPyModel.Parameters.MetaID.append(current_parameter.meta_id)
    [
    SciPyModel.Parameters.KineticFlag.append(False)
    for i in range(SciPyModel.Parameters.Quantity)
    ]
    
    # Extract Reaction Data
    # -- Names, Formulas, Stoichiometry
    SciPyModel.Reactions.Stoichiometry = numpy.zeros(
        [SBMLModel.getNumSpecies(),
         SBMLModel.getNumReactions()])
    SciPyModel.Reactions.Quantity = SBMLModel.getNumReactions()
    for i in range(SBMLModel.getNumReactions()):
        current_reaction = SBMLModel.getReaction(i)
        SciPyModel.Reactions.Names.append(current_reaction.name)
        SciPyModel.Reactions.Formulas.append(
            current_reaction.getKineticLaw().getFormula())

        # Try-Except in order to see if Names or MetaID are used in the functions
        try:
            for r in current_reaction.getListOfReactants():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                    r.getSpecies()), i] -= r.getStoichiometry()
            for p in current_reaction.getListOfProducts():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.Names.index(
                    p.getSpecies()), i] += p.getStoichiometry()
        except ValueError:
            for r in current_reaction.getListOfReactants():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.MetaID.index(
                    r.getSpecies()), i] -= r.getStoichiometry()
            for p in current_reaction.getListOfProducts():
                SciPyModel.Reactions.Stoichiometry[SciPyModel.Species.MetaID.index(
                    p.getSpecies()), i] += p.getStoichiometry()
        else:
            print 'ERROR: Unable to create Stoichiometric Matrix. Check species name/metaid.'

        # Remove Stoichiometry of Boundary State Variables
        for s in range(SciPyModel.Species.Quantity):
            if SciPyModel.Species.BoundaryValue[s]:
                SciPyModel.Reactions.Stoichiometry[s, :] = numpy.zeros(
                    (1, SciPyModel.Reactions.Quantity))

    # Vectorize Functions within SciPyModel object.
    for rxn_ix in range(SciPyModel.Reactions.Quantity):

        # Get information about the current reaction
        Formula = SciPyModel.Reactions.Formulas[rxn_ix]

        # Removes usage of compartments from reaction equations.
        for j in reversed(range(SciPyModel.Compartments.Quantity)):
            if SciPyModel.Compartments.Names[j] != '':  # If name isn't empty
                Formula = Formula.replace(SciPyModel.Compartments.Names[j] + ' * ',
                                          '')
                Formula = Formula.replace(' * ' + SciPyModel.Compartments.Names[j],
                                          '')
                Formula = Formula.replace(' / ' + SciPyModel.Compartments.Names[j],
                                          '')

        # Replace parameter names with index of vectorized parameter array.
        # Iterates through parameter names sorted by length of name.
        for key in sorted(
                SciPyModel.Parameters.Names, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(key, 'p[' + str(
                    SciPyModel.Parameters.Names.index(key)) + ']')

        for key in sorted(
                SciPyModel.Parameters.MetaID, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(key, 'p[' + str(
                    SciPyModel.Parameters.MetaID.index(key)) + ']')

        # Replace species names with index of species parameter array.
        for key in sorted(SciPyModel.Species.Names, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(
                    key, 'y[' + str(SciPyModel.Species.Names.index(key)) + ']')

        for key in sorted(SciPyModel.Species.MetaID, key=len, reverse=True):
            if key != '':
                Formula = Formula.replace(
                    key, 'y[' + str(SciPyModel.Species.MetaID.index(key)) + ']')

        # Reset formula declaration in SciPyModel class
        SciPyModel.Reactions.Formulas[rxn_ix] = Formula
    
    # Grab indecies of kinetic rate constant parameters
    ReactionIndex = []
    for rxn_ix in range(SciPyModel.Reactions.Quantity):
        ReactionIndex.append(
            int(SciPyModel.Reactions.Formulas[rxn_ix].split(']')[0].split('[')[
                -1]))

    # Order the parameters and track the internal index ordering
    SortedIndex = [
        i[0] for i in sorted(enumerate(ReactionIndex), key=lambda x: x[1])
    ]

    # Apply the index ordering to order the formula vector
    SciPyModel.Reactions.Formulas = [
        SciPyModel.Reactions.Formulas[i] for i in SortedIndex
    ]

    # Apply the index ordering to order the stoichiometry matrix
    SciPyModel.Reactions.Stoichiometry = numpy.vstack([
        SciPyModel.Reactions.Stoichiometry[:, i] for i in SortedIndex
    ]).transpose()
    
    return SciPyModel