###
#
# Define parameters which will be used for the enemy ships
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# Arrays
import numpy as np


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Function to return the enemy ship parameters
def loadEnemyShipParameters(generalParameters: Dict) -> Dict:
    """
    
    Define the parameters necessary for the enemy ships like sprite location and systems.
    Unlike the player ships, some values will be generated at ship creation and are missing here.
    
    Input:
        - generalParameters [Dict]: Dictionary with the general parameters
    
    """

    logger.debug('Define the player ship parameters')
    
    
    ###
    # Initialize dictionary
    enemyShipParameterDict = dict()
    
    
    ###
    # List of all ships for which data shall be loaded
    enemyShipParameterDict['ShipsAvailable'] = ['RebelFighter']

    ###
    # Shields
    # There is only one base enemy shield sprite which will need to be stretched to the size of the ship sprite
    enemyShipParameterDict['ShieldPath'] = generalParameters['PathFolderResources'] + 'img/ship/enemy_shields.png'

    ###
    # Define the rebel fighter
    enemyShipParameterDict['RebelFighter'] = dict()
    
    # Basepath
    enemyShipParameterDict['RebelFighter']['Basepath'] = generalParameters['PathFolderResources'] + 'img/ships_noglow/rebel_long'
    enemyShipParameterDict['RebelFighter']['Cloak'] = generalParameters['PathFolderResources'] + 'img/ship/rebel_long_cloak.png'
    
    # Coordinates
    enemyShipParameterDict['RebelFighter']['ShiftShields'] = np.array([0, 35])
    enemyShipParameterDict['RebelFighter']['ShiftOrigin'] = np.array([22, -24])
        
    # Shield stretch
    enemyShipParameterDict['RebelFighter']['StretchShields'] = np.array([1.1, 1.3])
    
    
    ##
    # Define the different paths for the sprites
    enemyShipParameterDict['RebelFighter']['BaseSprite'] = 'base'
    enemyShipParameterDict['RebelFighter']['GibSprites'] = ['gib' + str(i) for i in range(1,5)]
    
    # Define the layout
    enemyShipParameterDict['RebelFighter']['LayoutMatrix'] = np.array([[0, 0, 1, 0, 0],
                                                                       [0, 0, 1, 0, 0],
                                                                       [0, 0, 2, 0, 0],
                                                                       [0, 3, 2, 4, 0],
                                                                       [0, 3, 0, 4, 0],
                                                                       [5, 5, 6, 7, 7],
                                                                       [5, 5, 6, 7, 7]
                                                                       ], dtype = int)
    
    enemyShipParameterDict['RebelFighter']['DoorsVertical'] = [[], [], [], [], [3, 4], [], [3], [4], []]
    enemyShipParameterDict['RebelFighter']['DoorsHorizontal'] = [[], [], [6], [3], [6], [], []]
    
    # 'Shields', 'Engines', 'Oxygen', 'WeaponControl', 'DroneControl', 'Medbay', 'CrewTeleporter', 'Cloaking', 'Artillery', 'Clonebay', 'MindControl', 'Hacking', 'Piloting', 'Sensors', 'DoorSystem', 'BackupBattery'
    enemyShipParameterDict['RebelFighter']['RoomSpecifitions'] = {
            'System': np.array(generalParameters['ShipSystems']),
            'Position': np.array([7, 6, 4, 5, 0, 3, 2, 0, 0, 3, 0, 0, 1, 0, 0, 0]),
            'PowerMax': np.array([2, 2, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            'PowerCurrent': np.array([2, 2, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            'SystemPresent': np.array([True, True, True, True, False, True, True, False, False, False, False, False, True, False, False, False]),
            'Sprite': np.array([0] * 16)
            }
    
    enemyShipParameterDict['RebelFighter']['Consoles'] = {  # The console location can also be in the ship generator, just not at a door location
            'Rooms': [7, 6, 5, 1],
            'X': [1, 0, 0, 0],
            'Y': [0, 1, 0, 0],
            'Orientation': [4, 1, 2, 3]
            }

    enemyShipParameterDict['RebelFighter']['ClonebayOrientation'] = np.array([0,0,1])  # x, y, orientation

    # Reactor Power
    enemyShipParameterDict['RebelFighter']['ReactorStart'] = 10
    
    # Weapon positions
    ### TO BE ADDED
    
    # Set initial values for testing, should be set newly after ship initialization and before setup
    # Hull points
    enemyShipParameterDict['RebelFighter']['HullPoints'] = 11

    # Starting weapons
    enemyShipParameterDict['RebelFighter']['WeaponSlotsMax'] = 4       # If one wants to include events which increase the number of weapon slots    

    
    ###
    # Return the dictionary containing the enemy ship parameters
    return(enemyShipParameterDict)
    

