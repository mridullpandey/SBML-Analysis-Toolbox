# This file converts between a human-readable Antimony model and a machine readable SBML model
#
# 1 - Determines if input filename is Antimony or SBML model.
# 2 - Loads model using libAntimony module format.
# 3 - Outputs either SBML or Antimony depending on input.\
#

import antimony

def SBML2antimony( filename )

    if filename[-3:] == "xml" :
        model_name = filename.replace( filename[-3:], "ant" )
        antimony.loadSBMLFile( filename )
        antimony.writeAntimonyFile( model_name, antimony.getMainModuleName() )

    elif filename[-3:] == "ant" :
        model_name = filename.replace( filename[-3:], "xml" )
        antimony.loadAntimonyFile( filename )
        antimony.writeSBMLFile( model_name, antimony.getMainModuleName() )

    else:
        print("Error, input file not SBML '*.xml' or Antimony '*.ant' ")
