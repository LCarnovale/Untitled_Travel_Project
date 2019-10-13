# Virtual Environment Setup
This project makes use of a virtual environment to keep
the modules being used consistent across locations.
## Using Windows Command Prompt:
1) Go to the root directory of the repo. If you are using powershell, type `cmd` to switch to command prompt.
1) Python 3 comes with the newer venv module already installed. 
If the command `python --version` shows python 3+, skip this step. If not, make sure you have python 3 available with `python3 --version`. If not, you will need to get python 3.  
1) Once python 3 is available, then create a virtual environment with the command:
    ```cmd
    python -m venv --python=python3 project_venv
    ```
    If necessary use `python3` on the left instead of `python`.
1) Activate the virtual environment with:
    ```cmd
    project_venv\Scripts\activate
    ```
   Your terminal should now look like:
   ```cmd
   (project_venv) C:\>
   ```
   (with your current working directory after `C:\` )

## Using Linux Subsystem for Windows:
Setup the linux subsystem for windows [here.](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)

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

1) Once setup, activate the virtual environment with:
    ```bash
    $ source project_venv/lib/activate
    ```
    Your bash terminal should then look like:
    ```bash
    (project_venv) $ 
    ```
## Using the virtual environment
From here on the `$` for bash and `C:\>` prefix for cmd
will be omitted.

Depending on which terminal you use, the normal `pip`
command may work, but if not, use `python -m pip` in place of `pip`. 
For example, to update pip (which you may want to do, as sometimes the virtual environment will come with an old version of pip):
```
(project_venv) python -m pip install --upgrade pip
```
In your initial setup, or if the requirements change, update your virtual environment's modules with:
```bash
(project_venv) pip install -r requirements.txt
```
List dependencies with the command:
```
(project_venv) pip list
```
If you install a new library with pip,
add it to the requirements with:
```bash
(project_venv) pip freeze > requirements.txt
```
Any libraries you had installed out of the virtual 
environment will not be available in the virtual 
environment, until you install them again inside the 
virtual environment. Similarly, installing libraries 
from the virtual environment will not make them 
available outside the virtual environment.

To deactivate the virtual environment, run the following command:
```bash
(project_venv) deactivate
```

# Running the program
Currently the backend is configured to run in debug mode. Start the server by running `run.py`:

On windows:
```cmd
(project_venv) run.py
```

On posix systems:
```bash
(project_venv) ./run.py
```
