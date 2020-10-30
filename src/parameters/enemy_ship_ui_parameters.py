###
#
# Define parameters for the enemy ship ui elements like paths to UI sprites
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
def loadEnemyShipUiParameters(generalParameters: Dict) -> Dict:
    """

    Define enemy ship specific UI parameters.

    Input:
        - generalParameters [Dict]: Dictionary with the general parameters    
    
    """
    
    logger.debug('Define the enemy ship ui parameters')
    
    
    ###
    # Initialize dictionary
    enemyShipUiParameters = dict()
    
    
    ##
    # Box parameters
    enemyShipUiParameters['Box'] = dict()
    enemyShipUiParameters['Box']['Basepath'] = generalParameters['PathFolderResources'] + 'img/combatUI/'
    
    enemyShipUiParameters['Box']['BoxEnemy'] = 'box_hostiles2'
    enemyShipUiParameters['Box']['BoxEnemyMask'] = 'box_hostiles_mask'

    enemyShipUiParameters['Box']['BoxBoss'] = 'box_hostiles_boss'
    enemyShipUiParameters['Box']['BoxBossMask'] = 'box_hostiles_mask'    
    
    
    ###
    # Return the dictionary with the enemy ship ui parameters
    return(enemyShipUiParameters)

