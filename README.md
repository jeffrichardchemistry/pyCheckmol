# pyCheckmol

This is an application for detecting functional groups of a molecule, created using features from the compiled checkmol. This application was created thinking about providing a molecular descriptor in Python language for use in machine learning models.

# Install
<b>Dependencies:</b>
python3-dev python3-pip<br>
Ex: Distros based on Debian/ubuntu.
```
$ sudo apt-get install python3-dev python3-pip
```

<b>Via github</b>
```
$ git clone https://github.com/jeffrichardchemistry/pyCheckmol
$ cd pyCheckmol
$ python3 setup.py install
$ pycheckmol-config
```
# How to use in argsparse format
After installing the python package, as shown in the above code, go to the pyCheckmol folder directory downloaded from this repository: `.../pyCheckmol/pyCheckmol`

<b>Using smiles string</b>
```shellscript
$ cd .../pyCheckmol/pyCheckmol
$ python3 pyCheckmol.py -smi 'CCC(=O)OCCNC(=O)CCN(C)CCOCCNCC'
```
![image](https://github.com/jeffrichardchemistry/pyCheckmol/assets/52516615/61d3cd48-f9bc-4430-bff7-cf24acc8ec1c)

<b>Using molecules file path</b>
```shellscript
$ cd .../pyCheckmol/pyCheckmol
$ python3 pyCheckmol.py --path /path/to/file
```

