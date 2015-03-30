#!/bin/bash 
pyuic4 Qt/addPilotDialog.ui > Qt/addPilotDialog.py
pyuic4 Qt/battleViewerDialog.ui > Qt/battleViewerDialog.py
rm *.pyc -rf