# pylai
A little program that takes in the pylint output and tries to fix the problems with openai

## Install

1. `git clone https://github.com/ribalba/pylai.git`
2. `python -m venv venv`
3. `source venv/bin/active`
4. `pip install requrements.txt`
5. `which python3` and copy paste this value
6. edit the pylai.py file
   1. to have the copied python3 interepreter as shebang
   2. add your openai key

## The problem

When running pylint often you get loads of errors that are annoying to figure out and see what is wrong. Mostly
there are small problems that just take up your time.

```
callibrate.py:83:12: W0133: Exception statement has no effect (pointless-exception-statement)
callibrate.py:89:12: W0133: Exception statement has no effect (pointless-exception-statement)
callibrate.py:119:0: W1404: Implicit string concatenation found in list (implicit-str-concat)
callibrate.py:205:18: R1732: Consider using 'with' for resource-allocating operations (consider-using-with)
callibrate.py:279:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
callibrate.py:284:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
```

this the output after a coding session. Now you can use pylai to fix most of these issues:

```
pylint callibrate.py | pylai.py
```

Make sure that pylai.py is in your $PATH and the #! (shebang), in the pylai file, is set to the correct python
interpreter. This is needed so that it will find the venv files
