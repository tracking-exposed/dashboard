# dashboard
Python libraries for tracking-exposed

## Installation instructions

### Install basic Python libraries
```
sudo apt-get install git python3-venv python3-dev python3-tk python3-pip
```
Note: You need python 3.5.3+ to use altair

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
```
python3 src/wizard.py
```

The scripts create an entry in `config/` directory, you can edit it manually as well.


### Usage

To download you summary data, use
`
python3 src/summary.py --token yourtokenhere
`

To get info on the status of your extension data, use
`
python3 src/status.py --token yourtokenhere
`

Use `--help` to get more info on the arguments you can use.

If you have a configuration file, then try
`python3 src/summary.py -c config/yourname`
or `python3 src/status.py -c config/yourname`

### Configuration Notes

* `name` = arbitrary name to identify your user
* `token` = the fbtrex Token mandatory to retrieve data. 
* `config` = specify a configuration file (like the one created with wizard.py)
* `path` = default save path (must be a writable directory)
* `no-csv` = does not output a csv
* `json` = outputs json data (too)
* `amount` = amount of entries to fetch from api
* `skip` = amount of entries to skip


### How do i retrieve my authentication token?

1. install [fbtrex web-extension](https://facebook.tracking.exposed)
2. have a valid facebook account, and use it with the browser where the fbtrex extension is installed
3. click on "Your data" section, this will open an URL in your browser.
4. the token is part of the URL, for a simple copy-paste, click on the tab "Control your data"


### If the installation fails
If you get an error like "invalid command bdist\_wheel", try:
```
python3 -m pip install wheel
```
Please note that this code has been tested only on Ubuntu 18 or above
