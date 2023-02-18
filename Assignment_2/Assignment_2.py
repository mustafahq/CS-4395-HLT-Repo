import sys
import nltk
import random

#uncomment these if you don't have them installed
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')


def guessingGame(top50words):
    
    #start the user with 5 points
    userPoints = 5
    userGuess = ''
    first = True
    #continue the game until the score is negative or the user decides to quit
    while(userGuess!='!' and userPoints >0):
        
        if first:
            print("Let's play a word guessing game!")
            first = False
        else:
            print("Guess another word")
            
            
        #get a random word from the top 50 words    
        randomWord = top50words[random.randint(0, 49)]
        guessedWord = []
        for letter in randomWord:
            guessedWord.append('_')
            
        #while the user's score is not negative
        while userPoints >= 0:
            guessRight = False
            print(guessedWord)
            
            
            #if the user has guessed the word
            if '_' not in guessedWord:
                print("You solved it!\n")
                print("Current score:", userPoints,"\n")
                break
            
            
            #prompt user for a guess
            userGuess = input("Guess a letter: ")
            if userGuess == '!':
                break
            
            
            #fill in the correct underscores with the user guess
            if userGuess in randomWord:
                for i, letter in enumerate(randomWord):
                    if letter == userGuess:
                        guessedWord[i] = userGuess
                        guessRight= True
            
            
            #if the user made a correct guess, increment score
            #if the user made an incorrect guess, decrement
            #print score
            if guessRight:
                userPoints+=1
                print("Right! Score is", userPoints)
            else:
                userPoints-=1
                if userPoints < 0:
                    print("Sorry, score is negative")
                else:
                    print("Sorry, guess again. Score is", userPoints)
                    
    

def preprocess_text(raw_text):
    
    #get the stop words
    stop_words = set(nltk.corpus.stopwords.words('english'))
    
    #filter the raw text
    lowercase_words = nltk.word_tokenize(raw_text.lower())
    filtered_words = []
    for word in lowercase_words:
        if (word.isalpha()) and (len(word) > 5) and (word not in stop_words):
            filtered_words.append(word)


    #get the lemmas
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_words = []
    
    for word in filtered_words:
        lemmatized_words.append(lemmatizer.lemmatize(word))
        
    unique_lemmas = set(lemmatized_words)
    
    
    #tag the lemmas
    pos_tagged_lemmas = nltk.pos_tag(unique_lemmas)
    print("The first 20 tagged lemmas are: ", end="")
    for i in range(0,20):
        print(pos_tagged_lemmas[i][0], end=" ")
    
    
    #get the lemmas that are nouns    
    nouns = []
    for lemma in pos_tagged_lemmas:
        if lemma[1].startswith('N'):
            nouns.append(lemma[0])
    
    print("\n\nThe number of filtered tokens (from part a):", len(filtered_words),", The number of nouns:", len(nouns), "\n")
    

    #return the filtered tokens and the lemmas that are nouns
    return filtered_words, nouns
    
    
def main():
    #open the file path, error if no path provided by user
    try:    
        RelativePath = str(sys.argv[1])
    
    except:
        print("There was no path name provided or an en eror occurred trying to process the path name")
        quit()
    
    with open(RelativePath, 'r') as input_file:
        
        
        #tokenize the raw text
        raw_text = input_file.read()
        tokenized_text = nltk.word_tokenize(raw_text)
        #print(tokenized_text)
        
        
        
        #calculate the lexical diversity
        unique_words = set(tokenized_text)
        lexical_diversity = len(unique_words) / len(tokenized_text)
        print("The lexical diversity of the input file's text is", "{:.2f}".format(lexical_diversity),"\n")
        
        
        #get the nouns and list of filtered tokens
        token_list, nouns = preprocess_text(raw_text)
        
        
        #get the top 50 nouns by frequency
        noun_to_countOfNoun = {}
        for token in token_list:
            if token in nouns:
                noun_to_countOfNoun[token] = noun_to_countOfNoun.get(token, 0) + 1
        sorted_nounCountDict = dict(sorted(noun_to_countOfNoun.items(), key = lambda x : x[1], reverse=True))
        
        
        
        #print the top 50 nouns
        top50words = []
        print("Top 50 words and their counts: ")
        count = 0
        for key, value in sorted_nounCountDict.items():
            print(key, value)
            top50words.append(key)
            count += 1
            if count == 50:
                break
        
        #play the guessing game until the user quits with the top 50 nouns
        guessingGame(top50words)
        
        
        
if __name__ == "__main__":
    main()  