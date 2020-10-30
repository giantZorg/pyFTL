###
#
# Define a base class used for all the doors.
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict, Tuple

# Arrays and matrices
import numpy as np

# Pygame
import pygame


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the room class
class door(object):
    """
    
    Object which controls and returns the sprites for a given door. The active sprite is always found in the field currentSprite.
    
    """
    
    ###
    # Initialize
    def __init__(self, doorKey: str, vertical: bool, parameters: Dict, field1: Tuple, field2: Tuple, field1Roomkey: int, field2Roomkey: int, level: int, canvCoord: np.ndarray, hacked: bool = False, currentPosition: int = 0, bashed: bool = False):
        logger.debug('Initialize door {}'.format(doorKey))
        
        ##
        # Save parameters
        self.doorKey = doorKey
        self.parameters = parameters
        
        # Vertical or horizontal
        self.vertical = vertical
        
        # Position of first field in the layoutExpanded matrix (more upperleft)
        self.field1 = field1
        self.field1Roomkey = field1Roomkey

        # Position of second field in the layoutExpanded matrix (more lowerright)
        self.field2 = field2
        self.field2Roomkey = field2Roomkey

        # Further parameters
        self.hacked = hacked
        self.currentPosition = currentPosition
        self.level = level
        
        self.bashed = bashed    # Not used yet
        self.userOpened = False
                
        # Check if door is connected to space
        if (self.field1Roomkey == 0) or (self.field2Roomkey == 0):
            self.space = True
        else:
            self.space = False    

        # Maximum/Minimum position
        self.minimumPixel = 0   # Door closed
        self.maximumPixel = self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel']    # Door fully opened
        
        # Create dict for the sprites
        self.sprites = dict()
        
        # Create empty sprites
        for level in range(0, 5):   # Level of doors
            self.sprites[level] = dict()
            for position in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 1): # How far is the door retracted
                self.sprites[level][position] = pygame.sprite.Sprite()
        
        # Add for hacked doors
        self.sprites['Hacked'] = dict()
        for position in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 1): # How far is the door retracted
            self.sprites['Hacked'][position] = pygame.sprite.Sprite()
            
        # Initialize active sprite
        self.currentSprite = pygame.sprite.Sprite()
        
        # Create all the sprites
        self.drawAllDoors(canvCoord)
        
        # Set the first sprite
        self.selectSprite()


    ###
    # Function to set the current sprite based on the rooms condition
    def selectSprite(self) -> None:
        if self.hacked:
            self.currentSprite.image = self.sprites['Hacked'][self.currentPosition].image.copy()
            self.currentSprite.rect = self.sprites['Hacked'][self.currentPosition].rect
        else:
            self.currentSprite.image = self.sprites[self.level][self.currentPosition].image.copy()
            self.currentSprite.rect = self.sprites[self.level][self.currentPosition].rect
        

    ###
    # Function to change all room rects
    def moveDoorRects(self, delta: np.ndarray) -> None:
        logger.debug('Move door {doorKey} by x = {x}, y = {y} pixels'.format(doorKey = str(self.doorKey), x = str(delta[0]), y = str(delta[1])))
        for level in range(0, 5):   # Level of doors
            for position in range(0, self.maximumPixel + 1): # How far is the door retracted
                self.sprites[level][position].rect.topleft += delta
        
        for position in range(0, self.maximumPixel + 1):
            self.sprites['Hacked'][position].rect.topleft += delta
    
    
    ###    
    # Initial drawing of all the sprites
    def drawAllDoors(self, canvCoord: np.ndarray):
        # For each level of doors
        for level in range(0, 5):   # Level of doors
            for position in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 1): # How for is the door retracted
                if self.vertical:
                    self.sprites[level][position].image = pygame.Surface([6, 2 * self.parameters['General']['DoorHeightPixel'] + 3])
                else:
                    self.sprites[level][position].image = pygame.Surface([2 * self.parameters['General']['DoorHeightPixel'] + 3, 6])

                self.sprites[level][position].image.fill(self.parameters['Colors']['White'])
                self.sprites[level][position].image.set_colorkey(self.parameters['Colors']['White'])
                
                # Create the door wings
                if self.vertical:
                    if level <= 1:  # Two wings
                        # Upper wing
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, 4, self.parameters['General']['DoorHeightPixel'] - position])
        
                        # Lower wing
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, self.parameters['General']['DoorHeightPixel'] + 1 + position, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, self.parameters['General']['DoorHeightPixel'] + 2 + position, 4, self.parameters['General']['DoorHeightPixel'] - position])
                    
                    else: 
                        if position:    # Opened doors
                            # Upper wing
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, 4, self.parameters['General']['DoorHeightPixel'] - position])
                            
                            # Lower wing
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, self.parameters['General']['DoorHeightPixel'] + 1 + position, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, self.parameters['General']['DoorHeightPixel'] + 2 + position, 4, self.parameters['General']['DoorHeightPixel'] - position])

                            # Add the bars
                            if level == 3:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] - position + 1):
                                    if (i+3)%4 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 1 + i, 4, 1])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 4, 1])
                                        
                            elif level == 4:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] - position + 1):
                                    if (i+1)%2 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 1 + i, 4, 1])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 4, 1])

                        else:
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, 6, 2 * self.parameters['General']['DoorHeightPixel'] + 3])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, 4, 2 * self.parameters['General']['DoorHeightPixel'] + 1])

                            # Add the bars
                            if level == 3:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 2):
                                    if (i+3)%4 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 1 + i, 4, 1])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 4, 1])
                                        
                            elif level == 4:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 2):
                                    if (i+1)%2 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 1 + i, 4, 1])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1, 2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 4, 1])
                            

                    
                    # Set rect on canvas
                    self.sprites[level][position].rect = self.sprites[level][position].image.get_rect()
                    
                    self.sprites[level][position].rect.x = canvCoord[0] - 3
                    self.sprites[level][position].rect.y = canvCoord[1] + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1
                
                # Horizontal doors
                else:
                    if level <= 1:  # Two wings
                        # Left wing
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])
        
                        # Right wing
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [self.parameters['General']['DoorHeightPixel'] + 1 + position, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [self.parameters['General']['DoorHeightPixel'] + 2 + position, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])

                    else: 
                        if position:    # Opened doors
                            # Left wing
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])
                            
                            # Right wing
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [self.parameters['General']['DoorHeightPixel'] + 1 + position, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [self.parameters['General']['DoorHeightPixel'] + 2 + position, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])

                            # Add the bars
                            if level == 3:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] - position + 1):
                                    if (i+3)%4 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1 + i, 1, 1, 4])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 1, 1, 4])
                                        
                            elif level == 4:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] - position + 1):
                                    if (i+1)%2 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1 + i, 1, 1, 4])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 1, 1, 4])

                        else:
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['Black'], [0, 0, 2 * self.parameters['General']['DoorHeightPixel'] + 3, 6])
                            pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorLevel' + str(level)], [1, 1, 2 * self.parameters['General']['DoorHeightPixel'] + 1, 4])
                            
                            # Add the bars
                            if level == 3:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 2):
                                    if (i+3)%4 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1 + i, 1, 1, 4])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 1, 1, 4])
                                        
                            elif level == 4:
                                for i in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 2):
                                    if (i+1)%2 == 0:
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [1 + i, 1, 1, 4])
                                        pygame.draw.rect(self.sprites[level][position].image, self.parameters['Colors']['DoorGreyOverlay'], [2 * self.parameters['General']['DoorHeightPixel'] + 1 - i, 1, 1, 4])
                                        
                            
                    # Set rect on canvas
                    self.sprites[level][position].rect = self.sprites[level][position].image.get_rect()
                    
                    self.sprites[level][position].rect.x = canvCoord[0] + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1
                    self.sprites[level][position].rect.y = canvCoord[1] - 3
                                        

        # Create the hacked doors
        for position in range(0, self.parameters['General']['DoorHeightPixel'] - self.parameters['General']['DoorMinimumPixel'] + 1): # How far is the door retracted
            if self.vertical:
                self.sprites['Hacked'][position].image = pygame.Surface([6, 2 * self.parameters['General']['DoorHeightPixel'] + 3])
            else:
                self.sprites['Hacked'][position].image = pygame.Surface([2 * self.parameters['General']['DoorHeightPixel'] + 3, 6])

            self.sprites['Hacked'][position].image.fill(self.parameters['Colors']['White'])
            self.sprites['Hacked'][position].image.set_colorkey(self.parameters['Colors']['White'])
            
            # Create the door wings
            if self.vertical:
                # Upper wing
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['Black'], [0, 0, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['DoorHacked'], [1, 1, 4, self.parameters['General']['DoorHeightPixel'] - position])

                # Lower wing
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['Black'], [0, self.parameters['General']['DoorHeightPixel'] + 1 + position, 6, self.parameters['General']['DoorHeightPixel'] + 2 - position])
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['DoorHacked'], [1, self.parameters['General']['DoorHeightPixel'] + 2 + position, 4, self.parameters['General']['DoorHeightPixel'] - position])
            
                # Set rect on canvas
                self.sprites['Hacked'][position].rect = self.sprites['Hacked'][position].image.get_rect()
                
                self.sprites['Hacked'][position].rect.x = canvCoord[0] - 3
                self.sprites['Hacked'][position].rect.y = canvCoord[1] + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1
            
            else:
                # Left wing
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['Black'], [0, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['DoorHacked'], [1, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])

                # Right wing
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['Black'], [self.parameters['General']['DoorHeightPixel'] + 1 + position, 0, self.parameters['General']['DoorHeightPixel'] + 2 - position, 6])
                pygame.draw.rect(self.sprites['Hacked'][position].image, self.parameters['Colors']['DoorHacked'], [self.parameters['General']['DoorHeightPixel'] + 2 + position, 1, self.parameters['General']['DoorHeightPixel'] - position, 4])

                # Set rect on canvas
                self.sprites['Hacked'][position].rect = self.sprites[level][position].image.get_rect()
                
                self.sprites['Hacked'][position].rect.x = canvCoord[0] + self.parameters['General']['RoomHeightPixel'] // 2 - self.parameters['General']['DoorHeightPixel'] - 1
                self.sprites['Hacked'][position].rect.y = canvCoord[1] - 3

    
    
    
    
    
    