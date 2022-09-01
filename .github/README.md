
## Project Setup

* Install scoop from www.scoop.sh
* Install allure commandline by running the following command:

```
scoop install allure
```

* git clone
* cd to project directory
* Install virtualenv:

```
py -m pip install --user virtualenv
```

* Create a virtual environment:

```
py -m venv env
```

* Activate your virtual environment:

```
.\env\Scripts\activate
```

* Install pipenv:

```
pip install pipenv
```

* Install project dependencies using pipenv:

```
pipenv install
```

## Running Tests

```
pipenv run pytest --alluredir=allure-results --browser <firefox/chrome_headless>
```

When no browser was selected then chrome will be used.

* Run according to tags:

```
pipenv run pytest -m <tag_name> --browser <firefox/chrome_headless>
```

## Viewing Test Results

* View allure results locally:

```
allure serve allure-results
```

## View Help And Custom CLI Options

```
pytest --help
```
