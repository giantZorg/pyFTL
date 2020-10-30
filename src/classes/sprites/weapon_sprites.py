###
#
# Define a class which contains the sprites for the weapons and corresponding projectiles
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
# Define the class for the weapon and projectile images
class weaponSprites(object):
    """
    
    Load the sprites for the weapons and the projectiles.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - laserList [List]: List containing the available laser weapons
        - chargeUpSprites [Dict]: Dictionary containing all the loaded weapon charge-up sprites with initial rect fields (-> not shifted)
        - fireAnimationSprites [Dict]: Dictionary containing all the loaded weapon fire animation sprites with initial rect fields (-> not shifted)
        - laserProjectiles [Dict]: Dictionary containing all the loaded laser projectile sprites with initial rect fields (-> not shifted)
    
    Methods:
        - createLaserList(): Creates a list of all available laser weapons and saves them in self.laserList
        - loadLaserSprites(parameters [Dict]): Imports all sprites for lasers and saves them into self.chargeUpSprites, self.fireAnimationSprites and self.laserProjectiles
    
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the weapon images')        

        ###
        # Initialize dictionaries
        self.chargeUpSprites = dict()
        self.fireAnimationSprites = dict()
        
        self.laserProjectiles = dict()
        
        ###
        # List all available weapons
        self.createLaserList(parameters)
        
        ###
        # Load in the sprites
        self.loadLaserSprites(parameters)
        
        

    ###
    # Create a list of all available lasers
    def createLaserList(self, parameters: Dict) -> None:
        self.laserList = list()
        
        for weapon in parameters['Weapons']:
            if weapon not in ['BasePath']:
                if parameters['Weapons'][weapon]['Type'] == 'Laser':
                    self.laserList.append(weapon)
    
    
    ###
    # Load all lasers
    def loadLaserSprites(self, parameters: Dict) -> None:
        logger.debug('Import the laser weapon sprites')
        
        ##
        # Picture format always the same
        pictureFormat = 'png'
                
        # Create the sprites in the relevant directions [34 = Upward right, 32 = Upward left, 41 = Rightside down, 43 = Rightside up]
        orientationsWeapons = [34, 32, 41, 43]
        
        for weapon in self.laserList:
            # Setup dicts und lists
            self.chargeUpSprites[weapon] = dict()
            self.fireAnimationSprites[weapon] = dict()
            
            for direction in orientationsWeapons:
                self.chargeUpSprites[weapon][direction] = list()
                self.fireAnimationSprites[weapon][direction] = list()            
            
            self.laserProjectiles[weapon] = list()
            
            # Load spritesheet
            weaponSpriteSheet = pygame.image.load('{basepath}{weaponSprites}.{pictureFormat}'.format(basepath = parameters['Weapons']['BasePath'], weaponSprites = parameters['Weapons'][weapon]['WeaponSprites'], pictureFormat = pictureFormat)).convert_alpha()
            
            # Get sprite width
            spriteWidth = weaponSpriteSheet.get_rect().w // parameters['Weapons'][weapon]['WeaponSpritesNumber']
            spriteHeight = weaponSpriteSheet.get_rect().h
            
            # Cut out the sprites
            for i in range(0, parameters['Weapons'][weapon]['WeaponSpritesChargeUp']):
                self.chargeUpSprites[weapon][34].append(pygame.sprite.Sprite())
                self.chargeUpSprites[weapon][34][-1].image = weaponSpriteSheet.subsurface([i * spriteWidth, 0, spriteWidth, spriteHeight]).copy()
                self.chargeUpSprites[weapon][34][-1].rect = self.chargeUpSprites[weapon][34][-1].image.get_rect()
                
                # Create also the other directions
                self.chargeUpSprites[weapon][32].append(pygame.sprite.Sprite())
                self.chargeUpSprites[weapon][32][-1].image = pygame.transform.flip(self.chargeUpSprites[weapon][34][-1].image, True, False)
                self.chargeUpSprites[weapon][32][-1].rect = self.chargeUpSprites[weapon][32][-1].image.get_rect()
                
                self.chargeUpSprites[weapon][41].append(pygame.sprite.Sprite())
                self.chargeUpSprites[weapon][41][-1].image = pygame.transform.rotate(self.chargeUpSprites[weapon][34][-1].image, -90)
                self.chargeUpSprites[weapon][41][-1].rect = self.chargeUpSprites[weapon][41][-1].image.get_rect()
                
                self.chargeUpSprites[weapon][43].append(pygame.sprite.Sprite())
                self.chargeUpSprites[weapon][43][-1].image = pygame.transform.flip(self.chargeUpSprites[weapon][41][-1].image, False, True)
                self.chargeUpSprites[weapon][43][-1].rect = self.chargeUpSprites[weapon][43][-1].image.get_rect()
                
            
            for i in range(parameters['Weapons'][weapon]['WeaponSpritesChargeUp'], parameters['Weapons'][weapon]['WeaponSpritesNumber']):
                self.fireAnimationSprites[weapon][34].append(pygame.sprite.Sprite())
                self.fireAnimationSprites[weapon][34][-1].image = weaponSpriteSheet.subsurface([i * spriteWidth, 0, spriteWidth, spriteHeight]).copy()
                self.fireAnimationSprites[weapon][34][-1].rect = self.chargeUpSprites[weapon][34][-1].image.get_rect()

                # Create also the other directions
                self.fireAnimationSprites[weapon][32].append(pygame.sprite.Sprite())
                self.fireAnimationSprites[weapon][32][-1].image = pygame.transform.flip(self.fireAnimationSprites[weapon][34][-1].image, True, False)
                self.fireAnimationSprites[weapon][32][-1].rect = self.fireAnimationSprites[weapon][32][-1].image.get_rect()
                
                self.fireAnimationSprites[weapon][41].append(pygame.sprite.Sprite())
                self.fireAnimationSprites[weapon][41][-1].image = pygame.transform.rotate(self.fireAnimationSprites[weapon][34][-1].image, -90)
                self.fireAnimationSprites[weapon][41][-1].rect = self.fireAnimationSprites[weapon][41][-1].image.get_rect()
                
                self.fireAnimationSprites[weapon][43].append(pygame.sprite.Sprite())
                self.fireAnimationSprites[weapon][43][-1].image = pygame.transform.flip(self.fireAnimationSprites[weapon][41][-1].image, False, True)
                self.fireAnimationSprites[weapon][43][-1].rect = self.fireAnimationSprites[weapon][43][-1].image.get_rect()
            
            del weaponSpriteSheet
        
            # Load projectiles
            projectileSpriteSheet = pygame.image.load('{basepath}{projectilesSprites}.{pictureFormat}'.format(basepath = parameters['Weapons']['BasePath'], projectilesSprites = parameters['Weapons'][weapon]['ProjectileSprites'], pictureFormat = pictureFormat)).convert_alpha()
        
            # Get sprite width
            spriteWidth = projectileSpriteSheet.get_rect().w // parameters['Weapons'][weapon]['ProjectileSpritesNumber']
            spriteHeight = projectileSpriteSheet.get_rect().h

            for i in range(0, parameters['Weapons'][weapon]['ProjectileSpritesNumber']):
                self.laserProjectiles[weapon].append(pygame.sprite.Sprite())
                self.laserProjectiles[weapon][-1].image = projectileSpriteSheet.subsurface([i * spriteWidth, 0, spriteWidth, spriteHeight]).copy()
                self.laserProjectiles[weapon][-1].rect = self.laserProjectiles[weapon][-1].image.get_rect()

            del projectileSpriteSheet


    
    
    
    