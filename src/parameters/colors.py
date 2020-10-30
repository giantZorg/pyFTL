###
#
# Define colors to be used throughout the game
#
###

###
# Load packages
from typing import Dict

# Logging
import logging


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Function which returns the colors
def loadColors() -> Dict:
    """
    
    Specify all the colors used throughout the game as RGB-triplets (tuples)
    
    """
    
    logger.debug('Define colors')
    
    
    ###
    # Initialize the dictionary
    colors = dict()
    
    
    ##
    # General colors
    colors['White'] = (255, 255, 255)
    colors['Black'] = (0, 0, 0)
    colors['Grey1'] = (112, 112, 112)
    colors['Grey2'] = (55, 55, 55)
    
    ##
    # Rooms
    colors['GreyRoom'] = (230, 226, 219)
    colors['PinkRoom'] = (255, 178, 172)
    colors['RedRoomNoOxygen'] = (255, 144, 135)
    
    ##
    # Systems
    colors['GreySystem'] = (125, 125, 125)
    colors['RedSystem'] = (255, 0, 0)
    colors['OrangeSystem'] = (255, 152, 48)
    colors['BlueSystem'] = (93, 234, 239)
    
    ##
    # Doors
    colors['DoorLevel0'] = (255, 114, 36)
    colors['DoorLevel1'] = (255, 150, 48)
    colors['DoorLevel2'] = (161, 161, 159)
    colors['DoorLevel3'] = (161, 161, 159)
    colors['DoorLevel4'] = (161, 161, 159)
    colors['DoorGreyOverlay'] = (81, 81, 80)
    colors['DoorHacked'] = (214, 67, 255)
    
    ##
    # UI
    colors['SystemGreen'] = (100, 255, 98)
    colors['ZoltanYellow'] = (255, 225, 100)
    colors['IonBlue'] = (129, 230, 236)
    colors['DamageRed'] = (255, 0, 0)
    colors['BlockedBlue'] = (89, 187, 196)
    colors['BackupBatteryBrown'] = (165,42,42)
    
    ##
    # Text
    
    
    
    ###
    # Return the dictionary with the colors
    return(colors)

