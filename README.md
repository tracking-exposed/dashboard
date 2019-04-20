# dashboard
Python libraries for tracking-exposed

## Installation instructions

### Install basic Python libraries
```
sudo apt-get install git python3-venv python3-dev python3-tk python3-pip
```

### Git clone
```
git clone https://github.com/tracking-exposed/dashboard.git && cd dashboard
```

### setting up virtualenv
We recommend using a virtual environment.
```
python3 -m venv venv && source venv/bin/activate
```

### Install requirements
```
python3 -m pip install -r requirements.txt
```

### Run the configuration wizard 
The scripts create an entry in `config/` directory, you can edit by hand
```
python3 src/wizard.py

```

The name you choose is the config name you will use to call the tester script.


### Usage
```
python3 src/app.py --help
```
If you have a configuration file ready in config/, try:
`python3 src/app.py -c config/$confname --csv`

### Configuration Notes

* `name` = arbitrary name to identify your user
* `token` = the fbtrex Token mandatory to retrieve data. 
* `config` = specify a configuration file (like the one created with configure.py)
* `start` = start date, format yyyy-mm-dd
* `end` = end date, format yyyy-mm-dd
* `path` = default save path (must be a writable directory already existing)
* `csv` = outputs a csv
* `png` = putputs a png chart, available only for impression-count
* `html` = outputs an HTML table without styling
* `json` = outputs json data
* `impression-count` = performs impression count instead of showing the whole data, sets to True or False

##### How do i retrieve my authentication token?

1. you should have installed [fbtrex web-extension](https://facebook.tracking.exposed)
2. you should have a valid facebook account, and use it with the browser where the fbtrex extension is installed
3. click on "Your data" section, this would open an URL in your browser. 
4. the token is part of the URL, for a simple copy-paste, click on the tab "Control your data"

##### Usage

The simplest way to produce a csv or json out of your data is to call the script (from the virtual environment):
`python3 src/app.py -c config/Name --csv` or `python3 app.py -c config/Name --json`

If you want to produce impression count instead, you can do:
`python3 src/app.py -c config/Name --png`

You can read some helpful information by running `python3 src/app.py --help`.


### If the installation fails
If you get an error like "invalid command bdist\_wheel", try:
```
python3 -m pip install wheel
```
