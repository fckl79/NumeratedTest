## NUMERATED Coding Test - Igor Oliynyk

#### 1. Functionality
----
  1. Module _data/datemodel.py_ - initial data load and data model
      1. The code loads available train routes and directions (_load_routes_)
      2. For every train route it
          1. Loads Route Stops (list stops in certain order) - (_load_stops_)
          2. Records whether stops are aligned with directions - (_find_index_)
  2. Module _data/dataform.py_ - data interface to UI functionality
      1. The results of prior step are recorded in dictionary __dict_routes_stops_directions__ - see _init_dict_routes_
      2. Creates a list of available routes - _populate_routes_
      3. Creates a list of stops for selected route - _populate_stops_
      4. Create a list of directons for routes and stops selected above - _populate_directions_
      5. Calculate predicted departure time - _extract_departure_time_
  3. Module _run.py_ is merely a wrapper to _data/dataform.py_, and it is data interface to UI
      1. This module is in the root
      2. __We do not provide UI here - we worked on the code exchange piece only__


#### 2. How to Run
---
  1. At command prompt run 
     
     _$ python3.* run.py_
     
     It will run some sample test case - it gives a good idea about inputs and outputs
     
  2. Dependencies - _requests, json, datetime, unittest_
  3. Test cases are located in _test/test_dataform.py_
      1. We tested methods in _data/dataform.py_ **only**, since these are dependent on data loads procedures in _data/datemodel.py_
      2. To run test runs
      
      _$ python3.6 -m test.test_dataform_
      
#### 3. Important
---
   1. Any errors affecting sought for result will are propagated, so that they could be shown to the user
   2. We are making several attempts to connect to the server to get the data needed before we exit