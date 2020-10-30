###
#
# Helperfunctions
#
###


###
# Load packages

# Typing
from typing import Tuple, List, Dict

# Pygame
import pygame


###
# Functions

##
# Function to properly copy a sprite
def copySprite(sprite: pygame.sprite.Sprite) -> pygame.sprite.Sprite:
    # Create sprite
    newSprite = pygame.sprite.Sprite()
    
    # Copy sprite
    newSprite.image = sprite.image.copy()
    newSprite.rect = sprite.rect.copy()
    
    # Return sprite
    return(newSprite)


##
# Function for color interpolation
def colorInterpolation(farbe1: [Tuple, List], farbe2: [Tuple, List], rho: float) -> Tuple:
    return((int(farbe1[0] * rho + farbe2[0] * (1 - rho)), int(farbe1[1] * rho + farbe2[1] * (1 - rho)), int(farbe1[2] * rho + farbe2[2] * (1 - rho))))


##
# Function to get the number of bars to be drawn in the correct order for main systems
def powerBarsMainSystem(systemInformation: Dict) -> List:
    ###
    # Initialize lists
    powerBars = list()
    powerBarsNoEnergy = list()
    
    
    ###
    # Go through all the bars with energy
    for i in range(0, systemInformation['PowerCurrent']):
        # Check for blocked power by cooldown
        if systemInformation['PowerCooldown']:
            powerBars.append('ShortWhite')
            systemInformation['PowerCooldown'] -= 1
            
        # Check for Zoltan power
        elif systemInformation['PowerZoltans']:
            powerBars.append('ShortYellow')
            systemInformation['PowerZoltans'] -= 1
        
        # Check if ionized
        elif systemInformation['IonCharges']:
            powerBars.append('ShortBlue')

        # Default reactor power
        elif systemInformation['PowerBackup'] == 0:
            powerBars.append('ShortGreen')
        
        # Backup power
        else:
            powerBars.append('ShortBackup')
            systemInformation['PowerBackup'] -= 1
    
    
    ###
    # Go through the bars without energy
    for i in range(0, systemInformation['PowerMax'] - systemInformation['PowerCurrent']):
        # Check for power blocked by events
        if systemInformation['PowerBlocked']:
            powerBarsNoEnergy.append('ShortBlocked')
            systemInformation['PowerBlocked'] -= 1
            
        # Check for damaged bars
        elif systemInformation['Damaged']:
            powerBarsNoEnergy.append('ShortDamaged')
            systemInformation['Damaged'] -= 1
        
        # Otherwise unassigned power bar
        else:
            powerBarsNoEnergy.append('ShortUnassigned')
            
    
    ###
    # Return
    return(powerBars + list(reversed(powerBarsNoEnergy)))


