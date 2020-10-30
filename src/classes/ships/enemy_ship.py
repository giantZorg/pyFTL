###
#
# Define a class for the enemy ship based on the class for all ships
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


###
# Load ressources
import src.classes.ships.base_ship as baseShip


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Define the class for the player ship
class enemyShip(baseShip.baseShip):
    """
    
    Class for the player ship. After initialization, variables can still be set.
    After this, the ship will be finally constructed using the inherited shipSetup() method.
    
    Initialization:
        - parameters [Dict]: All loaded parameters
        - spritesAll [Dict]: All loaded sprites
        - ship [str]: Selected ship
        - variant [str]: Selected ship variant
        
    
    Fields:
        - parameters: Reference to all parameters
        - spritesAll: Reference to the loaded sprites
        
        - ship: Ship selection
        - variant: Ship variant selection
        
        - playerShip: Logical to differentiate between the player and the enemy ship
        - battle: Logical to indicate whether the ship is in battle or not
    
    """


    ###
    # Initialization
    def __init__(self, parameters: Dict, spritesAll: Dict, enemyBoxType: str = 'BoxEnemy', ship: str = 'RebelFighter', variant: str = '', hostile: bool = False) -> None:
        logger.debug('Initialize the enemy ship object')
        
        ###
        # Save parameters and sprites
        self.parameters = parameters
        self.spritesAll = spritesAll
        
        ###
        # Ship and box selection
        self.ship = ship
        self.variant = variant
        
        # Box selection
        self.enemyBoxType = enemyBoxType
        
        # Set the box rect
        self.enemyBox = self.spritesAll['EnemyUi'].rectFromBattleBox(self.enemyBoxType)
        self.enemyBoxOffset = np.array(self.enemyBox.center)
        
        ###
        # Distinction between player and enemy ship, state of the ship
        self.playerShip = False
        
        # Battle position
        self.battle = True
        
        # Ship hostile or not
        self.hostile = hostile





