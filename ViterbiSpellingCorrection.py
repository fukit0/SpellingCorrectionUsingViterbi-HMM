import csv
from collections import Counter

import numpy as np

# kabul
# 20000 karakter okuduktan sonra  okunmaya başlanan ilk kelime parçaso

# CONSTANTS
numberOfTestCharacter = 20000
numberOfWords = 0
delimiterConstant = ' '

# her harf sayacı 1 ile ilkleniyor. daha sonra 1 çıkartılarak initialize edilecek
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

# holds the number of letters
letterCounts = Counter(alphabet)

## alphabet dictionary: enumerate etmek için kullanılacak
alphabetEnum = {
	'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
	'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
	}

probabilityOfWordStartsWithLetter = []  # FIRST STATE VECTOR

# A[x][y] : (Transtion Probability Matrix) Durum Geçiş Olasılık Matrisi: Eğitim setinde bir kelimede x harfinden sonra y harfi gelme olasılığı
countOfTransitionProbabilityMatrix = np.zeros(shape=(26, 27))
transitionProbabilityMatrix = np.zeros(shape=(26, 26))

# B[x][o] : (Emission Probability Matrix) Çıkış Olasılık Matrisi: Eğitim setinde x harfi olması gerekirken o harfinin görülme olasılığı.
countOfEmissionProbabilityMatrix = np.zeros(shape=(26, 27))
emissionProbabilityMatrix = np.zeros(shape=(26, 26))


################################################################### FUNCTIONS DEFINITIONS #############################################################################


# ilk durum harf olasılıklarının çıkartılması
def createFirstStateLetterPossibilitiesVector( ):
	for letterIndex in range(0, 26):
		# her harf 1 ile ilklendiği için 1 çıkarıyoruz
		numberOfLetterInTrainSet = letterCounts[alphabet[letterIndex]] - 1
		probabilityOfWordStartsWithLetter.append((100 * numberOfLetterInTrainSet) / (numberOfWords))
	return


# emission ve transition matrix için olasılık matrisi
def createProbabilityMatrixOfCountMatrix( countMatrix, probMatrix ):
	for row in range(0, 26):
		total = countMatrix[row][26]
		if (total == 0):
			continue
		else:
			for column in range(0, 26):
				count = countMatrix[row][column]
				probability = (100 * count) / total
				probMatrix[row][column] = probability
	return probMatrix


# emission ve transition matrixlerin adetlerini tutuyor
# transition matrix için x: previous, y: current letter temsil eder
# emission matrix için x: olması gereken harf, y ise gözlenen yanlış harfi temsil eder
def incrementCountOfMatrixByTarget( x, y, targetCountMatrix ):
	xIndex = alphabetEnum[x]
	yIndex = alphabetEnum[y]
	targetCountMatrix[xIndex, yIndex] += 1
	targetCountMatrix[xIndex, 26] += 1
	return targetCountMatrix


# viterbi algorithm
def runViterbi( testWord, probabilityOfWordStartsWithLetter, transitionProbabilityMatrix, emissionProbabilityMatrix):



	return

######################################################################## BEGINNING OF PROGRAM ###################################################################

# reads file as numberOfline X 2 matrix
f = open('docs.data')
reader = csv.reader(f, delimiter=delimiterConstant)

# create test and train matrix
testMatrix = np.empty(shape=(numberOfTestCharacter, 2), dtype=np.str)
numberOfTrainCharachter = 0

# dosyadaki egitimdeki harflerin sayıları ve transition matrix sayıları hesaplanır
testCharacterCounter = 0
previousLetter = ""

for row in reader:
	# test section
	if (testCharacterCounter < numberOfTestCharacter):
		testMatrix[testCharacterCounter] = row
		if (row[0] != "_"):
			testCharacterCounter +=1

	# train section
	else:
		leftSideLetter = row[0]  # true
		rightSideLetter = row[1]  # false

		# ilk egitim datasında önceki harf yok sonraki harften devam et
		if (previousLetter == ""):
			previousLetter = leftSideLetter
			continue

		if (leftSideLetter == "_"):
			previousLetter = leftSideLetter
		else:
			# dosyanın ilk karakteri ya da önceki karakter underscore ise yeni kelime sayısını 1 arttır
			if (previousLetter == "_"):
				numberOfWords += 1
				letterCounts[leftSideLetter] += 1

			# ilk karakter ve önceki karakter underscore ise matrix update edilmez
			if (previousLetter != "_"):
				countOfTransitionProbabilityMatrix = incrementCountOfMatrixByTarget(previousLetter, leftSideLetter,
				                                                                    countOfTransitionProbabilityMatrix)
				# eğer soldaki ile sağdaki aynı karakter değilse emission matrixi update et
				if (leftSideLetter != rightSideLetter):
					incrementCountOfMatrixByTarget(leftSideLetter, rightSideLetter, countOfEmissionProbabilityMatrix)

			previousLetter = leftSideLetter


# ilk durum harf olasılıklarının çıkartılması
createFirstStateLetterPossibilitiesVector()

# transition matrix olasılıklarının çıkarılması
# createStateTransitionMatrix()
transitionProbabilityMatrix = createProbabilityMatrixOfCountMatrix(countOfTransitionProbabilityMatrix,
                                                                   transitionProbabilityMatrix)

# emission matrix olasılıklarının çıkarılması
# createEmissionProbabilityMatrix()
emissionProbabilityMatrix = createProbabilityMatrixOfCountMatrix(countOfEmissionProbabilityMatrix,
                                                                 emissionProbabilityMatrix)

testWord = ""
trueWord = ""
numberOfTrueCorrection = 0
numberOfFalseCorrection = 0

for row in testMatrix:
	# use the right side of doc
	if (row[1] == "_"):
		expectedWord = runViterbi(testWord, probabilityOfWordStartsWithLetter, transitionProbabilityMatrix,
		                          emissionProbabilityMatrix)
		testWord = ""
	else:
		testWord += row[1]
