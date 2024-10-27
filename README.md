Por favor no crear carpetas, para que el agente de IA
pueda calificar sus trabajos

Please do not create nested folders and do not nest files into
the folders in order to the AI agent be able to grade your homeworks

## Create and activate Python virtual environment
```bash
    python3 -m venv venv
    .\venv\Scripts\activate
```

## Install dependencies
Create file *requirements.txt*

```bash
    pip3 install -r requirements.txt
```

## Run uvicorn project

```bash
    uvicorn app.main:app --reload
    http://127.0.0.1:8000/docs
```


# Utilities
## Steps to remove virtual environment
```bash
    deactivate
    rm -rf venv
```