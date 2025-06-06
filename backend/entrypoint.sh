#!/bin/bash

# Indítjuk a C++ worker-t háttérben
/usr/local/bin/cpp_worker &

# Indítjuk a Python Flask appot
corn
python app.py