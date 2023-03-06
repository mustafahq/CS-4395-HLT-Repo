import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import math

#nltk.download('punkt')

def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    
    p_gt = 1       # calculate p using a variation of Good-Turing smoothing
    p_laplace = 1  # calculate p using Laplace smoothing
    p_log = 0      # add log(p) to prevent underflow

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1/N
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        if d == 0:
            p_gt = p_gt * (1 / N)
        else:
            p_gt = p_gt * (n_gt / d)
        p_laplace = p_laplace * ((n + 1) / (d + V))
        p_log = p_log + math.log((n + 1) / (d + V))

    #print("\nprobability with simplified Good-Turing is %.5f" % (p_gt))
    #print("probability with laplace smoothing is %.5f" % p_laplace)
    #print("log prob is %.5f == %.5f" % (p_log, math.exp(p_log)))
    
    return p_laplace


def main():

    with open('pickles/EnglishUnigrams.pickle', 'rb') as filename:
        english_unigrams_dict = pickle.load(filename)
    with open('pickles/EnglishBigrams.pickle', 'rb') as filename:
        english_bigrams_dict = pickle.load(filename)

    with open('pickles/FrenchUnigrams.pickle', 'rb') as filename:
        french_unigrams_dict = pickle.load(filename)
    with open('pickles/FrenchBigrams.pickle', 'rb') as filename:
        french_bigrams_dict = pickle.load(filename)

    with open('pickles/ItalianUnigrams.pickle', 'rb') as filename:
        italian_unigrams_dict = pickle.load(filename)
    with open('pickles/ItalianBigrams.pickle', 'rb') as filename:
        italians_bigrams_dict = pickle.load(filename)

    english_N = sum(english_unigrams_dict.values())
    french_N = sum(french_unigrams_dict.values())
    italian_N = sum(italian_unigrams_dict.values())

    counter = 0
    number_of_guesses = 0
    number_of_correct_guesses = 0
    with open("data/LangId.test", "r", encoding='utf-8') as filename:

        with open("data/LangId.sol", "r") as solution:
            solutions = []
            for line in solution:
                solutions.append(line.strip())

            for line in filename:
                #print(line)

                english_probability = compute_prob(line, english_unigrams_dict, english_bigrams_dict, english_N, len(english_unigrams_dict))

                french_probability = compute_prob(line, french_unigrams_dict, french_bigrams_dict, french_N, len(french_unigrams_dict))
                
                italian_probability = compute_prob(line, italian_unigrams_dict, italians_bigrams_dict, italian_N, len(italian_unigrams_dict))


                #print("English prob:", english_probability)
                #print("french prob:", french_probability)
                #print("italian prob:", italian_probability)
                

                predicted_language = ""
                highest_probability = max(english_probability, french_probability, italian_probability)

                if highest_probability == english_probability:
                    predicted_language = "English"
                elif highest_probability == french_probability:
                    predicted_language = "French"
                else:
                    predicted_language = "Italian"

                actual_language = word_tokenize(solutions[counter])[1]
                if predicted_language == actual_language:
                    number_of_correct_guesses+=1
                else:
                    print("Incorrect classification of line #" + str(counter+1))


                counter+=1
                number_of_guesses+=1
        
        print("The accuracy of the language predictor is", str(number_of_correct_guesses/number_of_guesses))




main()    