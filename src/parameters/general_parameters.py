###
#
# Define parameters which will be used throughout various places in the game
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
# Function which returns the general parameters
def loadGeneralParameters() -> Dict:
    """
    
    Define all the parameters which will be used throughout various places of the game and return them in a dictionary.
    
    """

    logger.debug('Define general parameters')
    
    
    ###
    # Initialize the dictionary
    generalParameters = dict()
    
    
    ##
    # Screen parameters
    generalParameters['DisplayWidth'] = 1280
    generalParameters['DisplayHeight'] = 720
    generalParameters['DisplayTitle'] = 'pyFTL'
    
    generalParameters['MaxFramerate'] = 60
    generalParameters['UpdateFramerateDisplay'] = 1000

    generalParameters['PositionOffsetFight'] = np.array([450, int(generalParameters['DisplayHeight'] / 2)])
    generalParameters['PositionOffsetIdle'] = np.array([int(generalParameters['DisplayWidth'] / 2), int(generalParameters['DisplayHeight'] / 2)])
    
    generalParameters['OffsetEnemyBox'] = (0, 70)
        
    
    ##
    # Paths to datafiles
    generalParameters['PathFolderResources'] = 'data/ftldata/'
    generalParameters['PathFoldersBackgroundPictures'] = ['data/images/background']


    ##
    # Background pictures
    generalParameters['BackgroundScalePictures'] = True
    generalParameters['BackgroundPictureFormats'] = ['.png', '.jpeg', '.jpg']
    

    ##
    # Ship
    generalParameters['ShipSystems'] = ['Shields', 'Engines', 'Oxygen', 'WeaponControl', 'DroneControl', 'Medbay', 'CrewTeleporter', 'Cloaking', 'Artillery', 'Clonebay', 'MindControl', 'Hacking', 'Piloting', 'Sensors', 'DoorSystem', 'BackupBattery']
    
    # Rooms
    generalParameters['RoomHeightPixel'] = 35
    generalParameters['DoorHeightPixel'] = 9   # Door span (colored part of level 0/1 doors)
    generalParameters['DoorMinimumPixel'] = 1   # Door minimum
    generalParameters['DoorMinimumPixelBroken'] = 3 # Door minimum if door is bashed in [not yet implemented]
    generalParameters['DoorWidthSide'] = 2
    
    generalParameters['DoorAnimationTimePerPixel'] = 32 # Time in milliseconds for to open/close the door one pixel
    
    # Shields
    generalParameters['ShieldMaxLevel'] = 6         # Maximal available shield level
    generalParameters['ShieldMultAlpha'] = 230
    generalParameters['ZoltanShieldMaxHealth'] = 5
    
    # Oxygen
    generalParameters['MinOxygenPrzNecessary'] = 5  # Minimal oxygen level without taking damage
    
    generalParameters['OxygenLevel1'] = 2       # 2% oxygen gets refilled per second
    generalParameters['OxygenLossGeneral'] = 1  # 1% oxygen gets lost per second
    generalParameters['OxygenLossSpace'] = 500  # 500% oxygen gets lost to space if a room to space is open
    generalParameters['OxygenLossBreach'] = 3
    
    generalParameters['OxygenEquilibriumSpeed'] = 1.6
    
    # Weapons
    generalParameters['WeaponsExtendPixels'] = 10
    generalParameters['WeaponsExtendTimeSeconds'] = 0.4
    
    generalParameters['WeaponDepowerRate'] = 2  # Factor how much faster weapons will depower than power up
    
    # Systems
    generalParameters['MainSystems'] = ['Shields', 'Engines', 'Oxygen', 'WeaponControl', 'DroneControl', 'Medbay', 'CrewTeleporter', 'Cloaking', 'Artillery', 'Clonebay', 'MindControl', 'Hacking']
    generalParameters['SubSystems'] = ['Piloting', 'Sensors', 'DoorSystem', 'BackupBattery']
    generalParameters['SystemWithConsolePercentageBonus'] = ['Piloting', 'Shields', 'Engines', 'WeaponControl']
    
    # Reactor
    generalParameters['MaxReactorPowerPossible'] = 34
    
    
    ##
    # UI
    generalParameters['UiMainSystemOrder'] = ['Shields', 'Engines', 'Medbay', 'Clonebay', 'Oxygen', 'CrewTeleporter', 'Cloaking', 'Artillery', 'MindControl', 'Hacking']    # Order of the main systems in the UI without weapons and drone control
    
    # Bars
    generalParameters['WideBarLength'] = 28
    generalParameters['ShortBarLength'] = 16
    generalParameters['WideBarHeight'] = 7
    generalParameters['ShortBarHeight'] = 6
    generalParameters['BarPixelsSkip'] = 2
    generalParameters['BarPixelsSkipShields'] = [2, 6]
    
    # Positioning
    generalParameters['UiWiresOffsetBottomLeft'] = np.array([30, 14])
    generalParameters['UiWiresOffsetReactorBar'] = np.array([9, -32])  # Offset for the first reactor bar
    generalParameters['UiWiresOffset'] = 19
    generalParameters['UiEnergySymbolsOffset'] = np.array([-33, -4])
    generalParameters['UiEnergyWeaponSymbolFirst'] = -1
    generalParameters['UiEnergyWeaponSymbolCorrection'] = -6
    generalParameters['UiEnergyBarsOffset'] = np.array([24, 14])
    generalParameters['UiEnergySymbolsMaxDistance'] = 13
    
    
    ##
    # Texts
    generalParameters['TextFont'] = 'lucidaconsole'
    generalParameters['PauseOffsetY'] = 550

    
    
    ###
    # Return the general parameters
    return(generalParameters)


