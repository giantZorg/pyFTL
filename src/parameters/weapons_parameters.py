###
#
# Define parameters which will be used for weapons
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


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Function to return the weapon parameters
def loadWeaponParameters(generalParameters: Dict) -> Dict:
    """
    
    Define the parameters for the weapons.
    
    Input:
        - generalParameters [Dict]: Dictionary with the general parameters
    
    """
    
    logger.debug('Define the weapon parameters')


    ###
    # Initialize dictionary
    weaponParameters = dict()
    
    # Basepath for the sprites
    weaponParameters['BasePath'] = generalParameters['PathFolderResources'] + 'img/weapons/'
    

    ###
    # Different weapons
    
    ## Basic laser
    #
    weaponParameters['BasicLaser'] = dict()
    
    # Set type
    weaponParameters['BasicLaser']['Type'] = 'Laser'
    weaponParameters['BasicLaser']['Projectile'] = True
    weaponParameters['BasicLaser']['Targetable'] = False     # Targetable for defense drone M1
    
    # Set sprites/spritesheets
    # Weapon
    weaponParameters['BasicLaser']['WeaponSprites'] = 'laser1_strip12'
    weaponParameters['BasicLaser']['WeaponSpritesNumber'] = 12
    weaponParameters['BasicLaser']['WeaponSpritesChargeUp'] = 6              # Number of sprites in the chargeup
    weaponParameters['BasicLaser']['WeaponAttachPoint'] = np.array([0, 33])  # Top left attach point of the weapon
    weaponParameters['BasicLaser']['WeaponCenter'] = np.array([10, 9])       # Center of the weapon where the laser shot will be placed first
    
    # Projectile
    weaponParameters['BasicLaser']['ProjectileSprites'] = 'laser_light_strip4'
    weaponParameters['BasicLaser']['ProjectileSpritesNumber'] = 4
    weaponParameters['BasicLaser']['ProjectileCenter'] = np.array([40, 10])  # Center of the projectile which will be used to calculate hits with other objects and the room
    weaponParameters['BasicLaser']['ProjectileRadiusPixels'] = 2
    
    # Set weapon parameters
    weaponParameters['BasicLaser']['ShotsFired'] = 1
    weaponParameters['BasicLaser']['DamageHull'] = 1
    weaponParameters['BasicLaser']['DamageCrew'] = 15
    weaponParameters['BasicLaser']['FireChance'] = 0.1
    weaponParameters['BasicLaser']['BreachChance'] = 0
    weaponParameters['BasicLaser']['StunChance'] = 0
    weaponParameters['BasicLaser']['ScrapCost'] = 20
    weaponParameters['BasicLaser']['RarityPlayer'] = 0
    weaponParameters['BasicLaser']['RarityEnemy'] = 1        # Needed for the generation of the enemy ship weaponry
    weaponParameters['BasicLaser']['ProjectileSpeed'] = 60   # Pixels per second
    
    weaponParameters['BasicLaser']['CooldownSeconds'] = 10
    weaponParameters['BasicLaser']['TimeBetweenShotsSeconds'] = 0.2
    
    weaponParameters['BasicLaser']['PowerNeeded'] = 1    
    
    
    ###
    # Return the dictionary containing the weapon parameters
    return(weaponParameters)





