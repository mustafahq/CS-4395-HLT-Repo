import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

#nltk.download('punkt')


def language_model(filename):

    with open(filename, "r", encoding='utf-8') as filename:
        raw_text = filename.read().replace('\n', '')

        tokens = word_tokenize(raw_text)
        unigrams = tokens
        bigrams = list(ngrams(tokens, 2))

        unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
        bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

        return unigram_dict, bigram_dict



def main():

    english_unigram_dict, english_bigram_dict = language_model("data/LangId.train.English")

    with open('pickles/EnglishUnigrams.pickle', 'wb') as filename:
        pickle.dump(english_unigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)

    with open('pickles/EnglishBigrams.pickle', 'wb') as filename:
        pickle.dump(english_bigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)



    french_unigram_dict, french_bigram_dict = language_model("data/LangId.train.French")

    with open('pickles/FrenchUnigrams.pickle', 'wb') as filename:
        pickle.dump(french_unigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)

    with open('pickles/FrenchBigrams.pickle', 'wb') as filename:
        pickle.dump(french_bigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)

    

    italian_unigram_dict, italian_bigram_dict = language_model("data/LangId.train.Italian")

    with open('pickles/ItalianUnigrams.pickle', 'wb') as filename:
        pickle.dump(italian_unigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)

    with open('pickles/ItalianBigrams.pickle', 'wb') as filename:
        pickle.dump(italian_bigram_dict, filename, protocol=pickle.HIGHEST_PROTOCOL)












main()    