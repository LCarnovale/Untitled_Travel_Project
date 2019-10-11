# Setup
## Linux subsystem on Windows.
Setup the linux subsystem for windows [here.](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)

## Virtual environment setup
Once bash is working in windows powershell/cmd:
1) Go to the root directory of the repo, in the linux shell.
1) Type the command:
    ```bash
    $ pip3 install virtualenv
    ```
1) Now create the virtual environment with the command below:
    ```bash
    $ virtualenv --python=python3 project_venv
    ```
    This will create a folder called `project_venv`.

## Using the virtual environment
Once setup, activate the virtual environment with:
<!-- The virtual environment is setup already, to use it,
navigate to the root directory of the repository and 
enter the following command in bash: -->
```bash
$ source project_venv/lib/activate
```
Your bash terminal should then look like:
```bash
(project_venv) $ 
```
To use pip in the virtual environment, the normal `pip`
command may work, but if not, use the following to 
install - for example - flask:
```bash
(project_venv) $ python3 -m pip install numpy
```
List dependencies with the command:
```bash
(project_venv) $ python3 -m pip list
```
If you install a new library with pip,
add it to the requirements with:
```bash
(project_venv) $ python3 -m pip freeze > requirements.txt
```
Any libraries you had installed out of the virtual 
environment will not be available in the virtual 
environment, until you install them again inside the 
virtual environment. Similarly, installing libraries 
from the virtual environment will not make them 
available outside the virtual environment.

To deactivate the virtual environment, run the following command:
```bash
(project_venv) $ deactivate
```

