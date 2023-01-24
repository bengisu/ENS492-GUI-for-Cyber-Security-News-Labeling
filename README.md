# ENS492-GUI-for-Cyber-Security-News-Labeling

Setup:
  
  To add your models: Add models to ./src/models/"your ML model name"/...
    
    Ex: .src/models/lstm/fraud model
    
    Ex: .src/models/lstm/cyber attack model
    
    ...

  run "pip install -r requirements1.txt"

  If on MacOS:
  
    reverse path slashes in model scripts (bert_model, cnn_model, lstm_model) to "/"

    Ex: Current code in "cnn_model": str(Path().absolute()) + "\models\cnn\\" + str(label) + " model"
        Converted code: str(Path().absolute()) + "/models/cnn/" + str(label) + " model"

Launch GUI:

  cd src
  
  python3 gui.py

