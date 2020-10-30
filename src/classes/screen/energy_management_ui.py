###
#
# Define a class for the player energy management and corresponding UI
#
###


###
# Load packages

# Logging
import logging

# Typing
from typing import Dict

# Arrays and matrices
import numpy as np

# Pygame
import pygame

# Proper copies
import copy


###
# Load ressources

# Ships
import src.classes.ships.player_ship as playerShip

# Helperfunctions
from src.misc.helperfunctions import copySprite, powerBarsMainSystem


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the energy management ui
class energyManagementUi(object):
    """
    
    Object which controls the UI-elements corresponding to energy management.
    
    Fields:
        - parameters [Dict]: All loaded parameters
        - spritesAll [Dict]: All loaded sprites

        - energySystemsRectMatrix [np.matrix]: Matrix of all system rects for the energy management ui
        - energySystemsForRects [np.array]: Vector of the systems corresponding to the energySystemsRectMatrix rows
    
    
    """
    
    ###
    # Initialization
    def __init__(self, parameters: Dict, spritesAll: Dict, activePlayerShip: playerShip.playerShip) -> None:
        logger.debug('Initialize the energy management ui object')
        
        ###
        # Save references to the passed parameters
        self.parameters = parameters
        self.spritesAll = spritesAll
        self.activePlayerShip = activePlayerShip
        
        self.uiSprites = list()
                
        
        ###
        # Initialize dictionary
        self.energySystemsRectMatrix = dict()
        
    
    ###
    # Function that selects and returns the appropriate sprites for the power ui
    def updateScreenSprites(self, screenRect: pygame.Rect, saveRects: bool = False) -> None:
        ###
        # screenRect is the rect of the screen given by screen.get_rect()
        # screenRect = screen.get_rect()
        #
        # saveRects: When true, then the rects for the control are saved. Should only be called initially or when systems are added
        
        
        ###
        # Delete and reinitialize the list with the sprites to be returned
        del self.uiSprites
        uiSprites = list()
        
        
        ###
        # Set the necessary values
        
        # Reactor power
        totalReactorPower = self.activePlayerShip.reactor['SystemPower'] + self.activePlayerShip.reactor['SystemBackupPower']
        totalBlockedPower = self.activePlayerShip.reactor['PowerBlocked']
        totalAvailableNormalPower = self.activePlayerShip.reactor['PowerAvailable'] - self.activePlayerShip.reactor['BackupPowerAvailable']
        totalAvailableBackupPower = self.activePlayerShip.reactor['BackupPowerAvailable']
        
        totalAvailablePower = totalAvailableNormalPower + totalAvailableBackupPower
        
        # Used power
        totalUsedPower = totalReactorPower - totalBlockedPower - totalAvailablePower
        
        screenOffset = screenRect.bottomleft + self.parameters['General']['UiWiresOffsetBottomLeft']
        
        screenOffsetWires = np.array(screenOffset.copy())
        screenOffsetWires[1] -= self.parameters['General']['UiWiresOffset']
        
        
        ###
        # Add the reactor sprites to the output list
        if totalUsedPower == 0: # No power used, no grey wires needed
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['ReactorPowerAvailable'][totalReactorPower]))
            uiSprites[-1].rect.bottomleft = screenOffset
            
            greyWires = ''
        elif totalAvailablePower: # Power available: Both white and grey wires
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['ReactorPowerAvailableGrey'][totalReactorPower]))
            uiSprites[-1].rect.bottomleft = screenOffset
            
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['ReactorPowerAvailable'][totalAvailablePower]))
            uiSprites[-1].rect.bottomleft = screenOffset
            
            greyWires = ''
        else:   # No power available
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['ReactorPowerAvailableGrey'][totalReactorPower]))
            uiSprites[-1].rect.bottomleft = screenOffset

            greyWires = 'Grey'

        # Pixel offset to add the next wire or symbol
        pixelOffset = uiSprites[-1].rect.width
        pixelOffsetSymbols = np.array(uiSprites[-1].rect.width)
        
        
        ###
        # Add power bars
        barOffset = 0
        screenBarOffset = screenRect.bottomleft + self.parameters['General']['UiWiresOffsetReactorBar']
        
        # Normal available power
        for i in range(0, totalAvailableNormalPower):
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars['WideGreen']))
            uiSprites[-1].rect.bottomleft = screenBarOffset.copy()
            uiSprites[-1].rect.y -= barOffset
            
            barOffset += uiSprites[-1].rect.height + self.parameters['General']['BarPixelsSkip']
            
        # Backup battery available power
        for i in range(0, totalAvailableBackupPower):
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars['WideBackup']))
            uiSprites[-1].rect.bottomleft = screenBarOffset.copy()
            uiSprites[-1].rect.y -= barOffset
            
            barOffset += uiSprites[-1].rect.height + self.parameters['General']['BarPixelsSkip']

        # Power used
        for i in range(0, totalUsedPower):
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars['WideUsed']))
            uiSprites[-1].rect.bottomleft = screenBarOffset.copy()
            uiSprites[-1].rect.y -= barOffset
            
            barOffset += uiSprites[-1].rect.height + self.parameters['General']['BarPixelsSkip']

        # Blocked power
        for i in range(0, totalBlockedPower):
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars['WideBlocked']))
            uiSprites[-1].rect.bottomleft = screenBarOffset.copy()
            uiSprites[-1].rect.y -= barOffset
            
            barOffset += uiSprites[-1].rect.height + self.parameters['General']['BarPixelsSkip']        


        ###
        # Add system wires
        presentSystems = list(self.activePlayerShip.systemsPresent)
        systemsInDrawingOrder = list()
        for system in self.parameters['General']['UiMainSystemOrder']:
            if system in presentSystems:
                systemsInDrawingOrder.append(system)
        
        if saveRects:
            systemRectVector = list()
            systemRectList = list()
        
        # Go through all the systems but the last one
        for index, system in enumerate(systemsInDrawingOrder[0:-1]):
            ###
            # Add the wires
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires[self.parameters['EnergyManagementUi']['Wires']['TypePerSystem'][system] + 'Path' + greyWires]))
            uiSprites[-1].rect.bottomleft = screenOffsetWires
            uiSprites[-1].rect.x += pixelOffset
            
            pixelOffset += uiSprites[-1].rect.width
            
            
            ###
            # Add the symbol
            
            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols
                if index == 0:
                    uiSprites[-1].rect.x += self.parameters['General']['UiEnergyWeaponSymbolFirst']
                
                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)
                
                pixelOffsetSymbols += uiSprites[-2].rect.width
            else:
                logger.warning('Symbol for ionized systems not implemented yet')
                pixelOffsetSymbols += uiSprites[-1].rect.width
            
            
            ###
            # Add the energy bars
            powerBars = powerBarsMainSystem(copy.deepcopy(systemInformation))
            symbolRect = np.array(uiSprites[-1].rect.topleft) + self.parameters['General']['UiEnergyBarsOffset']
            
            offsetBar = 0
            for index, bar in enumerate(powerBars):
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars[bar]))
                uiSprites[-1].rect.bottomleft = symbolRect
                uiSprites[-1].rect.y -= offsetBar
                
                if system == 'Shields':
                    offsetBar += self.parameters['General']['BarPixelsSkipShields'][index % 2] + uiSprites[-1].rect.height
                else:
                    offsetBar += self.parameters['General']['BarPixelsSkip'] + uiSprites[-1].rect.height
            

        # Last system: Sprites depends on whether drone control is present or not
        system = systemsInDrawingOrder[-1]
        if 'DroneControl' in presentSystems:
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires[self.parameters['EnergyManagementUi']['Wires']['TypePerSystem'][system] + 'Path' + greyWires]))
            uiSprites[-1].rect.bottomleft = screenOffsetWires
            uiSprites[-1].rect.x += pixelOffset

            pixelOffset += uiSprites[-1].rect.width

            ###
            # Add the symbol
            
            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols

                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)
                
                pixelOffsetSymbols += uiSprites[-2].rect.width
            else:
                logger.warning('Symbol for ionized systems not implemented yet')
                pixelOffsetSymbols += uiSprites[-1].rect.width


            ###
            # Add the energy bars
            powerBars = powerBarsMainSystem(copy.deepcopy(systemInformation))
            symbolRect = np.array(uiSprites[-1].rect.topleft) + self.parameters['General']['UiEnergyBarsOffset']
            
            offsetBar = 0
            for index, bar in enumerate(powerBars):
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars[bar]))
                uiSprites[-1].rect.bottomleft = symbolRect
                uiSprites[-1].rect.y -= offsetBar
                
                if system == 'Shields':
                    offsetBar += self.parameters['General']['BarPixelsSkipShields'][index % 2] + uiSprites[-1].rect.height
                else:
                    offsetBar += self.parameters['General']['BarPixelsSkip'] + uiSprites[-1].rect.height

            
            ###
            # Add the weapons
            system = 'WeaponControl'

            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols

                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)
            else:
                logger.warning('Symbol for ionized systems not implemented yet')


            ###
            # Add the energy bars
            powerBars = powerBarsMainSystem(copy.deepcopy(systemInformation))
            symbolRect = np.array(uiSprites[-1].rect.topleft) + self.parameters['General']['UiEnergyBarsOffset']
            
            offsetBar = 0
            for index, bar in enumerate(powerBars):
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars[bar]))
                uiSprites[-1].rect.bottomleft = symbolRect
                uiSprites[-1].rect.y -= offsetBar
                
                if system == 'Shields':
                    offsetBar += self.parameters['General']['BarPixelsSkipShields'][index % 2] + uiSprites[-1].rect.height
                else:
                    offsetBar += self.parameters['General']['BarPixelsSkip'] + uiSprites[-1].rect.height
                            
            
            # Add drone control wire
            if self.activePlayerShip.weapons['WeaponSlotsAvailable'] == 3:
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['UnderWeapons3' + greyWires]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires
                uiSprites[-1].rect.x += pixelOffset

            elif self.activePlayerShip.weapons['WeaponSlotsAvailable'] == 4:
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires['UnderWeapons4' + greyWires]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires
                uiSprites[-1].rect.x += pixelOffset

            else:
                # Other number of weapons not implemented yet
                raise AssertionError('Ui for the given number of weapons {} not defined yet'.format(str()))

            pixelOffsetSymbols += uiSprites[-1].rect.width

            
            ##
            # Add the drone control
            system = 'DroneControl'

            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols + self.parameters['General']['UiEnergyWeaponSymbolCorrection']

                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)
            else:
                logger.warning('Symbol for ionized systems not implemented yet')


            ###
            # Add the energy bars
            powerBars = powerBarsMainSystem(copy.deepcopy(systemInformation))
            symbolRect = np.array(uiSprites[-1].rect.topleft) + self.parameters['General']['UiEnergyBarsOffset']
            
            offsetBar = 0
            for index, bar in enumerate(powerBars):
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars[bar]))
                uiSprites[-1].rect.bottomleft = symbolRect
                uiSprites[-1].rect.y -= offsetBar
                
                if system == 'Shields':
                    offsetBar += self.parameters['General']['BarPixelsSkipShields'][index % 2] + uiSprites[-1].rect.height
                else:
                    offsetBar += self.parameters['General']['BarPixelsSkip'] + uiSprites[-1].rect.height
            
        else:
            ###
            # Add the wire
            uiSprites.append(copySprite(self.spritesAll['EnergyUi'].wires[self.parameters['EnergyManagementUi']['Wires']['TypePerSystem'][system] + 'EndPath' + greyWires]))
            uiSprites[-1].rect.bottomleft = screenOffsetWires
            uiSprites[-1].rect.x += pixelOffset


            ###
            # Add the symbol
            
            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols

                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)
                
                pixelOffsetSymbols += uiSprites[-2].rect.width
            else:
                logger.warning('Symbol for ionized systems not implemented yet')
                pixelOffsetSymbols += uiSprites[-1].rect.width

            
            ###
            # Then add the weapon system
            system = 'WeaponControl'

            # Get system color
            systemInformation = self.activePlayerShip.systems[system]
            suffix = '2' if system in self.parameters['General']['SubSystems'] else ''
            if systemInformation['IonCharges']:
                colorSymbol = 'Ionized'
            elif systemInformation['Destroyed']:
                colorSymbol = 'Red' + suffix
            elif systemInformation['Damaged']:
                colorSymbol = 'Orange' + suffix
            elif systemInformation['PowerCurrent']:
                colorSymbol = 'Green' + suffix
            else:
                colorSymbol = 'Grey' + suffix
            
            if colorSymbol != 'Ionized':
                uiSprites.append(copySprite(self.spritesAll['GeneralShip'].symbolSprites[system][colorSymbol]))
                uiSprites[-1].rect.bottomleft = screenOffsetWires + self.parameters['General']['UiEnergySymbolsOffset']
                uiSprites[-1].rect.x += pixelOffsetSymbols + self.parameters['General']['UiEnergyWeaponSymbolCorrection']

                if saveRects:
                    systemRectVector.append(system)
                    systemRectList.append(uiSprites[-1].rect)

            else:
                logger.warning('Symbol for ionized systems not implemented yet')


            ###
            # Add the energy bars
            powerBars = powerBarsMainSystem(copy.deepcopy(systemInformation))
            symbolRect = np.array(uiSprites[-1].rect.topleft) + self.parameters['General']['UiEnergyBarsOffset']
            
            offsetBar = 0
            for index, bar in enumerate(powerBars):
                uiSprites.append(copySprite(self.spritesAll['EnergyUi'].bars[bar]))
                uiSprites[-1].rect.bottomleft = symbolRect
                uiSprites[-1].rect.y -= offsetBar
                
                if system == 'Shields':
                    offsetBar += self.parameters['General']['BarPixelsSkipShields'][index % 2] + uiSprites[-1].rect.height
                else:
                    offsetBar += self.parameters['General']['BarPixelsSkip'] + uiSprites[-1].rect.height
                    
        
        if saveRects:
            self.energySystemsForRects = np.array(systemRectVector)
            self.energySystemsRectMatrix = np.array(systemRectList)

            # Save the center point of the symbols to check whether they have been clicked on in the main loop
            self.energySystemsRectCenters = np.array([rect.center for rect in systemRectList])

            # Reference the Rects also in the player ship
            self.activePlayerShip.energySystemsForRects = self.energySystemsForRects
            self.activePlayerShip.energySystemsRectMatrix = self.energySystemsRectMatrix
            self.activePlayerShip.energySystemsRectCenters = self.energySystemsRectCenters
            
        
        ###
        # Add the subsystems
            

        
        ###
        # Save the list
        self.uiSprites = uiSprites

























