###
#
# Define a base class used for all the ships. Contains the basic functions needed for all the ships to function correctly.
#
###


###
# Load packages

# Logging
import logging

# Typing
#from typing import Dict

# Arrays and matrices
import numpy as np

# Pygame
import pygame

# Proper copies
import copy


###
# Import ressources

# Rooms
import src.classes.elements.rooms as rooms

# Doors
import src.classes.elements.doors as doors

# Helperfunctions
from src.misc.helperfunctions import copySprite




###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class used for all the ships
class baseShip(object):
    """
    
    Base class used for all the ships. Contains the functions necessary for the correct ship setup.
    
    Fields:
        - weapons [List]: List of all active weapons
        - augments [List]: List of all augments on the ship
        
        - activeSprites [Dict]: Dictionary with the active sprites which shall be drawn by the draw function
        
        - layoutExpanded [np.matrix]: Matrix of the ship layout with the space padded around the rooms
        - doorMatrixHorizontal [np.matrix]: Matrix of the horizontal doors
        - doorMatrixVertical [np.matrix]: Matrix of the vertical doors
        
        - roomSpecifications [Dict]: Dictionary with the rooms and the systems present within them
        - clonebayOrientation [np.array]: Position and orientation of the clonebay within the clonebay room (x, y, orientation)
        
        - systems [Dict]: Dictionary with all the present systems on the ship. Contains their power levels and status, as well as sprite selection information
        - systemsPresent [Set]: Set of all the present systems
        - systemsPresentRoomMapping [Dict]: Mapping RoomKey:System to lookup the present system for a given room
        - roomsWithSystems [Set]: Set of all roomkeys with systems present
        
        - zoltanShieldPresent [bool]: Indicator if a zoltan shield is present
        - zoltanShieldStrength [int]: Number of zoltan shield layers
        
        - reactor [Dict]: Dictionary containing the reactor informations with the fields SystemPower, PowerAvailable, PowerBlocked, SystemBackupPower, BackupPowerAvailable
        
        - originShipCanvas [np.array]: Offset for the conversion of room coordinates to pixel coordinates
        - originShields [np.array]: Offset for the shield sprite relative to the hull sprites
        
        - deltaBattleToIdle [np.array]: Pixle changes between idle and battle
        
        - shipSprites [Dict]: Dictionary containing the ship sprites Base, Gib, Shield{level}, ZoltanShield, Cloak
        
        - shipRooms [Dict]: Dictionary containing information about the rooms, including the pixel positions.
        - shipFields [Dict]: Dictionary containing information about the individual fields on the ships and whether they are accessible by crew.
        - presentRooms [np.array]: Array containing the identifiers for the present rooms on the ship
        - presentDoors [np.array]: Array containing the identifiers for the present doors on the ship
        
        - rooms [Dict]: Dictionary holding the room objects. Keys are the roomIndex as defined in the ship layout in the parameters
        - doors [Dict]: Dictionary holding the door objects. Keys are the doorIndex as defined by {x1}_{y1}_{x2}_{y2} with x being the upperleft and y being the lowerright field of the door
        
        - roomConnections [np.matrix]: Matrix of dimension nDoors[unique room connections] x 2 with rooms connected by doors by rows. The rooms are indicated by the roomKeys, space is denoted with 0. The matrix is ordered by columns
        - roomConnections [np.matrix, None]: Matrix of rooms connected by open doors, specified the same way like roomConnections. None if all doors are closed
        
        - doorRooms [Dict]: Dictionary which lists for each doorKey the connected rooms in a tuple
        - roomDoors [Dict]: Dictionary which lists for each roomKey the connected doors in a tuple
        - spaceDoors [set]: Set of all doorKeys which are connected to space
        
        - doorRectMatrix [np.matrix]: Matrix of all door rects in pixels on the screen. Every door is a row of the matrix
        - doorKeysForRects [np.array]: Vector of all doorKeys in the order they appear in the doorRectMatrix
        - doorRectForSelection[np.matrix]: Matrix of all door rects with the inverted lowerright point appended for quicker comparisons later on
        
        - currentMaxShieldStrength [int]: Current max shield strength based on current power
    
    Fields to be provided by the derived class:
        - parameters [Dict]: Reference to all parameters
        - spritesAll [Dict]: Reference to the loaded sprites
        
        - ship [str]: Ship selection
        - variant [str]: Ship variant selection
        
        - playerShip [bool]: Logical to differentiate between the player and the enemy ship
        - battle [bool]: Logical to indicate whether the ship is in battle or not

    Methods:
        - shipSetup(): After all the fields are set, this function constructs the initial state of the ship
        - expandLayout(): Zero-pad the ship layout to add empty space around the ship. 
        - setupSystemLevels(): Create the system and reactor dictionaries which contain the present systems and the reactor informations
        - loadShipAndShieldsSprites(): Load all the relevant ship sprites (Base, Gib, Shields, Zoltanshields, Cloak)
        - createRoomInformation(): Set the room informations from the provided parameters. Creates the dictionaries shipRooms with the room coordinates and shipFields with the field information inside the rooms
        - createRoomObjects(): Create and store room objects for all the rooms on the ship
        - createDoorObjects(): Create and store door objects for all the doors on the ship
        - updateRoomConnectivityAll(): Create or update the matrix of room connections by doors
        - updateRoomConnectivityOpenDoors(): Create or update the matrix of room connected by open doors
        - updateDoorRoomkeys(): Create or update dictionaries connecting rooms with doors and vice versa. Also sets the field spaceDoors
        - updateDoorRects(): Create or update the rects for the doors needed for the door animation control
        - setCurrentMaxShieldSprite(): Set maximal shield strength sprite based on the current power to shields
        - updateRoom(roomKey [int]): Update the activeSprite field for the given room
        - updateDoor(doorKey [str]): Update the activeSprite field for the given door
        - updateOxygen(dt [int]): Update the oxygen in the rooms with a time step of dt given in milliseconds
        
    Auxiliary methods (called internally):
        - setDeltaRectBattleAndIdle(): Set the delta in pixels between idle and battle
        - rectIdle(rect [pygame.Rect]): Move a ship sprite into the correct idle position
        - rectShields(rect [pygame.Rect]): Correct a shield sprite into the correct idle position as they don't have the same size as the hull sprites

    To debug and develop:

        ship = 'Kestrel'
        variant = 'A'

    """
    
    
    ###
    # Initialization
    def __init__(self) -> None:
        logger.debug('Initialize ship base object')


    ###
    # Initial construct of the ship
    def shipSetup(self) -> None:
        logger.debug('Start ship {ship}-{variant} construction'.format(ship = self.ship, variant = self.variant))
        
        ###
        # Set the parameter selector variable
        self.parameterShipSelector = 'PlayerShip' if self.playerShip else 'EnemyShip'
        
        ###
        # Initalize lists and dictionaries
        self.weapons = dict()
        self.augments = list()
        self.activeSprites = dict()
        
        
        ###
        # Set hull points
        self.hullPoints = self.parameters[self.parameterShipSelector][self.ship + self.variant]['HullPoints']
        
        
        ###
        # Transform the ship layout from the initial matrix and save the ship layout
        self.expandLayout()
        self.createDoorMatrixHorizontal()
        self.createDoorMatrixVertical()
        
        
        ###
        # Save the room specifications and clonebay orientation (copy so it can be modified later on)
        self.roomSpecifications = copy.deepcopy(self.parameters[self.parameterShipSelector][self.ship + self.variant]['RoomSpecifitions'])
        self.clonebayOrientation = copy.deepcopy(self.parameters[self.parameterShipSelector][self.ship + self.variant]['ClonebayOrientation'])


        ###
        # Setup the ship system and their levels, set Zoltan shield to zero (has to be added later when dealing with augments)
        self.setupSystemLevels()
        
        
        ###
        # Setup screen related values
        
        # Set the coordinate origin on the canvas for the conversion from room coordinates to pixels
        self.originShipCanvas = copy.deepcopy(self.parameters[self.parameterShipSelector][self.ship]['ShiftOrigin'])
        
        # Set the relative position of the shields to the ship sprite
        self.originShields = copy.deepcopy(self.parameters[self.parameterShipSelector][self.ship]['ShiftShields'])
        
        # Set the pixel delta between idle and battle for the player ship
        if self.playerShip:
            self.setDeltaRectBattleAndIdle()
        
        
        ###
        # Load or define the relevant sprites
        self.loadShipAndShieldsSprites()
        
        
        ###
        # Create the rooms and doors
        
        # Create the rooms
        self.createRoomInformation()
        self.createRoomObjects()
                
        # Create the doors
        self.createDoorObjects()
        self.updateRoomConnectivityAll()
        self.updateRoomConnectivityOpenDoors()
        
        
        ##
        # Process rooms and doors
        
        # Connect rooms and corresponding doors
        self.updateDoorRoomkeys()
        
        # Set the door rects for animation control
        self.updateDoorRects()
        
        
        ###
        # Set the initial shields
        self.setCurrentMaxShieldSprite()
        
        
        ###
        # TO BE PROPERLY INCORPORATED LATER ON
        self.weapons['WeaponSlotsAvailable'] = self.parameters[self.parameterShipSelector][self.ship + self.variant]['WeaponSlotsMax']
    
    
    ###
    # Function to expand the system layout -> Zero padding around the matrix to add empty space
    def expandLayout(self) -> None:
        logger.debug('Expand the ship layout')
        
        # Reference the provided ship layout
        shipLayout = self.parameters[self.parameterShipSelector][self.ship + self.variant]['LayoutMatrix']

        # Expland the layout
        layoutExpanded = np.append(np.zeros((shipLayout.shape[0], 1), dtype = int), shipLayout, axis = 1)
        layoutExpanded = np.append(layoutExpanded, np.zeros((layoutExpanded.shape[0], 1), dtype = int), axis = 1)
        layoutExpanded = np.append(np.zeros((1, layoutExpanded.shape[1]), dtype = int), layoutExpanded, axis = 0)
        layoutExpanded = np.append(layoutExpanded, np.zeros((1, layoutExpanded.shape[1]), dtype = int), axis = 0)        
        
        # Save the expanded layout
        self.layoutExpanded = layoutExpanded


    ###
    # Function to get the horizontal doors in matrix shape
    def createDoorMatrixHorizontal(self) -> None:
        logger.debug('Create the horizontal door matrix')
        
        # Reference the provided horizontal doors
        doorsHorizontal = self.parameters[self.parameterShipSelector][self.ship + self.variant]['DoorsHorizontal']
        
        # Convert the horizontal doors to a matrix
        doorMatrix = np.zeros((self.layoutExpanded.shape[0]-1, self.layoutExpanded.shape[1]), dtype = int)
        for i, j in zip(range(0, self.layoutExpanded.shape[1]), doorsHorizontal):
            if len(j):
                doorMatrix[np.array(j)-1, i] = 1
        
        # Save the horizontal door layout
        self.doorMatrixHorizontal = doorMatrix


    ###
    # Function to get the vertical doors in matrix shape
    def createDoorMatrixVertical(self) -> None:
        logger.debug('Create the vertical door matrix')
        
        # Reference the provided horizontal doors
        doorsVertical = self.parameters[self.parameterShipSelector][self.ship + self.variant]['DoorsVertical']
        
        # Convert the horizontal doors to a matrix        
        doorMatrix = np.zeros((self.layoutExpanded.shape[0], self.layoutExpanded.shape[1]-1), dtype = int)
        for i, j in zip(range(0, self.layoutExpanded.shape[0]), doorsVertical):
            if len(j):
                doorMatrix[i, np.array(j)-1] = 1
                
        # Save the vertical door layout
        self.doorMatrixVertical = doorMatrix


    ###
    # Initialize the present systems and their power
    def setupSystemLevels(self) -> None:
        logger.debug('Setup the present systems with their power levels')
        
        ###
        # Power of a system:
        # PowerMax is the maximum assignable power
        # PowerCurrent is the current power amount
        #
        # PowerBlocked is power blocked by events and unavailable to be assigned
        # PowerCooldown is power blocked by cooldowns, can only be released if the system gets damaged or broken
        # PowerZoltans is power provided by Zoltans in the room [total number of Zoltans in the room, can be bigger than the total number of power]
        # PowerBackup is power coming from the backup battery
        
        ##
        # Initialize the dictionary
        self.systems = dict()

        ##
        # Go through all systems, if they are present, add them to the systems dict
        for i in range(0, len(self.roomSpecifications['System'])):
            if self.roomSpecifications['SystemPresent'][i]:
                # Set up system entry
                system = self.roomSpecifications['System'][i]
                self.systems[system] = dict()
                
                # Fill in systme entries
                self.systems[system]['RoomKey'] = self.roomSpecifications['Position'][i]
                self.systems[system]['PowerMax'] = self.roomSpecifications['PowerMax'][i]
                self.systems[system]['PowerCurrent'] = self.roomSpecifications['PowerCurrent'][i]
                
                # Add additional entries which are always initalized the same way
                self.systems[system]['Manned'] = False
                self.systems[system]['Hacked'] = False

                self.systems[system]['IonCharges'] = 0      # Counter for the ion damage charges
                self.systems[system]['PowerZoltans'] = 0   # Counter for the power bars attributed to Zoltans
                
                self.systems[system]['PowerBlocked'] = 0    # Power blocked by events
                self.systems[system]['PowerBackup'] = 0     # Power provided by the backup battery
                
                self.systems[system]['Damaged'] = 0         # Number of damages energy units
                self.systems[system]['DamageFightOrFire'] = 0   # Damage done by fire or fighting (between 0 and 1)
                self.systems[system]['PowerCooldown'] = 0   # Power blocked by cooldown, should not be able to be taken out by Zoltans
                
                self.systems[system]['Destroyed'] = False   # System destroyed or not
                self.systems[system]['FightingOrFire'] = False   # System destroyed or not
                self.systems[system]['Repairing'] = False   # System destroyed or not
                
                
                self.systems[system]['RepairProgress'] = 0  # Repair progress (between 0 and 1)
                self.systems[system]['IonizedProgress'] = 0 # Cooldown progress for ion damage
                
                # Necessary to draw the rooms
                self.systems[system]['Sprite'] = self.roomSpecifications['Sprite'][i]

        ##
        # Add a set of all present systems (for easier comparison later)
        self.systemsPresent = set(self.systems.keys())

        ##
        # In addition, create a mapping between the present index rooms and the systems
        self.systemsPresentRoomMapping = {self.systems[system]['RoomKey']: system for system in self.systemsPresent}
        self.roomsWithSystems = set(self.systemsPresentRoomMapping.keys())

        ##
        # Set Zoltan shield strength to zero
        self.zoltanShieldPresent = False
        self.zoltanShieldStrength = 0

        ##
        # Set reactor levels
        self.reactor = dict()   # Object which holds all information for the total reactor power
        
        self.reactor['SystemPower'] = self.parameters[self.parameterShipSelector][self.ship + self.variant]['ReactorStart']    # Maximum in system reactor power
        self.reactor['PowerAvailable'] = self.reactor['SystemPower']                                            # Free system power (includes backup battery powers)
        self.reactor['PowerBlocked'] = 0                                                                        # Power blocked by events
        self.reactor['SystemBackupPower'] = 0                                                                   # Maximum power provided by the backup battery
        self.reactor['BackupPowerAvailable'] = 0                                                                # Free backup battery power
        
        # Set initial power levels
        for system in self.systemsPresent:
            if system in self.parameters['General']['MainSystems']:
                self.reactor['PowerAvailable'] -= self.systems[system]['PowerCurrent']
                
                if self.reactor['PowerAvailable'] < 0:
                    raise AssertionError('Initial system configuration uses more power than available for ship {ship}-{variant}'.format(ship = self.ship, variant = self.variant))
                

    ###
    # Set the deltas to change between battle and idle
    def setDeltaRectBattleAndIdle(self) -> None:
        self.deltaBattleToIdle = np.array((self.parameters['General']['PositionOffsetIdle'][0] - self.parameters['General']['PositionOffsetFight'][0], self.parameters['General']['PositionOffsetIdle'][1] - self.parameters['General']['PositionOffsetFight'][1]))
    
    
    ###
    # Load the ship and shields sprite
    def loadShipAndShieldsSprites(self) -> None:
        logger.debug('Load the ship sprites for {ship}-{variant}'.format(ship = self.ship, variant = self.variant))
        
        ##
        # Select the sprite dictionary
        if self.playerShip:
            spriteDictionary = 'PlayerShip'
        else:
            spriteDictionary = 'EnemyShip'
        
        ##
        # Initialize the dictionary containing the ship sprites
        self.shipSprites = dict()
        
        # Base
        self.shipSprites['Base'] = copySprite(self.spritesAll[spriteDictionary].loadedSprites[self.ship + self.variant]['Base'])
        self.rectIdle(self.shipSprites['Base'].rect)
        
        # Gibs
        self.shipSprites['Gib'] = list()
        for gib in range(0, len(self.spritesAll[spriteDictionary].loadedSprites[self.ship + self.variant]['Gib'])):
            self.shipSprites['Gib'].append(copySprite(self.spritesAll[spriteDictionary].loadedSprites[self.ship + self.variant]['Gib'][gib]))
            self.rectIdle(self.shipSprites['Gib'][-1].rect)

        # Shields
        if self.playerShip:
            for level in range(0, self.parameters['General']['ShieldMaxLevel']):
                self.shipSprites['Shield' + str(level+1)] = copySprite(self.spritesAll[spriteDictionary].loadedSprites[self.ship]['ShieldsLevel' + str(level + 1)])
                
                self.rectIdle(self.shipSprites['Shield' + str(level+1)].rect)
                self.rectShields(self.shipSprites['Shield' + str(level+1)].rect)

            # Zoltan shield
            self.shipSprites['ZoltanShield'] = copySprite(self.spritesAll[spriteDictionary].loadedSprites[self.ship]['ZoltanShield'])
            self.rectIdle(self.shipSprites['ZoltanShield'].rect)
            self.rectShields(self.shipSprites['ZoltanShield'].rect)
                
        else:
            for level in range(0, self.parameters['General']['ShieldMaxLevel']):
                self.shipSprites['Shield' + str(level+1)] = copySprite(self.spritesAll[spriteDictionary].loadedSprites['ShieldsLevel' + str(level + 1)])

                # Stretch the shield 
                self.shipSprites['Shield' + str(level+1)].image = pygame.transform.scale(self.shipSprites['Shield' + str(level+1)].image, (np.array(self.shipSprites['Shield' + str(level+1)].rect.size) * self.parameters[self.parameterShipSelector][self.ship + self.variant]['StretchShields']).astype(int))
                self.shipSprites['Shield' + str(level+1)].rect = self.shipSprites['Shield' + str(level+1)].image.get_rect()
                
                self.rectIdle(self.shipSprites['Shield' + str(level+1)].rect)
                self.rectShields(self.shipSprites['Shield' + str(level+1)].rect)

            # Zoltan shield
            self.shipSprites['ZoltanShield'] = copySprite(self.spritesAll[spriteDictionary].loadedSprites['ZoltanShield'])
            self.rectIdle(self.shipSprites['ZoltanShield'].rect)
            self.rectShields(self.shipSprites['ZoltanShield'].rect)
            
        # Cloak
        self.shipSprites['Cloak'] = copySprite(self.spritesAll[spriteDictionary].loadedSprites[self.ship]['Cloak'])
        self.rectIdle(self.shipSprites['Cloak'].rect)


    ###
    # Set the rect properly for idle
    def rectIdle(self, rect: pygame.Rect) -> None:
        if self.playerShip:
            rect.x = self.parameters['General']['PositionOffsetIdle'][0] - rect.w // 2
            rect.y = self.parameters['General']['PositionOffsetIdle'][1] - rect.h // 2
        else:
            rect.x = self.enemyBoxOffset[0] - rect.w // 2 - 5   # Box is not perfectly centered
            rect.y = self.enemyBoxOffset[1] - rect.h // 2    


    ###
    # Correct the shield sprite location
    def rectShields(self, rect: pygame.Rect) -> None:
        rect.topleft += self.originShields
#        rect.x += self.originShields[0]
#        rect.y += self.originShields[1]


    ###
    # Function to set the room informations to be used later on
    def createRoomInformation(self) -> None:
        logger.debug('Set room and field informations')
        
        ##
        # Initialize dictionaries
        self.shipRooms = dict()
        self.shipFields = dict()
        
        # General informations
        roomSize = list()
        roomWidth = list()
        roomHeight = list()
        
        roomSystem = list()
        
        roomOriginCoord = list()
        roomOriginCoordCanvas = list()
        
        roomIndex = list()

        # Room connectivity        
        fieldX = list()
        fieldY = list()
        fieldIndex = list()
        fieldSystem = list()
        fieldAvailable = list()

        # Number of rooms present
        self.shipRooms['nRooms'] = len(np.unique(self.layoutExpanded)) - 1
        presentRooms = np.unique(self.layoutExpanded)
        self.presentRooms = presentRooms[presentRooms != 0]
        
        # Create canvas shifted room coordinates
        self.shiftRoomCoord = np.array([self.shipSprites['Base'].rect.x, self.shipSprites['Base'].rect.y]) + self.originShipCanvas
        
        for i in self.presentRooms:
            roomIndex.append(i)
            
            # Room sizes
            roomSize.append(np.sum(self.layoutExpanded == i))
            roomWidth.append(np.sum(np.sum(self.layoutExpanded == i, axis = 0) != 0))
            roomHeight.append(np.sum(np.sum(self.layoutExpanded == i, axis = 1) != 0))
            
            # System information
            if sum(self.roomSpecifications['Position'] == i):
                roomSystem.append(str(self.roomSpecifications['System'][self.roomSpecifications['Position'] == i][0]))
                
            else:                
                roomSystem.append('')
            
            # Add room coordinates
            roomOriginCoord.append([np.where(np.sum(self.layoutExpanded == i, axis = 0) != 0)[0][0], np.where(np.sum(self.layoutExpanded == i, axis = 1) != 0)[0][0]])
            roomOriginCoordCanvas.append(self.shiftRoomCoord + np.array([roomOriginCoord[-1][0] * self.parameters['General']['RoomHeightPixel'], roomOriginCoord[-1][1] * self.parameters['General']['RoomHeightPixel']]))

            for ix in range(0, roomWidth[-1]):
                for iy in range(0, roomHeight[-1]):
                    fieldX.append(roomOriginCoord[-1][0] + ix)
                    fieldY.append(roomOriginCoord[-1][1] + iy)
                    
                    fieldIndex.append(i)
                    fieldSystem.append(roomSystem[-1])
                    
                    if (roomSystem[-1] == 'Medbay') or (roomSystem[-1] == 'Clonebay'):
                        if (roomSize[-1] > 2) and (ix == self.clonebayOrientation[0]) and (iy == self.clonebayOrientation[1]):   # Don't block the space in 2-room
                            fieldAvailable.append(False)
                        else:
                            fieldAvailable.append(True)
                    else:
                        fieldAvailable.append(True)

        ##
        # Save everything inside the room dictionary
        self.shipRooms['RoomSize'] = roomSize
        self.shipRooms['RoomWidth'] = roomWidth
        self.shipRooms['RoomHeight'] = roomHeight

        self.shipRooms['RoomSystem'] = roomSystem

        self.shipRooms['RoomOriginCoord'] = roomOriginCoord
        self.shipRooms['RoomOriginCoordCanvas'] = roomOriginCoordCanvas

        self.shipRooms['RoomIndex'] = np.array(roomIndex)
        
        # Save everything inside the fields dictionary
        self.shipFields['FieldX'] = fieldX
        self.shipFields['FieldY'] = fieldY
        self.shipFields['FieldIndex'] = fieldIndex
        self.shipFields['FieldSystem'] = fieldSystem
        self.shipFields['FieldAvailable'] = fieldAvailable


    ###
    # Function to create the room objects
    def createRoomObjects(self) -> None:
        logger.debug('Create the room objects')
        
        ##
        # Initialize the dictionary holding the room objects
        self.rooms = dict() 

        if self.playerShip:
            consoleOrientationEnemyShip = None
        else:
            consoleOrientationEnemyShip = self.parameters['EnemyShip'][self.ship + self.variant]['Consoles']
        
        # Add dictionary pointing at the active sprites
        self.activeSprites['Rooms'] = dict()
            
        # Go through all rooms
        for roomIndex in self.presentRooms:
            # Collect the relevant room information
            roomArrayIndex = np.where(self.shipRooms['RoomIndex'] == roomIndex)[0][0]
            
            # Get a copy of the relevant room informations
            relevantSystemInformation = dict()
            for feld in ['RoomSize', 'RoomWidth', 'RoomHeight', 'RoomOriginCoord', 'RoomOriginCoordCanvas']:
                relevantSystemInformation[feld] = self.shipRooms[feld][roomArrayIndex]

            if roomIndex in self.systemsPresentRoomMapping.keys():
                system = self.systemsPresentRoomMapping[roomIndex]
                                                    
                # The playership also gets background sprites for the rooms
                relevantSystemInformation['BackgroundSprite'] = self.playerShip
                if self.playerShip:
                    # Add sprite number
                    relevantSystemInformation['Sprite'] = self.systems[system]['Sprite']
                
            else:
                system = None
            
            # Create room object
            self.rooms[roomIndex] = rooms.room(roomIndex, self.parameters, self.spritesAll, self.doorMatrixHorizontal, self.doorMatrixVertical, self.clonebayOrientation, self.playerShip, consoleOrientationEnemyShip, relevantSystemInformation, system)
            
            
            ##
            # Add the room to the sprites to be drawn
            self.activeSprites['Rooms'][roomIndex] = dict()
            self.activeSprites['Rooms'][roomIndex]['Sprite'] = self.rooms[roomIndex].currentSprite
            self.activeSprites['Rooms'][roomIndex]['Draw'] = True


    ###
    # Function to create the door objects
    def createDoorObjects(self) -> None:
        logger.debug('Create the door objects')

        ##
        # Initialize dictionary
        self.doors = dict()

        # Get initial door level
        if 'DoorSystem' in self.systemsPresent:
            doorLevel = self.systems['DoorSystem']['PowerCurrent'] + self.systems['DoorSystem']['Manned']
        else:
            doorLevel = 0

        # Add dictionary pointing at the active sprites
        self.activeSprites['Doors'] = dict()
        
        # First create all the vertical doors
        vertical = True
        for i in range(0, self.doorMatrixVertical.shape[0]):
            for j in range(0, self.doorMatrixVertical.shape[1]):
                if self.doorMatrixVertical[i,j]:
                    field1 = (j, i)     # x, y
                    field2 = (j+1, i)   # x, y
                    
                    field1Roomkey = self.layoutExpanded[field1[1], field1[0]]
                    field2Roomkey = self.layoutExpanded[field2[1], field2[0]]
                    
                    doorKey = '_'.join(map(str, field1 + field2))
                    
                    # Coordinates of second field
                    canvCoord = self.shiftRoomCoord + np.array(((j + 1) * self.parameters['General']['RoomHeightPixel'], i * self.parameters['General']['RoomHeightPixel']))
                    
                    # Create the door objects                        
                    self.doors[doorKey] = doors.door(doorKey, vertical, self.parameters, field1, field2, field1Roomkey, field2Roomkey, doorLevel, canvCoord)

                    
                    ##
                    # Add the door to the sprites to be drawn
                    self.activeSprites['Doors'][doorKey] = dict()
                    self.activeSprites['Doors'][doorKey]['Sprite'] = self.doors[doorKey].currentSprite
                    self.activeSprites['Doors'][doorKey]['Draw'] = True 
                    
        
        # Then create all the horizontal doors
        vertical = False
        for i in range(0, self.doorMatrixHorizontal.shape[0]):
            for j in range(0, self.doorMatrixHorizontal.shape[1]):
                if self.doorMatrixHorizontal[i,j]:
                    field1 = (j, i)     # x, y
                    field2 = (j, i+1)   # x, y
                    
                    field1Roomkey = self.layoutExpanded[field1[1], field1[0]]
                    field2Roomkey = self.layoutExpanded[field2[1], field2[0]]
                    
                    doorKey = '_'.join(map(str, field1 + field2))
                    
                    # Coordinates of second field
                    canvCoord = self.shiftRoomCoord + np.array([j * self.parameters['General']['RoomHeightPixel'], (i + 1) * self.parameters['General']['RoomHeightPixel']])
        
                    # Create the door objects
                    self.doors[doorKey] = doors.door(doorKey, vertical, self.parameters, field1, field2, field1Roomkey, field2Roomkey, doorLevel, canvCoord)


                    ##
                    # Add the door to the sprites to be drawn
                    self.activeSprites['Doors'][doorKey] = dict()
                    self.activeSprites['Doors'][doorKey]['Sprite'] = self.doors[doorKey].currentSprite
                    self.activeSprites['Doors'][doorKey]['Draw'] = True
        
        
        # Get the unique doorkeys
        self.presentDoors = np.unique(list(self.doors.keys()))


    ###
    # Function to create/update an array of all avaiable room connections
    def updateRoomConnectivityAll(self) -> None:
        logger.debug('Update room connectivity')
        
        roomConnections = list()
        for door in self.doors.keys():
            roomConnections.append([min(self.doors[door].field1Roomkey, self.doors[door].field2Roomkey), max(self.doors[door].field1Roomkey, self.doors[door].field2Roomkey)])
        
        self.roomConnections = np.unique([tuple(row) for row in roomConnections], axis = 0)
        

    ###
    # Function to create/update an array of all open room connections
    def updateRoomConnectivityOpenDoors(self) -> None:
        logger.debug('Update open room connectivity')

        roomConnectionsOpen = list()
        for door in self.doors.keys():
            if self.doors[door].currentPosition:
                roomConnectionsOpen.append([min(self.doors[door].field1Roomkey, self.doors[door].field2Roomkey), max(self.doors[door].field1Roomkey, self.doors[door].field2Roomkey)])
        
        if len(roomConnectionsOpen):
            self.roomConnectionsOpen = np.unique([tuple(row) for row in roomConnectionsOpen], axis = 0)
        else:
            self.roomConnectionsOpen = None    


    ###
    # Function which connects the rooms with the corresponding door keys
    def updateDoorRoomkeys(self) -> None:
        logger.debug('Update connections between rooms and doors')
        
        self.doorRooms = dict()
        spaceDoors = list()
        for doorKey in self.doors.keys():
            self.doorRooms[doorKey] = (self.doors[doorKey].field1Roomkey, self.doors[doorKey].field2Roomkey)
            if self.doors[doorKey].space:
                spaceDoors.append(doorKey)
        
        self.spaceDoors = set(spaceDoors)
        
        self.roomDoors = dict()
        for roomKey in self.rooms.keys():
            roomDoors = list()
            for doorKey in self.doorRooms.keys():
                if roomKey in self.doorRooms[doorKey]:
                    roomDoors.append(doorKey)
            
            self.roomDoors[roomKey] = tuple(roomDoors)


    ###
    # Function to get the doors rects into one matrix for the door opening/closing per mouse events
    def updateDoorRects(self) -> None:
        logger.debug('Update door rects for animation control')
        
        # Get the rects as x, y, w, h
        doorRectList = list()
        doorKeyListForRect = list()
        for doorKey in self.doors.keys():
            doorRectList.append(list(self.doors[doorKey].currentSprite.rect))
            doorKeyListForRect.append(doorKey)
        
        # Save the fields
        self.doorRectMatrix = np.array(doorRectList)
        self.doorKeysForRects = np.array(doorKeyListForRect)
        
        # Change the rects to the format for the mouse checks 
        self.doorRectForSelection = copy.deepcopy(self.doorRectMatrix)
        
        self.doorRectForSelection[:,2] = -(self.doorRectForSelection[:,0] + self.doorRectForSelection[:,2] - 1)
        self.doorRectForSelection[:,3] = -(self.doorRectForSelection[:,1] + self.doorRectForSelection[:,3] - 1)        



    ###
    # Shield select function
    def setCurrentMaxShieldSprite(self) -> None:
        logger.debug('Select the current shield sprite')
        
        # Calculate number of shield layers
        if 'Shields' in self.systemsPresent:
            self.currentMaxShieldStrength = self.systems['Shields']['PowerCurrent'] // 2
        else:
            self.currentMaxShieldStrength = 0
        
        # Remove the old setting
        if 'Shields' in self.activeSprites.keys():
            del self.activeSprites['Shields']
                    
        # Select the corresponding sprite
        if self.currentMaxShieldStrength:
            self.activeSprites['Shields'] = dict()
            
            self.activeSprites['Shields']['Sprite'] = self.shipSprites['Shield' + str(self.currentMaxShieldStrength)]
            self.activeSprites['Shields']['Draw'] = True    # Set to redraw completely
        else:
            self.activeSprites['Shields'] = None


    ###
    # Update a room do be drawn
    def updateRoom(self, roomKey: int) -> None:
        # Update room
        self.activeSprites['Rooms'][roomKey]['Sprite'] = self.rooms[roomKey].currentSprite
        self.activeSprites['Rooms'][roomKey]['Draw'] = True
        
        # Update neighboring doors
        for doorKey in self.roomDoors[roomKey]:
            self.activeSprites['Doors'][doorKey]['Draw'] = True
            self.activeSprites['Doors'][doorKey]['Sprite'] = self.doors[doorKey].currentSprite
            
    
    ###
    # Update a door to be drawn
    def updateDoor(self, doorKey):
        # Update door
        self.activeSprites['Doors'][doorKey]['Draw'] = True
        self.activeSprites['Doors'][doorKey]['Sprite'] = self.doors[doorKey].currentSprite
        
        # Update neighboring rooms
        for roomKey in self.doorRooms[doorKey]:
            if roomKey: # Don't update space
                self.activeSprites['Rooms'][roomKey]['Sprite'] = self.rooms[roomKey].currentSprite
                self.activeSprites['Rooms'][roomKey]['Draw'] = True
                
                # Also update all the doors in that room, otherwise those doors will be overdrawn
                for secondaryDoorKey in self.roomDoors[roomKey]:
                    self.activeSprites['Doors'][secondaryDoorKey]['Draw'] = True
                    self.activeSprites['Doors'][secondaryDoorKey]['Sprite'] = self.doors[secondaryDoorKey].currentSprite    


    ###
    # Function to update the oxygen in the rooms, dt is the time update step in milliseconds
    def updateOxygen(self, dt: int) -> None:
        allRoomKeys = list(self.presentRooms)
        
        # Get list of old oxygen values, list of rooms with space
        oxygenOld = dict()
        oxygenRoomConnected = dict()
        
        for roomKey in allRoomKeys:
            oxygenOld[roomKey] = self.rooms[roomKey].oxygen
            
            if self.roomConnectionsOpen is not None:
                selectionRooms = self.roomConnectionsOpen[np.any(self.roomConnectionsOpen == roomKey, axis = 1),]
                if selectionRooms.shape[0]:
                    oxygenRoomConnected[roomKey] = list(selectionRooms[selectionRooms != roomKey])
                
                else:
                    oxygenRoomConnected[roomKey] = list()
            else:
                oxygenRoomConnected[roomKey] = list()
        
        # Create new list of oxygen values
        if 'Oxygen' in self.systems.keys():
            oxygenLevel = self.systems['Oxygen']['PowerCurrent']
        else:
            oxygenLevel = 0
            
        oxygenNew = dict()
        for roomKey in allRoomKeys:
            newValue = oxygenOld[roomKey] + (oxygenLevel * self.parameters['General']['OxygenLevel1'] - self.parameters['General']['OxygenLossGeneral']) * dt / 1000
            
            for roomKeyAdjacent in oxygenRoomConnected[roomKey]:
                if roomKeyAdjacent:
                    newValue += min(max((oxygenOld[roomKeyAdjacent] - oxygenOld[roomKey]) * 15, -30), 30) * self.parameters['General']['OxygenEquilibriumSpeed'] * dt / 1000
                else:   # Space door
                    newValue -= self.parameters['General']['OxygenLossSpace'] * dt / 1000
            
            # Limits
            newValue = max(min(newValue, 100), 0)
            
            oxygenNew[roomKey] = newValue
        
        # Set the new values and check if the room needs to be redrawn
        for roomKey in allRoomKeys:
            self.rooms[roomKey].oxygen = oxygenNew[roomKey]
            
            if (oxygenOld[roomKey] // 5) != (oxygenNew[roomKey] // 5):  # If the room needs to be updated
                self.rooms[roomKey].selectSprite()
                self.updateRoom(roomKey)  


    ###
    # Add damage to a room/system
    def damageToRoom(self, roomKey: int, damageSystem: int, damageHull: int) -> None:
        logger.info('{damageSystem}, {damageHull} points of system/hull damage for ship {ship} is applied to room {roomKey} {system}'.format(damageSystem = str(damageSystem), damageHull = str(damageHull), ship = 'player ship' if self.playerShip else 'enemy ship', roomKey = str(roomKey), system = self.systemsPresentRoomMapping[roomKey] if roomKey in self.roomsWithSystems else ''))
        
        ###
        # Apply damage to hull
        self.hullPoints -= damageHull
        
        if self.hullPoints <= 0:
            logger.warning('Ship destruction not implemented yet')
        
        
        ###
        # Apply system damage if applicable
        if roomKey in self.roomsWithSystems:
            raise NotImplementedError
    
    
    ###
    # Try to add power to a system. newPower will be used when adding weapons or drones
    def addSystemPower(self, system: str, newPower: [None, int] = None) -> None:
        logger.debug('Try to add power to system {}'.format(system))
        
        ###
        # Check how much power can/shall be added
        
        # Default
        powerNecessary = 0
        
        # Differentiate between systems
        if system in ['WeaponControl', 'DroneControl']:
            logger.warning('Adding system power for system {} not implemented yet'.format(system))
        
        elif system == 'Shields':
            # Determine at first whether and how much energy can be added
            if not self.systems[system]['Destroyed'] and self.systems[system]['IonCharges'] == 0:
                if self.systems[system]['PowerCurrent'] < (self.systems[system]['PowerMax'] - self.systems[system]['Damaged']):
                    # Power not maxed out
                    if self.systems[system]['PowerCurrent'] % 2:
                        # Odd number of energy assigned
                        powerNecessary = 1
                    
                    elif (self.systems[system]['PowerMax'] - self.systems[system]['Damaged'] - self.systems[system]['PowerCurrent']) >= 2:
                        # Even number of energy assigned and 2 levels assignable
                        powerNecessary = 2
                        
                    else:
                        logger.debug('System {} needs 2 assignable energy slots')
                                    
                else:
                    logger.debug('System {} power already maxed out'.format(system))
            else:
                logger.debug('System {} is destroyed or ionized'.format(system))
        
        else:
            # Determine at first whether energy can be added
            if not self.systems[system]['Destroyed'] and self.systems[system]['IonCharges'] == 0:
                if self.systems[system]['PowerCurrent'] < (self.systems[system]['PowerMax'] - self.systems[system]['Damaged']):
                    powerNecessary = 1

                else:
                    logger.debug('System {} power already maxed out'.format(system))
            else:
                logger.debug('System {} is destroyed or ionized'.format(system))
        
        
        ###
        # Check if the power is available
        if powerNecessary:
            if self.reactor['PowerAvailable'] >= powerNecessary:
                # Separate between normal and backup power
                powerFromBackupBattery = min(self.reactor['BackupPowerAvailable'], powerNecessary)
                powerFromReactor = powerNecessary - powerFromBackupBattery
                
                # Substract the power from the reactor/backup battery
                self.reactor['PowerAvailable'] -= powerFromReactor
                self.reactor['BackupPowerAvailable'] -= powerFromBackupBattery
                
                # Add the power to the system
                self.systems[system]['PowerCurrent'] += powerNecessary
                self.systems[system]['PowerBackup'] += powerFromBackupBattery                
                
            else:
                logger.debug('Not enough reactor power to add energy to system {}'.format(system))
            
    
    ###
    # Try to remove power from a system
    def removeSystemPower(self, system: str, newPower: [None, int] = None) -> None:
        logger.debug('Try to remove power from system {}'.format(system))
        
        ###
        # Check whether power can be removed
        powerToBeRemoved = 0
        
        # Differentiate between systems
        if system in ['WeaponControl', 'DroneControl']:
            logger.warning('Removing system power for system {} not implemented yet'.format(system))

        elif system == 'Shields':
            # Check if there is power to be removed
            if not self.systems[system]['Destroyed'] and self.systems[system]['IonCharges'] == 0:
                if self.systems[system]['PowerCurrent'] > self.systems[system]['PowerZoltans']:
                    if self.systems[system]['PowerCurrent'] % 2:
                        powerToBeRemoved = 1
                    else:
                        powerToBeRemoved = min(self.systems[system]['PowerCurrent'] - self.systems[system]['PowerZoltans'], 2)
                        
                else:
                    logger.debug('System {} has no removable power'.format(system))
            else:
                logger.debug('System {} is destroyed or ionized'.format(system))

        else:
            # Check if there is power to be removed
            if not self.systems[system]['Destroyed'] and self.systems[system]['IonCharges'] == 0:
                if self.systems[system]['PowerCurrent'] > self.systems[system]['PowerZoltans']:
                    powerToBeRemoved = 1
                        
                else:
                    logger.debug('System {} has no removable power'.format(system))
            else:
                logger.debug('System {} is destroyed or ionized'.format(system))
            

        ###
        # Remove power if applicable
        if powerToBeRemoved:
            # Check whether power from the backup battery has to removed
            powerToBackupBattery = min(self.systems[system]['PowerBackup'], powerToBeRemoved)
            powerToReactor = powerToBeRemoved - powerToBackupBattery
            
            # Substract the power from the system
            self.systems[system]['PowerCurrent'] -= powerToBeRemoved
            self.systems[system]['PowerBackup'] -= powerToBackupBattery
            
            # Add the power to the reactor
            self.reactor['PowerAvailable'] += powerToReactor
            self.reactor['BackupPowerAvailable'] += powerToBackupBattery


























