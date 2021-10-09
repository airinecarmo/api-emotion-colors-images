## API for Analysis Colors and Emotions in Images
---

This project is a REST API to analyse images by colors and their emotions. 


### Install and execute locally

1. Install python 3.8.10

2. Install dependences: `pip install -r requirement.txt`

3. To run project: `python main.py`

### Running in Docker Build

To build project image, run:

```bash
docker build -t emotions_in_colors_api:1.0.0 .
```

To run image:

```bash
docker run -d -p 8080:8080 --name eic_api_container emotions_in_colors_api:1.0.0
```

To see api documentation locally, access http://localhost:8080/docs.

### Running in Docker Compose

To run:

```
docker-compose up -d
```

to stop:

```
docker-compose down
```