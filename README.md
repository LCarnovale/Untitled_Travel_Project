# Hosted Azure website
**This website is also available online at [http://untitled-travel.azurewebsites.net/](http://untitled-travel.azurewebsites.net/)**. This is automatically hosting the server for the master branch of this respository, updating every few minutes, and you **do not need to clone this repository or run any code** to access it.

The following instructions are for running the website locally, or for hosting the website on a different azure instance/third-party hosting service.

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

# Giving the backend access to a database
This step is required to allow the program to access a database.
Also required is an ODBC Driver for SQL servers, available for Windows 
[here](https://www.microsoft.com/en-us/download/details.aspx?id=56567).


Once the repository has been cloned to your computer, create a new file in the top level of the repo
called `connect_config.py`. Copy the following into that file:

```python
import pyodbc

DRIVER = "{ODBC Driver 17 for SQL Server}" # Change the version number from 17 if necessary
SERVER = "<server>"        # SQL Server name, eg: 'tcp:servername.database.net'
DATABASE = "<database>"    # Database name
UNAME = "<username>"       # Server's username
PASSWORD = "<password>"    # Server's password

def get_connection():
	cnxn = pyodbc.connect(f"Driver={DRIVER};Server={SERVER};Database={DATABASE};Uid={UNAME};Pwd={PASSWORD};Encrypt=yes;")
	return cnxn

if __name__ == "__main__":
	print("Attempting connection (no output on success)")
	get_connection()
```
And use the target SQL server's name, database, username and password (and change the driver if necessary) 
in the incomplete fields. You can check this works by running it in any environment that has pyodbc installed:
```cmd
(project_venv) connect_config.py
Attempting connection (no output on success)

(project_venv) 
```
**For a new database** use the script [here](#dbgen) to create a database that can be used by the program.

**If you want to use our existing database** (for marking purposes), use the following values:

```python
DRIVER = "{ODBC Driver 17 for SQL Server}" # Change the version number from 17 if necessary
SERVER = "tcp:untitledtestserver.database.windows.net,1433"
DATABASE = "testVenueDB"
UNAME = "admin1"
PASSWORD = "password1!"
```

If you choose to use the existing database, we will need to add your IP to the whitelist. Please email any of us with your IP and we give you access to the database:

Ian Thorvaldson: i.thorvaldson@unsw.edu.au

Leo Carnovale: l.carnovale@unsw.edu.au

Kittipat Sangdao: k.sangdao@student.unsw.edu.au

Bryan Liauw: b.liauw@unsw.edu.au

**NOTE:** The program is able to detect if a firewall has blocked your ip address, and will raise an exception 
giving your ip address, and saying that it has been blocked:
```
Exception: Your ip (***.***.***.***) was denied.
```
You will still be able to run the website, but any interactions with the database will raise this error.

# Running the program
On windows, the most reliable way to run the server is to specify the current default python install which will
use the virtual environment's python path:
```cmd
(project_venv) python run.py
```

On posix systems:
```bash
(project_venv) ./run.py
```

If you recieve an error including the following text:
```
Can't open lib 'ODBC Driver 17 for SQL Server'
```
You have an error with the ODBC Driver for SQL servers, mentioned in the section "Giving the backend access to the database".


# Running the crawler
The crawler can be run the same way as the main program, but with `runcrawler.py`. 
Currently the crawler is configured to crawl AirBnb sites only.

# <a name="dbgen"></a>Creating a fresh database
The following SQL script will create a fresh database including a sentinal external source owner:
```sql
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- Create Addresses table --
CREATE TABLE [dbo].[Addresses](
	[aid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[location] [text] NULL,
	[lat] [varchar](10) NULL,
	[lng] [varchar](10) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

-- Create Users table --
CREATE TABLE [dbo].[Users](
	[userid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [varchar](100) NOT NULL,
	[userName] [varchar](30) UNIQUE NOT NULL,
	[email] [varchar](100) NULL,
	[phone] [varchar](15) NULL,
	[description] [text] NULL,
	[pwdhash] [varbinary](512) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

-- Create Owners table --
CREATE TABLE [dbo].[Owners](
	[ownerid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [varchar](100) NOT NULL,
	[userName] [varchar](30) UNIQUE NOT NULL,
	[email] [varchar](100) NULL,
	[phone] [varchar](15) NULL,
	[description] [text] NULL,
	[pwdhash] [varbinary](512) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
-- Add external source owner --
SET IDENTITY_INSERT Owners ON
INSERT INTO Owners (ownerid, name, userName)
VALUES (-1, '_ExternalOwner', '_ExternalOwner')
SET IDENTITY_INSERT Owners OFF
GO

-- Create Venues table --
CREATE TABLE [dbo].[Venues](
	[venueid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[ownerid] [int] NOT NULL,
	[addressid] [int] NOT NULL,
	[name] [varchar](200) NOT NULL,
	[bedCount] [tinyint] NULL,
	[bathCount] [tinyint] NULL,
	[carCount] [tinyint] NULL,
	[description] [text] NULL,
	[rate] [smallmoney] NULL,
	[minStay] [int] NULL,
	[maxStay] [int] NULL,
	[details] [text] NULL,
	[ExtSource] [varchar](250) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

-- Create Availabilities table --
CREATE TABLE [dbo].[Availabilities](
	[avId] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[venueid] [int] NULL,
	[startDate] [date] NULL,
	[endDate] [date] NULL
) ON [PRIMARY]
GO

-- Create Bookings table --
CREATE TABLE [dbo].[Bookings](
	[bookid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[venueid] [int] NOT NULL,
	[userid] [int] NOT NULL,
	[startDate] [date] NOT NULL,
	[endDate] [date] NOT NULL
) ON [PRIMARY]
GO

-- Create Images table --
CREATE TABLE [dbo].[Images](
	[imId] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[venueid] [int] NULL,
	[path] [nvarchar](250) NOT NULL
) ON [PRIMARY]
GO



-- Create Reviews table --
CREATE TABLE [dbo].[Reviews](
	[revid] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[venueid] [int] NOT NULL,
	[userid] [int] NOT NULL,
	[postDateTime] [datetime] NULL,
	[recommends] [bit] NULL,
	[reviewBad] [text] NULL,
	[reviewGood] [text] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

-- Set References --
ALTER TABLE [dbo].[Availabilities]  WITH CHECK ADD FOREIGN KEY([venueid])
REFERENCES [dbo].[Venues] ([venueid])
GO
ALTER TABLE [dbo].[Bookings]  WITH CHECK ADD FOREIGN KEY([userid])
REFERENCES [dbo].[Users] ([userid])
GO
ALTER TABLE [dbo].[Bookings]  WITH CHECK ADD FOREIGN KEY([venueid])
REFERENCES [dbo].[Venues] ([venueid])
GO
ALTER TABLE [dbo].[Images]  WITH CHECK ADD FOREIGN KEY([venueid])
REFERENCES [dbo].[Venues] ([venueid])
GO
ALTER TABLE [dbo].[Reviews]  WITH CHECK ADD FOREIGN KEY([userid])
REFERENCES [dbo].[Users] ([userid])
GO
ALTER TABLE [dbo].[Reviews]  WITH CHECK ADD FOREIGN KEY([venueid])
REFERENCES [dbo].[Venues] ([venueid])
GO
ALTER TABLE [dbo].[Venues]  WITH CHECK ADD FOREIGN KEY([addressid])
REFERENCES [dbo].[Addresses] ([aid])
GO
ALTER TABLE [dbo].[Venues]  WITH CHECK ADD FOREIGN KEY([ownerid])
REFERENCES [dbo].[Owners] ([ownerid])
GO
```
