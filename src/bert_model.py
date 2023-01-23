import nltk
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import re, string
import contractions
from transformers import AutoTokenizer
import torch
from torch.optim import AdamW
from torch.utils.data import TensorDataset, SequentialSampler, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer, EvalPrediction, AutoTokenizer
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
import numpy as np

nltk.download('punkt')
nltk.download('wordnet')

import numpy as np

def url_remover(data): # remove any url in text
  return re.sub(r'https?\S+','',data)

# def web_associated(text):
#   text = url_remover(text)
#   return text

# -------------------------------

def remove_round_brackets(data): # remove anything between two round brackets
   return re.sub('\(.*?\)','',data)

punctList = string.punctuation + '“”' 
def remove_punc(data): # remove any punctuation
  trans = str.maketrans('','', punctList)
  return data.translate(trans)

def remove_emojis(data): # remove any emojis
   emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
   return emoji_pattern.sub(r'', data) # no emoji

def white_space(data): # remove any double or more space
  return ' '.join(data.split())

def complete_noise(data):
  new_data = remove_round_brackets(data)
  new_data = remove_punc(new_data)
  new_data = remove_emojis(new_data)
  new_data = white_space(new_data)
  return new_data

# -------------------------------
def text_lower(data): # make every letter lowercase
  return data.lower()

def contraction_replace(data): # fix contractions (e.g. won't => will not)
  return contractions.fix(data)

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

def normalization(data):
  text = text_lower(data)
  text = number_to_text(text)
  text = contraction_replace(text)
  tokens = nltk.word_tokenize(text)
  return tokens

# -------------------------------

def stopword(data): # remove stopwords
  clean = []
  for i in data:
    if i not in stopwords.words('english'):
      clean.append(i)
  return clean

def stemming(data): # stem the text
  stemmer = LancasterStemmer()
  stemmed = []
  for i in data:
    stem = stemmer.stem(i)
    stemmed.append(stem)
  return stemmed

def lemmatization(data): # lemmatize the text
  lemma = WordNetLemmatizer()
  lemmas = []
  for i in data:
    lem = lemma.lemmatize(i, pos='v')
    lemmas.append(lem)
  return lemmas  

def final_process(data, type= "stem"):
  return " ".join(data)

# -------------------------------

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def preprocessForPrediction(myStr):
    text = url_remover(myStr)
    text = complete_noise(text)
    text = normalization(text)
    text = final_process(text)
    encoding = tokenizer(text, truncation=True, padding="max_length", max_length=512, return_tensors="pt")
    # encoding = tokenizer.encode(text, truncation=True, padding="max_length", max_length=512, return_attention_mask=True, return_tensors="pt")
    return encoding

def bert_interface(model, text):
  softmax = torch.nn.Sigmoid()
  preprocessed_text = preprocessForPrediction(text)

  input_ids = preprocessed_text["input_ids"]
  attention_mask = preprocessed_text["attention_mask"]

  logits = model(input_ids, attention_mask)[0]
  prob = softmax(logits).detach().numpy()[0][0]
  return prob > 0.5

def label_bert(text):
  return text

model = BertForSequenceClassification.from_pretrained("/content/drive/MyDrive/ENS 492 Models/11-01-23/bert-model-outputs_network security/checkpoint-5365")

# 0s
text = "Microsoft, Adobe Exploits Top List of Crooks’ Wish List https://threatpost.com/top-microsoft-adobe-exploits-list/166241/ You can’t possibly patch all CVEs, so focus on the exploits crooks are willing to pay for, as tracked in a study of the underground exploit market."
# text = "Fujitsu SaaS Hack Sends Govt. of Japan Scrambling https://threatpost.com/fujitsu-saas-hack-japan-scrambling/166517/ Tech giant disables ProjectWEB cloud-based collaboration platform after threat actors gained access and nabbed files belonging to several state entities."
# text = "ASDSDAD deneme deneme"

# 1s
# text = '‼ CVE-2021-20600 ‼ Uncontrolled resource consumption in MELSEC iQ-R series C Controller Module R12CCPU-V all versions allows a remote unauthenticated attacker to cause a denial-of-service (DoS) condition by sending a large number of packets in a short time while the module starting up. 📖 Read via "National Vulnerability Database".'
# text = "WireX DDoS botnet admin charged for attacking hotel chain The US Department of Justice charged the admin of the WireX Android botnet for targeting an American multinational hotel chain in a distributed denial-of-service (DDoS) attack."

bert_interface(model, text)