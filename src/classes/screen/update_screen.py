###
#
# Define a class which draws everything onto the screen that is necessary
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
# Load ressources

# Background images
import src.classes.setup.background_images as backgroundImages

# Ships
import src.classes.ships.player_ship as playerShip

# Energy management ui
import src.classes.screen.energy_management_ui as energyManagementUi

# Helperfunctions
from src.misc.helperfunctions import copySprite


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the screen update class
class updateScreen(object):
    """
    
    Object which takes all the active sprites to be drawn and draws them onto the screen.
    All objects come with a draw [bool] attribute, which could be used to not always draw everything onto the screen, but this is not implemented yet. This would increase the drawing speed if it turnes out to be too slow.
    
    Fields:
        - screen [pygame.Surface]: Active pygame window
        - allBackgroundImages [backgroundImages]: Object holding the loaded background images
        - spritesAll [Dict]: Dictionary containing the loaded sprites. Necessary for the enemy ui boxes
        
        - activePlayerShip [playerShip]: Active player ship
        - activeEnemyShip [, None]: Active enemy ship, None if no enemy ship is active
        
        - orderDrawingPlayerShip [List]: Order in which the individual elements for the player ship are to be drawn
        - orderDrawingEnemyShip [List]: Order in which the individual elements for the enemy ship are to be drawn
    
    Methods:
        - selectBackgroundImage(): Select a new random background image
        - getUpdateSpriteCollection(): Returns an OrderedUpdates collection of all sprites to be drawn
    
    
    """
    
    
    ###
    # Initialization
    def __init__(self, screen: pygame.Surface, allBackgroundImages: backgroundImages, activePlayerShip: playerShip, activeEnemyShip: [None], spritesAll: Dict, parameters: Dict) -> None:
        logger.debug('Initialize the screen update object')
        
        ###
        # Save object references
        self.screen = screen
        self.allBackgroundImages = allBackgroundImages
        self.spritesAll = spritesAll
        self.parameters = parameters
        
        self.activePlayerShip = activePlayerShip
        self.activeEnemyShip = activeEnemyShip

        # Order, in which elements shall be drawn [Background is not mentioned explicitly but comes first]
        self.orderDrawingPlayerShip = ['Shield', 'ZoltanShield', 'ShipHull', 'ShipRooms', 'ShipDoors']
        self.orderDrawingEnemyShip = ['Shield', 'ZoltanShield', 'ShipHull', 'ShipRooms', 'ShipDoors']
        
        # Select an initial background
        self.selectBackgroundImage()
        
        # Set the energy management ui
        self.energyManagementUi = energyManagementUi.energyManagementUi(self.parameters, self.spritesAll, self.activePlayerShip)
        
        # Set the pause textboxes
        self.setPauseUiElements()
    
    
    ###
    # Set the fix screen ui elements like pause and text fields
    def setPauseUiElements(self) -> None:
        logger.debug('Setup main box ui elements')
        
        ###
        # Initialize objects
        self.sprites = dict()
        
        for field in ['Pause']:
            self.sprites[field] = dict()
        
        # Selector variables
        self.pause = 0
        
        
        ###
        # Pause elements
        for pauseElement in ['GeneralPause1', 'GeneralPause2']:
            self.sprites['Pause'][pauseElement] = copySprite(self.spritesAll['MainBoxUi'].loadedSprites[pauseElement])
            self.sprites['Pause'][pauseElement].rect.center = self.screen.get_rect().center
            self.sprites['Pause'][pauseElement].rect.y = self.parameters['General']['PauseOffsetY']
    
    
    ###
    # Select a background image
    def selectBackgroundImage(self):
        logger.debug('Select a new background image')
        
        # Remove first if present
        if 'currentBackground' in dir(self):
            del self.currentBackground
        
        # Add a new background picture        
        self.currentBackground = self.allBackgroundImages.getRandomBackgroundImage()
        
        
    ###
    # Function to select the current sprites and to draw them onto the screen
    def drawScreen(self, redrawEnergyUi: bool = False) -> None:
        ###
        # Get the collection of sprites to be drawn
        drawSpriteGroup = self.getUpdateSpriteCollection(redrawEnergyUi)
        
        
        ###
        # Draw onto the screen
        if len(drawSpriteGroup):
            pygame.display.update(drawSpriteGroup.draw(self.screen))
        
        
        ###
        # Delete the collection object not to have lingering sprite objects accumulating in the background
        drawSpriteGroup.empty()
        del drawSpriteGroup
    
    
    ###
    # Function to collect all the active sprites and add them to an OrderedUpdate-Collection
    def getUpdateSpriteCollection(self, redrawEnergyUi: bool = False) -> pygame.sprite.OrderedUpdates:
#        logger.debug('Collect all active sprites for drawing')
        
        ###
        # Initialize the output object
        drawSpriteGroup = pygame.sprite.OrderedUpdates()
        
        
#        ###
#        # Add the background image
#        if newImage:
#            # Set the background
        drawSpriteGroup.add(self.currentBackground)
#        else:
#            # Detect which sprites have to be drawn
#            drawSelection = dict()
#            
#            ###
#            # Go through the active sprites. If they should be drawn, check for them what has to be redrawn
            
            
            
        
        ###
        # Go through all the various sprites which have to be drawn for the player ship
        for field in self.orderDrawingPlayerShip:
            ##
            # Handle the various options
            
            # Shields
            if field == 'Shield':
                if self.activePlayerShip.activeSprites['Shields'] is not None:  # Shield is present
                    drawSpriteGroup.add(self.activePlayerShip.activeSprites['Shields']['Sprite'])
                
            # Hull
            elif field == 'ShipHull':
                drawSpriteGroup.add(self.activePlayerShip.shipSprites['Base'])
            
            # Rooms
            elif field == 'ShipRooms':
                for roomKey in self.activePlayerShip.activeSprites['Rooms'].keys():
                    drawSpriteGroup.add(self.activePlayerShip.activeSprites['Rooms'][roomKey]['Sprite'])
            
            # Doors
            elif field == 'ShipDoors':
                for doorKey in self.activePlayerShip.activeSprites['Doors'].keys():
                    drawSpriteGroup.add(self.activePlayerShip.activeSprites['Doors'][doorKey]['Sprite'])


        ###
        # Go through all the various sprites which have to be drawn for the player ship
        if self.activeEnemyShip is not None:
            ###
            # At first, add the battle box UI
            # Then blit all images onto the box mask so the outer parts all become invisible
            # In the end, add the mask with all images blitted onto to the collection
            
            
            ###
            # Add the outer overlay
            drawSpriteGroup.add(self.spritesAll['EnemyUi'].boxSprites[self.activeEnemyShip.enemyBoxType])
            
            
            ###
            # Create the inner box to be drawn onto
            enemyBoxMaskToBeDrawnOnto = copySprite(self.spritesAll['EnemyUi'].boxSprites[self.activeEnemyShip.enemyBoxType + 'MaskDraw'])
            
            
            ###
            # Go through all the various sprites which have to be drawn for the enemy ship
            enemyBoxRectTopleft = np.array(enemyBoxMaskToBeDrawnOnto.rect.topleft)
            for field in self.orderDrawingEnemyShip:
                ##
                # Handle the various options
                
                # Shields
                if field == 'Shield':
                    if self.activeEnemyShip.activeSprites['Shields'] is not None:  # Shield is present
                        enemyBoxMaskToBeDrawnOnto.image.blit(self.activeEnemyShip.activeSprites['Shields']['Sprite'].image, np.array(self.activeEnemyShip.activeSprites['Shields']['Sprite'].rect.topleft) - enemyBoxRectTopleft)
                
                # Hull
                elif field == 'ShipHull':
                    enemyBoxMaskToBeDrawnOnto.image.blit(self.activeEnemyShip.shipSprites['Base'].image, np.array(self.activeEnemyShip.shipSprites['Base'].rect.topleft) - enemyBoxRectTopleft)
                
                # Rooms
                elif field == 'ShipRooms':
                    for roomKey in self.activeEnemyShip.activeSprites['Rooms'].keys():
                        enemyBoxMaskToBeDrawnOnto.image.blit(self.activeEnemyShip.activeSprites['Rooms'][roomKey]['Sprite'].image, np.array(self.activeEnemyShip.activeSprites['Rooms'][roomKey]['Sprite'].rect.topleft) - enemyBoxRectTopleft)

                # Doors
                elif field == 'ShipDoors':
                    for doorKey in self.activeEnemyShip.activeSprites['Doors'].keys():
                        enemyBoxMaskToBeDrawnOnto.image.blit(self.activeEnemyShip.activeSprites['Doors'][doorKey]['Sprite'].image, np.array(self.activeEnemyShip.activeSprites['Doors'][doorKey]['Sprite'].rect.topleft) - enemyBoxRectTopleft)
                    
            
            ###
            # Postprocessing
            
            ##
            # Convert to per-pixel alpha
            enemyBoxMaskToBeDrawnOnto.image = enemyBoxMaskToBeDrawnOnto.image.convert_alpha()
            
            ##
            # Apply mask
            enemyBoxMaskToBeDrawnOnto.image.blit(self.spritesAll['EnemyUi'].boxSprites[self.activeEnemyShip.enemyBoxType + 'Mask'].image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            ##
            # Add to the collection of sprites to be drawn
            drawSpriteGroup.add(enemyBoxMaskToBeDrawnOnto)
        
        
        ###
        # Add the energy ui elements
        if redrawEnergyUi:
            self.energyManagementUi.updateScreenSprites(self.screen.get_rect(), redrawEnergyUi)
            
        for sprite in self.energyManagementUi.uiSprites:
            drawSpriteGroup.add(sprite)
            
        
        ###
        # Add pause if necessary
        if self.pause:
            drawSpriteGroup.add(self.sprites['Pause']['GeneralPause' + str(self.pause)])
        
        
        ###
        # Return the collected sprites
        return(drawSpriteGroup)



























    