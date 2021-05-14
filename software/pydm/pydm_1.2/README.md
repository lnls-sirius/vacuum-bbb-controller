Setup the environment

```powershell
conda create --name vbc python=3.6
conda install qt=5.12.9 epics-base pyepics
pip install -r requirements.txt
```

the file conda-requirements.txt may be used:
```
conda create --name vbc --file conda-requirements.txt
```

Clone and install lnk

```
cd $Home\Documents
git clone https://github.com/lnls-sirius/vacuum-bbb-controller
cd vacuum-bbb-controller\software\pydm\pydm_1.2\python
.\Create-Shortcut.ps1
```

