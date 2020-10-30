###
#
# Test script for the player ship only. This script assumes that the working directory is at the root folder of the project
#
###


###
# Load packages

# Logging
import logging

# Pygame
import pygame


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

# Screen update
import src.classes.screen.update_screen as updateScreen



###
# Setup logging
logger = logging.getLogger(__name__)

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
    activeEnemyShip = None
    
    ##
    # UI
    
    
    ###
    # Create screen update object
    activeScreenUpdate = updateScreen.updateScreen(screen, allBackgroundImages, activePlayerShip, activeEnemyShip, spritesAll)
    
    ##
    # Set the first image on the screen
    activeScreenUpdate.drawScreen()
    
    
    ###
    # Setup the animation control objects
    animationsPlayerShip = setup.loadAllAnimations(parameters, activePlayerShip)
    
    
    
    ###
    # Game loop
    gameLoop.mainGameplayLoop(activeScreenUpdate, parameters, keyBindings, activePlayerShip, animationsPlayerShip)


    ###
    # End game
    pygame.quit()


















