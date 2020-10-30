###
#
# Base class for the door animations
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
# Import ressources

# Doors
import src.classes.elements.doors as doors


###
# Setup logging
logger = logging.getLogger(__name__)


###
# Animation object definition for a door
class animationDoors(object):
    """
    
    Door animation control object.
    
    Fields:
        - door [doors.door]: Door object which is controlled by the animation object
        - parameters [Dict]: Reference to all parameters
        
        - doorOpening [bool]: Controls whether the door is opening or closing
        - timePerPixel [int]: Time between animation steps in milliseconds
        - stillRunning [bool]: True if the animation is still running and should be updated

        - animationTime[int]: Animation time from start in milliseconds
        - sequencePosition [np.array]: Positions for the door for the animation frames
        - framesNumber [int]: Total number of animation frames
        - sequenceTime [int]: Total animation running time in milliseconds
        - sequenceCurrentFrame [int]: Current frame position within the sequencePosition-Array
        
    Methods:
        - startAnimation(onClick [bool]): Setup the animation, onClick is true if the player started the animation manually
        - updateAnimation(dt [int]): Advance the animation by dt milliseconds. Checks internally if an animation is running
    
    
    """
    
    ###
    # Initialization
    def __init__(self, parameters: Dict, doorObject: doors.door) -> None:
        logger.debug('Initialize the animation control object for door {}'.format(doorObject.doorKey))
        
        ###
        # Save the values
        self.door = doorObject
        self.parameters = parameters
        
        
        ###
        # Animation control variables
        self.doorOpening = True     # Inverted on click to opening/closing
        self.timePerPixel = self.parameters['General']['DoorAnimationTimePerPixel']
        self.stillRunning = False
        
    
    ###
    # Start the animation to open/close doors, define all necessary fields
    def startAnimation(self, onClick: bool) -> None:
        # At first, determine whether the door can and shall be opened/closed
        # onClick: If true then the animation shall be started on manual input
        
        # Check manual input
        if onClick:
            # Check if the door can be manipulated
            if self.door.level and not self.door.hacked and not self.door.bashed:
                # Set the animation time to 0
                self.animationTime = 0
                
                # If door is closed, open it, otherwise close it and set the direction. Otherwise invert the direction
                if self.door.currentPosition == self.door.minimumPixel:   # Door closed
                    self.doorOpening = True
                   
                    # Set the sequence
                    self.sequencePosition = np.arange(0, self.door.maximumPixel + 1)
                
                elif self.door.currentPosition == self.door.maximumPixel:   # Door opened
                    self.doorOpening = False
                   
                    # Set the sequence
                    self.sequencePosition = np.flip(np.arange(0, self.door.maximumPixel + 1))

                else:   # Door is somewhere in between
                    self.doorOpening = not self.doorOpening   # Invert the current pathway
                    
                    if self.doorOpening:
                        self.sequencePosition = np.arange(self.door.currentPosition, self.door.maximumPixel + 1)
                    else:
                        self.sequencePosition = np.flip(np.arange(0, self.door.currentPosition + 1))        

                logger.debug('Start animation {status} door {doorKey}'.format(status = 'opening' if self.doorOpening else 'closing', doorKey = self.door.doorKey))
        
                # Finish animation definition
                self.framesNumber = len(self.sequencePosition)  # Number of frames remaining
                self.sequenceTime = np.arange(self.framesNumber) * self.timePerPixel    # Total animation running time
                self.sequenceCurrentFrame = -1

                # Set the animation to running
                self.stillRunning = True
                
            else:
                logger.debug('Door {doorKey} cannot be manually manipulated'.format(doorKey = self.door.doorKey))
    
    
    ###
    # Update the animation to the next state
    def updateAnimation(self, dt: int) -> bool:
        """
        
        Update the animation frame by the given time step dt in milliseconds if the animation is active
        
        """
        
        ###
        # Check if the animation is running
        updateSprites = False
        if self.stillRunning:
            ##
            # Update time and the current frame selection
            self.animationTime += dt
            currentFrame = max(np.where(self.sequenceTime <= self.animationTime)[0])    
                        
            ##
            # Check if a framechange happened
            if currentFrame > self.sequenceCurrentFrame:
                # Update the frame and door position
                self.sequenceCurrentFrame = currentFrame
                self.door.currentPosition = self.sequencePosition[self.sequenceCurrentFrame]
                
                # Update the door sprite
                self.door.selectSprite()
                updateSprites = True
                
                # Check if the animation is finished
                if self.sequenceCurrentFrame == (self.framesNumber - 1):
                    logger.debug('End animation {status} door {doorKey}'.format(status = 'opening' if self.doorOpening else 'closing', doorKey = self.door.doorKey))
                    
                    self.stillRunning = False
        
        
        ###
        # Return the indicator whether the sprites have to be reloaded
        return(updateSprites)






























