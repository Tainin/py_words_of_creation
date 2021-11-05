# PyWordsOfCreation



# Setup
## Cloning
In your terminal of choice run:
```git clone https://github.com/Tainin/py_words_of_creation```
## Initializing a python environment
```python -m venv <envirionment name>``` where ```<environment name>``` is replaced with the name you want to give your virtual environment (I use ```pyenv```).
## Installing dependency packages
**Make sure you activate your virtual environment**

On windows: ```<environment name>\Scripts\activate.bat```

On Unix or macOS: ```source <environment name>/Scripts/activate```


**Now you can install pacakges from** ```requirements.txt```

```pip install -r requirements.txt```

# Running
**Make sure you activate your virtual environment. See above for instructions.**

```python test.py <element count>``` where ```<element count>``` is replaced with the number of elements to attempt to generate. If this number is two large the program will never complete (```^C``` to kill it) as the generator will not be able to generate that many elements (they won't all fit on the layer without colliding). If it is two low you might not get interesting images. Play around with it to get different results.
