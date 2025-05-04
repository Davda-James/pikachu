<h1 align="center"> Pikachoo AI </h1>
<div align="center">
  <img src="./pikachu/public/images/pikachu_small.svg" style="height: 400px; width: 400px;">
</div>

[![ultralytics](https://img.shields.io/badge/ultralytics-8.3.123-blue)](https://pypi.org/project/ultralytics/)
[![opencv-python](https://img.shields.io/badge/opencv--python-4.10.0.84-blue)](https://pypi.org/project/opencv-python/)
[![pyyaml](https://img.shields.io/badge/pyyaml-6.0.2-blue)](https://pypi.org/project/PyYAML/)
[![fastapi](https://img.shields.io/badge/fastapi-0.115.12-blue)](https://pypi.org/project/fastapi/)
[![uvicorn](https://img.shields.io/badge/uvicorn-0.34.2-blue)](https://pypi.org/project/uvicorn/)
[![python-multipart](https://img.shields.io/badge/python--multipart-0.0.20-blue)](https://pypi.org/project/python-multipart/)
[![lap](https://img.shields.io/badge/lap-0.5.12-blue)](https://pypi.org/project/lap/)
[![aiortc](https://img.shields.io/badge/aiortc-1.11.0-blue)](https://pypi.org/project/aiortc/)
[![rich](https://img.shields.io/badge/rich-13.7.1-blue)](https://pypi.org/project/rich/)
[![google-auth](https://img.shields.io/badge/google--auth-2.39.0-blue)](https://pypi.org/project/google-auth/)
[![google-auth-oauthlib](https://img.shields.io/badge/google--auth--oauthlib-1.2.2-blue)](https://pypi.org/project/google-auth-oauthlib/)
[![google-auth-httplib2](https://img.shields.io/badge/google--auth--httplib2-0.2.0-blue)](https://pypi.org/project/google-auth-httplib2/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-0.21.0-blue)](https://pypi.org/project/python-dotenv/)
[![google-api-python-client](https://img.shields.io/badge/google--api--python--client-2.169.0-blue)](https://pypi.org/project/google-api-python-client/)


## 📚 Table of Contents
- [Download app](#download-app)
- [Pipeline](#pipeline)
- [Demo](#demo)
  - [Object Detection Demo](#object-detection-demo)
  - [Demo of Tracking Path](#track-path-demo)
  - [Demo of velocity map](#velocity-map-demo)
  - [Demo of anamoly detection](#anamoly-detection-demo)
<!-- - [Data Preparation](#data-preparation) -->
- [Setting project locally](#setting-up-project-locally)
  - [Setting up backend locally](#setting-up-backend)
  - [Setting up frontend locally](#setting-up-frontend)

## Download app


## Pipeline 
<img src="./pikachu/public/images/pipeline.png">

## Demo
### Object Detection Demo



### Track Path Demo

### Velocity Map Demo


### Anamoly Detection

## Setting project locally

### Setting up backend 
- Cloning the repo **https:github.com:Davda-James/pikachu.git**
```bash
git clone https:github.com:Davda-James/pikachu.git
```
- Change the working directory
```bash
cd pikachu
```
- Creating python virtual environment
```bash
python -m venv venv
```
- Activate python virtual environment
  - For linux 
  ```bash
  source venv/bin/activate
  ```
  - For windows
  ```bash
  venv/scripts/activate
  ```
- Install requirements
```bash
pip install -r requirements.txt
```
- Starting backend fastapi server
```bash
uvicorn pikachu.app:app --host 0.0.0.0 --port 8000
```

## Setting up gmail service account
- Visit **https://github.com/Davda-James/InboxGenie/blob/main/README.md**
- Follow above README (skip GEMINI API portion as not needed here)
- Store credentials.json in root directory pikachu

## Setting up frontend
- No need have direct download apk, download from below
- Link to **github** frontend [Frontend](https://github.com/Davda-James/pikachu_frontend.git) if wanted to visit. 
