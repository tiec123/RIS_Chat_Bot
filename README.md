# RIS_Chat_Bot

RIS chat bot is a Llama based AI assistant that is designed to be implemented in the Radiology Information System (RIS) developed by TIEC (Pvt.) Ltd. This application uses a quantized model ([model quantization](https://www.llama.com/docs/how-to-guides/quantization/)) of Llama 3.1 ([model link](https://drive.google.com/drive/folders/1FZT8Zokf3XQIRNZF5xHGeorMY13rwMla)) coupled with Retrieval Augmented Generation (RAG) to specialize the application in specific subjects ([the unquantized original model can be found at llama.com](https://www.llama.com/)). 

Features

  1. This application is designed to be executed locally in a machine without connecting to an external server.
  2. The user can define the scope for the AI assistant by customizing the data set for the application.
  3. The application uses multiple agents created with Llama 3.1 model to ensure accurate and precise results.
  4. A web search function that broadens the scope of the AI assistant.

## Running the code

This application was developed using Python 3.12.4 ([download python](https://www.python.org/downloads/)). The python packages required to run this application is listed in the **requirements.txt** file.

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

You will need to create a **data** directory in the same directory you saved the codes for this application. If your using the **main_api.py** code you can simply add files to the data directly from the UI otherwise if your using the **main.py** code you will need to manually add the required resources to the **data** directory (the resources need to be in pdf format). As for the URLs similarly you can use the UI or manually edit the **urls.txt** file to add resources in URL form.

### Adding pdfs form UI

<div align="center">
  <img src="https://github.com/user-attachments/assets/d49d2d5c-f6a9-4764-b09e-2c28a494ed86" alt="Screenshot (15)" width="500" height="300">
  <img src="https://github.com/user-attachments/assets/5405d9d8-2486-436f-82d7-5530425e1f42" alt="Screenshot (15)" width="500" height="300">
</div>

### Adding URLs form UI

<div align="center">
  <img src="https://github.com/user-attachments/assets/bd537432-c760-4598-b50d-d4e3811b7d39" alt="Screenshot (15)" width="300" height="200">
  <img src="https://github.com/user-attachments/assets/56a7b95d-35f6-4b7a-b70e-0113f9781881" alt="Screenshot (15)" width="300" height="200">
  <img src="https://github.com/user-attachments/assets/12514f9a-9507-428f-a8cd-b552c99b06f1" alt="Screenshot (15)" width="300" height="200">
</div>



