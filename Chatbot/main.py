from urllib.parse import urlparse
from urllib import request
import random
from bs4 import BeautifulSoup
import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pickle

##Function extract_link used to extract 15 urls from the chosen url
def extract_links(url):
    ##Create 2 lists for internal and external urls
    urls_internal = []
    urls_external = []
   ##make sure the urls are in the domain of the chosen url
    original_domain = urlparse(url).netloc
    ##exctact external and internal and external urls using beautiful Soup
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            parsed_href = urlparse(href)
            if parsed_href.netloc == original_domain and len(urls_internal) < 10:
                urls_internal.append(href)
            elif parsed_href.netloc != '' and len(urls_external) < 6:
                urls_external.append(href)

    return urls_internal, urls_external

##create function clean_text to clean each text in the pages for newlines,tabs and stopwords
def clean_text(text):
    # Remove newlines and tabs
    cleaned_text = re.sub(r'[\n\t]+', ' ', text)

    # Lowercase everything
    cleaned_text = cleaned_text.lower()

    # Remove punctuation
    cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(cleaned_text)
    cleaned_words = [word for word in words if word not in stop_words]

    return cleaned_words

##create function save_text that stores text from pages as the original text as well as the modified ones.
def save_text(link):
    try:
        ##using html and beautuful soyp to extract the text
        html = request.urlopen(link).read().decode('utf8')
        soup = BeautifulSoup(html)
        text = soup.get_text()

        # Save the original text
        with open(link.split('/')[-1] + ".txt", "w", encoding='utf-8') as f:
            f.write(text)
       ## print(f"Text from {link} has been saved.")

        # Save the cleaned text
        cleaned_text = clean_text(text)
        with open(link.split('/')[-1] + "_cleaned.txt", "w", encoding='utf-8') as f:
            f.write(" ".join(cleaned_text))
       ## print(f"Cleaned text from {link} has been saved.")

        # Save the top 25-40 terms
        word_count = Counter(cleaned_text)
        top_words = [word for word, count in word_count.most_common(40)]
        with open(link.split('/')[-1] + "_top_words.txt", "w", encoding='utf-8') as f:
            f.write("\n".join(top_words))
        print(f"Top words from {link} have been saved.")
    except:
         print(f"Error processing {link}.")


##main function
if __name__ == '__main__':
    ##main url
    exit_keywords = ['thanks', 'thank you', 'okay', 'ok', "that's it", 'bye']
    url = 'https://www.vogue.com/'
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html)

    internal_links, external_links = extract_links(url)
    links = internal_links + external_links
    ## print both external and internal urls
    ##print("Internal links:")
    for url in internal_links:
        print(url)

   ## print("\nExternal links:")
    for url in external_links:
       print(url)

    for link in links:
        save_text(link)

    # Print top words from each cleaned/tokonized file
    for filename in os.listdir():
        if filename.endswith("_cleaned.txt"):
            with open(filename, "r", encoding='utf-8') as file:
                cleaned_text = file.read().lower()
                cleaned_words = clean_text(cleaned_text)
                word_count = Counter(cleaned_words)
                top_words = [word for word, count in word_count.most_common(40)]
               ## print(f"Top words from {filename}:")
               ## print("\n".join(top_words))
    #top 10 terms  manually generated.
    terms=['fashion', 'makeup','shades','style','designer','artist','trendy','outfit','look','2022']

    ##Create a knoledge base using the top 10 terms, using python dicts and pickes
    knowledge_base = {
        'fashion': [
            'Fashion is a form of self-expression and autonomy at a particular period and place and in a specific context',
            'Fahsion consists of clothing, footwear, lifestyle, accessories, makeup, hairstyle, and body posture.',
            'The term implies a look defined by the fashion industry as that which is trending.'
        ],
        'makeup': [
            'Makeup is a form of self-expression that has been around for thousands of years.',
            'cosmetics such as lipstick or powder applied to the face, used to enhance or alter the appearance',
            'Makeup mainly is used to change or enhance the way we look, to feel more confident and also to hide our imperfection'
        ],
        'shades': [
            'Shades are a type of eyewear designed to protect the eyes from sunlight.',
            'Sunglasses can reduce the risk of developing cataracts and other eye diseases.',
            'A shade is when a color remains its original hue but has been darkened.'
        ],
        'style': [
            'Style is a way of expressing oneself through clothing, accessories, and other aesthetic choices.',
            'In the fashion world, “style” is usually shorthand for “personal style,” or the way an individual expresses themselves through aesthetic choices such as their clothing, accessories, '
            'hairstyle, and the way they put an outfit together.'
        ],
        'designer': [
            'A fashion designer is someone who creates clothing, footwear, and accessories.',
            'Famous fashion designers include Coco Chanel, Christian Dior, and Giorgio Armani.',
            'The fashion industry relies heavily on designers to create new and innovative products.'
        ],
        'artist': [
            'Fashion designers can be considered artists because they use creative expression to design clothing and accessories.',
            'Many fashion designers also collaborate with artists on special collections.',
            'The Metropolitan Museum of Art in New York City has a Costume Institute that showcases fashion as art.'
        ],
        'trendy': [
            'Trendy refers to something that is popular or fashionable at a particular time.',
            'Trends can come and go quickly in the fashion industry.',

        ],
        'outfit': [
            'a set of clothes worn for a particular occasion or activity',
            'An outfit refers to a set of clothing and accessories worn together.',
            'The right outfit can make a person feel confident and stylish.'

        ],
        'look': [
            'A look refers to a particular style or appearance that a person is trying to achieve.',
            'Fashion influencers and bloggers often showcase their looks on social media.'
        ],
        '2022': [
            'Fashion trends for 2022 include bold prints, oversized clothing, and bright colors.',
            '2022 is expected to be a year of experimentation and creativity in the fashion industry.'
        ],
        'runway': [
            'Refers to the platform where fashion models showcase the latest designs during fashion shows.',
            'The runway is an essential element of fashion shows, providing a stage for designers to showcase their creations.',
            'Fashion shows are often held on runways, where models walk to display the latest fashion designs.'
        ],
        'couture': [
            'High-end, custom-made fashion designed for individual clients, often using luxurious materials and intricate craftsmanship.',
            'Couture fashion is known for its exclusivity and craftsmanship, with each piece meticulously crafted for the client.',
            'Couture fashion is considered the pinnacle of luxury in the fashion industry, with a limited clientele who can afford it.'
        ],
        'accessories': [
            'Items such as jewelry, handbags, belts, and scarves that complement and enhance an outfit.',
            'Accessories are an important part of fashion, adding personality and style to an outfit.',
            'Fashionable accessories can elevate a simple outfit and make a fashion statement.'
        ],
        'vintage': [
            'Refers to clothing or accessories that are from a previous era and have a unique, nostalgic appeal.',
            'Vintage fashion is popular for its uniqueness and historical significance.',
            'Vintage clothing and accessories are often sought after by fashion enthusiasts for their retro charm.'
        ],
        'haute couture': [
            'French term for high fashion, typically referring to exclusive, custom-made clothing by top fashion designers.',
            'Haute couture is known for its exquisite craftsmanship and attention to detail.',
            'Haute couture designs are often seen on red carpets and worn by celebrities for special occasions.'
        ],
        'street style': [
            'Fashion trends and styles that originate from everyday people on the streets, often captured by street photographers.',
            'Street style is known for its individuality and creativity, reflecting the fashion choices of people in different cultures and cities.',
            'Street style influences mainstream fashion and is often a source of inspiration for designers and fashion enthusiasts.'
        ],
        'sustainable fashion': [
            'Fashion that is environmentally and socially responsible, incorporating ethical and eco-friendly practices.',
            'Sustainable fashion focuses on reducing the environmental impact of the fashion industry and promoting fair labor practices.',
            'Sustainable fashion is gaining popularity due to increasing awareness about environmental and social issues in the fashion industry.'
        ],
        'athleisure': [
            'A fashion trend that combines athletic wear with casual or leisure wear for a comfortable yet stylish look.',
            'Athleisure is known for its comfort and versatility, blurring the lines between athletic wear and casual wear.',
            'Athleisure is popular among people who prioritize comfort and style in their everyday clothing choices.'
        ],
        'capsule wardrobe': [
            'A small, curated collection of essential clothing items that can be mixed and matched to create multiple outfits.',
            'Capsule wardrobe is a minimalist approach to fashion, focusing on quality over quantity and versatility in styling.',
            'Capsule wardrobe is popular among those who seek a streamlined and sustainable approach to their wardrobe.'
        ],
        'red carpet': [
            'Refers to the prestigious events where celebrities showcase their glamorous outfits and styles on the red carpet before an awards show or premiere.',
            'The red carpet is known for its high fashion and glamorous looks, with celebrities often wearing designer outfits and accessories.',
            'Red carpet events are closely followed by fashion enthusiasts and media for the latest fashion trends and styles.'
        ],
        'fashion-forward': [
            'Describes someone who is ahead of current fashion trends and often seeks out unique and innovative styles.',
            'Fashion-forward individuals are known for their bold fashion choices and experimentation with new styles.',
            'Fashion-forward people often influence mainstream fashion with their unique and innovative'
    ]


    }
    with open("knowledge_base.pickle", "wb") as picke_file:
        pickle.dump(knowledge_base, picke_file)


# Function to generate a response based on input
def generate_response(input_text):
    # Tokenize input text
    input_tokens = input_text.lower().split()
    exit_keywords = ['thanks', 'thank you', 'okay', 'ok', "that's it", 'bye']
    # Check if input text includes exit keywords

    # Iterate through the knowledge base and find relevant terms
    relevant_terms = []
    for term in knowledge_base.keys():
        if term in input_tokens:
            relevant_terms.append(term)

    # If no relevant terms found, return a default response
    if not relevant_terms:
        return "Chatbot: I'm sorry, I don't have information on that topic. Can you ask me something else?"

    # Select a random term from the relevant terms
    selected_term = random.choice(relevant_terms)

    # Select a random response from the knowledge base for the selected term
    response = random.choice(knowledge_base[selected_term])

    return "ChatbotVogue: " + response


# Get user's name
user_name = input("ChatBotVogue: Hello, my name is Chatbot Vogue. To whom am I speaking to today? ")
file_name = user_name.lower().replace(" ", "_") + ".txt"  # Generate file name from user's name

# Ask for user's age

user_age = input("ChatbotVogue: Nice to meet you, " + user_name + "! How old are you? ")

# Check if user is interested in fashion
user_interest = input("Do you like fashion? (yes/no) ")
if user_interest.lower() in ['yes', 'yes, i do', 'i do like fashion']:
    print("ChatbotVogue: Great! Let's talk about fashion. How can I help you today?")
elif user_interest.lower() == 'no':
    print("ChatbotVogue: No problem. How can I help you today?")
else:
    print("ChatbotVogue: How can I help you today?")

# Example chatbot loop
# List of exit keywords
exit_keywords = ['yes', 'no']

# Chatbot loop
while True:
    input_text = input("You: ")
    response = generate_response(input_text)
    print(response)
    # Store chat log in a text file
    with open(file_name, 'a') as file:
        file.write("You: " + input_text + "\n")
        file.write(response + "\n")

    exit_option = input("Do you want to exit? (yes/no) ")
    if exit_option.lower() == 'yes':
        print("Chatbot: My pleasure! It was nice talking to you. Goodbye!")
        break
    elif exit_option.lower() == 'no':
        print("Chatbot: Great! Any other vogue terms you would like to know about?")
        continue
    else:
        print("Chatbot: Invalid input. Please enter 'yes' or 'no'.")
        continue





