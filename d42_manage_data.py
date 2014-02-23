#!/usr/bin/python

#   Combination of GNU and MIT/X11 licenses is required because GC3 software
#   is issued with GNU licenses. Part of the code instead comes from 
#   device42 and is issued with the MIT/X11 license. The compatibility
#   between the two licenses grant us the rights to combine and publish
#   the code.

#   Copyright (C) 2010 2014 GC3, University of Zurich
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#   Copyright (c) 2012 http://www.device42.com/

#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation
#   files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use,
#   copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following
#   conditions:
#   
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#   LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#   OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

############################################################################################
import types
import urllib2
import urllib
import base64
import csv
import os, sys
import argparse

##### Change Following lines to match your environment #####
### API URLS available at http://docs.device42.com/apis/ ###

parser = argparse.ArgumentParser(description="Parses input arguments for API access of device42")
usage = "usage: %prog api method password user url"

parser.add_argument("API", help="Set the api to be used", default="api/ip/")
parser.add_argument("API_METHOD", help="Set the api method", default="put")
parser.add_argument("D42_PASSWORD", help="Set passoword for access")
parser.add_argument("D42_USERNAME", help="Set usename to be used")
parser.add_argument("D42_API_URL", help="Set URL for access")
parser.add_argument("-f", "--file", help="Choose the INPUT file", dest="CSV_FILE_NAME", default="input.csv") 
parser.add_argument("-d", "--debug", help="Enable debug messages", dest="DEBUG", default="False")
args = parser.parse_args()

D42_API_URL = args.D42_API_URL + args.API
CSV_FILE_NAME = args.CSV_FILE_NAME
D42_USERNAME = args.D42_USERNAME
D42_PASSWORD = args.D42_PASSWORD
API_METHOD = args.API_METHOD
DEBUG = args.DEBUG

def post(params):
    data= urllib.urlencode(params)
    headers = {
            'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
    req = urllib2.Request(D42_API_URL, data, headers)
    if DEBUG: print '---REQUEST---',req.get_full_url()
    if DEBUG: print req.headers
    if DEBUG: print req.data
    if API_METHOD == 'put': req.get_method = lambda: 'PUT'
    try:
        urllib2.urlopen(req)
        return True, ''
    except urllib2.HTTPError, e:
        error_response = e.read()
        if DEBUG: print e.code, error_response
        return False, error_response

def to_ascii(s): #not used in example, but provided incase you would need to convert certain values to ascii
    """remove non-ascii characters"""
    if type(s) == types.StringType:
        return s.encode('ascii','ignore')
    else:
        return str(s)

def changerow_to_api_args(row_values, header_row):
    args = {}
    for i, heading in enumerate(header_row):
        if row_values[i]: args.update({heading.strip().lower(): row_values[i].strip()})
    return args

def read_csv_parse_and_call_api_function(filename):
    
    notadded = []
    added = []
    with open(filename, 'rb') as csvfile:
        ReadLine = csv.reader(csvfile)
        header_row = ReadLine.next()
        for i in ReadLine:
            if i:
                try:
                    args = changerow_to_api_args(i, header_row)
                    ADDED, msg = post(args)
                    if ADDED: added.append(i)
                    else: notadded.append(i+[' ',msg])
                except Exception, Err:
                    notadded.append(i+[str(Err),])
    print 'notadded %s' % notadded
    print 'added %s' % added

read_csv_parse_and_call_api_function(CSV_FILE_NAME)
