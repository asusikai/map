#!/bin/bash

echo "start"

/home/dongjun/.local/share/virtualenvs/map-2fGTvbJF/bin/python /home/dongjun/project/newmap/map/crawl/py_crawling.py

echo "crawl fin"

/home/dongjun/.local/share/virtualenvs/map-2fGTvbJF/bin/ipython /home/dongjun/project/newmap/map/ml_files/ml_test.ipynb

echo "ml fin"