def compareModels( sbmlModel, antModel ):
    '''
    This code needs to be rewritten.
    '''
    
    import roadrunner, pylab, antimony

    sbmlModel = "00001-sbml-l2v4.xml"
    antModel  = sbmlModel.replace(sbmlModel[-3:],"ant")

    # Make a round trip to and from Antimony
    antimony.loadSBMLFile( sbmlModel )
    antimony.writeAntimonyFile( antModel, antimony.getModuleNames()[1] )
    antimony.loadAntimonyFile( antModel )
    antimony.writeSBMLFile( "test.xml", antimony.getModuleNames()[1] )

    rr1 = roadrunner.RoadRunner( sbmlModel )
    rr2 = roadrunner.RoadRunner( "test.xml" )

    result1 = rr1.simulate( 0, 10, 101 )
    result2 = rr2.simulate( 0, 10, 101 )

    result = result1 - result2

    pylab.plot( result[:,0], result[:,1:] )


    pylab.show()