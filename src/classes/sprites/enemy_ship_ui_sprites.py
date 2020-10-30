###
#
# Define a class which contains the sprites for the enemy ship ui
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# Pygame
import pygame


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the enemy ship ui elements
class enemyShipUiSprites(object):
    """
    
    Load the sprites for the enemy ship ui.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - boxSprites [Dict]: Dictionary containing all the loaded box sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadBoxes(parameters [Dict]): Imports all the enemy ui box sprites and stores them in the dictionary self.boxSprites
        
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the enemy ship ui images')
        
        ###
        # Initialize dictionary
        self.boxSprites = dict()

        ###
        # Load the sprites
        self.loadBoxes(parameters)
    
    
    ##
    # Function to load the enemy box
    def loadBoxes(self, parameters: Dict) -> None:
        logger.debug('Import the enemy UI boxes')
        
        # Load the various sprites
        for image in ['BoxEnemy', 'BoxEnemyMask', 'BoxBoss', 'BoxBossMask']:
            self.boxSprites[image] = pygame.sprite.Sprite()
            self.boxSprites[image].image = pygame.image.load('{basepath}{image}.png'.format(basepath = parameters['EnemyShipUi']['Box']['Basepath'], image = parameters['EnemyShipUi']['Box'][image])).convert_alpha()
            self.boxSprites[image].rect = self.boxSprites[image].image.get_rect()
            
            # Set rects
            self.boxSprites[image].rect.x = parameters['General']['DisplayWidth'] - self.boxSprites[image].rect.w + parameters['General']['OffsetEnemyBox'][0]
            self.boxSprites[image].rect.y = parameters['General']['OffsetEnemyBox'][1]
            
            # Mask image
            if 'Mask' in image:
                # Change color from black to white
                pixelImage = pygame.surfarray.pixels3d(self.boxSprites[image].image)
                pixelImage[:] = 255 # Set to white
                
                del pixelImage
                
                # Also create a full background to draw on
                self.boxSprites[image + 'Draw'] = pygame.sprite.Sprite()

                self.boxSprites[image + 'Draw'].image = pygame.Surface(self.boxSprites[image].rect.size, pygame.SRCALPHA)
                self.boxSprites[image + 'Draw'].image.fill(parameters['Colors']['White'])
                self.boxSprites[image + 'Draw'].image.set_colorkey(parameters['Colors']['White'])
                
                self.boxSprites[image + 'Draw'].image = self.boxSprites[image + 'Draw'].image.convert_alpha()
                
                self.boxSprites[image + 'Draw'].rect = self.boxSprites[image].rect
    
    
    ##
    # Function to return the rect information
    def rectFromBattleBox(self, box: str) -> pygame.Rect:
        return(self.boxSprites[box].rect)
        



