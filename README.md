# ENS492-GUI-for-Cyber-Security-News-Labeling

Setup:
  run "pip install -r requirements1.txt"

  If on MacOS:
    reverse path slashes in model scripts (bert_model, cnn_model, lstm_model) to "/"

    Ex: Current code in "cnn_model": str(Path().absolute()) + "\models\cnn\\" + str(label) + " model"
        Converted code: str(Path().absolute()) + "/models/cnn/" + str(label) + " model"

Launch GUI:
  cd src
  python3 gui.py

