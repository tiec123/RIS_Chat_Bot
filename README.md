# RIS_Chat_Bot

RIS chat bot is a Llama based AI assistant that is designed to be implemented in the Radiology Information System (RIS) developed by TIEC (Pvt.) Ltd. This application uses a quantized model (model quantization) of Llama 3.1 (model link) coupled with Retrieval Augmented Generation (RAG) to specialize the application in specific subjects (the unquantized original model can be found at llama.com). 

Features

  1. This application is designed to be executed locally in a machine without connecting to an external server.
  2. The user can define the scope for the AI assistant by customizing the data set for the application.
  3. The application uses multiple agents created with Llama 3.1 model to ensure accurate and precise results.
  4. A web search function that broadens the scope of the AI assistant.

## Running the code

This application was developed using Python 3.12.4 (download python). The python packages required to run this application is listed in the **requirements.txt** file.

```
pip install -r requirements.txt
```

You can run the **main.py** code which dose not use a UI or you can run the **main_api.py** code.

```
cd /file_path
python main.py
```
or
```
cd /file_path
python main_api.py
```

## Adding resources to define the scope of the AI assistant 
