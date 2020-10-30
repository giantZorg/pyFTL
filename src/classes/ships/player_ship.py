###
#
# Define a class for the player ship based on the class for all ships
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# Arrays and matrices
#import numpy as np

# Pygame
import pygame


###
# Load ressources
import src.classes.ships.base_ship as baseShip


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the player ship
class playerShip(baseShip.baseShip):
    """
    
    Class for the player ship. After initialization, variables can still be set.
    After this, the ship will be finally constructed using the inherited shipSetup() method.
    
    Initialization:
        - parameters [Dict]: All loaded parameters
        - spritesAll [Dict]: All loaded sprites
        - ship [str]: Selected ship
        - variant [str]: Selected ship variant
        
    
    Fields:
        - parameters: Reference to all parameters
        - spritesAll: Reference to the loaded sprites
        
        - ship: Ship selection
        - variant: Ship variant selection
        
        - playerShip: Logical to differentiate between the player and the enemy ship
        - battle: Logical to indicate whether the ship is in battle or not
    
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict, spritesAll: Dict, ship: str = 'Kestrel', variant: str = 'A') -> None:
        logger.debug('Initialize the player ship object')
        
        ###
        # Save parameters and sprites
        self.parameters = parameters
        self.spritesAll = spritesAll
        
        ###
        # Ship selection
        self.ship = ship
        self.variant = variant
        
        ###
        # Distinct player and enemy ship
        self.playerShip = True
        
        ###
        # Initialize as not in battle
        self.battle = False
                
        
    ###
    # Method to move all sprites to battle positions
    def moveRectsForBattle(self, toBattle: bool) -> None:
        logger.debug('Change all player ship rects to {} positions'.format('battle' if toBattle else 'idle'))
        
        ###
        # Set the movefactor
        moveFactor = -1 if toBattle else 1
        
        
        ###
        # Move sprites in the shipSprites dictionary
        for spriteOrList in self.shipSprites.values():
            # Separate by type
            if type(spriteOrList) == list:
                for sprite in spriteOrList:
                    sprite.rect.topleft += self.deltaBattleToIdle * moveFactor
            elif type(spriteOrList) == pygame.sprite.Sprite:
                spriteOrList.rect.topleft += self.deltaBattleToIdle * moveFactor
            else:
                raise AssertionError('Element in sprite container is not a sprite')
        
        
        ###
        # Move rooms
        for roomKey in self.presentRooms:
            self.rooms[roomKey].moveRoomRects(self.deltaBattleToIdle * moveFactor)
        
        
        ###
        # Move doors
        for doorKey in self.presentDoors:
            self.doors[doorKey].moveDoorRects(self.deltaBattleToIdle * moveFactor)


        ###
        # Update the rect positions
        self.updateDoorRects()













