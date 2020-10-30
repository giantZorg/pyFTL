###
#
# Define a class which contains the sprites for the energy ui elements
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
# Import ressources
from src.misc.helperfunctions import copySprite


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the wire ui images
class energyUiSprites(object):
    """
    
    Load or create the sprites for the energy management.
    
    Init:
        - parameters [Dict]: Dictionary containing all parameters
    
    Fields:
        - wires [Dict]: Dictionary containing all the loaded wire sprites with initial rect fields (-> not shifted)
        - bars [Dict]: Dictionary containing all the loaded bar sprites with initial rect fields (-> not shifted)
    
    Methods:
        - loadSprites(parameters [Dict]): Imports all the wire sprites and stores them in the dictionary self.wires
        - createBarSprites(parameters [Dict]): Creates all the bar sprites and stores them in the dictionary self.bars
    
    """
    
    
    ###
    # Initialization
    def __init__(self, parameters: Dict) -> None:
        logger.debug('Initialize the object holding all the energy ui images')
        
        ###
        # Initialize
        self.wires = dict()
        self.bars = dict()
                
        # Load all sprites
        self.loadSprites(parameters)
        
        # Create missing sprites
        self.createBarSprites(parameters)
    
    
    ###
    # Load sprites
    def loadSprites(self, parameters: Dict) -> None:
        logger.debug('Import the energy ui sprites')
        
        ##
        # Image are all of the same type
        pictureFormat = 'png'
        
        # Wires
        for fig in ['shortPath', 'shortEndPath', 'widePath', 'wideEndPath', 'UnderWeapons3', 'UnderWeapons4', 'ReactorFull']:
            self.wires[fig] = pygame.sprite.Sprite()
            self.wires[fig].image = pygame.image.load('{basepath}{wires}.{pictureFormat}'.format(basepath = parameters['EnergyManagementUi']['Wires']['Basepath'], wires = parameters['EnergyManagementUi']['Wires'][fig], pictureFormat = pictureFormat)).convert_alpha()
            self.wires[fig].rect = self.wires[fig].image.get_rect()
            
                    
        ##
        # Create a version for each power amount
        self.wires['ReactorPowerAvailable'] = dict()
        
        # Create a sprite for the stem
        reactorWireStem = pygame.Surface([self.wires['ReactorFull'].rect.width, parameters['EnergyManagementUi']['Wires']['PixelHeightStem']], pygame.SRCALPHA)
        reactorWireStem.blit(self.wires['ReactorFull'].image, [0,0], [0, self.wires['ReactorFull'].rect.height - parameters['EnergyManagementUi']['Wires']['PixelHeightStem'], self.wires['ReactorFull'].rect.width, parameters['EnergyManagementUi']['Wires']['PixelHeightStem']])
        
        reactorWireStemAlpha = pygame.surfarray.pixels_alpha(reactorWireStem)
        
        
        # Create a sprite to add one bar
        reactorWireAddBar = pygame.Surface([self.wires['ReactorFull'].rect.width, parameters['EnergyManagementUi']['Wires']['PixelHeightAdditionalBar']], pygame.SRCALPHA)
        reactorWireAddBar.blit(self.wires['ReactorFull'].image, [0,0], [0, 0, self.wires['ReactorFull'].rect.width, parameters['EnergyManagementUi']['Wires']['PixelHeightAdditionalBar']])
        
        # Correct alphas
        reactorWireAddBarAlpha = pygame.surfarray.pixels_alpha(reactorWireAddBar)
        for i in range(4,18):
            reactorWireAddBarAlpha[i, i+5] = int(reactorWireAddBarAlpha[i, i+5] * 0.65)
        
        reactorWireAddBarAlpha[20, 25] = 75
        reactorWireAddBarAlpha[21, 26] = 58
        reactorWireAddBarAlpha[22, 27] = 42
        reactorWireAddBarAlpha[23, 28] = 28
        
        for i in range(0, 19):
            for j in range(11+i, 30):
                reactorWireAddBarAlpha[i,j] = 0

        for i in range(10, 18):
            reactorWireAddBarAlpha[i, i+10] = reactorWireAddBarAlpha[i, i+9]

        
        # Fix the stem alphas
        for i in range(0, 4):
            reactorWireStemAlpha[:,i] = reactorWireAddBarAlpha[:,i+8].copy()
            
        for i in range(4, 14):
            reactorWireStemAlpha[i+7:, i] = reactorWireAddBarAlpha[i+7:, i+8].copy()
            
        for i in range(14, 17):
            reactorWireStemAlpha[20:, i] = reactorWireAddBarAlpha[20:, i+8].copy()  
            
        del(reactorWireStemAlpha)
        del(reactorWireAddBarAlpha)
                 
        # Create first one
        self.wires['ReactorPowerAvailable'][1] = pygame.sprite.Sprite()
        self.wires['ReactorPowerAvailable'][1].image = reactorWireStem.copy()
        self.wires['ReactorPowerAvailable'][1].image = self.wires['ReactorPowerAvailable'][1].image.convert_alpha()
        self.wires['ReactorPowerAvailable'][1].rect = self.wires['ReactorPowerAvailable'][1].image.get_rect()
        
        for i in range(2, parameters['General']['MaxReactorPowerPossible']+1):
            self.wires['ReactorPowerAvailable'][i] = pygame.sprite.Sprite()
#            if i == 2:
#                self.wires['ReactorPowerAvailable'][i].image = pygame.Surface([self.wires['ReactorPowerAvailable'][i-1].rect.width, self.wires['ReactorPowerAvailable'][i-1].rect.height + reactorWireAddBar.get_rect().height - 20], pygame.SRCALPHA)
#            else:
            self.wires['ReactorPowerAvailable'][i].image = pygame.Surface([self.wires['ReactorPowerAvailable'][i-1].rect.width, self.wires['ReactorPowerAvailable'][i-1].rect.height + reactorWireAddBar.get_rect().height - 21], pygame.SRCALPHA)

            self.wires['ReactorPowerAvailable'][i].image.blit(self.wires['ReactorPowerAvailable'][i-1].image, [0, reactorWireAddBar.get_rect().height - 21])

            self.wires['ReactorPowerAvailable'][i].image.blit(reactorWireAddBar, [0, -8])
            self.wires['ReactorPowerAvailable'][i].image = self.wires['ReactorPowerAvailable'][i].image.convert_alpha()
            self.wires['ReactorPowerAvailable'][i].rect = self.wires['ReactorPowerAvailable'][i].image.get_rect()
        
        
        ## 
        # Create grey versions for all the sprites
        for fig in ['shortPath', 'shortEndPath', 'widePath', 'wideEndPath', 'UnderWeapons3', 'UnderWeapons4']:
            self.wires[fig + 'Grey'] = copySprite(self.wires[fig])
            
            pixelValues = pygame.surfarray.pixels3d(self.wires[fig + 'Grey'].image)
            pixelValues //= 2
            
            del(pixelValues)
        
        self.wires['ReactorPowerAvailableGrey'] = dict()
        for fig in self.wires['ReactorPowerAvailable'].keys():
            self.wires['ReactorPowerAvailableGrey'][fig] = copySprite(self.wires['ReactorPowerAvailable'][fig])
        
            pixelValues = pygame.surfarray.pixels3d(self.wires['ReactorPowerAvailableGrey'][fig].image)
            pixelValues //= 2

            del(pixelValues)        

    
    ###
    # Create bars
    def createBarSprites(self, parameters: Dict) -> None:
        logger.debug('Create the energy bar sprites')

        ##
        # Wide bars
        
        # Power available
        self.bars['WideGreen'] = pygame.sprite.Sprite()
        self.bars['WideGreen'].image = pygame.Surface([parameters['General']['WideBarLength'], parameters['General']['WideBarHeight']])
        self.bars['WideGreen'].image.fill(parameters['Colors']['SystemGreen'])
        self.bars['WideGreen'].rect = self.bars['WideGreen'].image.get_rect()
        self.bars['WideGreen'].image = self.bars['WideGreen'].image.convert_alpha()

        # Power blocked by an event
        innerSurfaceWide = pygame.Surface([parameters['General']['WideBarLength'] - 2, parameters['General']['WideBarHeight'] - 2])
        innerSurfaceWide.fill(parameters['Colors']['Black'])

        greenSurfaceWide = pygame.Surface([parameters['General']['WideBarLength'] - 4, parameters['General']['WideBarHeight'] - 4])
        greenSurfaceWide.fill(parameters['Colors']['SystemGreen'])

        # Blocked power        
        self.bars['WideBlocked'] = pygame.sprite.Sprite()
        self.bars['WideBlocked'].image = pygame.Surface([parameters['General']['WideBarLength'], parameters['General']['WideBarHeight']])
        self.bars['WideBlocked'].image.fill(parameters['Colors']['BlockedBlue'])
        self.bars['WideBlocked'].image.blit(innerSurfaceWide, [1,1])
        
        self.bars['WideBlocked'].image.set_colorkey(parameters['Colors']['Black'])
        pygame.draw.line(self.bars['WideBlocked'].image, parameters['Colors']['BlockedBlue'], [parameters['General']['WideBarLength']-1, 0], [0, parameters['General']['WideBarHeight']-1])
        
        self.bars['WideBlocked'].image = self.bars['WideBlocked'].image.convert_alpha()
        self.bars['WideBlocked'].rect = self.bars['WideBlocked'].image.get_rect()
        
        # Power used
        self.bars['WideUsed'] = pygame.sprite.Sprite()
        self.bars['WideUsed'].image = pygame.Surface([parameters['General']['WideBarLength'], parameters['General']['WideBarHeight']])
        self.bars['WideUsed'].image.fill(parameters['Colors']['White'])
        self.bars['WideUsed'].image.blit(innerSurfaceWide, [1,1])
        
        self.bars['WideUsed'].image.set_colorkey(parameters['Colors']['Black'])
        self.bars['WideUsed'].image = self.bars['WideUsed'].image.convert_alpha()
        self.bars['WideUsed'].rect = self.bars['WideUsed'].image.get_rect()
        
        # Backup battery power
        self.bars['WideBackup'] = pygame.sprite.Sprite()
        self.bars['WideBackup'].image = pygame.Surface([parameters['General']['WideBarLength'], parameters['General']['WideBarHeight']])
        self.bars['WideBackup'].image.fill(parameters['Colors']['BackupBatteryBrown'])
        self.bars['WideBackup'].image.blit(greenSurfaceWide, [2,2])
        
        self.bars['WideBackup'].image.set_colorkey(parameters['Colors']['White'])
        self.bars['WideBackup'].image = self.bars['WideBackup'].image.convert_alpha()
        self.bars['WideBackup'].rect = self.bars['WideBackup'].image.get_rect()
        
        
        
        ##
        # Short bars for above the symbols
        
        # Power in the system
        self.bars['ShortGreen'] = pygame.sprite.Sprite()
        self.bars['ShortGreen'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortGreen'].image.fill(parameters['Colors']['SystemGreen'])
        self.bars['ShortGreen'].rect = self.bars['ShortGreen'].image.get_rect()
        self.bars['ShortGreen'].image = self.bars['ShortGreen'].image.convert_alpha()

        # Zoltan power in the system
        self.bars['ShortYellow'] = pygame.sprite.Sprite()
        self.bars['ShortYellow'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortYellow'].image.fill(parameters['Colors']['ZoltanYellow'])
        self.bars['ShortYellow'].rect = self.bars['ShortYellow'].image.get_rect()
        self.bars['ShortYellow'].image = self.bars['ShortYellow'].image.convert_alpha()

        # Ionized power in the system
        self.bars['ShortBlue'] = pygame.sprite.Sprite()
        self.bars['ShortBlue'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortBlue'].image.fill(parameters['Colors']['IonBlue'])
        self.bars['ShortBlue'].rect = self.bars['ShortBlue'].image.get_rect()
        self.bars['ShortBlue'].image = self.bars['ShortBlue'].image.convert_alpha()

        # Power locked by cooldown
        self.bars['ShortWhite'] = pygame.sprite.Sprite()
        self.bars['ShortWhite'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortWhite'].image.fill(parameters['Colors']['White'])
        self.bars['ShortWhite'].rect = self.bars['ShortWhite'].image.get_rect()
        self.bars['ShortWhite'].image = self.bars['ShortWhite'].image.convert_alpha()

        # Power not assigned to the system
        innerSurfaceShort = pygame.Surface([parameters['General']['ShortBarLength'] - 2, parameters['General']['ShortBarHeight'] - 2])
        innerSurfaceShort.fill(parameters['Colors']['Black'])

        self.bars['ShortUnassigned'] = pygame.sprite.Sprite()
        self.bars['ShortUnassigned'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortUnassigned'].image.fill(parameters['Colors']['White'])
        self.bars['ShortUnassigned'].image.blit(innerSurfaceShort, [1,1])
        
        self.bars['ShortUnassigned'].image.set_colorkey(parameters['Colors']['Black'])
        self.bars['ShortUnassigned'].image = self.bars['ShortUnassigned'].image.convert_alpha()
        self.bars['ShortUnassigned'].rect = self.bars['ShortUnassigned'].image.get_rect()

        # Blocked power by events    
        self.bars['ShortBlocked'] = pygame.sprite.Sprite()
        self.bars['ShortBlocked'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortBlocked'].image.fill(parameters['Colors']['BlockedBlue'])
        self.bars['ShortBlocked'].image.blit(innerSurfaceShort, [1,1])
        
        self.bars['ShortBlocked'].image.set_colorkey(parameters['Colors']['Black'])
        pygame.draw.line(self.bars['ShortBlocked'].image, parameters['Colors']['BlockedBlue'], [parameters['General']['ShortBarLength']-1, 0], [0, parameters['General']['ShortBarHeight']-1])
        
        self.bars['ShortBlocked'].image = self.bars['ShortBlocked'].image.convert_alpha()
        self.bars['ShortBlocked'].rect = self.bars['ShortBlocked'].image.get_rect()

        # System damaged
        self.bars['ShortDamaged'] = pygame.sprite.Sprite()
        self.bars['ShortDamaged'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortDamaged'].image.fill(parameters['Colors']['DamageRed'])
        self.bars['ShortDamaged'].image.blit(innerSurfaceShort, [1,1])
        
        self.bars['ShortDamaged'].image.set_colorkey(parameters['Colors']['Black'])
        pygame.draw.line(self.bars['ShortDamaged'].image, parameters['Colors']['DamageRed'], [parameters['General']['ShortBarLength']-1, 0], [0, parameters['General']['ShortBarHeight']-1])
        
        self.bars['ShortDamaged'].image = self.bars['ShortDamaged'].image.convert_alpha()
        self.bars['ShortDamaged'].rect = self.bars['ShortDamaged'].image.get_rect()

        # Backup battery power
        greenSurfaceShort = pygame.Surface([parameters['General']['ShortBarLength'] - 4, parameters['General']['ShortBarHeight'] - 4])
        greenSurfaceShort.fill(parameters['Colors']['SystemGreen'])

        self.bars['ShortBackup'] = pygame.sprite.Sprite()
        self.bars['ShortBackup'].image = pygame.Surface([parameters['General']['ShortBarLength'], parameters['General']['ShortBarHeight']])
        self.bars['ShortBackup'].image.fill(parameters['Colors']['BackupBatteryBrown'])
        self.bars['ShortBackup'].image.blit(greenSurfaceShort, [2,2])
        
        self.bars['ShortBackup'].image.set_colorkey(parameters['Colors']['White'])
        self.bars['ShortBackup'].image = self.bars['ShortBackup'].image.convert_alpha()
        self.bars['ShortBackup'].rect = self.bars['ShortBackup'].image.get_rect()
        

















































