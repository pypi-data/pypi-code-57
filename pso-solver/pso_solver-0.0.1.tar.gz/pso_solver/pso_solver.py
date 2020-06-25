import math
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from inspect import signature
import sys

PRINT_WIDTH = 20

class Particle:
    """
    Class to represent a particle of the particle swarm optimization (PSO)
    algorithm. Each particle has a current position, a best position that
    minimizes/maximizes the value of the function and a velocity indicating its
    direction of movement.

    Attributes:
    currPos (tuple): Current position of the particle in n-dimensional space,
        where n is the dimension of the tuple.
    pBestPos (tuple): Position among the all the positions visited visited by
        the particle, that minimizes/maximizes the value of the function to be
        optimized.
    vel (tuple): Velocity of the particle as defined in the PSO algorithm.
    """

    def __init__(self, currPos):
        self.currPos = currPos
        self.pBestPos = tuple(currPos)
        self.vel = 0

    def __str__(self):
        """
        Returns the attributes of the object as a string.

        Parameters:
        self (Particle): Object itself.

        Returns:
        str: String that contains the attributes of self.
        """
        return f'currPos: {self.currPos} pBestPos: {self.pBestPos} vel: {self.vel}'

def set_seed(seed=None):
    """
    Sets seed for random number generators. Use this function to set the seed in
    your program before calling any function that uses a PRNG if you want to get
    reproducible results.

    Parameters:
    seed (float, optional): Seed for the PRNG.

    Returns:
    None
    """

    random.seed(seed)
    # If later versions use np.random somewhere, make sure to uncomment the next
    # line to set the seed for np.random as well.
    # np.random.seed(seed)

def generateRandomNTuple(n, lower=0, upper=100):
    """
    Generates a random n-tuple.

    Parameters:
    n (int): Dimesion of the tuple.
    lower (float, optional): Lower bound of values in the tuple (inclusive).
    upper (float, optional): Upper bound of values in the tuple (exclusive).

    Returns:
    tuple: n-tuple with random values in the range [lower, upper).
    """

    randomList = list()

    for i in range(n):
        randomList.append(random.uniform(lower, upper))

    return tuple(randomList)

def generateRandomNTupleList(n, numTuples=10, lower=0, upper=100):
    """
    Generates a list of random n-tuples.

    Parameters:
    n (int): Dimesion of the tuple.
    numTuples (int, optional): Number of n-tuples to generate.
    lower (float, optional): Lower bound of values in the tuple (inclusive).
    upper (float, optional): Upper bound of values in the tuple (exclusive).

    Returns:
    list: List of n-tuples with random values in the range [lower, upper).
    """

    randomList = list()

    for i in range(numTuples):
        randomList.append(generateRandomNTuple(n, lower, upper))

    return randomList

def createParticleList(currPosList):
    """
    Takes a list of initial positions and returns a list of particles in particleList
    initialized to those positions. pBestPos of each particle is initialized to
    position passed in the list.

    Parameters:
    currPosList (list): List of positions (each position is an n-tuple).

    Returns:
    list: List of Particle objects initialized by the positions in currPosList.
    """

    particleList = list()
    for i in range(len(currPosList)):
        particleList.append(Particle(currPosList[i]))
    return particleList

def createRandomParticleList(n, numParticles=10, lower=0, upper=100):
    """
    Returns a list of particles with randomly initialized positions.

    Parameters:
    n (int): Dimesion of the position tuple.
    numParticles (int, optional): Number of particles to be initialized in the
        list.
    lower (float, optional): Lower bound of values in the tuple (inclusive).
    upper (float, optional): Upper bound of values in the tuple (exclusive).

    Returns:
    list: List of Particle objects initialized randomly.
    """

    currPosList = generateRandomNTupleList(n, numParticles, lower, upper)
    return createParticleList(currPosList)

def evaluateF(f, position):
    """
    Evaluates the value of function f at position position.

    Parameters:
    f (lambda): Function to be evaluated at position.
    position (tuple): An n-tuple representing the position at which f is to be
        evaluated.

    Returns:
    float: Value of the function f at position.
    """

    return f(*position) # * is to unpack the n-tuple before evauating f at position

def extractCurrPos(particleList):
    """
    Returns the currPos of all particles in particleList as a list.

    Parameters:
    particleList (list): A list of Particle objects.

    Returns:
    list: List of currPos of the Particle objects in particleList, in the same
        order as the input.
    """
    return [particle.currPos for particle in particleList]

def extractPBestPos(particleList):
    """
    Returns the pBestPos of all particles in particleList as a list.

    Parameters:
    particleList (list): A list of Particle objects.

    Returns:
    list: List of pBestPos of the Particle objects in particleList, in the same
        order as the input.
    """
    return [particle.pBestPos for particle in particleList]

def findGBestPos(f, particleList, accuracy=2):
    """
    Finds pBestPos values in pBestPosList that give minimum/maximum value of f.
    Let these positions be called gBestPos.

    Parameters:
    f (lambda): Function to be optimized (minimized/maximized).
    particleList (list): A list of Particle objects among which the global best
        position is to be found.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    tuple: A 4-tuple in the format (globalMin, globalMinVal, globalMax, globalMaxVal),
        where   globalMin: Best position among pBestPos of particles in
                    particleList that gives minimum value of f
                globalMinVal: Value of f at globalMin
                globalMax: Best position among pBestPos of particles in
                    particleList that gives maximum value of f
                globalMaxVal: Value of f at globalMax.
    """
    pBestPosList = extractPBestPos(particleList)
    # fValues is the list of values of f at all pBestPos of pBestPosList
    fValues = [(evaluateF(f, pBestPos), pBestPos) for pBestPos in pBestPosList]
    fValues.sort()
    # fValues is now sorted in ascending order of f(pBestPos)
    # Return the min, minVal, max, maxVal as a tuple.
    return (np.round(fValues[0][1], accuracy), round(fValues[0][0], accuracy), np.round(fValues[-1][1], accuracy), round(fValues[-1][0], accuracy))

def pso_step(particleList, f, c1=1, c2=1, W=0.5, maxFlag=False, accuracy=2):
    """
    Takes a step (i.e., one iteration) of the PSO algorithm.

    Parameters:
    particleList (list): A list of particles, must be initialized before feeding
        into this function.
    f (lambda): Function to be globally minimized/maximized.
    c1 (float, optional): Parameter of the PSO algorithm, refer algorithm.txt.
    c2 (float, optional): Parameter of the PSO algorithm, refer algorithm.txt.
    W (float, optional): Parameter of the PSO algorithm, refer algorithm.txt.
    maxFlag (bool, optional): If False, finds global minimum of function f, else
        if True, finds global maximum of function f.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    list: List of particles after taking a step of the PSO algorithm.
    """

    # Finding gBestPos
    if(maxFlag == True):
        gBestPos = findGBestPos(f, particleList, accuracy=accuracy)[2]
    else:
        gBestPos = findGBestPos(f, particleList, accuracy=accuracy)[0]

    for particle in particleList:
        # Current state of particle
        vel = np.array(particle.vel)
        pBestPos = np.array(particle.pBestPos)
        currPos = np.array(particle.currPos)

        # Updating velocity
        term1 =  W * vel
        term2 = c1 * random.random() * np.subtract(pBestPos, currPos)
        term3 = c2 * random.random() * np.subtract(gBestPos, currPos)
        vel = term1 + term2 + term3
        particle.vel = tuple(vel)

        # Updating current position
        # Note that vel has been used to update currPos, and not particle.vel.
        # This is because particle.vel now has the velocity of the next
        # iteration, as we updated it. But particle.currPos must be updated
        # using the current value of velocity, which is stored in vel.
        currPos = currPos + vel
        currPos = np.around(currPos, decimals=accuracy)
        particle.currPos = tuple(currPos)

        # Maximizing f
        if(maxFlag == True):
            # Updating pBestPos
            if(evaluateF(f, particle.currPos) > evaluateF(f, particle.pBestPos)):
                particle.pBestPos = tuple(particle.currPos)
        # Minimizing f
        else:
            # Updating pBestPos
            if(evaluateF(f, particle.currPos) < evaluateF(f, particle.pBestPos)):
                particle.pBestPos = tuple(particle.currPos)

    return particleList

def pso(particleList, f, c1=1, c2=1, W=0.5, numIters=10, maxFlag=False, accuracy=2, verbose=False):
    """
    Finds minimum or maximum (set maxFlag to True) of function f using the PSO
    algorithm.

    Parameters:
    Same as for pso_step.
    verbose (bool, optional): If True, prints details of each iteration to
        stdout.

    Returns:
    None
    """

    print(f'Particle swarm optimization, {len(particleList)} particles, {numIters} iterations:')
    print('-' * 10)

    if(verbose == True):
        # Printing initial state
        print('Initial state:')
        printParticleListBrief(particleList, f, accuracy=accuracy)
        print('-' * 10)
        # Taking numIters number of steps of the PSO algorithm (verbose)
        for i in range(numIters):
            print(f'Iteration {(i + 1)}/{numIters}:')
            # Taking a step of the PSO algorithm
            particleList = pso_step(particleList, f, c1=c1, c2=c2, W=W, maxFlag=maxFlag, accuracy=accuracy)
            # Printing summary of current iteration
            printParticleListBrief(particleList, f, maxFlag=maxFlag, accuracy=accuracy)
            print('-' * 10)
    # Taking numIters number of steps of the PSO algorithm (not verbose)
    elif(verbose == False):
        for i in tqdm(range(numIters)):
            # Taking a step of the PSO algorithm
            particleList = pso_step(particleList, f, c1=c1, c2=c2, W=W, maxFlag=maxFlag, accuracy=accuracy)

    if(maxFlag == False):
        print('(minimum, minimimumValue):\t', end='')
        printGBestPos(particleList, f, maxFlag=False, accuracy=accuracy)
    elif(maxFlag == True):
        print('(maximum, maximumValue):\t', end='')
        printGBestPos(particleList, f, maxFlag=True, accuracy=accuracy)

def generateContourPlot(particleList, f, xlower, xupper, ylower, yupper, sleepTime=0.1, density=100, cmap='Oranges', particleColor='k'):
    """
    Plots particles and contour plot of f.

    Parameters:
    particleList (list): A list of particles, must be initialized before feeding
        into this function.
    f (lambda): Function to be globally minimized/maximized.
    xlower (float): Lower bound for x-axis in plot.
    xupper (float): Upper bound for x-axis in plot.
    ylower (float): Lower bound for y-axis in plot.
    yupper (float): Upper bound for y-axis in plot.
    sleepTime (float, optional): Time in milliseconds to wait between plotting successive
        iterations of the PSO algorithm.
    density (int, optional): Density of points to take for the contour plot, think of this
      as resolution, higher the density, more the points taken to plot the
      contour plot.
    cmap (str or matplotlib.pyplot.Colormap, optional): Colormap to be used for the
        contour plot.
    particleColor (str, optional): Colour in which to plot particles.

    Returns:
    None
    """

    # Meshgrid for the contour plot
    X, Y = np.meshgrid(np.linspace(xlower, xupper, density), np.linspace(ylower, yupper, density))

    # Generating contour plot
    currPosList = extractCurrPos(particleList)
    fig, ax = plt.subplots(1, 1)
    contourPlot = ax.contourf(X, Y, f(X, Y), cmap=cmap)
    # Adding colorbar
    fig.colorbar(contourPlot)

    # Plotting particles
    particleX = [position[0] for position in currPosList]
    particleY = [position[1] for position in currPosList]
    plt.scatter(particleX, particleY, color=particleColor)

    # Setting aspect ratio, axes labels and axes limits
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xlower, xupper)
    plt.ylim(ylower, yupper)

    # Displaying plot
    plt.show(block=False)

    # Waiting for sleepTime milliseconds before plotting next iteration
    plt.pause(sleepTime)
    plt.close()

def psoVisualize(particleList, f, xlower, xupper, ylower, yupper, c1=1, c2=1, W=0.5, numIters=10, maxFlag=False, sleepTime=0.1, density=100, cmap='Oranges', particleColor='k', accuracy=2, verbose=False):
    """
    Finds minimum or maximum (set maxFlag to True) of function f using the PSO
    algorithm and provides a nice visualization of the motion of the particles.

    Parameters:
    Same as for pso and generateContourPlot.

    Returns:
    None
    """

    if(len(signature(f).parameters) != 2):
        print('Error: psoVisualize is available only for functions of two variables.')
        sys.exit()

    print(f'Particle swarm optimization, {len(particleList)} particles, {numIters} iterations:')
    print('-' * 10)

    # Taking numIters number of steps of the PSO algorithm (verbose)
    if(verbose == True):
        # Printing initial state
        print('Initial state:')
        printParticleListBrief(particleList, f, accuracy=accuracy)
        print('-' * 10)
        # Taking numIters number of steps of the PSO algorithm (verbose)
        for i in range(numIters):
            print(f'Iteration {(i + 1)}/{numIters}:')
            # Taking a step of the PSO algorithm
            particleList = pso_step(particleList, f, c1=c1, c2=c2, W=W, maxFlag=maxFlag, accuracy=accuracy)
            # Printing summary of current iteration
            printParticleListBrief(particleList, f, maxFlag=maxFlag, accuracy=accuracy)
            print('-' * 10)
            generateContourPlot(particleList, f, xlower, xupper, ylower, yupper, sleepTime=sleepTime, density=density, cmap=cmap, particleColor=particleColor)
    # Taking numIters number of steps of the PSO algorithm (not verbose)
    elif(verbose == False):
        for i in tqdm(range(numIters)):
            # Taking a step of the PSO algorithm
            particleList = pso_step(particleList, f, c1=c1, c2=c2, W=W, maxFlag=maxFlag, accuracy=accuracy)
            generateContourPlot(particleList, f, xlower, xupper, ylower, yupper, sleepTime=sleepTime, density=density, cmap=cmap, particleColor=particleColor)

    if(maxFlag == False):
        print('(minimum, minimimumValue):\t', end='')
        printGBestPos(particleList, f, maxFlag=False, accuracy=accuracy)
    elif(maxFlag == True):
        print('(maximum, maximumValue):\t', end='')
        printGBestPos(particleList, f, maxFlag=True, accuracy=accuracy)

def printParticle(particle, f=None, accuracy=2):
    """
    Pretty prints to stdout attributes of particle and optionally values of f at
    currPos and pBestPos.

    Parameters:
    particle (Particle): Particle object to be printed.
    f (lambda, optional): Function to be minimized/maximized, if not None,
        prints value of f at currPos and pBestPos.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    None
    """

    print('currPos: ', particle.currPos, end='\t\t')
    print('pBestPos: ', particle.pBestPos, end='\t\t')
    print('vel: ', particle.vel, end='\t\t')

    if(f is not None):
        print('f(currPos) = ', round(evaluateF(f, particle.currPos), accuracy), end='\t')
        print('f(pBestPos) = ', round(evaluateF(f, particle.pBestPos), accuracy))

def printParticleList(particleList, f=None, maxFlag=False, accuracy=2):
    """
    Pretty prints to stdout attributes of particle and optionally values of f at
    currPos and pBestPos for each particle in particleList. Also prints gBestPos of
    the particles.

    Parameters:
    particleList (list): A list of Particle objects.
    f (lambda, optional): Function to be minimized/maximized, if not None,
        prints value of f at currPos and pBestPos.
    maxFlag (bool, optional): If False, finds global minimum of function f, else
        if True, finds global maximum of function f.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    None
    """

    for particle in particleList:
        printParticle(particle, f, accuracy=accuracy)

    if(maxFlag == True):
        print('gBestPos = ', findGBestPos(f, particleList, accuracy=accuracy)[2])
    else:
        print('gBestPos = ', findGBestPos(f, particleList, accuracy=accuracy)[0])

def printParticleListBrief(particleList, f, maxFlag=False, accuracy=2):
    """
    Pretty prints currPos (CP), pBestPos (PBP), f(currPos) (f(CP)) and
    f(pBestPos) (f(PBP)),
    Also prints gBestPos (GBP) of the particles.

    Parameters:
    particleList (list): A list of Particle objects.
    f (lambda, optional): Function to be minimized/maximized, if not None,
        prints value of f at currPos and pBestPos.
    maxFlag (bool, optional): If False, finds global minimum of function f, else
        if True, finds global maximum of function f.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    None
    """

    for particle in particleList:
        print(f'CP = {tuple(round(element, accuracy) for element in particle.currPos)}'.ljust(PRINT_WIDTH, ' '), end='  ')
        print(f'PBP = {tuple(round(element, accuracy) for element in particle.pBestPos)}'.ljust(PRINT_WIDTH, ' '), end='  ')
        print(f'f(CP) = {round(evaluateF(f, particle.currPos), accuracy)}'.ljust(PRINT_WIDTH, ' '), end='  ')
        print(f'f(PBP) = {round(evaluateF(f, particle.pBestPos), accuracy)}'.ljust(PRINT_WIDTH, ' '))

    if(maxFlag == True):
        print('GBP = ', tuple(findGBestPos(f, particleList, accuracy=accuracy)[2]))
    else:
        print('GBP = ', tuple(findGBestPos(f, particleList, accuracy=accuracy)[0]))

def printGBestPos(particleList, f, maxFlag=False, accuracy=2):
    """
    Prints value of gBestPos for an iteration.

    f (lambda, optional): Function to be minimized/maximized, if not None,
        prints value of f at currPos and pBestPos.
    maxFlag (bool, optional): If False, finds global minimum of function f, else
        if True, finds global maximum of function f.
    accuracy (int, optional): Number of decimal places to which to print the
        numbers in positions.

    Returns:
    None
    """

    if(maxFlag == True):
        print((tuple(findGBestPos(f, particleList, accuracy=accuracy)[2]), findGBestPos(f, particleList, accuracy=accuracy)[3]))
    else:
        print((tuple(findGBestPos(f, particleList, accuracy=accuracy)[0]), findGBestPos(f, particleList, accuracy=accuracy)[1]))
