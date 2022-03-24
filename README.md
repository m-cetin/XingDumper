# XingDumper
Python 3 script to dump company employees from XING API. Perfect OSINT tool ;-)

The results contain firstname, lastname, position, gender, location and a user's profile link. Only 2 API calls are required to retrieve all employees. 

With the `--full` CLI flag an additional API request will be made for each employee to retrieve contact details such as email, fax, mobile and phone number. However, this data is most often unset by XING users.

## How-To
1. Run the tool, it'll ask you for your xing username (email) and password
2. The script will locally save your credentials into a file called "auth.txt" and use these for authentication
3. Browse your company on XING and note the url
4. Install requirements via ``pip install -r requirements.txt``
5. Run the Python script and enjoy results

## Usage
````
usage: xingdumper.py [-h] --url <xing-url> [--count <number>] [--full] [--quiet]

optional arguments:
  -h, --help         show this help message and exit
  --url <xing-url>   A XING company url - https://xing.com/pages/<company>
  --count <number>   Amount of employees to extract - max. 2999
  --full             Dump additional contact details (slow) - email, phone, fax, mobile
  --quiet            Show employee results only
````

## Examples

Dumping all Audi employee emails from XING API (max. 3000) into outfile using `--quiet` mode:
````
python3 xingdumper.py --url https://www.xing.com/pages/audiag --msuffix @audi.de --quiet > audi_employees.out
````
Dumping all Audi employees from XING API (max. 3000) into outfile using `--quiet` mode:
````
python3 xingdumper.py --url https://www.xing.com/pages/audiag --quiet > audi_employees.out
````
Dumping 10 Apple employees from XING API with additional contact details as terminal output:
````
python3 xingdumper.py --url https://www.xing.com/pages/appleretaildeutschlandgmbh --count 10 --full
````
**Note**: Contact details are most often empty. We Germans take privacy seriously! Further, the details may only be accessible if you already belong to the contact list of the crawled employee. Kinda unlikely, however the default privacy settings of XING would allow a retrival, if the data is configured and the privacy settings not changed by the user.

## Results

The script will return a list of emails, which can be stored as txt file.

````

▒██   ██▒ ██▓ ███▄    █   ▄████ ▓█████▄  █    ██  ███▄ ▄███▓ ██▓███  ▓█████  ██▀███  
▒▒ █ █ ▒░▓██▒ ██ ▀█   █  ██▒ ▀█▒▒██▀ ██▌ ██  ▓██▒▓██▒▀█▀ ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
░░  █   ░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░░██   █▌▓██  ▒██░▓██    ▓██░▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
 ░ █ █ ▒ ░██░▓██▒  ▐▌██▒░▓█  ██▓░▓█▄   ▌▓▓█  ░██░▒██    ▒██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ▒██▒░██░▒██░   ▓██░░▒▓███▀▒░▒████▓ ▒▒█████▓ ▒██▒   ░██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
▒▒ ░ ░▓ ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒  ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░░   ░▒ ░ ▒ ░░ ░░   ░ ▒░  ░   ░  ░ ▒  ▒ ░░▒░ ░ ░ ░  ░      ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
 ░    ░   ▒ ░   ░   ░ ░ ░ ░   ░  ░ ░  ░  ░░░ ░ ░ ░      ░   ░░          ░     ░░   ░ 
 ░    ░   ░           ░       ░    ░       ░            ░               ░  ░  by LRVT                                                   

Valid credentials found!
[i] Company Name: AUDI AG
[i] Company X-ID: 26119.97c242
[i] Company Slug: audiag
[i] Dumping Date: 24/03/2022 14:47:34

E-Mail
S.AMBROSETTI@audi.de
M.ANTONIO@audi.de
A.ARMENGOL GASSOL@audi.de
A.A_@audi.de
G.Abatti@audi.de
I.Abdalrahman@audi.de
K.Abdelgawad@audi.de
J.Abel@audi.de
C.Abel@audi.de
A.Abele@audi.de
M.Aberle@audi.de
F.Abermann@audi.de
E.Ablassmeier@audi.de
B.Ablaßmeier@audi.de
D.Achhammer@audi.de
F.Achhammer@audi.de
(...)
````
