###
#
# Functions that contain the gameplay loops
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

# Arrays and matrices
import numpy as np

# Garbage collection
import gc


###
# Load ressources

# Key bindings
import src.classes.setup.key_bindings as inputKeyBindings

# Ships
import src.classes.ships.player_ship as playerShip
import src.classes.ships.enemy_ship as enemyShip

# Screen update
import src.classes.screen.update_screen as updateScreen

# Helper functions
import src.misc.check_clicks_and_collisions as checkClicksAndCollisions


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Functions

##
# Main gameplay loop when idle or in battle (as opposed to e.g. the main menu or when there are textboxes)
def mainGameplayLoop(activeScreenUpdate: updateScreen.updateScreen, parameters: Dict, keyBindings: inputKeyBindings.getKeyBindings, activePlayerShip: playerShip.playerShip, activeEnemyShip: [None, enemyShip.enemyShip], animationsPlayerShip: Dict):
    """
    
    Main gameplay loop which handles the player and enemy ship if present.
    
    Returns:
        - 0 if stopped correctly
        - 1 if exited by pressing the exit-button on the screen
    
    
    """
    
    logger.debug('Started main gameplay loop')
    
    ###
    # Initialize the clock
    running = True
    clock = pygame.time.Clock()
    
    ##
    # Initialize indicators
    pause = False

    ##
    # Loop counter and timer for the output of the framerate
    loopCounter = 0
    loopTimer = 0
    
    ##
    # Animation tracking between mouse clicks and buttons (not to start the same animation multiple times)
    animationTracking = dict()
    for field in ['Doors', 'AddSystemPower', 'RemoveSystemPower']:
        animationTracking[field] = list()
    
    
    ###
    # Main loop
    while running:        
        ###
        # Wait for the time to the next frame according to the framerate to elapse
        if parameters['General']['MaxFramerate']:
            clock.tick_busy_loop(parameters['General']['MaxFramerate'])
        else:
            clock.tick_busy_loop()

        # Get elapsed time since last clock tick
        dt = clock.get_time()   # Time in milliseconds


        ###
        # Update counters for FPS display
        loopCounter += 1
        loopTimer += dt

        if loopTimer >= parameters['General']['UpdateFramerateDisplay']:
            logger.info('FPS {fps}, gameplay loops {loops}, time elapsed {time}'.format(fps = round(loopCounter / loopTimer * 1000), loops = loopCounter, time = round(loopTimer / 1000, 4)))

            # Reset values
            loopCounter = 0
            loopTimer = 0
            
            # Garbage collection
            gc.collect()
        
        
        ###
        # Reset values
        redrawEnergyUi = False
        
        
        ###
        # Get all events from the event queue which happened since the last call/loop
        events = pygame.event.get()
        
        
        ###
        # Evaluate all the events
        for event in events:
            if event.type != pygame.MOUSEMOTION:
                logger.debug(event)
            
            ###
            # Quit, for now exit directly without any processing like e.g. saving the game state
            if event.type == pygame.QUIT:
                return(1)
            
            
            ###
            # Store the current inputs so they can later on be appropriately processed
            
            ##
            # Mouse control

            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in keyBindings.keysUsed['Mouse']:
                    keyBindings.keyPressed['Mouse'][keyBindings.keyBindingsInverse['Mouse'][event.button]] = True
                    keyBindings.mousePosition['Mouse'][keyBindings.keyBindingsInverse['Mouse'][event.button]]['PositionPressed'] = np.array(event.pos)

        
            # Mouse button released            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in keyBindings.keysUsed['Mouse']:
                    keyBindings.keyReleased['Mouse'][keyBindings.keyBindingsInverse['Mouse'][event.button]] = True
                    keyBindings.mousePosition['Mouse'][keyBindings.keyBindingsInverse['Mouse'][event.button]]['PositionReleased'] = np.array(event.pos)
            
            
            ##
            # Keyboard control
            
            # Keyboard button pressed
            if event.type == pygame.KEYDOWN:
                if event.key in keyBindings.keysUsed['Keyboard']:
                    keyBindings.keyPressed['Keyboard'][keyBindings.keyBindingsInverse['Keyboard'][event.key]] = True
                    keyBindings.mousePosition['Keyboard'][keyBindings.keyBindingsInverse['Keyboard'][event.key]]['PositionPressed'] = np.array(pygame.mouse.get_pos())
            
            # Keyboard button released
            if event.type == pygame.KEYUP:
                if event.key in keyBindings.keysUsed['Keyboard']:
                    keyBindings.keyReleased['Keyboard'][keyBindings.keyBindingsInverse['Keyboard'][event.key]] = True
                    keyBindings.mousePosition['Keyboard'][keyBindings.keyBindingsInverse['Keyboard'][event.key]]['PositionReleased'] = np.array(pygame.mouse.get_pos())
            
        
        ###
        # Game loop updates
        
        ##
        # Leftclick released
        if keyBindings.keyReleased['Mouse']['LeftClick']:   # Leftclick released
            logger.debug('Left click released. Pressed at {x1}, {y1}, released at {x2}, {y2}'.format(x1 = str(keyBindings.mousePosition['Mouse']['LeftClick']['PositionPressed'][0]), y1 = str(keyBindings.mousePosition['Mouse']['LeftClick']['PositionPressed'][1]), x2 = str(keyBindings.mousePosition['Mouse']['LeftClick']['PositionReleased'][0]), y2 = str(keyBindings.mousePosition['Mouse']['LeftClick']['PositionReleased'][1])))
            
            ##
            # Reset the leftclick to unpressed
            keyBindings.keyPressed['Mouse']['LeftClick'] = False    # This will lead to missed input if one clicks faster than the framerate (should not happen)
            keyBindings.keyReleased['Mouse']['LeftClick'] = False
            
            
            ###
            # Select the different actions
            
            ##
            # Doors, clicking on crew will have higher priority than doors later
            # To open or close doors: Mouse has been clicked over the door (both key down and key up)
            
            # Check if click has been made over a door for both start and end of click
            logger.debug('Check door rects')
            
            checkDoorsButtonDown = checkClicksAndCollisions.checkRects(keyBindings.mousePosition['Mouse']['LeftClick']['PositionPressed'], activePlayerShip.doorRectForSelection)
            checkDoorsButtonUp = checkClicksAndCollisions.checkRects(keyBindings.mousePosition['Mouse']['LeftClick']['PositionReleased'], activePlayerShip.doorRectForSelection)
            
            # Door click boxes do not overlap, so if there is a valid click there is only one door selected for both click pressed and released
            if (len(checkDoorsButtonDown) == 1) and (len(checkDoorsButtonUp) == 1):
                # Check whether the press and release has been made over the same door
                if checkDoorsButtonDown[0] == checkDoorsButtonUp[0]:
                    ##
                    # Read out the doorkey
                    chosenDoorKey = activePlayerShip.doorKeysForRects[checkDoorsButtonDown[0]]
                    logger.debug('Selected door: {}'.format(str(chosenDoorKey)))
                    
                    ##
                    # Add the animation to the control object
                    animationTracking['Doors'].append(chosenDoorKey)
                
                else:
                    logger.debug('Press and release were not made over the same system symbol')
                
            else:
                logger.debug('Press or release were not made over a door')
            
            
            ##
            # System energy manipulation
            logger.debug('Check system energy addition')
            
            checkSystemEnergyAdditionButtonDown = checkClicksAndCollisions.checkCenters(keyBindings.mousePosition['Mouse']['LeftClick']['PositionPressed'], activePlayerShip.energySystemsRectCenters, parameters['General']['UiEnergySymbolsMaxDistance'])
            checkSystemEnergyAdditionButtonUp = checkClicksAndCollisions.checkCenters(keyBindings.mousePosition['Mouse']['LeftClick']['PositionReleased'], activePlayerShip.energySystemsRectCenters, parameters['General']['UiEnergySymbolsMaxDistance'])
            
            # Add energy to a system if possible. The symbols do not overlap
            if (len(checkSystemEnergyAdditionButtonDown) == 1) and (len(checkSystemEnergyAdditionButtonUp) == 1):
                # Check whether the press and release has been made over the same door
                if checkSystemEnergyAdditionButtonDown[0] == checkSystemEnergyAdditionButtonUp[0]:
                    ##
                    # Read out the doorkey
                    chosenSystem = activePlayerShip.energySystemsForRects[checkSystemEnergyAdditionButtonDown[0]]
                    logger.debug('Selected system for energy addition: {}'.format(chosenSystem))
                    
                    ##
                    # Add the animation to the control object
                    animationTracking['AddSystemPower'].append(chosenSystem)
                
                else:
                    logger.debug('Press and release were not made over the same door')
                
            else:
                logger.debug('Press or release were not made over a system symbol')
        
        
        ##
        # Rightclick released
        if keyBindings.keyReleased['Mouse']['RightClick']:   # Rightclick released
            logger.debug('Right click released. Pressed at {x1}, {y1}, released at {x2}, {y2}'.format(x1 = str(keyBindings.mousePosition['Mouse']['RightClick']['PositionPressed'][0]), y1 = str(keyBindings.mousePosition['Mouse']['RightClick']['PositionPressed'][1]), x2 = str(keyBindings.mousePosition['Mouse']['RightClick']['PositionReleased'][0]), y2 = str(keyBindings.mousePosition['Mouse']['RightClick']['PositionReleased'][1])))
            
            ##
            # Reset the rightclick to unpressed
            keyBindings.keyPressed['Mouse']['RightClick'] = False    # This will lead to missed input if one clicks faster than the framerate (should not happen)
            keyBindings.keyReleased['Mouse']['RightClick'] = False
            
            
            ###
            # Select the different actions

            ##
            # System energy manipulation
            logger.debug('Check system energy removal')
            
            checkSystemEnergyRemovalButtonDown = checkClicksAndCollisions.checkCenters(keyBindings.mousePosition['Mouse']['RightClick']['PositionPressed'], activePlayerShip.energySystemsRectCenters, parameters['General']['UiEnergySymbolsMaxDistance'])
            checkSystemEnergyRemovalButtonUp = checkClicksAndCollisions.checkCenters(keyBindings.mousePosition['Mouse']['RightClick']['PositionReleased'], activePlayerShip.energySystemsRectCenters, parameters['General']['UiEnergySymbolsMaxDistance'])
            
            # Add energy to a system if possible
            if (len(checkSystemEnergyRemovalButtonDown) == 1) and (len(checkSystemEnergyRemovalButtonUp) == 1):
                # Check whether the press and release has been made over the same door
                if checkSystemEnergyRemovalButtonDown[0] == checkSystemEnergyRemovalButtonUp[0]:
                    ##
                    # Read out the doorkey
                    chosenSystem = activePlayerShip.energySystemsForRects[checkSystemEnergyRemovalButtonDown[0]]
                    logger.debug('Selected system for energy removal: {}'.format(chosenSystem))

                    ##
                    # Add the animation to the control object
                    animationTracking['RemoveSystemPower'].append(chosenSystem)
                
                else:
                    logger.debug('Press and release were not made over the same system symbol')
                
            else:
                logger.debug('Press or release were not made over a system symbol')
        
        
        ###
        # Check keyboard
        
        ##
        # Pause activated/deactivated
        if keyBindings.keyReleased['Keyboard']['Space']:   # Space released
            logger.debug('{} pause'.format('Deactivate' if pause else 'Active'))
            
            ##
            # Invert pause flag
            pause = not pause
            
            if pause:
                activeScreenUpdate.pause = 2
            else:
                activeScreenUpdate.pause = 0
            
            ##
            # Reset the pause to unpressed
            keyBindings.keyPressed['Keyboard']['Space'] = False    # This will lead to missed input if one clicks faster than the framerate (should not happen)
            keyBindings.keyReleased['Keyboard']['Space'] = False
            
            
        ###
        # Change system states
        
        ##
        # Add system power
        if len(animationTracking['AddSystemPower']):
            for system in animationTracking['AddSystemPower']:
                activePlayerShip.addSystemPower(system)
            
            # Reset tracking
            animationTracking['AddSystemPower'] = list()
            
            # Redraw energy ui
            redrawEnergyUi = True
        
        
        ##
        # Remove system power
        if len(animationTracking['RemoveSystemPower']):
            for system in animationTracking['RemoveSystemPower']:
                activePlayerShip.removeSystemPower(system)
            
            # Reset tracking
            animationTracking['RemoveSystemPower'] = list()
            
            # Redraw energy ui
            redrawEnergyUi = True            

        
        ###
        # Add animations
        
        ##
        # Doors
        if len(animationTracking['Doors']):
            # Start animations
            for doorKey in animationTracking['Doors']:
                animationsPlayerShip['Doors'][chosenDoorKey].startAnimation(True)
            
            # Reset tracking
            animationTracking['Doors'] = list()

        
        ###
        # Update all animations and oxygen     
        # Only run animations if the game is not on pause        

        if not pause:
            ##
            # Animate player doors
            doorsChanged = False
            for doors in animationsPlayerShip['Doors'].items():
                # Update door
                updateDoorKey = doors[1].updateAnimation(dt)
                
                # If framechange happened, update the door sprite
                if updateDoorKey:
                    activePlayerShip.updateDoor(doors[0])
                    doorsChanged = True
            
            # Update open room connectivity if necessary
            if doorsChanged:
                activePlayerShip.updateRoomConnectivityOpenDoors()
        
        
            ###
            # Update oxygen
            activePlayerShip.updateOxygen(dt)

            if activeEnemyShip is not None:
                activeEnemyShip.updateOxygen(dt)
    
    
        ###
        # Redraw everything
        activeScreenUpdate.drawScreen(redrawEnergyUi = redrawEnergyUi)
        
        
    
    ###
    # Return 0 for normal end
    return(0)
    
































