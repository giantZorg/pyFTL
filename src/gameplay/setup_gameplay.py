###
#
# Functions to setup various things needed for the gameplay
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
# Load ressources

# Parameter files
import src.parameters.general_parameters as generalParameters
import src.parameters.colors as colors

import src.parameters.player_ship_parameters as playerShipParameters
import src.parameters.general_ship_sprite_parameters as generalShipSpriteParameters
import src.parameters.enemy_ship_parameters as enemyShipParameters

import src.parameters.enemy_ship_ui_parameters as enemyShipUiParameters
import src.parameters.energy_management_ui_parameters as energyManagementUiParameters

import src.parameters.weapons_parameters as weaponParameters

import src.parameters.main_box_ui_parameters as mainBoxUiParameters

# Sprite objects
import src.classes.sprites.player_ship_sprites as playerShipSprites
import src.classes.sprites.general_ship_sprites as generalShipSprites
import src.classes.sprites.enemy_ship_sprites as enemyShipSprites

import src.classes.sprites.enemy_ship_ui_sprites as enemyShipUiSprites
import src.classes.sprites.energy_ui_sprites as energyUiSprites

import src.classes.sprites.weapon_sprites as weaponSprites

import src.classes.sprites.main_box_ui_sprites as mainBoxUiSprites

# Animation control objects
import src.classes.animations.animation_doors as animationDoors

# Ships
import src.classes.ships.player_ship as playerShip


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Functions

##
# Load all the different parameters found in the different files in the parameters folder
def loadAllParameters() -> Dict:
    """
    
    Load all parameters, return a dictionary containing the different loaded dictionaries as entries
    
    
    """
    
    logger.debug('Load all the various parameters and values needed')
    
    ###
    # Initialize dictionary
    parameters = dict()
    
    
    ###
    # Load the data
    
    ##
    # Load the colors
    parameters['Colors'] = colors.loadColors()
    
    ##
    # Load the general parameters
    parameters['General'] = generalParameters.loadGeneralParameters()
    
    ##
    # Load the player ship parameters
    parameters['PlayerShip'] = playerShipParameters.loadPlayerShipParameters(parameters['General'])
    
    ##
    # Load the enemy ship parameters
    parameters['EnemyShip'] = enemyShipParameters.loadEnemyShipParameters(parameters['General'])
    
    ##
    # Load the enemy ship ui parameters
    parameters['EnemyShipUi'] = enemyShipUiParameters.loadEnemyShipUiParameters(parameters['General'])
    
    ##
    # Load the energy management ui parameters
    parameters['EnergyManagementUi'] = energyManagementUiParameters.loadEnergyManagementUiParameters(parameters['General'])

    ##
    # Load the general ship sprites parameters
    parameters['GeneralShipSprites'] = generalShipSpriteParameters.loadGeneralShipSpriteParameters(parameters['General'])
    
    ##
    # Load the weapon parameters
    parameters['Weapons'] = weaponParameters.loadWeaponParameters(parameters['General'])
    
    ##
    # Load the main box and text parameters
    parameters['MainBoxUi'] = mainBoxUiParameters.loadMainBoxUiParameters(parameters['General'])
    
    
    ###
    # Return the parameters
    return(parameters)


##
# Function to set the screen correctly
def screenSetup(parameters: Dict) -> pygame.Surface:
    """
    
    Set the screen for the gameplay correctly and return the screen object.
    
    """
    
    logger.debug('Initialize the game screen')
    
    
    ###
    # Initialize pygame
    pygame.init()
    
    
    ###
    # Fenster erstellen
    screen = pygame.display.set_mode((parameters['General']['DisplayWidth'], parameters['General']['DisplayHeight']))
    
    # Fenster einrichten
    screen.fill(parameters['Colors']['White'])
    pygame.display.set_caption(parameters['General']['DisplayTitle'])
    pygame.display.update()
    
    
    ###
    # Return the screen object
    return(screen)


##
# Function to load all the sprites
def loadAllSprites(parameters: Dict) -> Dict:
    """
    
    Function to load in the sprites needed throughout the game.
    
    """
    
    logger.debug('Load in all the sprites needed throughout the game')
    
    
    ###
    # Initialize the dictionary for the sprites
    sprites = dict()
    
    
    ###
    # Load the data
    
    ##
    # Load player ship sprites
    sprites['PlayerShip'] = playerShipSprites.playerShipSprites(parameters)
    
    ##
    # Load general ship sprites
    sprites['GeneralShip'] = generalShipSprites.generalShipSprites(parameters)

    ##
    # Load player ship sprites
    sprites['EnemyShip'] = enemyShipSprites.enemyShipSprites(parameters)
    
    ##
    # Load enemy ship ui elements
    sprites['EnemyUi'] = enemyShipUiSprites.enemyShipUiSprites(parameters)

    ##
    # Load all energy ui elements
    sprites['EnergyUi'] = energyUiSprites.energyUiSprites(parameters)
    
    ##
    # Load all weapon and projectile sprites
    sprites['Weapons'] = weaponSprites.weaponSprites(parameters)
    
    ##
    # Load the main box and text parameters
    sprites['MainBoxUi'] = mainBoxUiSprites.mainBoxUiSprites(parameters)
    
    
    ###
    # Return the loaded sprites
    return(sprites)


##
# Function to load all the animation controls
def loadAllAnimations(parameters: Dict, ship: [playerShip.playerShip]) -> Dict:
    """
    
    Function to load in the animation controls needed for the ship
    
    """
    
    logger.debug('Initialize all the animations for the {} ship'.format('player' if ship.playerShip else 'enemy'))
    
    
    ###
    # Initialize dictionary
    animations = dict()
    
    
    ###
    # Load all the door animations
    doorAnimations = dict()
    for doorKey in ship.presentDoors:
        doorAnimations[doorKey] = animationDoors.animationDoors(parameters, ship.doors[doorKey])
    
    animations['Doors'] = doorAnimations
    
    
    ###
    # Return the dictionary with all the animation objects
    return(animations)
        
































