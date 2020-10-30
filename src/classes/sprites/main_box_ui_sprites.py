###
#
# Define a class which contains the sprites for the main text boxes
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

## Arrays
#import numpy as np

# Pygame
import pygame


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the enemy ship images
class mainBoxUiSprites(object):
    """
    
    Load the sprites specific to the main text boxes.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - loadedSprites [Dict]: Dictionary containing all the loaded sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadMainBoxUiSprites(parameters [Dict]): Imports all the enemy ship sprites and stores them in the dictionary self.loadedSprites
    
    """
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the main box ui images')
        
        ###
        # Initialize dictionary
        self.loadedSprites = dict()
        
        ###
        # Load sprites for the player ships
        self.loadMainBoxUiSprites(parameters)
    
    
    ###
    # Funtion to read in all the sprites as defined in the parameters parameters['EnemyShip']
    def loadMainBoxUiSprites(self, parameters: Dict) -> None:
        logger.debug('Import the main box ui sprites')
    
        ##
        # ALways the same picture format
        pictureFormat = '.png'
        
        
        ##
        # Load pause images
        for spriteName in ['GeneralPause1', 'GeneralPause2']:
            self.loadedSprites[spriteName] = pygame.sprite.Sprite()
            self.loadedSprites[spriteName].image = pygame.image.load('{base}{path}{pictureFormat}'.format(base = parameters['MainBoxUi']['Pause']['Basepath'], path = parameters['MainBoxUi']['Pause'][spriteName], pictureFormat = pictureFormat)).convert_alpha()
            self.loadedSprites[spriteName].rect = self.loadedSprites[spriteName].image.get_rect()
                    
























