# IndoorNavigation - [InsertProjectNameHere]
## Overview
Presently simply shows an estimated depth stream from the OAK-D camera.

Look into the depthai and opencv APIs for programming info.

Can simply be run with `python3 main.py`.  If no camera is connected, the program will crash.

Other, more complicated sample programs with more fancy features are available.  We can look to those for inspiration if we wish.  https://github.com/luxonis/depthai-experiments

## SETUP
```
$ sudo apt install python3
$ sudo apt install virtualenv
 # In a separate folder from the repo #
$ python3 -m virtualenv env
$ source env/bin/activate
 # cd into your repo #
$ pip3 install -r requirements.txt
$ python3 main.py
 # to deactivate virtualenv #
$ deactivate 
```
