# dashboard
Python libraries for tracking-exposed

## Installation instructions

### Install basic Python libraries
```
sudo apt-get install git python3-venv python3-dev python3-tk python3-pip
```

### Git clone
```
git clone https://github.com/tracking-exposed/dashboard-git.git && cd dashboard-git/dashboard
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

### Run configure
```
python3 configure.py
```

The name you choose is the config name you will use to call the tester script.

### You can use tester
```
python3 test/tester.py -c config/NAME-YOU-CHOOSE
```

### Usage
```
python3 app.py --help
```

### Configuration Notes

* name = arbitrary name to identify your user
* id = the ID you can retrieve in the URL you reach by clicking on *'Your Data'* on the browser in which you installed the extension.

##### How do i retrieve my id?

provide step by step explanation

### If the installation fails
If you get an error like "invalid command bdist\_wheel", try:
```
python3 -m pip install wheel
```
