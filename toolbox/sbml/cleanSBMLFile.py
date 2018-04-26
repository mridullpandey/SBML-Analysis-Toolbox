def cleanSBMLFile( sbmlfile ):
    '''
    This function needs to be rewritten to use the SciPyModel
    object format.
    '''
    import libsbml, sys
    
    doc = libsbml.readSBMLFromFile( sbmlfile )

    # Return errors with SBML model.
    if doc.getNumErrors( libsbml.LIBSBML_SEV_FATAL ):
        print( 'Encountered serious errors while reading file' )
        print( doc.getErrorLog().toString() )
        sys.exit(1)

    # Clear non-fatal errors.
    doc.getErrorLog().clearLog()

    #
    # Prepare conversion of SBML model
    #
    # Make all parameters global.
    props = libsbml.ConversionProperties()
    props.addOption( "promoteLocalParameters", True )

    # Return parameter conversion error.
    if doc.convert(props) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print( 'The document could not be converted' )
        print( doc.getErrorLog().toString() )

    # Get all initial conditions.
    props = libsbml.ConversionProperties()
    props.addOption( "expandInitialAssignments", True )

    # Return initial condition error.
    if doc.convert(props) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print( 'The document could not be converted' )
        print( doc.getErrorLog().toString() )

    # Remove internal function usage.
    props = libsbml.ConversionProperties()
    props.addOption( "expandFunctionDefinitions", True )

    # Return function expansion error.
    if doc.convert(props) != libsbml.LIBSBML_OPERATION_SUCCESS:
        print( 'The document could not be converted' )
        print( doc.getErrorLog().toString() )

    # Get SBML model from document.
    libsbml.writeSBMLToFile( doc, sbmlfile )

    return sbmlfile