#!/usr/bin/python
# BACKup File Locator
#
logo="                 ."
logo1="              ,' `."
logo2="            ,' `,' `."
logo3="     ____    '.' `,' `."
logo4="    /_|__|     `.' `,' `."
logo5="   |     |       `.' `,'|"
logo6="   |_,-._|=====,-.=`.'  |"
logo7=" --- '-' ----- `-' --.`:."
logo8="                      \.,';.,,"
logo9="                       \':';,.:.. Files"
logo10="BACKup File Locator by Tobias Mccurry"

print logo;
print logo1;
print logo2;
print logo3;
print logo4;
print logo5;
print logo6;
print logo7;
print logo8;
print logo9;
print logo10;
print ;

import os, optparse
import socket, urllib, urllib2
import subprocess
import sys, getopt
import time

parser = optparse.OptionParser(usage='python %prog -u URL or python %prog -l LIST',
                               prog=sys.argv[0],
                               )
parser.add_option('-l','--list',action="store", help="List of URLs to test. REQUIRED if a URL is not defined.", type="string", dest="listfile")

parser.add_option('-u', '--url',action="store", help="Test of a single URL. REQUIRED", type="string", dest="url")

#parser.add_option('-r', '--rules',action="store", help="Rules File. Default rules.lst will be used.", type="string", dest="rules", default="rules.lst")

parser.add_option('-e', '--exts',action="store", help="Extensions File. Default ext.lst will be used.", type="string", dest="exts", default="ext.lst")

parser.add_option('-o', '--out',action="store", help="Output File. Default results will be written to BACKFiL.html.", type="string", dest="outfile", default="BACKFiL.html")

parser.add_option('-v', '--verbose',action="store", help="Turn on verbose output. Must be set to on.", dest="ver")

options, args = parser.parse_args()

#grab the options into variables
urlvar = options.url
listvar = options.listfile
#rulesvar = options.rules
extsvar = options.exts
outputvar = options.outfile
vervar = options.ver

#print vervar;

regchecka=0
regcheckb=0
#print urlvar;
#print listvar;

if (urlvar is None):
   #print "URL had no var";
   regchecka = 1
#print "first check";
#print regchecka; 

if (listvar is None):
   #print "List had no var";
   regcheckb = 1
#print "second check";
#print regcheckb;

if (regchecka == 1 ):
 if (regcheckb == 1):
   print "-u or -l mandatory option is missing\n"
   parser.print_help()
   exit(-1)

if ((regchecka == 0) and (regcheckb == 0)):
   print "Only one required argument. Use either -u or -l"
   parser.print_help()
   exit(-1)


#URLTesthtml, return HTML result
def URLTesthtml (url):
 if (vervar == 'on'):
  print "in URLTesthtml";
  print url;
  print "";
 try:
  response = urllib2.urlopen(url)
 except urllib2.HTTPError, err:
  if err.code == 404:
   if (vervar == 'on'):
    print "404 file";
  if err.code == 403:
   if (vervar == 'on'):
    print "403 file";
  else: 
    if (vervar == 'on'):
     print "Error in URLTesthtml.";
 result = response.read()
 return result

def URLTestCode (url):
 if (vervar == 'on'):
  print "in URLTestCode";
  print url;
  print "";
 
 try:
  response = urllib2.urlopen(url)
 except:
  if (vervar == 'on'):
   print "Error in URLTesthtml.";
 try:
  response = urllib.urlopen(url)
 except:
   if (vervar == 'on'):
     print "Error in URLTesthtml.";
 try:
  result = response.getcode()
 except:
  result=0
  if (vervar == 'on'):
   print "Error in URLTesthtml.";
 return result

def URLList (file_name):
 if (vervar == 'on'):
  print "Here is the file name";
  print file_name;
 of = open(file_name, 'r').readlines()
 list = []
 for lines in of: 
   #print "Add line to list";
   #print "";
   #print lines;
   list.append(lines.strip())
 #of.close()  
 return list

#Replace url extenstion with one in list
def replaceext (url, ext_list):
 of = open(ext_list, 'r').readlines()
 list = []
 fileName, fileExtension = os.path.splitext(url)
 
 for ext in of:
  testurl=fileName+"."+ext.strip()
  if (vervar == 'on'):
   print "Testing a Replace URL";
   print testurl;
   print "";
   
  Testcode = URLTestCode (testurl)
  #Do something based on the code
  if (Testcode == 200):
     print "Might have found a Backup file";
     print "Check out :";
     print testurl;
     print "";
     ResultsList.append(testurl)

#Add to url extenstion with one in list
def addext (url, ext_list):
 of = open(ext_list, 'r').readlines()
 list = []
 fileName, fileExtension = os.path.splitext(url)
 for ext in of:
  testurl=fileName+fileExtension+"."+ext.strip()
  if (vervar == 'on'):
   print "Testing an Add URL";
   print testurl;
   print "";
  Testcode = URLTestCode (testurl)
  #Do something based on code
  if (Testcode == 200):
     print "Might have found a Backup File";
     print "Check out :"
     print testurl;
     print "";
     ResultsList.append(testurl)



#main program
ResultsList = []

if (urlvar is None): 
 #open URLlist
 filelist = URLList (listvar)

 #work through the list to check each site for 200 then content
 for fileurls in filelist:
  if (vervar == 'on'):
   print "Testurl " + fileurls + ":";
   print "";
  
  Code = URLTestCode (fileurls);
  #print "The code returned was ";
  #print Code;
  #print "Getting content";
  #Content = URLTesthtml (fileurls)
  #print Content;
  
  #Do Rules stuff here
  replaceext(fileurls, extsvar)
  addext(fileurls, extsvar)  
  
  #write output if selected
  if (outputvar != None):
   f = open(outputvar, 'w')
   f.write('<html>')
   f.write('<head>')
   f.write('<title>BACKFiL Results</title>')
   f.write('</head>')   
   f.write('<body>')
   f.write('<pre>')
   f.write(logo)
   f.write("<br>")
   f.write(logo1)
   f.write("<br>")
   f.write(logo2)
   f.write("<br>")
   f.write(logo3)
   f.write("<br>")
   f.write(logo4)
   f.write("<br>")
   f.write(logo5)
   f.write("<br>")
   f.write(logo6)
   f.write("<br>")
   f.write(logo7)
   f.write("<br>")
   f.write(logo8)
   f.write("<br>")
   f.write(logo9)
   f.write("<br>")
   f.write(logo10)
   f.write('</pre>')
   f.write('<br>')
   f.write("BACKup File Locator by Tobias Mccurry")
   f.write('<br>')
   f.write('<br>')
   f.write('Here are the links to possible backup files:')
   f.write('<br>')
   for item in ResultsList:
     buildtext= '<A HREF="' + item + '">' + item + '</a>'
     f.write(buildtext)
     f.write('<br>') 
   f.write('</body>')
   f.write('</html>')

  #print the successes
  print "Here are some interesting results:"
  for item in ResultsList:
   print item

if (listvar is None):
  Code = URLTestCode (urlvar)
  Content = URLTesthtml (urlvar)
  #print Code;
  #print Content;

  #Do Rules stuff here
  replaceext(urlvar, extsvar)
  addext(urlvar, extsvar)
 
  #write output if selected
  if (outputvar != None):
   f = open(outputvar, 'w')
   f.write('<html>')
   f.write('<head>')
   f.write('<title>BACKFiL Results</title>')
   f.write('</head>')   
   f.write('<body>')
   f.write('<pre>')
   f.write(logo)
   f.write("<br>")
   f.write(logo1)
   f.write("<br>")
   f.write(logo2)
   f.write("<br>")
   f.write(logo3)
   f.write("<br>")
   f.write(logo4)
   f.write("<br>")
   f.write(logo5)
   f.write("<br>")
   f.write(logo6)
   f.write("<br>")
   f.write(logo7)
   f.write("<br>")
   f.write(logo8)
   f.write("<br>")
   f.write(logo9)
   f.write("<br>")
   f.write(logo10)
   f.write('</pre>')
   f.write('<br>')
   f.write("BACKup File Locator by Tobias Mccurry")
   f.write('<br>')
   f.write('<br>')
   f.write('Here are the links to possible backup files:')
   f.write('<br>')
   for item in ResultsList:
     buildtext= '<A HREF="' + item + '">' + item + '</a>'
     f.write(buildtext)
     f.write('<br>') 
   f.write('</body>')
   f.write('</html>')

  #print the successes
  print "Here are some interesting results:"
  for item in ResultsList:
   print item
