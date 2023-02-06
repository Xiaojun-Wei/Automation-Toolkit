# Sentence Tagger

This Sentence Tagger is a 3-tier application, deployed on **Heroku**.

1. Frontend: UI is written in HTML/CSS/JavaScript
2. Backend: Python, Flask
3. Database: SQLAlchemy

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
