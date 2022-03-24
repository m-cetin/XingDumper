#!/usr/bin/python
# -*- coding: utf-8 -*-
# modified version of xingdumper: https://github.com/l4rm4nd/XingDumper

import requests
import json
import re
import unicodedata
import argparse
from datetime import datetime
import os
from time import sleep

def login(mail, password):
        s = requests.Session()
        payload = {
            'username': mail,
            'password': password,
            'perm':'0'
        }

        #print('Login:')
        #print("First Request: requesting CSRF token")
        response1 = requests.get('https://login.xing.com/login/api/login')
        #print(response1.cookies)
        cookies_dict = response1.cookies.get_dict()
        cookies_values = list(cookies_dict.values())
        csrf1 = cookies_values[2]
        csrf_check1 = cookies_values[1]
        #print("---------------------------------------------------------------------------------------------------")

        #print("Second Request: Receiving link including Auth: ")
        response2 = requests.post("https://login.xing.com/login/api/login", json=payload, cookies=response1.cookies, headers={"X-Csrf-Token": csrf1, "Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0 (X11; Linux x86_x64) AppleWebKit/537.11 (KHTML, like Gecko)", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8", "Accept-Charset":"ISO-8859-1,utf--8;q=0.7,*;q=0.3","Accept-Encoding":"none","Connection":"keep-alive","Accept-Language":"en-US,en;q=0.8"}, allow_redirects=False)
        #print(response2)
        result = re.search('(?<=href=").*?(?=")', response2.text)
        link= result.group(0)
        #print("Success. Authentication Link: ", link)
        #print("---------------------------------------------------------------------------------------------------")

        #print("Third Request: Following Auth Link and receiving Login tken + new CSRF tokens")
        response3 = requests.get(link, allow_redirects=False, cookies=response2.cookies)
        cookies_dict2 = response3.cookies.get_dict()
        cookie_values2 = list(cookies_dict2.values())
        login_token = cookie_values2[2]
        #print("Successfully logged in. Token: ", login_token)
        #print("---------------------------------------------------------------------------------------------------")

        return login_token


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--url", metavar='<xing-url>', help="A XING company url - https://xing.com/pages/<company>", type=str, required=True)
parser.add_argument("--count", metavar='<number>', help="Amount of employees to extract - max. 2999", type=int, required=False)
parser.add_argument("--msuffix", help="Mail suffix of the company, for example: @google.com", type=str, required=True,)
parser.add_argument("--full", help="Dump additional contact details (slow) - email, phone, fax, mobile", required=False, action='store_true')
parser.add_argument("--quiet", help="Show employees email address only", required=False, action='store_true')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='python xing.py --url https://www.xing.com/pages/googlegermanygmbh --msuffix @google.com')

args = parser.parse_args()
url = args.url
msuffix = args.msuffix

#############################################################
########### CREDENTIALS FOR YOUR XING ACCOUNT ###############
########### NEEDED FOR AUTHENTICATION #######################
#############################################################

# uncomment the next line, if you want to store the credentials
# inside this script and delete "session = 0":

#session = login('xing-username@gmail.com','SecretPass')
session = 0

######## checking if credentials are provided ###############

authentication_file = "auth.txt"

def authentication():
    if os.path.exists(authentication_file) and os.path.getsize(authentication_file) > 0:
        print("Valid credentials found!")
        f=open("auth.txt","r")
        lines=f.readlines()
        xing_user=lines[1].rstrip("\n")
        xing_pass=lines[2].rstrip("\n")
        f.close()
        return xing_user,xing_pass
    else:
        try:
            print("No credentials for XING found to make this script work!")
            xing_username = input("Your XING email (e.g. test@gmail.com): ")
            xing_password = input("Your XING password: ")
            print("Saving results into auth.txt..")
            sleep(1)
            f=open("auth.txt","a")
            f.write("[+] XING credentials\n")
            f.write(xing_username+"\n")
            f.write(xing_password+"\n")
            sleep(1)
            print("Successfully saved credentials..")
            f.close()
        except:
            print("Something went wrong..")
            exit(1)

while True:
    try:
        global userXing
        global passXing
        creds = authentication()
        userXing = creds[0]
        passXing = creds[1]
        if userXing != 0 and passXing != 0:
            break
    except:
        pass

session = login(userXing,passXing)

#############################################################
#############################################################
####### ALTERNATIVELY USE THE CONFIG FILE auth.txt ##########
#############################################################
#############################################################

if session != 0:
    LOGIN_COOKIE = session
    if (args.count and args.count < 3000):
        count = args.count
    else:
        # according to XING, the result window must be less than 3000
        count = 2999

    api = "https://www.xing.com/xing-one/api"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_x64) AppleWebKit/537.11 (KTHML, like Gecko)', 'Content-type': 'application/json', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding':'none','Accept-Language':'en-US,en;q=0.8','Accept-Charset':'ISO-8859-1,utf-8,q=0.7,*;q=0.3', 'cache-control':'no-cache','Connection':'keep-alive'}
    cookies_dict = {"login": LOGIN_COOKIE}

    if (url.startswith('https://www.xing.com/pages/')):
        try:
            before_keyword, keyword, after_keyword = url.partition('pages/')
            company = after_keyword

            # retrieve company id from the api
            postdata1 = {"operationName":"EntitySubpage","variables":{"id":company,"moduleType":"employees"},"query":"query EntitySubpage($id: SlugOrID!, ) {\n entityPageEX(id: $id) {\n ... on EntityPage {\n slug\n  title\n context {\n  companyId\n }\n  }\n }\n}\n"}
            r = requests.post(api, data=json.dumps(postdata1), headers=headers, cookies=cookies_dict)
            response1 = r.json()
            #print(response1)
            companyID = response1["data"]["entityPageEX"]["context"]["companyId"]

            # retrieve employee information from the api based on previously obtained company id
            postdata2 = {"operationName":"Employees","variables":{"consumer":"","id":companyID,"first":count,"query":{"consumer":"web.entity_pages.employees_subpage","sort":"CONNECTION_DEGREE"}},"query":"query Employees($id: SlugOrID!, $first: Int, $after: String, $query: CompanyEmployeesQueryInput!, $consumer: String! = \"\", $includeTotalQuery: Boolean = false) {\n  company(id: $id) {\n id\n totalEmployees: employees(first: 0, query: {consumer: $consumer}) @include(if: $includeTotalQuery) {\n total\n }\n employees(first: $first, after: $after, query: $query) {\n total\n edges {\n node {\n profileDetails {\n id\n firstName\n lastName\n displayName\n gender\n pageName\n location {\n displayLocation\n  }\n occupations {\n subline\n }\n }\n }\n }\n }\n }\n}\n"}
            r2 = requests.post(api, data=json.dumps(postdata2), headers=headers, cookies=cookies_dict)
            response2 = r2.json()



            if not args.quiet:

                print("[i] Company Name: " + response1["data"]["entityPageEX"]["title"])
                print("[i] Company X-ID: " + companyID)
                print("[i] Company Slug: " + company)
                print("[i] Dumping Date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                print()

            if args.full:
                legende = "Firstname;Lastname;Location;E-Mail;Fax;Mobile;Phone"
            else:
                legende = "E-Mail"

            print(legende)

            dump_count = 0

            # loop over employees
            for employee in response2['data']['company']['employees']['edges']:
                dump_count += 1
                firstname = employee['node']['profileDetails']['firstName']
                lastname = employee['node']['profileDetails']['lastName']

                if args.full:
                    # dump additional contact details for each employee. Most often is "None", so no default api queries for this data
                    postdata3 = {"operationName":"getXingId","variables":{"profileId":pagename},"query":"query getXingId($profileId: SlugOrID!, $actionsFilter: [AvailableAction!]) {\n  profileModules(id: $profileId) {\n    __typename\n    xingIdModule(actionsFilter: $actionsFilter) {\n      xingId {\n        status {\n          localizationValue\n          __typename\n        }\n        __typename\n      }\n      __typename\n      ...xingIdContactDetails\n       }\n  }\n}\n\nfragment xingIdContactDetails on XingIdModule {\n  contactDetails {\n    business {\n          email\n      fax {\n        phoneNumber\n   }\n      mobile {\n        phoneNumber\n  }\n      phone {\n        phoneNumber\n   }\n   }\n        __typename\n  }\n  __typename\n}\n"}
                    r3 = requests.post(api, data=json.dumps(postdata3), headers=headers, cookies=cookies_dict)
                    response3 = r3.json()
                    try:
                        # try to extract contact details
                        fax = response3['data']['profileModules']['xingIdModule']['contactDetails']['business']['fax']['phoneNumber']
                        mobile = response3['data']['profileModules']['xingIdModule']['contactDetails']['business']['mobile']['phoneNumber']
                        phone = response3['data']['profileModules']['xingIdModule']['contactDetails']['business']['phone']['phoneNumber']
                    except:
                        # if contact details are missing in the API response, set to 'None'
                        fax = "None"
                        mobile = "None"
                        phone = "None"
                    # print employee information as Comma Separated Values (CSV)
                    print(firstname + ";" + lastname + ";" + position + ";" + fax + ";" + mobile + ";" + phone + ";" + firstname[0] + '.' + lastname + msuffix)
                else:
                    print(firstname[0] + '.' + lastname + msuffix)

            if not args.quiet:
                            print("[i] Successfully crawled " + str(dump_count) + " " + response1["data"]["entityPageEX"]["title"] + " employees.")
        except:
            # likely authorization error due to incorrect 'login' cookie
            # otherwise the script is broken or the api has been changed
            print()
            #print("[!] Authentication required. Login failed!")

            #print("[debug] " + str(e))
    else:
        print()
        print("[!] Invalid URL provided.")
        print("[i] Example URL: 'https://www.xing.com/pages/appleretaildeutschlandgmbh'")
