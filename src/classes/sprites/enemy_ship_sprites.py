###
#
# Define a class which contains the sprites for the enemy ships
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

# Pygame
import pygame


###
# Import ressources
from src.misc.helperfunctions import copySprite


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the enemy ship images
class enemyShipSprites(object):
    """
    
    Load the sprites specific to the enemy ships. These include shields (also Zoltan-shields), cloak, hull, gib-sprites.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - loadedSprites [Dict]: Dictionary containing all the loaded sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadEnemyShipSprites(parameters [Dict]): Imports all the enemy ship sprites and stores them in the dictionary self.loadedSprites
    
    """


    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the enemy ship images')
        
        ###
        # Initialize dictionary
        self.loadedSprites = dict()
        
        ###
        # Load sprites for the player ships
        self.loadEnemyShipSprites(parameters)


    ###
    # Funtion to read in all the sprites as defined in the parameters parameters['EnemyShip']
    def loadEnemyShipSprites(self, parameters: Dict) -> None:
        logger.debug('Import the enemy ship sprites')
        
        ##
        # ALways the same picture format
        pictureFormat = 'png'
        
        # Load shields
        self.loadedSprites['Shields'] = pygame.sprite.Sprite()
        self.loadedSprites['Shields'].image = pygame.image.load(parameters['EnemyShip']['ShieldPath']).convert_alpha()
        self.loadedSprites['Shields'].rect = self.loadedSprites['Shields'].image.get_rect()
        
        ##
        # Go through all the avaiable ships
        for ship in parameters['EnemyShip']['ShipsAvailable']:
            self.loadedSprites[ship] = dict()
            
            # Load cloaking
            self.loadedSprites[ship]['Cloak'] = pygame.sprite.Sprite()
            self.loadedSprites[ship]['Cloak'].image = pygame.image.load(parameters['EnemyShip'][ship]['Cloak']).convert_alpha()
            self.loadedSprites[ship]['Cloak'].rect = self.loadedSprites[ship]['Cloak'].image.get_rect()
            
            # Load base sprite
            self.loadedSprites[ship]['Base'] = pygame.sprite.Sprite()
            self.loadedSprites[ship]['Base'].image = pygame.image.load('{basepath}_{baseSprite}.{pictureFormat}'.format(basepath = parameters['EnemyShip'][ship]['Basepath'], baseSprite = parameters['EnemyShip'][ship]['BaseSprite'], pictureFormat = pictureFormat)).convert_alpha()
            self.loadedSprites[ship]['Base'].rect = self.loadedSprites[ship]['Base'].image.get_rect()
            
            # Load gib sprites
            self.loadedSprites[ship]['Gib'] = list()
            for gibStr in parameters['EnemyShip'][ship]['GibSprites']:
                self.loadedSprites[ship]['Gib'].append(pygame.sprite.Sprite())
                self.loadedSprites[ship]['Gib'][-1].image = pygame.image.load('{basepath}_{gibStr}.{pictureFormat}'.format(basepath = parameters['EnemyShip'][ship]['Basepath'], gibStr = gibStr, pictureFormat = pictureFormat)).convert_alpha()
                self.loadedSprites[ship]['Gib'][-1].rect = self.loadedSprites[ship]['Gib'][-1].image.get_rect()
            
            
        ##
        # Create the different shield levels as well as Zoltan shields
        self.loadedSprites['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])] = copySprite(self.loadedSprites['Shields'])

        # For the alpha-multiplication
        alphaImg = pygame.Surface(self.loadedSprites['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect.size, pygame.SRCALPHA)
        alphaImg.fill((255, 255, 255, parameters['General']['ShieldMultAlpha']))

        for level in reversed(range(1, parameters['General']['ShieldMaxLevel'])):
            self.loadedSprites['ShieldsLevel' + str(level)] = pygame.sprite.Sprite()
            
            # Sprites aufhellen
            self.loadedSprites['ShieldsLevel' + str(level)].image = self.loadedSprites['ShieldsLevel' + str(level + 1)].image.copy()
            self.loadedSprites['ShieldsLevel' + str(level)].image.blit(alphaImg, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            self.loadedSprites['ShieldsLevel' + str(level)].rect = self.loadedSprites['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect

        # Generate the Zoltan shield
        self.loadedSprites['ZoltanShield'] = pygame.sprite.Sprite()
        self.loadedSprites['ZoltanShield'].image = self.loadedSprites['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].image.copy()
        self.loadedSprites['ZoltanShield'].rect = self.loadedSprites['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect

        # Swap blue and green and adapt the colors
        pixelImage = pygame.surfarray.pixels3d(self.loadedSprites['ZoltanShield'].image)
        blueOld = pixelImage[:,:,2].copy()
        greenOld = pixelImage[:,:,1].copy()
        pixelImage[:,:,0] = np.round(pixelImage[:,:,0] / 1.1).astype(int)
        pixelImage[:,:,1] = np.round(blueOld / 1.1).astype(int)
        pixelImage[:,:,2] = np.round(greenOld / 1.8).astype(int)
        
        del pixelImage




















    