conda activate vbc
set EPICS_CA_ADDR_LIST="10.128.40.1:5064 10.128.40.1:5068 10.128.40.2:5064 10.128.40.2:5068 10.128.40.3:5064 10.128.40.3:5068 10.128.40.4:5064 10.128.40.4:5068 10.128.40.5:5064 10.128.40.5:5068 10.128.40.6:5064 10.128.40.6:5068 10.128.40.7:5064 10.128.40.7:5068 10.128.40.8:5064 10.128.40.8:5068 10.128.40.9:5064 10.128.40.9:5068 10.128.40.10:5064 10.128.40.10:5068"
pydm --hide-nav-bar --hide-status-bar --hide-menu-bar launch_ui_main_window.py