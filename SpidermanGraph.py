from pylab import *             # allows for numpy and histograms
from random import randint      # allows for random call for character numbers
from time import time           # allows for tracking of processing time

set_printoptions(threshold=nan) # allows for a block of matrix to be printed, not just the corners

# Create data structures to hold the character numbers array, character vertexes array,
# comicbook vertexes array, Spider Man Numbers array, Edges matrix, and Collaboration matrix
#
vertexNumArray = []
characterArray = []
comicbookArray = []
global numCharacters
global numComicbooks
global SMNArray
global edgesMatrix
global collaborationMatrix

# Method for reading in the data from text file
#
def read_file():
    global numCharacters
    global numComicbooks
    # Import the file to read from
    marvel = open('porgat.txt')

    # Read the first line for vertex number sizes
    firstLine = marvel.readline().strip().split(" ")
    numComicbooks = int(firstLine[1])
    numCharacters = int(firstLine[2])

    # Read in character number and name, line by line, create character name vertex array
    for i in range(1, numCharacters + 1):
        a = marvel.readline().strip().split('"')
        vertexNumArray.append(int(a[0]))
        characterArray.append(a[1])

    # Read in comicbook number and name, line by line, create comicbook name vertex array
    for j in range(numCharacters + 2, numComicbooks + 2):
        b = marvel.readline().strip().split('"')
        vertexNumArray.append(int(b[0]))
        comicbookArray.append(b[1])

    # Create a 2 dimensional numpy matrix of all zeros
    edgesMatrix = np.zeros((numCharacters, numComicbooks), dtype=np.int)

    # Read and ignore the '*Edgeslist' line in the input text file
    marvel.readline()

    # Read in edges, create edges matrix of boolean equivalents, 1's & 0's
    for k in range(numComicbooks + 2, ):
        c = marvel.readline().strip().split(" ")
        for word in c:
            if word != c[0]:
                edgesMatrix[int(c[0]) - 1, int(word) - numCharacters - 1] = 1

    return edgesMatrix

# Method to print start and end of Vertex arrays and partially print Edge matrix to verify input
#
def print_input_verification():
    print()
    print("The Vertex Number Array has", len(vertexNumArray), "numbers.")
    # Partially print the Character vertexes array
    print()
    print("The Character Array has", len(characterArray), "names.")
    print()
    print("The first 10 names in the Character Array are:")
    for i in range(10) :
        print(vertexNumArray[i], ':', characterArray[i])
    print()
    print("...")
    print()
    print("The last 10 names in the Character Array are:")
    for i in range(len(characterArray)-10, len(characterArray)) :
        print(vertexNumArray[i], ':', characterArray[i])
    print()

    # Partially print the Comicbook vertexes array
    print()
    print("The Comicbook Array has", len(comicbookArray), "names.")
    print()
    print("The first 10 names in the Comicbook Array are:")
    for i in range(10):
        print(vertexNumArray[i], ':', comicbookArray[i])
    print()
    print("...")
    print()
    print("The last 10 names in the Comicbook Array are:")
    for i in range(len(comicbookArray)-10, len(comicbookArray)) :
        print(vertexNumArray[i], ':', comicbookArray[i])
    print()

    # Partially print the Edges matrix
    print("The Edges Matrix has the following dimensions:", edgesMatrix.shape)
    print()
    print("The Edges Matrix has", edgesMatrix.size, "elements.")
    print()
    # Print the matrix, first 37 rows and first 24 columns
    print("This is the first 37 rows and 24 columns of the Edges Matrix:")
    print(edgesMatrix[0:37, 0:24])
    print()

# Method to create the Collaboration matrix
#
def create_collaboration_matrix():
    global collaborationMatrix
    # Create a transpose matrix for edgesArray using numpy
    edgesTransMatrix = edgesMatrix.transpose()

    # Multiple the two edges matrix's together to make a Collaboration matrix using numpy and track the process time
    collaborationMatrix = np.dot(edgesMatrix, edgesTransMatrix)

    # Save the Collaboration matrix, Character Number array and Character Name array to binary files for quicker runtimes.
    np.save('collmatrix', collaborationMatrix)
    np.save('charnums', numCharacters)
    np.save('charnames', characterArray)

# Method to print a partial Collaboration matrix
#
def print_collaboration_matrix():
    global collaborationMatrix
    # Read in Collaboration matrix from binary file
    collaborationMatrix = np.load('collmatrix.npy') # For use during debugging for quicker runtimes
    # Partially print the Collaboration matrix specifics
    print()
    print("The Collaboration Matrix has the following dimensions:", collaborationMatrix.shape)
    print()
    print("The Collaboration Matrix has", collaborationMatrix.size, "elements.")
    print()
    # Print the matrix, first 37 rows and first 24 columns
    print("This is the first 37 rows and 24 columns of the Collaboration Matrix:")
    print(collaborationMatrix[0:37, 0:24])

# Method for calculating the Spider Man Number for each character
#
def find_SMN():
    global numCharacters
    global collaborationMatrix
    global SMNArray

    # Read in Character Number Array from binary file
    numCharacters = np.load('charnums.npy') # For use during debugging for quicker runtimes

    # Create a new numpy array to hold the Spider Man Number for each character
    SMNArray = np.zeros(numCharacters, dtype=np.int)

    spideynum = 5306  # set the character number for Spider Man

    # Find the characters that have a SMN of 1
    spideynum1Array = np.nonzero(collaborationMatrix[spideynum - 1, :])
    # Assign a SMN of 1 to these characters
    for element in spideynum1Array:
        SMNArray[element] = 1

    # Find the characters that have a SMN of 2
    for i in range(size(SMNArray)):
        if SMNArray[i] == 1:
            spideynum2Array = np.nonzero(collaborationMatrix[i, :])
            for element in spideynum2Array:
                for i in element:
                    if SMNArray[i] != 1:
                        SMNArray[i] = 2
            del(spideynum2Array)

    # Find the characters that have a SMN of 3
    for i in range(size(SMNArray)):
        if SMNArray [i] == 2:
            spideynum3Array = np.nonzero(collaborationMatrix[i, :])
            for element in spideynum3Array:
                for i in element:
                    if SMNArray[i] != 1 and SMNArray[i] != 2:
                        SMNArray[i] = 3
            del(spideynum3Array)

    # Find the characters that have a SMN of 4
    for i in range(size(SMNArray)):
        if SMNArray[i] == 3:
            spideynum4Array = np.nonzero(collaborationMatrix[i, :])
            for element in spideynum4Array:
                for i in element:
                    if SMNArray[i] != 1 and SMNArray[i] != 2 and SMNArray[i] != 3:
                        SMNArray[i] = 4
            del (spideynum4Array)

    # Find the characters that have a SMN of 5
    for i in range(size(SMNArray)):
        if SMNArray[i] == 4:
            spideynum5Array = np.nonzero(collaborationMatrix[i, :])
            for element in spideynum5Array:
                for i in element:
                    if SMNArray[i] != 1 and SMNArray[i] != 2 and SMNArray[i] != 3 and SMNArray[i] != 4:
                        SMNArray[i] = 5
            del (spideynum5Array)

    # Find the characters that have a SMN of 6
    for i in range(size(SMNArray)):
        if SMNArray[i] == 5:
            spideynum6Array = np.nonzero(collaborationMatrix[i, :])
            for element in spideynum6Array:
                for i in element:
                    if SMNArray[i] != 1 and SMNArray[i] != 2 and SMNArray[i] != 3 and SMNArray[i] != 4 and SMNArray[i] != 5:
                        SMNArray[i] = 6
            del (spideynum6Array)

    # Determine if any Characters have no SMN
    for i in range(size(SMNArray)):
        if SMNArray[i] == 0:
            SMNArray[i] = -1

    # Set Spider Man's SMN
    SMNArray[spideynum - 1] = 0  # Spider Man's Number for himself is 0 by definition

    # Total the count of different Spider Man Numbers amongst all the characters and print the results
    sum0 = sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = sum6plus = 0
    for element in SMNArray:
        if element == 0:
            sum0 += 1
        elif element == 1:
            sum1 += 1
        elif element == 2:
            sum2 += 1
        elif element == 3:
            sum3 += 1
        elif element == 4:
            sum4 += 1
        elif element == 5:
            sum5 += 1
        elif element == 6:
            sum6 += 1
        elif element == -1:
            sum6plus += 1

    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 0:", sum0))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 1:", sum1))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 2:", sum2))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 3:", sum3))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 4:", sum4))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 5:", sum5))
    print()
    print('{0:40} {1!s:>4}'.format("The number of Characters with Spider Man Number of 6:", sum6))
    print()
    print('{0:40} {1!s:>6}'.format("The number of Characters with no Spider Man Number:", sum6plus))

    # Ask user if a printed histogram is desired
    print()
    print("Would you like to print out a Histogram of the Spider Man Numbers?")
    answer = input("Please enter Y for yes or N for No: ")
    if answer == 'Y' or answer == 'y':
        # Define the histogram data
        data = SMNArray

        # Create the histogram
        plt.hist(data, bins=[0.0, 1.0, 2.0, 3.0], align='left')

        # Label and scale the graph
        plt.xlabel('x')
        plt.ylabel('Count')
        plt.title(' Spider Man Number Histogram ')
        plt.axis([-0.5, 6.5, 0, 5000])
        plt.grid(True)

        # Print the graph to a new screen
        plt.show()

# Method for printing a random number of Marvel character's names with their associated Spider Man Numbers
#
def print_randomcharacter_SMN():
    global SMNArray
    # Read in Character Name Array from binary file
    characterArray = np.load('charnames.npy')  # For use during debugging for quicker runtimes
    print()

    # Request Input to set number of random Characters and get their Spider Man Number
    num = int(
        input("Please enter an integer for the number of random Characters to display their Spider Man Number: "))
    print()
    for i in range(num):
        characterNum = randint(0, 6485)
        if SMNArray[characterNum] != -1:
            print('{0:25} {1:20} {2!s:3}'.format(characterArray[characterNum], "has a Spider Man Number of:",
                                             SMNArray[characterNum]))
        else:
            print('{0:25} {1:20}'.format(characterArray[characterNum], "has NO Spider Man Number"))

# Main driver program
#
def main():
    global edgesMatrix
    global collaborationMatrix

    startTime = time()

    # Call method to read in text and create the various arrays
#    edgesMatrix = read_file()

    # Call method to printout input for verification
    '''print()
    print("Would you like to print out verification of the input?")
    answer = input("Please enter Y for yes or N for No: ")
    if answer == 'Y' or answer == 'y':
       print_input_verification()'''

    # Call method to create the collaboration matrix
#    create_collaboration_matrix()

    # Call method to printout the collaboration matrix
    print_collaboration_matrix()

    # Call method to create the Spider Man Number array of shortest paths
    find_SMN()

    endTime = time()

    # Print the total seconds to run the algorithm
    print()
    print("The number of seconds for the total calculation:", round((endTime - startTime), 3))
    print()

    # Call method to create a printout of random Marvel characters with their associated Spider Man Numbers
    answer = 'Y'
    while answer is 'Y' or 'y':
        print()
        print("Would you like to print out randomly generated Characters and their Spider Man Numbers?")
        answer = input("Please enter Y for yes or N for No: ")
        if answer == 'Y' or answer == 'y':
            print_randomcharacter_SMN()
        else:
            break

# Run the main program
#
main()
