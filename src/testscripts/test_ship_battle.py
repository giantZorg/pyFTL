###
#
# Test script for the player ship only. This script assumes that the working directory is at the root folder of the project
#
###


###
# Load packages

# OS
import os, sys

# Logging
import logging

# Pygame
import pygame


###
# Set main game directory and system path variable if necessary
if '__file__' in dir():
    os.chdir(os.path.abspath(__file__).replace('\\', '/').split('/src/')[0])
    sys.path.append(os.getcwd())


###
# Load ressources

# Gameplay ressources
import src.gameplay.setup_gameplay as setup
import src.gameplay.game_loop as gameLoop

# Key bindings
import src.classes.setup.key_bindings as inputKeyBindings

# Background images
import src.classes.setup.background_images as backgroundImages

# Ships
import src.classes.ships.player_ship as playerShip
import src.classes.ships.enemy_ship as enemyShip

# Screen update
import src.classes.screen.update_screen as updateScreen


###
# Setup logging
logger = logging.getLogger(__name__)

#logging.basicConfig(level = logging.INFO)
logging.basicConfig(level = logging.DEBUG)


###
# Main routine
if __name__ == "__main__":
    ###
    # Load values and parameters from files
    parameters = setup.loadAllParameters()
    
    
    ###
    # Load key bindings
    keyBindings = inputKeyBindings.getKeyBindings()

    
    ###
    # Start display as loading the sprites requires a running screen
    screen = setup.screenSetup(parameters)
    
    
    ###
    # Load pictures and sprites
    
    ##
    # Load the background images
    allBackgroundImages = backgroundImages.backgroundImages(parameters)
    
    ##
    # Load the sprites
    spritesAll = setup.loadAllSprites(parameters)
    
    
    ###
    # Initialize the various classes like player ship and UI
    
    ##
    # Player ship
    activePlayerShip = playerShip.playerShip(parameters, spritesAll)
    activePlayerShip.shipSetup()
    
    ##
    # Enemy ship
    activeEnemyShip = enemyShip.enemyShip(parameters, spritesAll)
    activeEnemyShip.shipSetup()
    
    ##
    # UI
    
    
    
    ###
    # Set playership to battle mode
    activePlayerShip.moveRectsForBattle(True)
    
    
    
    ###
    # Create screen update object
    activeScreenUpdate = updateScreen.updateScreen(screen, allBackgroundImages, activePlayerShip, activeEnemyShip, spritesAll, parameters)
    
    ##
    # Set the first image on the screen
    activeScreenUpdate.drawScreen(redrawEnergyUi = True)
    
    
    ###
    # Setup the animation control objects
    animationsPlayerShip = setup.loadAllAnimations(parameters, activePlayerShip)
    
    
    
    ###
    # Game loop
    gameLoop.mainGameplayLoop(activeScreenUpdate, parameters, keyBindings, activePlayerShip, activeEnemyShip, animationsPlayerShip)


    ###
    # End game
    pygame.quit()


















