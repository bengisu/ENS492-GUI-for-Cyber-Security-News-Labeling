from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords

import tensorflow as tf
import re
import demoji
import contractions
import inflect
from pathlib import Path

def number_to_text(data): # write numbers as text and return (...12... => ...twelve...)
  temp_str = data.split()
  string = ""
  for i in temp_str:
    if i.isdigit(): # if the word is digit, converted to 
      temp = inflect.engine().number_to_words(i)
      string += temp + " "
    else:
      string += i + " "
  return string.strip()

def preprocess_text(text):
    # Remove emoticons
    text = demoji.replace(text, '')

    # Lowercase the text
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    #Remove URLs
    text = re.sub(r'https?\S+','',text)

    #Expand contractions
    text = contractions.fix(text)

    #Change numbers to text
    text = number_to_text(text)


    # Initialize stemmer and lemmatizer
    stemmer = LancasterStemmer()
    lemmatizer = WordNetLemmatizer()

    # Tokenize words
    words = nltk.word_tokenize(text)

    # Stem and lemmatize words
    stemmed_words = [stemmer.stem(word) for word in words]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in stemmed_words]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    lemmatized_words = [word for word in lemmatized_words if word not in stop_words]

    return " ".join(lemmatized_words)

def predict(input_text, model,label):
    THRESHOLD= 0.6
    
    lst=[]
    #Preprocess text
    t= preprocess_text(input_text[0])
    lst.append(t)

    max_len = 500 
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = '<OOV>' # out of vocabulary token
    vocab_size = 500
    tokenizer = Tokenizer(num_words = vocab_size, 
                        char_level = False,
                        oov_token = oov_tok)
    tokenizer.fit_on_texts(lst)
    word_index = tokenizer.word_index
    #total_words = len(word_index)
    training_sequences = tokenizer.texts_to_sequences(lst)
    training_padded = pad_sequences(training_sequences,
                                    maxlen = max_len,
                                    padding = padding_type,
                                    truncating = trunc_type)
    y_pred_train = model.predict(training_padded)
    print(label)
    print( y_pred_train)
    if y_pred_train>THRESHOLD:
      return label

def label_lstm(txt):
  final_labels=[]
  for label in labels:
    model_path = str(Path().absolute()) + "\models\lstm\\" + str(label) + "model"
    print(model_path)
    model = load_model(model_path)
    if predict(txt,model,label) != None:
      final_labels.append(predict(txt,model,label))
  return final_labels

txt=["The third quarter of 2022, APWG observed 1,270,883 total phishing attacks — is the worst quarter for phishing that APWG has ever observed. The total for August 2022 was 430,141 phishing sites, the highest monthly total ever reported to APWG. Over recent years, reported phishing attacks submitted to APWG have more than quintupled since the first quarter of 2020, when APWG observed 230,554 attacks. The rise in Q3 2022 was attributable, in part, to increasing numbers of attacks reported against several specific targeted brands. These target companies and their customers suffered from large numbers of attacks from persistent phishers. John Wilson, Senior Fellow, Threat Research at Fortra, noted: “We saw a 488 percent increase in response-based email attacks in Q3 2022 compared to the prior quarter. While every subtype of these attacks increased compared to Q2, the largest increase was in Advance Fee Fraud schemes, which rose by a staggering 1,074 percent.” In the third quarter of 2022, APWG founding member OpSec Security found that phishing attacks against the financial sector, which includes banks, remained the largest set of attacks, accounting for 23.2 percent of all phishing. Attacks against webmail and software-as-a-service (SaaS) providers remained prevalent as well. Phishing against social media services fell to 11 percent of the total, down from 15.3 percent. Phishing against cryptocurrency targets — such as cryptocurrency exchanges and wallet providers — fell from 4.5 percent of all phishing attacks in Q2 2022 to 2 percent in Q3. This mirrored the fall in value of many cryptocurrencies since mid-year. Matthew Harris, Senior Product Manager, Fraud at Opsec, noted: “The Logistics and Shipping sector saw a large fraud volume increase, led specifically by a large increase in phishing against the U.S. Postal Service. And continuing a trend we observed in Q2, we’re tracking a huge increase in mobile phone-based fraud; vishing detection volumes are more than three times what we saw in Q2."]

labels = ["fraud","hacker groups","government", "corporation", "unrelated", "darknet", "cyber defense", "hacking", 
          "security concepts", "security products", "network security", "cyberwar", "geopolitical", "data breach",
          "vulnerability", "platform", "cyber attack"]


#label_list = label_lstm(txt, labels)
#print("====LABEL LIST ====", label_list)
