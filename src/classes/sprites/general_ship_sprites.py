###
#
# Define a class which contains sprites for all the ships
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
# Define the class for the ship images
class generalShipSprites(object):
    """
    
    Load the sprites used for all ships.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - consoleSprites [Dict]: Dictionary containing all the loaded console sprites with initial rect fields (-> not shifted)
        - roomSprites [Dict]: Dictionary containing all the loaded room sprites with initial rect fields (-> not shifted)
        - symbolSprites [Dict]: Dictionary containing all the loaded symbol sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadConsoleSprites(parameters [Dict]): Imports all the console sprites and stores them in the dictionary self.consoleSprites
        - loadRoomSprites(parameters [Dict]): Imports all the console sprites and stores them in the dictionary self.roomSprites
        - loadSymbolSprites(parameters [Dict]): Imports all the console sprites and stores them in the dictionary self.symbolSprites
    
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding the general ship sprites')
        
        ###
        # Initialize dictionaries
        self.roomSprites = dict()
        self.symbolSprites = dict()
        self.consoleSprites = dict()
        
        ###
        # Load the different sprites
        
        # Load all room sprites
        self.loadRoomSprites(parameters)
        
        # Load all symbol sprites
        self.loadSymbolSprites(parameters)
        
        # Load all console sprites
        self.loadConsoleSprites(parameters)


    ###
    # Function to load all the console sprites
    def loadConsoleSprites(self, parameters: Dict) -> None:
        logger.debug('Import the console sprites')
        
        # Load console for enemy ships
        self.consoleSprites['Console'] = pygame.sprite.Sprite()
        self.consoleSprites['Console'].image = pygame.image.load('{basepath}{console}'.format(basepath = parameters['GeneralShipSprites']['ConsoleSprites']['Basepath'], console = parameters['GeneralShipSprites']['ConsoleSprites']['Console'])).convert_alpha()
        self.consoleSprites['Console'].rect = self.consoleSprites['Console'].image.get_rect()
        
        self.consoleSprites['Console'].image.set_colorkey(parameters['Colors']['White'])
        
        # System console glow
        self.consoleSprites['ConsoleSystems'] = dict()
        for level in parameters['GeneralShipSprites']['ConsoleSprites']['ConsoleSystems'].keys():
            self.consoleSprites['ConsoleSystems'][level] = pygame.sprite.Sprite()
            self.consoleSprites['ConsoleSystems'][level].image = pygame.image.load('{basepath}{consoleSystems}'.format(basepath = parameters['GeneralShipSprites']['ConsoleSprites']['Basepath'], consoleSystems = parameters['GeneralShipSprites']['ConsoleSprites']['ConsoleSystems'][level])).convert_alpha()
            self.consoleSprites['ConsoleSystems'][level].rect = self.consoleSprites['ConsoleSystems'][level].image.get_rect()
            
            self.consoleSprites['ConsoleSystems'][level].image.set_colorkey(parameters['Colors']['White'])

        # Pilot console glow
        self.consoleSprites['ConsolePilot'] = dict()
        for level in parameters['GeneralShipSprites']['ConsoleSprites']['ConsolePilot'].keys():
            self.consoleSprites['ConsolePilot'][level] = pygame.sprite.Sprite()
            self.consoleSprites['ConsolePilot'][level].image = pygame.image.load('{basepath}{consolePilot}'.format(basepath = parameters['GeneralShipSprites']['ConsoleSprites']['Basepath'], consolePilot = parameters['GeneralShipSprites']['ConsoleSprites']['ConsolePilot'][level])).convert_alpha()
            self.consoleSprites['ConsolePilot'][level].rect = self.consoleSprites['ConsolePilot'][level].image.get_rect()
            
            self.consoleSprites['ConsolePilot'][level].image.set_colorkey(parameters['Colors']['White'])
        

    ###
    # Function to load all the room sprites
    def loadRoomSprites(self, parameters: Dict) -> None:
        logger.debug('Import the room sprites')
        
        for system in parameters['GeneralShipSprites']['RoomSprites']['Paths'].keys():
            if system == 'Basepath':    # Not a system
                continue
        
            ##
            # Initialize dictionary
            self.roomSprites[system] = dict()

            ##
            # First the special cases teleporter and clone bay, then the others
            if system == 'CrewTeleporter':
                self.roomSprites[system]['Room'] = pygame.sprite.Sprite()
                self.roomSprites[system]['Room'].image = pygame.image.load('{basepath}{room}'.format(basepath = parameters['GeneralShipSprites']['RoomSprites']['Paths']['Basepath'], room = parameters['GeneralShipSprites']['RoomSprites']['Paths'][system]['Room'])).convert_alpha()
                self.roomSprites[system]['Room'].rect = self.roomSprites[system]['Room'].image.get_rect()
                
                self.roomSprites[system]['Room'].image.set_colorkey(parameters['Colors']['White'])
                
            elif system == 'Clonebay':
                self.roomSprites[system]['Room'] = list()
                
                for spritePath in parameters['GeneralShipSprites']['RoomSprites']['Paths'][system]['Room']:
                    self.roomSprites[system]['Room'].append(pygame.sprite.Sprite())
                    self.roomSprites[system]['Room'][-1].image = pygame.image.load('{basepath}{spritePath}'.format(basepath = parameters['GeneralShipSprites']['RoomSprites']['Paths']['Basepath'], spritePath = spritePath)).convert_alpha()
                    self.roomSprites[system]['Room'][-1].rect = self.roomSprites[system]['Room'][-1].image.get_rect()
                
                    self.roomSprites[system]['Room'][-1].image.set_colorkey(parameters['Colors']['White'])
                
            else:
                self.roomSprites[system]['Room4'] = list()
                self.roomSprites[system]['Room2'] = list()

                for spritePath in parameters['GeneralShipSprites']['RoomSprites']['Paths'][system]['Room4']:
                    self.roomSprites[system]['Room4'].append(pygame.sprite.Sprite())
                    self.roomSprites[system]['Room4'][-1].image = pygame.image.load('{basepath}{spritePath}'.format(basepath = parameters['GeneralShipSprites']['RoomSprites']['Paths']['Basepath'], spritePath = spritePath)).convert_alpha()
                    self.roomSprites[system]['Room4'][-1].rect = self.roomSprites[system]['Room4'][-1].image.get_rect()
                
                    self.roomSprites[system]['Room4'][-1].image.set_colorkey(parameters['Colors']['White'])

                for spritePath in parameters['GeneralShipSprites']['RoomSprites']['Paths'][system]['Room2']:
                    self.roomSprites[system]['Room2'].append(pygame.sprite.Sprite())
                    self.roomSprites[system]['Room2'][-1].image = pygame.image.load('{basepath}{spritePath}'.format(basepath = parameters['GeneralShipSprites']['RoomSprites']['Paths']['Basepath'], spritePath = spritePath)).convert_alpha()
                    self.roomSprites[system]['Room2'][-1].rect = self.roomSprites[system]['Room2'][-1].image.get_rect()
                
                    self.roomSprites[system]['Room2'][-1].image.set_colorkey(parameters['Colors']['White'])
    
    
    ###
    # Function to load all the symbol sprites
    def loadSymbolSprites(self, parameters: Dict) -> None:
        logger.debug('Import the symbol sprites')
        
        ###
        # Always the same format
        pictureFormat = 'png'

        for system in parameters['GeneralShipSprites']['SymbolSprites']['Paths'].keys():
            ##
            # Initialize dictionary
            self.symbolSprites[system] = dict()
            
            # Load in system sprites
            for spriteName in parameters['GeneralShipSprites']['SymbolSprites']['SpriteSuffix'].keys():
                self.symbolSprites[system][spriteName] = pygame.sprite.Sprite()
                self.symbolSprites[system][spriteName].image = pygame.image.load('{basepath}{spritePrefix}{system}{spriteSuffix}.{pictureFormat}'.format(basepath = parameters['GeneralShipSprites']['SymbolSprites']['Basepath'], spritePrefix = parameters['GeneralShipSprites']['SymbolSprites']['SpritePrefix'], system = parameters['GeneralShipSprites']['SymbolSprites']['Paths'][system], spriteSuffix = parameters['GeneralShipSprites']['SymbolSprites']['SpriteSuffix'][spriteName], pictureFormat = pictureFormat)).convert_alpha()
                self.symbolSprites[system][spriteName].rect = self.symbolSprites[system][spriteName].image.get_rect()
            
            # Add grey overlay
            self.symbolSprites[system]['OverlayGrey'] = pygame.sprite.Sprite()
            self.symbolSprites[system]['OverlayGrey'].image = self.symbolSprites[system]['Overlay'].image.copy()
            self.symbolSprites[system]['OverlayGrey'].rect = self.symbolSprites[system]['OverlayGrey'].image.get_rect()

            bildPixel = pygame.surfarray.pixels3d(self.symbolSprites[system]['OverlayGrey'].image)
            for i in range(0, 3):
                bildPixel[bildPixel[:,:,i] == 255, i] = parameters['Colors']['GreySystem'][i]

            del bildPixel
            

            # Add orange overlay
            self.symbolSprites[system]['OverlayOrange'] = pygame.sprite.Sprite()
            self.symbolSprites[system]['OverlayOrange'].image = self.symbolSprites[system]['Overlay'].image.copy()
            self.symbolSprites[system]['OverlayOrange'].rect = self.symbolSprites[system]['OverlayOrange'].image.get_rect()

            bildPixel = pygame.surfarray.pixels3d(self.symbolSprites[system]['OverlayOrange'].image)
            for i in range(0, 3):
                bildPixel[bildPixel[:,:,i] == 255, i] = parameters['Colors']['OrangeSystem'][i]

            del bildPixel
            
            
            # Add red overlay
            self.symbolSprites[system]['OverlayRed'] = pygame.sprite.Sprite()
            self.symbolSprites[system]['OverlayRed'].image = self.symbolSprites[system]['Overlay'].image.copy()
            self.symbolSprites[system]['OverlayRed'].rect = self.symbolSprites[system]['OverlayRed'].image.get_rect()

            bildPixel = pygame.surfarray.pixels3d(self.symbolSprites[system]['OverlayRed'].image)
            for i in range(0, 3):
                bildPixel[bildPixel[:,:,i] == 255, i] = parameters['Colors']['RedSystem'][i]

            del bildPixel
            
            
            # Add blue (ionized) overlay
            self.symbolSprites[system]['OverlayBlue'] = pygame.sprite.Sprite()
            self.symbolSprites[system]['OverlayBlue'].image = self.symbolSprites[system]['Overlay'].image.copy()
            self.symbolSprites[system]['OverlayBlue'].rect = self.symbolSprites[system]['OverlayBlue'].image.get_rect()

            bildPixel = pygame.surfarray.pixels3d(self.symbolSprites[system]['OverlayBlue'].image)
            for i in range(0, 3):
                bildPixel[bildPixel[:,:,i] == 255, i] = parameters['Colors']['BlueSystem'][i]

            del bildPixel



















