# heroku-ch

### Prepare for Deploy

- create Procfile
  - state the web server used
- create runtime.txt
  - specify pyton version
- create requirements.txt
 - `pipenv run pip freeze > requirements.txt`

### deploy
```bash
git push heroku main
```