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
def loadGeneralShipSpriteParameters(generalParameters: Dict) -> Dict:
    """
    
    Define the parameters for ship sprites which are not specific to a certain ship.
    
    Input:
        - generalParameters [Dict]: Dictionary with the general parameters
    
    """
    
    logger.debug('Define the general ship sprite parameters')


    ###
    # Initialize dictionary
    generalShipSpriteParameters = dict()


    ###
    # Setup
    generalShipSpriteParameters['RoomSprites'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations'] = dict()
    
    
    ###
    # Define the room sprites
    generalShipSpriteParameters['RoomSprites']['Paths']['Basepath'] = generalParameters['PathFolderResources'] + 'img/ship/interior/'
    
    # Console orientation: [dx, dy, or]
    # dx: Displacement in x-direction
    # dy: Displacement in y-direction
    # Orientation of the console (1 = Facing down, 2 = Facing left, 3 = Facing up, 4 = Facing right)
    
    ##
    # Shields
    generalShipSpriteParameters['RoomSprites']['Paths']['Shields'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['Shields'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Shields']['Room4'] = ['room_shields.png'] + ['room_shields_' + str(x) + '.png' for x in np.arange(9) + 2]
    generalShipSpriteParameters['RoomSprites']['Informations']['Shields']['Console4'] = [[0, 0, 2], [0, 0, 2], [0, 1, 2], [0, 0, 2], [0, 0, 3], [0, 0, 2], [1, 0, 3], [0, 0, 2], [1, 0, 3], [1, 1, 1]]

    generalShipSpriteParameters['RoomSprites']['Paths']['Shields']['Room2'] = ['room_shields_11.png']
    generalShipSpriteParameters['RoomSprites']['Informations']['Shields']['Console2'] = [[1, 0, 1]]

    
    ##
    # Engines
    generalShipSpriteParameters['RoomSprites']['Paths']['Engines'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['Engines'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Engines']['Room4'] = ['room_engines.png'] + ['room_engines_' + str(x) + '.png' for x in [2, 4, 6, 7, 9]]
    generalShipSpriteParameters['RoomSprites']['Informations']['Engines']['Console4'] = [[0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 1], [1, 0, 3]]

    generalShipSpriteParameters['RoomSprites']['Paths']['Engines']['Room2'] = ['room_engines_' + str(x) + '.png' for x in [3, 5, 8]]
    generalShipSpriteParameters['RoomSprites']['Informations']['Engines']['Console2'] = [[1, 0, 4], [0, 0, 3], [0, 1, 2]]
    
    
    ##
    # Oxygen
    generalShipSpriteParameters['RoomSprites']['Paths']['Oxygen'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Oxygen']['Room4'] = ['room_oxygen_' + str(x) + '.png' for x in [3, 11]]
    generalShipSpriteParameters['RoomSprites']['Paths']['Oxygen']['Room2'] = ['room_oxygen.png'] + ['room_oxygen_' + str(x) + '.png' for x in [2, 4, 5, 6, 7, 8, 9, 10, 12, 13]]


    ##
    # Weapons
    generalShipSpriteParameters['RoomSprites']['Paths']['WeaponControl'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['WeaponControl'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['WeaponControl']['Room4'] = ['room_weapons.png'] + ['room_weapons_' + str(x) + '.png' for x in [2, 3, 4, 5, 6, 7, 9, 10]]
    generalShipSpriteParameters['RoomSprites']['Informations']['WeaponControl']['Console4'] = [[1, 0, 3], [1, 0, 3], [1, 0, 3], [0, 0, 3], [1, 0, 4], [1, 0, 3], [1, 0, 3], [1, 0, 3], [0, 0, 3]]

    generalShipSpriteParameters['RoomSprites']['Paths']['WeaponControl']['Room2'] = ['room_weapons_8.png']
    generalShipSpriteParameters['RoomSprites']['Informations']['WeaponControl']['Console2'] = [[1, 0, 3]]
    
    
    ##
    # Drone control
    generalShipSpriteParameters['RoomSprites']['Paths']['DroneControl'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['DroneControl']['Room4'] = ['room_drones.png'] + ['room_drones_' + str(x) + '.png' for x in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]
    generalShipSpriteParameters['RoomSprites']['Paths']['DroneControl']['Room2'] = ['room_drones_' + str(x) + '.png' for x in [2, 3, 14, 15]]
    
    
    ##
    # Medbay
    generalShipSpriteParameters['RoomSprites']['Paths']['Medbay'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['Medbay'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Medbay']['Room4'] = ['room_medbay.png'] + ['room_medbay_' + str(x) + '.png' for x in [3, 4, 7, 8]]
    generalShipSpriteParameters['RoomSprites']['Informations']['Medbay']['SpaceBlocked'] = [[1, 0], [1, 1], [0, 0], [0, 1], []]     # This space will not be available to crew
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Medbay']['Room2'] = ['room_medbay_' + str(x) + '.png' for x in [2, 5, 6, 9]]


    ##
    # Teleporter
    generalShipSpriteParameters['RoomSprites']['Paths']['CrewTeleporter'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['CrewTeleporter']['Room'] = 'teleporter_selected.png'
    
    
    ##
    # Cloaking
    generalShipSpriteParameters['RoomSprites']['Paths']['Cloaking'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Cloaking']['Room4'] = ['room_cloaking.png'] + ['room_cloaking_' + str(x) + '.png' for x in [2, 10, 11]]
    generalShipSpriteParameters['RoomSprites']['Paths']['Cloaking']['Room2'] = ['room_cloaking_' + str(x) + '.png' for x in [3, 4, 5, 6, 7, 8, 9]]


    ##
    # Artillery beam
    generalShipSpriteParameters['RoomSprites']['Paths']['ArtilleryBeam'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['ArtilleryBeam']['Room4'] = []
    generalShipSpriteParameters['RoomSprites']['Paths']['ArtilleryBeam']['Room2'] = ['room_artillery.png']
       

    ##
    # Artillery flak
    generalShipSpriteParameters['RoomSprites']['Paths']['FlakArtillery'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['FlakArtillery']['Room4'] = []
    generalShipSpriteParameters['RoomSprites']['Paths']['FlakArtillery']['Room2'] = ['room_artillery.png']
    
    
    ##
    # CLonebay
    generalShipSpriteParameters['RoomSprites']['Paths']['Clonebay'] = dict()
    generalShipSpriteParameters['RoomSprites']['Paths']['Clonebay']['Room'] = ['clone_bottom.png', 'clone_top.png']
       
    
    ##
    # Mind control
    generalShipSpriteParameters['RoomSprites']['Paths']['MindControl'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['MindControl']['Room4'] = ['room_mind.png'] + ['room_mind_' + str(x) + '.png' for x in [4, 10]]
    generalShipSpriteParameters['RoomSprites']['Paths']['MindControl']['Room2'] = ['room_mind_' + str(x) + '.png' for x in [2, 3, 5, 6, 7, 8, 9, 11, 12]]


    ##
    # Hacking
    generalShipSpriteParameters['RoomSprites']['Paths']['Hacking'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Hacking']['Room4'] = ['room_hacking_' + str(x) + '.png' for x in [6, 8]]
    generalShipSpriteParameters['RoomSprites']['Paths']['Hacking']['Room2'] = ['room_hacking.png'] + ['room_hacking_' + str(x) + '.png' for x in [2, 3, 4, 5, 7, 9]]
    
    
    ##
    # Piloting
    generalShipSpriteParameters['RoomSprites']['Paths']['Piloting'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['Piloting'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Piloting']['Room4'] = []
    generalShipSpriteParameters['RoomSprites']['Informations']['Piloting']['Console4'] = []

    generalShipSpriteParameters['RoomSprites']['Paths']['Piloting']['Room2'] = ['room_pilot.png'] + ['room_pilot_' + str(x) + '.png' for x in np.arange(3) + 2]
    generalShipSpriteParameters['RoomSprites']['Informations']['Piloting']['Console2'] = [[0, 0, 4], [1, 0, 4], [1, 0, 4], [0, 0, 4]]


    ##
    # Sensors
    generalShipSpriteParameters['RoomSprites']['Paths']['Sensors'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['Sensors'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['Sensors']['Room4'] = []
    generalShipSpriteParameters['RoomSprites']['Informations']['Sensors']['Console4'] = []

    generalShipSpriteParameters['RoomSprites']['Paths']['Sensors']['Room2'] = ['room_sensors.png'] + ['room_sensors_' + str(x) + '.png' for x in [2, 3, 4, 6]]
    generalShipSpriteParameters['RoomSprites']['Informations']['Sensors']['Console2'] = [[1, 0, 1], [0, 0, 3], [1, 0, 4], [0, 1, 2], [0, 1, 4]]


    ##
    # Doors    
    generalShipSpriteParameters['RoomSprites']['Paths']['DoorSystem'] = dict()
    generalShipSpriteParameters['RoomSprites']['Informations']['DoorSystem'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['DoorSystem']['Room4'] = []
    generalShipSpriteParameters['RoomSprites']['Informations']['DoorSystem']['Console4'] = []

    generalShipSpriteParameters['RoomSprites']['Paths']['DoorSystem']['Room2'] = ['room_doors.png'] + ['room_doors_' + str(x) + '.png' for x in np.arange(8) + 2]
    generalShipSpriteParameters['RoomSprites']['Informations']['DoorSystem']['Console2'] = [[1, 0, 3], [0, 0, 1], [1, 0, 4], [0, 0, 4], [0, 0, 4], [0, 1, 4], [1, 0, 3], [0, 0, 2], [1, 0, 4]]
    

    ##
    # Backup battery 
    generalShipSpriteParameters['RoomSprites']['Paths']['BackupBattery'] = dict()
    
    generalShipSpriteParameters['RoomSprites']['Paths']['BackupBattery']['Room4'] = ['room_battery_' + str(x) + '.png' for x in [4]]
    generalShipSpriteParameters['RoomSprites']['Paths']['BackupBattery']['Room2'] = ['room_battery.png'] + ['room_battery_' + str(x) + '.png' for x in [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
    


    ###
    # Symbols and icons
    generalShipSpriteParameters['SymbolSprites'] = dict()
    generalShipSpriteParameters['SymbolSprites']['Basepath'] = generalParameters['PathFolderResources'] + 'img/icons/'

    generalShipSpriteParameters['SymbolSprites']['Paths'] = {'Shields': 'shields', 'Engines': 'engines', 'Oxygen': 'oxygen', 'WeaponControl': 'weapons', 'DroneControl': 'drones', 'Medbay': 'medbay', 'CrewTeleporter': 'teleporter', 'Cloaking': 'cloaking', 'Artillery': 'artillery', 'MindControl': 'mind', 'Hacking': 'hacking', 'Clonebay': 'clonebay', 'Piloting': 'pilot', 'Sensors': 'sensors', 'DoorSystem': 'doors', 'BackupBattery': 'battery'}
    
    generalShipSpriteParameters['SymbolSprites']['SpritePrefix'] = 's_'
    generalShipSpriteParameters['SymbolSprites']['SpriteSuffix'] = {'White': '', 'Blue': '_blue1', 'Green': '_green1', 'Green2': '_green2', 'Grey': '_grey1', 'Grey2': '_grey2', 'Orange': '_orange1', 'Orange2': '_orange2', 'Overlay': '_overlay', 'Overlay2': '_overlay2', 'Red': '_red1', 'Red2': '_red2'}
    
    
    ###
    # Console sprites
    generalShipSpriteParameters['ConsoleSprites'] = dict()
    generalShipSpriteParameters['ConsoleSprites']['Basepath'] = generalParameters['PathFolderResources'] + 'img/ship/interior/'

    generalShipSpriteParameters['ConsoleSprites']['Console'] = 'computer1.png'  # Needed for the enemy ships
    generalShipSpriteParameters['ConsoleSprites']['ConsoleSystems'] = {0: 'computer1_glow1.png', 1: 'computer1_glow2.png', 2: 'computer1_glow3.png'}
    generalShipSpriteParameters['ConsoleSprites']['ConsolePilot'] = {0: 'glow_pilot1.png', 1: 'glow_pilot2.png', 2: 'glow_pilot3.png'}
        
    
    ###
    # Return the dictionary containing the general ship sprite parameters
    return(generalShipSpriteParameters)
    