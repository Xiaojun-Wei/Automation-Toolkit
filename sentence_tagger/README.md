# Sentence Tagger

This Sentence Tagger is a 3-tier application, deployed on **Docker**.

1. Frontend: UI is written in HTML/CSS/JavaScript
2. Backend: Python, Flask
3. Database: SQLAlchemy


The annotation dictionary is located in **sentence_tagger/static/data/annotation.json**

### How To Run

1. Install `virtualenv`:

```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:

```
$ virtualenv env
```

3. Then run the command:

```
$ .\env\Scripts\activate
```

4. Then install the dependencies:

```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:

```
$ (env) python app.py
```

### How To Build On Docker
1. Download Docker for your device and register an account first

2. Build an image

```
docker build -t "sentence-tagger" .
```

3. Run the container

```
docker run -it sentence-tagger
```
