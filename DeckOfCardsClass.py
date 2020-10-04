import sys
import random
import math

class DeckOfCards:
    isnt_seeded = True
    alpha = 1
    numeric = 2
    
    """ DeckOfCards will handle constructing a playing deck, shuffling, reshuffling, burning cards, and returning (dealing) cards
     that a client application can then present any way it likes. """
     
     
    
    """ get a random number
     NOTE BENE!!  A lot of work has been done to demonstarte how many pseudorandom number generators can be predicted
     given the approximate time of generation and knowledge of a few picks (i.e. cards).  If you use this card for any
     serious card playing game, you need to research that and replace this standard python random number generator with 
     a randomize funtion that can't be predicted.  That's why rando has been pulled out into this separate funxtion so
     it can be easily replaced.  YOU HAVE BEEN WARNED! """
    def randomMethod(self):
        """ Return a randomly generated number >=0 and <1. """
        return random.random()
        
        
    """ validate parameters using a defaultValue, the correct range, type, and the parameter """
    def valParam(self, defaultValue, range, type, parameter):
        try:
            parameter
        except NameError:
            return defaultValue
            
        if type == DeckOfCards.alpha:
            if parameter in range:
                return parameter
            else:
                return defaultValue
                
        if type == DeckOfCards.numeric:
            try:
                parameter = float(parameter)
            except ValueError:
                return defaultValue
            parameter = round(parameter)
            
            if parameter < range[0] or parameter > range[1]:
                return defaultValue
            else:
                return parameter
            
        
            

        
    """  initializer function 
         Construct the deck of cards requested.
         deckType can be 'standard' (52 cards), 'jass' (36 cards 6 to Ace), 'skat' (32 cards 7 to Ace)
         or 'euchre' (24 cards 9 to Ace).  A pincohle deck can be built by using type 'euchre' and setting
         numDecks to 2.  If deckType is invalid, it is set to 'standard'.
         numJokers is the number of Jokers added to the deck and must be a number from 0 to 10.  If omitted, not
         interpretable, negative, or greater than 10, it is set to 0.  If non-integer, it is rounded.
         numDecks is the number of identical decks created and must be a number from 1 to 10.  If omitted, not
         interpretable, negative, or greater than 10, it is set to 1.  If non-integer, it is rounded.
    """ 
    def __init__(self, deckType='standard', numJokers=0, numDecks=1):
        
        # seed the Random function on first instantiation
        if DeckOfCards.isnt_seeded:
            random.seed()
            DeckOfCards.isnt_seeded = False
      
        """ Validate the class parameters - numJokers, then numDecks,then deckType """
        jokerRange = [0, 10]
        numJokers = self.valParam(0, jokerRange, DeckOfCards.numeric, numJokers)
        
        decksRange = [1, 10]
        numDecks = self.valParam(1, decksRange, DeckOfCards.numeric, numDecks)
      
        lowCardIndex = -1
        typeRange = ["standard", "jass", "skat", "euchre"]
        deckType = self.valParam("standard", typeRange, DeckOfCards.alpha, deckType)
        if deckType == "jass":
            lowCardIndex = 4
        else:
            if deckType == "skat":
                lowCardIndex = 5
            else:
                if deckType == "euchre":
                    lowCardIndex = 7
                else:
                    lowCardIndex = 0
                    
        """ Calculate the deck size and create the deck list """
        
        highCardIndex = 12
        self.deckSize = (((highCardIndex - lowCardIndex + 1) * 4) + numJokers) * numDecks
        
        """ initilaize the suits """
        suit = ["D", "C", "H", "S"]
        """ initialize the card values """
        value = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        
        """ create a list for unshuffled card names and a list for shuffled deck pointers """
        self.deck = []
        self.shuffledPtrs = []
        for counter in range(self.deckSize):
            self.shuffledPtrs.append(counter)
        
        """ initialize our card names in an unshuffled deck """
        for suitCounter in range(4):
            for valueCounter in range(lowCardIndex, highCardIndex + 1):
                self.deck.append(value[valueCounter] + suit[suitCounter])
        """ add the jokers if any """
        for jokerCounter in range(numJokers):
            self.deck.append("J")
            
            
        
        """ Multiply the decks if required """
        if numDecks > 1:
            singleDeck = self.deck.copy()
            for decksCounter in range (1, numDecks):
                self.deck.extend(singleDeck)
                
        """ set some object values we're going to need """
        self.currentCard = 0
        self.cardsRemaining = self.deckSize
        
        print(self.deck)
        
        
    """ end of initializer """
    
    """ return a list of numCards to the caller representing the next numCards in the deck """
    def deal(self, numCards):
        
        try:
            int(numCards)
        except ValueError:
            return None
            
        if numCards < 1 or self.cardsRemaining == 0:
            return None
            
        if numCards > self.cardsRemaining:
            numCards = self.cardsRemaining
            
        returnedCards = []
        
        for counter in range(numCards):
            returnedCards.append(self.deck[self.shuffledPtrs[self.currentCard]])
            self.currentCard += 1
            self.cardsRemaining -= 1
        
        return returnedCards
        
    """ end of deal """
        
    """ discard the next numcards in the deck by incrementing currentCard """
    def burn(self, numCards):
        
        try:
            int(numCards)
        except ValueError:
            return None
            
        if numCards < 1 or self.cardsRemaining == 0:
            return None
            
        if numCards > self.cardsRemaining:
            numCards = self.cardsRemaining
            
        self.currentCard += numCards
        self.cardsRemaining -= numCards
        
        return numCards
        
    """ end of burn """
    
    """ shuffle a deck initialized to be in suit and rank order (times number of decks) """
    def shuffle(self):
        """ reinitialize deck to unshuffled """
        for counter in range(self.deckSize):
            self.shuffledPtrs[counter] = counter
        
        self.currentCard = 0
        self.cardsRemaining = self.deckSize

        """ initialize some working variables """
        place = 0
        saveplace = 0
        
        """ Now we're going to randomly swap cards to the bottom of the deck until we reach the top """
        for counter in reversed(range(self.deckSize)):
            
            place = self.randomMethod() * (counter + 1)
            place = math.floor(place)
            saveplace = self.shuffledPtrs[counter]
            self.shuffledPtrs[counter] = self.shuffledPtrs[place]
            self.shuffledPtrs[place] = saveplace
            
    """ end of shuffle """
    
    """ reshuffle wil only shuffle the remaining cards as oppoosed to the entire deck """
    def reshuffle(self):
        
        """ initialize some working variables """
        place = 0
        saveplace = 0

        """ Now we're going to randomly swap cards to the bottom of the deck until we reach the top """
        for counter in reversed(range(self.currentCard + 1, self.deckSize)):
            
            place = self.randomMethod() * (counter + 1 - self.currentCard)
            place = math.floor(place) + self.currentCard
            saveplace = self.shuffledPtrs[counter]
            self.shuffledPtrs[counter] = self.shuffledPtrs[place]
            self.shuffledPtrs[place] = saveplace
            
    """ end of reshuffle """
    
""" end of Class DeckOfCards """

      
      
