###
#
# Define parameters for box and text ui elements like paths to UI sprites
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Function to return the enemy ui element parameters
def loadMainBoxUiParameters(generalParameters: Dict) -> Dict:
    """

    Define enemy ship specific UI parameters.

    Input:
        - generalParameters [Dict]: Dictionary with the general parameters    
    
    """
    
    logger.debug('Define the main box ui parameters')
    
    
    ###
    # Initialize dictionary
    mainBoxUiParameters = dict()
    
    
    ##
    # Box parameters
    mainBoxUiParameters['Pause'] = dict()
    mainBoxUiParameters['Pause']['Basepath'] = generalParameters['PathFolderResources'] + 'img/'
    
    # Pause
    mainBoxUiParameters['Pause']['GeneralPause1'] = 'Text_pause1'
    mainBoxUiParameters['Pause']['GeneralPause2'] = 'Text_pause2'
    
    
    ###
    # Return parameters
    return(mainBoxUiParameters)


