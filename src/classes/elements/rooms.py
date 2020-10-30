###
#
# Define a base class used for all the rooms.
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# Arrays and matrices
import numpy as np

# Pygame
import pygame


###
# Import ressources
from src.misc.helperfunctions import colorInterpolation


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the room class
class room(object):
    """
    
    Object which controls and returns the sprites for a given room. The active sprite is always found in the field currentSprite.
    
    Fields:
        - system [str]: System present in the room, '' if no room is present
        - visible [bool]: Logical if the room is visible or not
        - roomKey [int]: Roomkey as assigned in the layout parameters
        
        - status [int]: Status of the system in the room: 0: Normal, 1: Damaged, 2: Destroyed, 3: Ionized. Hacked is treated separately
        - oxygen [float]: Amount of oxygen in the room, inside the interval [0, 100]. Crew takes damage below an oxygen level of 5
        - hacked [bool]: Logical indicating whether the room is hacked
        
        - currentSprite [pygame.sprite.Sprite]: Current sprite which should be drawn onto the screen
        
        - parameters [Dict]: Reference to all parameters
        
        - playerShip [bool]: Logical indicating whether the room is on the player or enemy ship
        - consoleOrientationEnemyShip [np.array, None]: Orientation of consoles on enemy ships
        - relevantSystemInformation [Dict]: Dictionary containing the relevant information necessary to draw the room
        
    
    Methods:
        - selectSprite(): Selects the currently valid sprite and copies it into the field currentSprite
        - moveRoomRects(delta [np.array]): Move all saved room sprites by the specified pixel amount. Updates the currentSprite afterwards
        
    
    """
    
    
    ###
    # Initialization
    def __init__(self, roomKey: int, parameters: Dict, spritesAll: Dict, doorMatrixHorizontal: np.ndarray, doorMatrixVertical: np.ndarray, clonebayOrientation: np.ndarray, playerShip: bool, consoleOrientationEnemyShip: [None, Dict], relevantSystemInformation: Dict, system: [str, None] = None, visible: bool = True, oxygen: float = 100, hacked: bool = False) -> None:
        logger.debug('Initialize room {}'.format(str(roomKey)))
        
        ###
        # Set values        
        self.system = system
        self.visible = visible
        self.roomKey = roomKey

        # Initialize rooms as normal with full oxygen
        self.status = 0     # 0: Normal, 1: Damaged, 2: Destroyed, 3: Ionized
        self.oxygen = oxygen
        self.hacked = False

        # Save for updates
        self.parameters = parameters
        self.playerShip = playerShip
        self.consoleOrientationEnemyShip = consoleOrientationEnemyShip  # Needed for enemy ships
        self.relevantSystemInformation = relevantSystemInformation

        # Prepare empty sprites
        self.sprites = dict()
        for visible in [True, False]:
            self.sprites[visible] = dict()
            for status in [0, 1, 2, 3]:
                if visible:
                    self.sprites[visible][status] = dict()
                    for oxygenRounded in range(0, 21):
                        self.sprites[visible][status][oxygenRounded] = pygame.sprite.Sprite()
                else:
                    self.sprites[visible][status] = pygame.sprite.Sprite()
        
        self.currentSprite = pygame.sprite.Sprite()

        # Create all the sprites
        self.drawAllRooms(spritesAll, doorMatrixHorizontal, doorMatrixVertical, clonebayOrientation)
        self.addConsole(spritesAll)
        
        # Set current sprite
        self.selectSprite()


    ###
    # Function to mpve all room rects by a given pixel amount
    def moveRoomRects(self, delta: np.ndarray) -> None:
        logger.debug('Move room {roomKey} by x = {x}, y = {y} pixels'.format(roomKey = str(self.roomKey), x = str(delta[0]), y = str(delta[1])))
        
        # Move all room sprites
        for visible in [True, False]:
            for status in [0, 1, 2, 3]:
                if visible:
                    for oxygenRounded in range(0, 21):
                        self.sprites[visible][status][oxygenRounded].rect.topleft += delta 
                else:
                    self.sprites[visible][status].rect.topleft += delta

        # Reset current sprite
        self.selectSprite()
        
    
    ###
    # Function to set the current sprite based on the rooms condition
    def selectSprite(self) -> None:        
        if self.visible:
            self.currentSprite.image = self.sprites[self.visible][self.status][int(self.oxygen) // 5].image.copy()
            self.currentSprite.rect = self.sprites[self.visible][self.status][int(self.oxygen) // 5].rect
        else:
            self.currentSprite.image = self.sprites[self.visible][self.status].image.copy()
            self.currentSprite.rect = self.sprites[self.visible][self.status].rect
            
        # Add the console glow
        self.drawConsole()
        
    
    ###
    # Function to draw all the rooms initially
    # Draw the rooms
    def drawAllRooms(self, spritesAll: Dict, doorMatrixHorizontal: np.ndarray, doorMatrixVertical: np.ndarray, clonebayOrientation: np.ndarray):
        # Define dict for color selection based on status
        colorSelection = dict()
        colorSelection[0] = 'OverlayGrey'
        colorSelection[1] = 'OverlayOrange'
        colorSelection[2] = 'OverlayRed'
        colorSelection[3] = 'OverlayBlue'
        
        surfaceRoomLines = pygame.Surface([self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
        surfaceRoomLines.fill(self.parameters['Colors']['White'])
        surfaceRoomLines.set_colorkey(self.parameters['Colors']['White'])
        surfaceRoomLines.set_alpha(100)

        # Add room lines
        for ix in range(0, self.relevantSystemInformation['RoomWidth'] - 1):
            pygame.draw.rect(surfaceRoomLines, self.parameters['Colors']['Grey1'], [(ix + 1) * self.parameters['General']['RoomHeightPixel'] - 1, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])

        for iy in range(0, self.relevantSystemInformation['RoomHeight'] - 1):
            pygame.draw.rect(surfaceRoomLines, self.parameters['Colors']['Grey1'], [0, (iy + 1) * self.parameters['General']['RoomHeightPixel'] - 1, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])
        
        for visible in [True, False]:
            for status in [0, 1, 2, 3]:
                if visible:
                    for oxygenRounded in range(0, 21):
                        oxyColor = colorInterpolation(self.parameters['Colors']['GreyRoom'], self.parameters['Colors']['PinkRoom'], oxygenRounded / 20)
                        
                        # Prepare Sprite
                        self.sprites[visible][status][oxygenRounded].image = pygame.Surface([self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                        self.sprites[visible][status][oxygenRounded].image.fill(oxyColor)
                        self.sprites[visible][status][oxygenRounded].image.set_colorkey(self.parameters['Colors']['White'])
                            
                        
                        # Rect
                        self.sprites[visible][status][oxygenRounded].rect = self.sprites[visible][status][oxygenRounded].image.get_rect()
                        
                        # Set rect on Canvas
                        self.sprites[visible][status][oxygenRounded].rect.x = self.relevantSystemInformation['RoomOriginCoordCanvas'][0]
                        self.sprites[visible][status][oxygenRounded].rect.y = self.relevantSystemInformation['RoomOriginCoordCanvas'][1]
                    

                        if oxygenRounded == 0:
                            # Add no oxygen stripes
                            
                            # Draw all lines
                            for ix in range(0, self.relevantSystemInformation['RoomWidth']):
                                for iy in range(0, self.relevantSystemInformation['RoomHeight']):
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(ix * self.parameters['General']['RoomHeightPixel'], 27 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (7 + ix * self.parameters['General']['RoomHeightPixel'], 34 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (ix * self.parameters['General']['RoomHeightPixel'], 34 + iy * self.parameters['General']['RoomHeightPixel'])
                                                        ])
    
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(ix * self.parameters['General']['RoomHeightPixel'], 9 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (25 + ix * self.parameters['General']['RoomHeightPixel'], 34 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (17 + ix * self.parameters['General']['RoomHeightPixel'], 34 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (ix * self.parameters['General']['RoomHeightPixel'], 17 + iy * self.parameters['General']['RoomHeightPixel'])                                                         
                                                         ])

                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(ix * self.parameters['General']['RoomHeightPixel'], iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (34 + ix * self.parameters['General']['RoomHeightPixel'], 34 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (34 + ix * self.parameters['General']['RoomHeightPixel'], 26 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (8 + ix * self.parameters['General']['RoomHeightPixel'], iy * self.parameters['General']['RoomHeightPixel'])                                                         
                                                         ])

                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(18 + ix * self.parameters['General']['RoomHeightPixel'], iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (34 + ix * self.parameters['General']['RoomHeightPixel'], 16 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (34 + ix * self.parameters['General']['RoomHeightPixel'], 8 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (26 + ix * self.parameters['General']['RoomHeightPixel'], iy * self.parameters['General']['RoomHeightPixel'])                                                         
                                                         ])
    
                        # Roomlines
                        self.sprites[visible][status][oxygenRounded].image.blit(surfaceRoomLines, [0,0])

                        
                        # Add room sprites (only for player ship)                        
                        if self.playerShip:
                            if self.system is not None and self.relevantSystemInformation['BackgroundSprite']:
                                if self.system == 'Clonebay':
                                    # First the clonebay background sprite, then the rest
                                    self.sprites[visible][status][oxygenRounded].image.blit(pygame.transform.rotate(spritesAll['GeneralShip'].roomSprites[self.system]['Room'][0].image, 360 - (clonebayOrientation[2] - 1) * 90), [clonebayOrientation[0] * self.parameters['General']['RoomHeightPixel'], clonebayOrientation[1] * self.parameters['General']['RoomHeightPixel']])
                                    self.sprites[visible][status][oxygenRounded].image.blit(pygame.transform.rotate(spritesAll['GeneralShip'].roomSprites[self.system]['Room'][1].image, 360 - (clonebayOrientation[2] - 1) * 90), [clonebayOrientation[0] * self.parameters['General']['RoomHeightPixel'], clonebayOrientation[1] * self.parameters['General']['RoomHeightPixel']])
                            
                                elif self.system == 'CrewTeleporter':
                                    for ix in range(0, self.relevantSystemInformation['RoomWidth']):
                                        for iy in range(0, self.relevantSystemInformation['RoomHeight']):
                                            self.sprites[visible][status][oxygenRounded].image.blit(spritesAll['GeneralShip'].roomSprites[self.system]['Room'].image, [ix * self.parameters['General']['RoomHeightPixel'] + (self.parameters['General']['RoomHeightPixel'] - 24) // 2, iy * self.parameters['General']['RoomHeightPixel'] + (self.parameters['General']['RoomHeightPixel'] - 23) // 2])
    
                                else:
                                    self.sprites[visible][status][oxygenRounded].image.blit(spritesAll['GeneralShip'].roomSprites[self.system]['Room' + str(self.relevantSystemInformation['RoomSize'])][self.relevantSystemInformation['Sprite']].image, [0, 0])
                        
                        # Draw the system sprite
                        if self.system is not None:
                            if self.system == 'Artillery':
                                self.sprites[visible][status][oxygenRounded].image.blit(spritesAll['GeneralShip'].symbolSprites['Artillery'][colorSelection[status]].image, [2 + ((self.relevantSystemInformation['RoomWidth'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2, 2 + ((self.relevantSystemInformation['RoomHeight'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2])
                            else:
                                self.sprites[visible][status][oxygenRounded].image.blit(spritesAll['GeneralShip'].symbolSprites[self.system][colorSelection[status]].image, [2 + ((self.relevantSystemInformation['RoomWidth'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2, 2 + ((self.relevantSystemInformation['RoomHeight'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2])
                        
                        # Draw the walls
                        pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['Black'], [0, 0, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])
                        pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['Black'], [0, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                        pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['Black'], [self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                        pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['Black'], [0, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])
                        
                        # Check for doors, if true then remove the walls for that section
                        for iy in range(0, self.relevantSystemInformation['RoomHeight']):
                            # Left room doors
                            if doorMatrixVertical[self.relevantSystemInformation['RoomOriginCoord'][1] + iy, self.relevantSystemInformation['RoomOriginCoord'][0] - 1]:
                                pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, oxyColor, [0, self.parameters['General']['RoomHeightPixel'] * iy + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3])

                                if oxygenRounded == 0:
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(0, 9 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (1, 10 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (1, 18 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (0, 17 + iy * self.parameters['General']['RoomHeightPixel'])                                                         
                                                         ])
                                
                            # Right room doors
                            if doorMatrixVertical[self.relevantSystemInformation['RoomOriginCoord'][1] + iy, self.relevantSystemInformation['RoomOriginCoord'][0] - 1 + self.relevantSystemInformation['RoomWidth']]:
                                pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, oxyColor, [self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, self.parameters['General']['RoomHeightPixel'] * iy + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3])

                                if oxygenRounded == 0:
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, 15 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 1, 16 + iy * self.parameters['General']['RoomHeightPixel']), 
                                                         (self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 1, 8 + iy * self.parameters['General']['RoomHeightPixel']),
                                                         (self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, 7 + iy * self.parameters['General']['RoomHeightPixel'])                                                         
                                                         ])
                                    
                        for ix in range(0, self.relevantSystemInformation['RoomWidth']):
                            # Upper room doors
                            if doorMatrixHorizontal[self.relevantSystemInformation['RoomOriginCoord'][1] - 1, self.relevantSystemInformation['RoomOriginCoord'][0] + ix]:
                                pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, oxyColor, [self.parameters['General']['RoomHeightPixel'] * ix + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 0, 2 * self.parameters['General']['DoorHeightPixel'] + 3, 2])

                                if oxygenRounded == 0:
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(18 + ix * self.parameters['General']['RoomHeightPixel'], 0), 
                                                         (19 + ix * self.parameters['General']['RoomHeightPixel'], 1), 
                                                         (27 + ix * self.parameters['General']['RoomHeightPixel'], 1),
                                                         (26 + ix * self.parameters['General']['RoomHeightPixel'], 0)                                                         
                                                         ])
                            # Lower room doors
                            if doorMatrixHorizontal[self.relevantSystemInformation['RoomOriginCoord'][1] - 1 + self.relevantSystemInformation['RoomHeight'], self.relevantSystemInformation['RoomOriginCoord'][0] + ix]:
                                pygame.draw.rect(self.sprites[visible][status][oxygenRounded].image, oxyColor, [self.parameters['General']['RoomHeightPixel'] * ix + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3, 2])

                                if oxygenRounded == 0:
                                    pygame.draw.polygon(self.sprites[visible][status][oxygenRounded].image, self.parameters['Colors']['RedRoomNoOxygen'], 
                                                        [(24 + ix * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2), 
                                                         (25 + ix * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 1), 
                                                         (17 + ix * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 1),
                                                         (16 + ix * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2)                                                         
                                                         ])
                
                else:   # Invisible
                    self.sprites[visible][status].image = pygame.Surface([self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                    self.sprites[visible][status].image.fill(self.parameters['Colors']['Grey2'])
                    self.sprites[visible][status].image.set_colorkey(self.parameters['Colors']['White'])

                    # Rect
                    self.sprites[visible][status].rect = self.sprites[visible][status].image.get_rect()
                    
                    # Set rect on Canvas
                    self.sprites[visible][status].rect.x = self.relevantSystemInformation['RoomOriginCoordCanvas'][0]
                    self.sprites[visible][status].rect.y = self.relevantSystemInformation['RoomOriginCoordCanvas'][1]
                    
                    # Add room lines
                    for ix in range(0, self.relevantSystemInformation['RoomWidth'] - 1):
                        pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Grey1'], [(ix + 1) * self.parameters['General']['RoomHeightPixel'] - 1, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
        
                    for iy in range(0, self.relevantSystemInformation['RoomHeight'] - 1):
                        pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Grey1'], [0, (iy + 1) * self.parameters['General']['RoomHeightPixel'] - 1, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])

                    # Draw the system sprite
                    if self.system is not None and self.relevantSystemInformation['BackgroundSprite']:
                        if self.system == 'Artillery':
                            self.sprites[visible][status].image.blit(spritesAll['GeneralShip'].symbolSprites['Artillery'][colorSelection[status]].image, [2 + ((self.relevantSystemInformation['RoomWidth'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2, 2 + ((self.relevantSystemInformation['RoomHeight'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2])
                        else:
                            self.sprites[visible][status].image.blit(spritesAll['GeneralShip'].symbolSprites[self.system][colorSelection[status]].image, [2 + ((self.relevantSystemInformation['RoomWidth'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2, 2 + ((self.relevantSystemInformation['RoomHeight'] - 1) * self.parameters['General']['RoomHeightPixel']) // 2])

                    # Draw the walls
                    pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Black'], [0, 0, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])
                    pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Black'], [0, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                    pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Black'], [self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, 0, 2, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel']])
                    pygame.draw.rect(self.sprites[visible][status].image, self.parameters['Colors']['Black'], [0, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2, self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'], 2])

                    # Check for doors, if true then remove the walls for that section
                    for iy in range(0, self.relevantSystemInformation['RoomHeight']):
                        # Left room doors
                        if doorMatrixVertical[self.relevantSystemInformation['RoomOriginCoord'][1] + iy, self.relevantSystemInformation['RoomOriginCoord'][0] - 1]:
                            pygame.draw.rect(self.sprites[visible][status].image, oxyColor, [0, self.parameters['General']['RoomHeightPixel'] * iy + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3])
                            
                        # Right room doors
                        if doorMatrixVertical[self.relevantSystemInformation['RoomOriginCoord'][1] + iy, self.relevantSystemInformation['RoomOriginCoord'][0] - 1 + self.relevantSystemInformation['RoomWidth']]:
                            pygame.draw.rect(self.sprites[visible][status].image, oxyColor, [self.relevantSystemInformation['RoomWidth'] * self.parameters['General']['RoomHeightPixel'] - 2, self.parameters['General']['RoomHeightPixel'] * iy + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3])
                    
                    for ix in range(0, self.relevantSystemInformation['RoomWidth']):
                        # Upper room doors
                        if doorMatrixHorizontal[self.relevantSystemInformation['RoomOriginCoord'][1] - 1, self.relevantSystemInformation['RoomOriginCoord'][0] + ix]:
                            pygame.draw.rect(self.sprites[visible][status].image, oxyColor, [self.parameters['General']['RoomHeightPixel'] * ix + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, 0, 2 * self.parameters['General']['DoorHeightPixel'] + 3, 2])

                        # Lower room doors
                        if doorMatrixHorizontal[self.relevantSystemInformation['RoomOriginCoord'][1] - 1 + self.relevantSystemInformation['RoomHeight'], self.relevantSystemInformation['RoomOriginCoord'][0] + ix]:
                            pygame.draw.rect(self.sprites[visible][status].image, oxyColor, [self.parameters['General']['RoomHeightPixel'] * ix + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1, self.relevantSystemInformation['RoomHeight'] * self.parameters['General']['RoomHeightPixel'] - 2, 2 * self.parameters['General']['DoorHeightPixel'] + 3, 2])


    ###
    # Function to add consoles if applicable
    def addConsole(self, spritesAll):
        # Will need to add an if self.playerShip: clause to draw the bare console for enemy ships
        
        if self.system is not None:
            if self.playerShip: # Player ship
                if self.system in self.parameters['GeneralShipSprites']['RoomSprites']['Informations'].keys():
                    if ('Console' + str(self.relevantSystemInformation['RoomSize'])) in self.parameters['GeneralShipSprites']['RoomSprites']['Informations'][self.system].keys():
                        self.console = True
                        self.consolePosition = self.parameters['GeneralShipSprites']['RoomSprites']['Informations'][self.system]['Console' + str(self.relevantSystemInformation['RoomSize'])][self.relevantSystemInformation['Sprite']]
                        
                        # Console initially unmanned
                        self.consoleManned = False
                        
                        # Differentiate between main systems and subsystems
                        self.crewLevel = 0  # 0: Blue console, 1: Green console, 2: Gold console. Only changable for main systems
                        if self.system in self.parameters['General']['SystemWithConsolePercentageBonus']:
                            self.consoleWithLevels = True
                            
                            if self.system == 'Piloting':
                                self.consoleSprites = spritesAll['GeneralShip'].consoleSprites['ConsolePilot'].copy()
                                self.consoleAdjust = {1: [], 2: [], 3: [], 4: [19, 9]}   # Only tested with 4 as the only one present
    
                            else:
                                self.consoleSprites = spritesAll['GeneralShip'].consoleSprites['ConsoleSystems'].copy()
                                self.consoleAdjust = {1: [-1, 1], 2: [-1, 2], 3: [-2, -2], 4: []}   # 4 not tested yet, to be checked with another ship!
    
                        else:
                            self.consoleWithLevels = False
                        
                    else:
                        self.console = False
                else:
                    self.console = False
                    
            else:   # Enemy ship
                if (self.roomKey in self.consoleOrientationEnemyShip['Rooms']):
                    indexConsole = np.where(np.array(self.consoleOrientationEnemyShip['Rooms']) == self.roomKey)[0][0]
                    
                    self.console = True
                    self.consolePosition = [self.consoleOrientationEnemyShip['X'][indexConsole], self.consoleOrientationEnemyShip['Y'][indexConsole], self.consoleOrientationEnemyShip['Orientation'][indexConsole]]

                    # Console initially unmanned
                    self.consoleManned = False
                    
                    # Save the console sprite
                    self.consoleBaseSprite = pygame.sprite.Sprite()
                    self.consoleBaseSprite.image = spritesAll['GeneralShip'].consoleSprites['Console'].image.copy()
                    self.consoleBaseSprite.rect = spritesAll['GeneralShip'].consoleSprites['Console'].rect.copy()
                    
                    # Enemy ship always gets the same console
                    self.crewLevel = 0  # 0: Blue console, 1: Green console, 2: Gold console. Only changable for main systems
                    if self.system in self.parameters['General']['SystemWithConsolePercentageBonus']:
                        self.consoleWithLevels = True
                        self.consoleSprites = spritesAll['GeneralShip'].consoleSprites['ConsoleSystems'].copy()
                        self.consoleAdjust = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0]}   # 4 not tested yet, to be checked with another ship!

                    else:
                        self.consoleWithLevels = False
                    
                else:
                    self.console = False

        else:   # No system present
            self.console = False


    ###
    # Add the console glow and the console itself for enemy ships
    def drawConsole(self) -> None:
        if self.console:
            if not self.playerShip: # Console needs to be added
                self.currentSprite.image.blit(pygame.transform.rotate(self.consoleBaseSprite.image, 180 - (self.consolePosition[2] - 1) * 90), [self.consolePosition[0] * self.parameters['General']['RoomHeightPixel'], self.consolePosition[1] * self.parameters['General']['RoomHeightPixel']])
            
            if self.consoleWithLevels and (self.status == 0):  # Only these consoles get colors
                if (self.status == 0) and not self.hacked:
                    self.currentSprite.image.blit(pygame.transform.rotate(self.consoleSprites[self.crewLevel].image, 180 - (self.consolePosition[2] - 1) * 90), [self.consolePosition[0] * self.parameters['General']['RoomHeightPixel'] + self.consoleAdjust[self.consolePosition[2]][0], self.consolePosition[1] * self.parameters['General']['RoomHeightPixel'] + self.consoleAdjust[self.consolePosition[2]][1]])
                else:
                    self.currentSprite.image.blit(pygame.transform.rotate(self.consoleSprites[0].image, 180 - (self.consolePosition[2] - 1) * 90), [self.consolePosition[0] * self.parameters['General']['RoomHeightPixel'] + self.consoleAdjust[self.consolePosition[2]][0], self.consolePosition[1] * self.parameters['General']['RoomHeightPixel'] + self.consoleAdjust[self.consolePosition[2]][1]])
                            
    