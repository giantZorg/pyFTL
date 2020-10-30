###
#
# Define parameters which will be used for the player ships
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
# Function to return the player ship parameters
def loadPlayerShipParameters(generalParameters: Dict) -> Dict:
    """
    
    Define the parameters necessary for the player ship like sprite location, systems and starting values.
    
    Input:
        - generalParameters [Dict]: Dictionary with the general parameters
    
    """

    logger.debug('Define the player ship parameters')
    
    
    ###
    # Initialize dictionary
    playerShipParameters = dict()
    
    
    ###
    # List of all the ships for which data shall be loaded
    playerShipParameters['ShipsAvailable'] = ['Kestrel']
    
    
    ###
    # Define the Kestrel ships
    playerShipParameters['Kestrel'] = dict()
    
    # Variants
    playerShipParameters['Kestrel']['Variants'] = ['A']  # ['A', 'B', 'C']
    
    # Basepath
    playerShipParameters['Kestrel']['Basepath'] = generalParameters['PathFolderResources'] + 'img/ship/Kestral'
    playerShipParameters['Kestrel']['Shields'] = 'shields1'
    playerShipParameters['Kestrel']['Cloak'] = 'cloak'

    # Coordinates
    playerShipParameters['Kestrel']['ShiftShields'] = np.array([-44, -1])
    playerShipParameters['Kestrel']['ShiftOrigin'] = np.array([22, 69])


    ##
    # Kestrel A
    playerShipParameters['KestrelA'] = dict()
    
    # Define the different paths for the sprites
    playerShipParameters['KestrelA']['BaseSprite'] = 'base'
    playerShipParameters['KestrelA']['GibSprites'] = ['gib' + str(i) for i in range(1,7)]
   
    # Define the layout
    playerShipParameters['KestrelA']['LayoutMatrix'] = np.array([[0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                                                                   [0, 2, 2, 5, 5, 0, 9, 9, 12, 12, 0, 0, 0, 0, 0],
                                                                   [1, 3, 3, 0, 6, 6, 9, 9, 12, 12, 14, 14, 16, 16, 17],
                                                                   [1, 3, 3, 0, 6, 6, 10, 10, 13, 13, 15, 15, 16, 16, 17],
                                                                   [0, 4, 4, 7, 7, 0, 10, 10, 13, 13, 0, 0, 0, 0, 0],
                                                                   [0, 0, 0, 0, 0, 0, 11, 11, 0, 0, 0, 0, 0, 0, 0]
                                                                   ], dtype = int)

    playerShipParameters['KestrelA']['DoorsVertical'] = [[], [], [4, 9], [1, 2, 7, 11, 13], [1, 2, 7, 11, 13, 15], [4, 9], [], []]
    playerShipParameters['KestrelA']['DoorsHorizontal'] = [[], [], [], [3, 5], [], [3, 5], [], [1, 7], [1, 2, 6, 7], [4], [], [], [], [], [], [], []]

    # 'Shields', 'Engines', 'Oxygen', 'WeaponControl', 'DroneControl', 'Medbay', 'CrewTeleporter', 'Cloaking', 'Artillery', 'Clonebay', 'MindControl', 'Hacking', 'Piloting', 'Sensors', 'DoorSystem', 'BackupBattery'
    #playerShipParameters['KestrelA']['RoomSpecifitions'] = {
    #        'System': np.array(generalParameters['ShipSystems']),
    #        'Position': np.array([13, 3, 2, 6, 16, 12, 4, 10, 0, 12, 9, 7, 17, 15, 14, 5]),
    #        'PowerMax': np.array([2, 2, 1, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]),
    #        'PowerCurrent': np.array([2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]),
    #        'SystemPresent': np.array([True, True, True, True, False, True, False, False, False, False, False, False, True, True, True, False]), 
    #        'Sprite': np.array([0] * 16)
    #        }

    playerShipParameters['KestrelA']['RoomSpecifitions'] = {
        'System': np.array(generalParameters['ShipSystems']),
        'Position': np.array([13, 3, 2, 6, 16, 12, 4, 10, 0, 12, 9, 7, 17, 15, 14, 5]),
        'PowerMax': np.array([4, 2, 1, 3, 2, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]),
        'PowerCurrent': np.array([2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]),
        'SystemPresent': np.array([True, True, True, True, True, True, False, True, False, False, False, False, True, True, True, False]), 
        'Sprite': np.array([0] * 16)
        }


    playerShipParameters['KestrelA']['ClonebayOrientation'] = np.array([1,0,1])  # x, y, orientation
#    playerShipParameters['KestrelA']['DoorLevel'] = 1

    # Hull points
    playerShipParameters['KestrelA']['HullPoints'] = 30

    # Reactor power
    playerShipParameters['KestrelA']['ReactorStart'] = 8    
    
    # Starting weapons
    playerShipParameters['KestrelA']['WeaponSlotsMax'] = 4       # If one wants to include events which increase the number of weapon slots
    playerShipParameters['KestrelA']['WeaponSlotsCurrent'] = 4
    
    playerShipParameters['KestrelA']['WeaponPosition'] = (np.array([530, 153]), np.array([530, 264]), np.array([377, 117]), np.array([377, 300]))    # Anchor points on the ship hull sprite in pixels
    playerShipParameters['KestrelA']['WeaponOrientation'] = (43, 41, 43, 41)
    playerShipParameters['KestrelA']['WeaponInset'] = (3, 3, 13, 13)

    playerShipParameters['KestrelA']['WeaponInitial'] = ['BasicLaser', 'BasicLaser', 'BasicLaser', 'BasicLaser']
    
    
    
    ###
    # Return the dictionary containing the player ship parameters
    return(playerShipParameters)
    

