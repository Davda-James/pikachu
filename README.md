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
- [Setting project locally](#setting-up-project-locally)
  - [Setting up backend locally](#setting-up-backend)
  - [Setting up frontend locally](#setting-up-frontend)
- [Canva](#canva-ppt-link)


## Pipeline 
<img src="./pikachu/public/images/pipeline.png">

## Demo
### Object Detection Demo
[Video](https://github.com/user-attachments/assets/a88cb2dd-fc75-4083-890d-2d2d244c9c39)


### Track Path Demo
[Video](https://github.com/user-attachments/assets/fca94df9-1a3c-4c4f-8226-36a46fe33dad)


### Track Path with overlay Demo
[Video](https://github.com/user-attachments/assets/7241c43c-8eff-4814-a146-e129a6d2a927)


### Velocity Map Demo
[Video](https://github.com/user-attachments/assets/09e0906b-c00a-41ef-8dbc-6c54734e0b9c)


### Anamoly Detection Demo
[Video](https://github.com/user-attachments/assets/c6d12907-c29b-4430-a27c-397617cc1c81)

## Setting up project locally

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

## Canva PPT Link
[Canva](https://www.canva.com/design/DAGmZe80NL8/MUc-exSD9r_IDL8zE9YlNg/edit?utm_content=DAGmZe80NL8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)