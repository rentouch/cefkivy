How to install
==============
Notes about the requirements.txt file:
The cefpython3 dependency is the cefpython python package built by Rentouch.
(used for CI). Please use your own version of cefpython either by
exporting the PYTHONPATH to the location of the built cefpython or by installing
cefpython globally.

You need the following dependencies installed listed in the requirements.txt


About this project
==================
This can be seen as a kivy/garden.cefpython fork. Rentouch needs more
flexibility in the repo itself (version numbers, room for experiments,
tighter integration with pip, by creating wheels etc...)


About the import of cefpython
=============================
It will try to import in the following order:
1. Cefpython binary in the PYTHONPATH
2. Cefpython binary globally installed