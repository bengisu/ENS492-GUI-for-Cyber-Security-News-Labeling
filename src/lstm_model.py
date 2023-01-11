from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re
import demoji
import contractions
import inflect

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
    total_words = len(word_index)
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

def label_lstm(txt, labels):
  final_labels=[]
  for label in labels:
    model_path = f'\models\lstm\{label}model'
    model = load_model(model_path)
    if predict(txt,model,label) != None:
      final_labels.append(predict(txt,model,label))
  return final_labels