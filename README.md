# dashboard
Python libraries for tracking-exposed

## Installation instructions

### Install basic Python libraries
```
sudo apt-get install git python3-venv python3-dev python3-tk python3-pip
```

### Git clone
```
git clone https://github.com/tracking-exposed/dashboard-git.git && cd dashboard-git
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

### Navigate to the app folder
```
cd dashboard
```

### Run configure
```
python3 configure.py
```

The name you choose is the config name you will use to call the tester script.


### Usage
```
python3 app.py --help
```
If you have a configuration file ready in config/, try:
`python3 app.py -c config/$confname`

### Configuration Notes

* `name` = arbitrary name to identify your user
* `id` = the ID you can retrieve in the URL you reach by clicking on *'Your Data'* on the browser in which you installed the extension.
* `config` = specify a configuration file (like the one created with configure.py)
* `start` = start date, format yyyy-mm-dd
* `end` = end date, format yyyy-mm-dd
* `path` = default save path (must be a writable directory)
* `no-csv` = do not output csv
* `no-png` = do not output png
* `no-html` = do not output html

##### How do i retrieve my id?

The easiest way to retrieve your unique id, right now, is to open your facebook profile in the browser where you installed the facebook.tracking.exposed extension. When you scroll the facebook wall, you will see a link with the name "Your Data". Follow that link, and look in your URL bar. Between two slashes (/) you will see an alphanumeric string. That string is your user id. It should be 40 characters long.

##### Usage

You can read some helpful information by running `python3 app.py --help`.


### If the installation fails
If you get an error like "invalid command bdist\_wheel", try:
```
python3 -m pip install wheel
```
