###
#
# Collection of functions used for clicks or collision detection
#
###


###
# Load packages

# Arrays and matrices
import numpy as np


###
# Functions

##
# Function to check if a mouse click has been somewhere in a series of provided rects
def checkRects(mousePosition: np.ndarray, rectMatrix: np.ndarray) -> np.ndarray:
    """
    
    Check whether a mouse click has been made within one or more rects given in the rectMatrix.
    The rectMatrix is expanded by the inverse lowerright point to enable the one-line comparison.
    
    Output:
        - foundPositions: Indizes of the rects which were clicked in. Can be of any length between [0, rectMatrix.shape[0])
    
    """
    
    ###
    # Expand the mouse position by the inverted mouse position
    mousePositionExtended = np.concatenate((mousePosition, -mousePosition))
    
    
    ###
    # Comparison whether a click has been within a rect
    foundPositions = np.where(np.all(mousePositionExtended >= rectMatrix, axis = 1))[0]

    
    ###
    # Return the found positions
    return(foundPositions)    
    

##
# Function to check if a mouse click has been somewhere close to a series of provided centers
def checkCenters(mousePosition: np.ndarray, centerMatrix: np.ndarray, maxDistance: [int, float]) -> np.ndarray:
    """
    
    Check whether a mouse click has been made within a specified distance maxDistance of one of the provided centers.
    
    Output:
        - foundPositions: Indizes of the centers which were within clicking distance. Can be of any length between [0, rectMatrix.shape[0])
    
    
    """
    
    ###
    # Calculate the distance to the provided centers
    distanceFromCenters = np.sqrt(np.sum((centerMatrix - mousePosition).astype(np.int64)**2, axis = 1))
    
    
    ###
    # Check whether a distance is below the maximum distance
    foundPositions = np.where(distanceFromCenters <= maxDistance)[0]
    
    
    ###
    # Return the found positions
    return(foundPositions)


















