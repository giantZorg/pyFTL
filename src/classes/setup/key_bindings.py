###
#
# Define a class which holds all the key bindings
#
###


###
# Load packages

# Logging
import logging

# Arrays
import numpy as np

# Pygame
import pygame


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the key bindings
class getKeyBindings(object):
    """
    
    Class which holds all the relevant key bindings. Changes to the key bindings ingame should be used within this class so no keys get hardcoded.
    Uses the devices 'Mouse' and 'Keyboard'. Throughout the code, the key values in the key:button pairs will be references, while the button refers to the pygame key code and can be changed.
    
    Relevant fields:
        - inputDevices: List of relevant input devices ['Mouse', 'Keyboard']
        - keyBindings: Dictionary over devices with key:button pairs
        - keyBindingsInverse: Dictionary over devices with button:key pairs
        - keyPressed: Dictionary over devices with pressed keys
        - keyReleased: Dictionary over devices with released keys
        - keysUsed: Dictionary over devices with all assigned keys
        - mousePosition: Dictionary over devices holding the positions on the screen when the button was pressed and released again as a numpy vector for all keys
    
    Methods:
        - initializeUnpressed: Set all keys as unpressed
        - createListOfUsedKeys: Creates a list of all keys which have bindings for all devices
        - createInverseMapping: Creates a list of all 
    
    
    """
    
    # Initialization
    def __init__(self):
        logger.debug('Create key bindings object')
        
        ###
        # Initialize dictionary
        self.keyBindings = dict()

        # All input devices
        self.inputDevices = ['Mouse', 'Keyboard']
        
        ###
        # Mouse control
        for device in self.inputDevices:
            self.keyBindings[device] = dict()
        
        # event.type == 5: MouseButtonDown
        # event.type == 6: MouseButtonUp
        # event.pos: Position
        self.keyBindings['Mouse']['LeftClick'] = pygame.BUTTON_LEFT
        self.keyBindings['Mouse']['RightClick'] = pygame.BUTTON_RIGHT
        
        self.keyBindings['Keyboard']['Space'] = pygame.K_SPACE
        
        
        # Initialize the other values
        self.initializeUnpressed()
        self.createListOfUsedKeys()
        self.createInverseMapping()
    


    # Initialize all keys as unpressed
    def initializeUnpressed(self) -> None:
        # Reset the dict
        self.keyPressed = dict()
        self.keyReleased = dict()
        
        self.mousePosition = dict()
        
        for device in self.inputDevices:
            self.keyPressed[device] = dict()
            self.keyReleased[device] = dict()

            self.mousePosition[device] = dict()
            
            for key in self.keyBindings[device].keys():
                self.keyPressed[device][key] = False
                self.keyReleased[device][key] = False
                
                self.mousePosition[device][key] = dict()
                self.mousePosition[device][key]['PositionPressed'] = np.array([0,0])
                self.mousePosition[device][key]['PositionReleased'] = np.array([0,0])


    # Create a list of all used keys
    def createListOfUsedKeys(self) -> None:
        # Reset the dict
        self.keysUsed = dict()

        for device in self.inputDevices:
            self.keysUsed[device] = list()
            
            for key in self.keyBindings[device].keys():
                self.keysUsed[device].append(self.keyBindings[device][key])
    
    
    # Create an inverse mapping
    def createInverseMapping(self) -> None:        
        # Reset the dict
        self.keyBindingsInverse = dict()

        for device in self.inputDevices:
            self.keyBindingsInverse[device] = {button: key for key, button in self.keyBindings[device].items()}
    

