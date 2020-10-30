###
#
# Define parameters for the power management ui elements like paths to UI sprites
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
# Function to return the energy management ui element parameters
def loadEnergyManagementUiParameters(generalParameters: Dict) -> Dict:
    """

    Define enemy energy management specific UI parameters.

    Input:
        - generalParameters [Dict]: Dictionary with the general parameters    
    
    """
    
    logger.debug('Define the energy management ui parameters')
    
    
    ###
    # Initialize dictionary
    energyManagementUiParameter = dict()
    
    
    ###
    # Setup
    energyManagementUiParameter['Wires'] = dict()
    
    
    ###
    # Wires
    energyManagementUiParameter['Wires']['Basepath'] = generalParameters['PathFolderResources'] + 'img/wireUI/'
    energyManagementUiParameter['Wires']['Basepath2'] = generalParameters['PathFolderResources'] + 'img/'
    
    # For every added/removed weapon slot, the wires have to be extended by this amount
    energyManagementUiParameter['LengthUnderWeapons'] = 97
    
    # Define length of the system
    energyManagementUiParameter['Wires']['TypePerSystem'] = {'Shields': 'short', 'Engines': 'short', 'Oxygen': 'short', 'Medbay': 'short', 'CrewTeleporter': 'wide', 'Cloaking': 'wide', 'Artillery': 'short', 'Clonebay': 'short', 'MindControl': 'wide', 'Hacking': 'wide'}

    # Paths to the different wire pictures
    energyManagementUiParameter['Wires']['shortPath'] = 'wire_36'
    energyManagementUiParameter['Wires']['shortEndPath'] = 'wire_36_cap'

    energyManagementUiParameter['Wires']['widePath'] = 'wire_54'
    energyManagementUiParameter['Wires']['wideEndPath'] = 'wire_54_cap'
    
    energyManagementUiParameter['Wires']['UnderWeapons3'] = 'wire_456_3weapon_cap'
    energyManagementUiParameter['Wires']['UnderWeapons4'] = 'wire_456_cap'
    
    energyManagementUiParameter['Wires']['ReactorFull'] = 'wire_full'
    
    # Different basepath
    energyManagementUiParameter['Wires']['ReactorMask'] = 'wire_left_mask'
    
    
    ###
    # Parameters to create the necessary sprites
    energyManagementUiParameter['Wires']['PixelHeightStem'] = 54
    energyManagementUiParameter['Wires']['PixelHeightAdditionalBar'] = 30
    
    
    ###
    # Return the dictionary containing the energy management ui parameters
    return(energyManagementUiParameter)
    
