# Web scraper service

A FastApi server running on Python 3.13

### Requirements
- Python 3.13
- Playwright

### Setup 
1. Install Python 3.13 and Playwright for Python
2. Install python dependencies(in venv for local):  `pip install -r requirements.txt`
3. Sync models and DB: `python db.py`
4. Start the service:
   - `fastapi dev main.py` for development

### Docker
1. Build image
2. Sync models and DB:  
`docker run -v /path/db:/db <image> db.py`
3. Start the image
`docker run -d -v /path/to/db:/db /path/to/screenshots:/screenshots -p 8000:8000 <image>`
