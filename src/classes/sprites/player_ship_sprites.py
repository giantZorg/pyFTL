###
#
# Define a class which contains the sprites for the player ships
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
# Define the class for the player ship images
class playerShipSprites(object):
    """
    
    Load the sprites specific to the player ships. These include shields (also Zoltan-shields), cloak, hull, gib-sprites.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - loadedSprites [Dict]: Dictionary containing all the loaded sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadPlayerShipSprites(parameters [Dict]): Imports all the player ship sprites and stores them in the dictionary self.loadedSprites
    
    """
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the player ship images')
        
        ###
        # Initalize dictionary for the loaded sprites
        self.loadedSprites = dict()
        
        ###
        # Load sprites for the player ships
        self.loadPlayerShipSprites(parameters)
    
    
    ###
    # Funtion to read in all the sprites as defined in the parameters parameters['PlayerShip']
    def loadPlayerShipSprites(self, parameters: Dict) -> None:
        logger.debug('Import the player ship sprites')
        
        ###
        # The image format is always png
        pictureFormat = 'png'

        for ship in parameters['PlayerShip']['ShipsAvailable']:
            ###
            # Initialize dictionary
            self.loadedSprites[ship] = dict()
            
            ###
            # Load sprites present for all variants
            
            # Load shields
            self.loadedSprites[ship]['Shields'] = pygame.sprite.Sprite()
            self.loadedSprites[ship]['Shields'].image = pygame.image.load('{basepath}_{shieldspath}.{pictureFormat}'.format(basepath = parameters['PlayerShip'][ship]['Basepath'], shieldspath = parameters['PlayerShip'][ship]['Shields'], pictureFormat = pictureFormat)).convert_alpha()
            self.loadedSprites[ship]['Shields'].rect = self.loadedSprites[ship]['Shields'].image.get_rect()
            
            # Load cloaking
            self.loadedSprites[ship]['Cloak'] = pygame.sprite.Sprite()
            self.loadedSprites[ship]['Cloak'].image = pygame.image.load('{basepath}_{cloakpath}.{pictureFormat}'.format(basepath = parameters['PlayerShip'][ship]['Basepath'], cloakpath = parameters['PlayerShip'][ship]['Cloak'], pictureFormat = pictureFormat)).convert_alpha()
            self.loadedSprites[ship]['Cloak'].rect = self.loadedSprites[ship]['Cloak'].image.get_rect()
            
            ###
            # Load variant specific sprites
            for variant in parameters['PlayerShip'][ship]['Variants']:
                # Load sprites for any specific variant
                self.loadedSprites[ship + variant] = dict()
                
                # Load base sprite
                self.loadedSprites[ship + variant]['Base'] = pygame.sprite.Sprite()
                self.loadedSprites[ship + variant]['Base'].image = pygame.image.load('{basepath}_{basesprite}.{pictureFormat}'.format(basepath = parameters['PlayerShip'][ship]['Basepath'], basesprite = parameters['PlayerShip'][ship + variant]['BaseSprite'], pictureFormat = pictureFormat)).convert_alpha()
                self.loadedSprites[ship + variant]['Base'].rect = self.loadedSprites[ship + variant]['Base'].image.get_rect()
                
                # Load gib sprites
                self.loadedSprites[ship + variant]['Gib'] = list()
                for gibStr in parameters['PlayerShip'][ship + variant]['GibSprites']:
                    self.loadedSprites[ship + variant]['Gib'].append(pygame.sprite.Sprite())
                    self.loadedSprites[ship + variant]['Gib'][-1].image = pygame.image.load('{basepath}_{gibStr}.{pictureFormat}'.format(basepath = parameters['PlayerShip'][ship]['Basepath'], gibStr = gibStr, pictureFormat = pictureFormat)).convert_alpha()
                    self.loadedSprites[ship + variant]['Gib'][-1].rect = self.loadedSprites[ship + variant]['Gib'][-1].image.get_rect()
            
            
            ##
            # Create the different shield levels as well as Zoltan shields
            self.loadedSprites[ship]['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])] = copySprite(self.loadedSprites[ship]['Shields'])

            # For the alpha-multiplication
            alphaImg = pygame.Surface(self.loadedSprites[ship]['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect.size, pygame.SRCALPHA)
            alphaImg.fill((255, 255, 255, parameters['General']['ShieldMultAlpha']))

            for level in reversed(range(1, parameters['General']['ShieldMaxLevel'])):
                self.loadedSprites[ship]['ShieldsLevel' + str(level)] = pygame.sprite.Sprite()
                
                # Sprites aufhellen
                self.loadedSprites[ship]['ShieldsLevel' + str(level)].image = self.loadedSprites[ship]['ShieldsLevel' + str(level + 1)].image.copy()
                self.loadedSprites[ship]['ShieldsLevel' + str(level)].image.blit(alphaImg, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                self.loadedSprites[ship]['ShieldsLevel' + str(level)].rect = self.loadedSprites[ship]['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect
    
            # Generate the Zoltan shield
            self.loadedSprites[ship]['ZoltanShield'] = pygame.sprite.Sprite()
            self.loadedSprites[ship]['ZoltanShield'].image = self.loadedSprites[ship]['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].image.copy()
            self.loadedSprites[ship]['ZoltanShield'].rect = self.loadedSprites[ship]['ShieldsLevel' + str(parameters['General']['ShieldMaxLevel'])].rect

            # Swap blue and green and adapt the colors
            pixelImage = pygame.surfarray.pixels3d(self.loadedSprites[ship]['ZoltanShield'].image)
            blueOld = pixelImage[:,:,2].copy()
            greenOld = pixelImage[:,:,1].copy()
            pixelImage[:,:,0] = np.round(pixelImage[:,:,0] / 1.1).astype(int)
            pixelImage[:,:,1] = np.round(blueOld / 1.1).astype(int)
            pixelImage[:,:,2] = np.round(greenOld / 1.8).astype(int)
            
            # Delete numpy-array
            del pixelImage



    



