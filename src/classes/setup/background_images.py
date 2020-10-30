###
#
# Define a class which contains all the possible backgrounds and returns one if requested
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# OS
import os

# Arrays
import numpy as np

# Pygame
import pygame


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the background images
class backgroundImages(object):
    """
    
    Object that reads in all available background pictures and returns one if requested.
    The picture will be scaled if set so in parameters['General']['BackgroundScalePictures'].
    If no images are found, a black screen will be returned.
    
    Init:
        - parameters[Dict]: Dictionary containing all parameters
    
    Fields:
        - allPictures[List]: List of all imported background images
        - nBackgroundPictures[int]: Number of imported background images
        
    Methods:
        - loadAllPictures(parameters [dict]): Loads and scales if necessary all available images into this object
        - getBackgroundImage(selection [int]): Returns a background sprite to be used in the plotting step. The variable selection is in the range [0, #loadedPictures), the picture in the list entry corresponding to selection will be returned
        - getRandomBackgroundImage(): Returns a random background sprite to be used in the plotting step               - 
    
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict):
        logger.debug('Initialize the object holding all the background images')
        
        # Load all pictures
        self.loadAllPictures(parameters)


    ###
    # Load all pictures
    def loadAllPictures(self, parameters):
        logger.debug('Load all the background images')
        self.allPictures = list()
        
        # Go through all specified folders
        picturesLoaded = False
        for pathFolder in parameters['General']['PathFoldersBackgroundPictures']:
            for picture in os.listdir(pathFolder):
                if any([True if pictureFormat in picture else False for pictureFormat in parameters['General']['BackgroundPictureFormats']]):
                    self.allPictures.append(pygame.image.load('{folder}/{picture}'.format(folder = pathFolder, picture = picture)))
                    
                    if not picturesLoaded:
                        picturesLoaded = True
                        
                    if parameters['General']['BackgroundScalePictures']:
                        self.allPictures[-1] = pygame.transform.scale(self.allPictures[-1], (parameters['General']['DisplayWidth'], parameters['General']['DisplayHeight']))

        # Create a black image if no image was loaded
        if not picturesLoaded:
           self.allPictures.append(pygame.Surface((parameters['General']['DisplayWidth'], parameters['General']['DisplayHeight'])))
           self.allPictures[-1].fill(parameters['Colors']['black'])
          
        # Store the number of available pictures
        self.nBackgroundPictures = len(self.allPictures)
    
    
    ###
    # Return a soecific image
    def getBackgroundImage(self, selection : int) -> pygame.sprite.Sprite:
        # selection: Integer in the range [0, self.nBackgroundPictures)
        logger.debug('Return background image {}'.format(selection))
        
        # Create sprite
        backgroundPicture = pygame.sprite.Sprite()
        backgroundPicture.image = self.allPictures[selection]
        backgroundPicture.rect = backgroundPicture.image.get_rect()
        
        # Return sprite
        return(backgroundPicture)
    
    
    ###
    # Return a random image
    def getRandomBackgroundImage(self) -> pygame.sprite.Sprite:
        logger.debug('Select a random background image')
        
        # Get a random selection
        selection = np.random.choice(self.nBackgroundPictures)
        
        # Return a random image
        return(self.getBackgroundImage(selection))








