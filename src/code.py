#!/usr/bin/env python
# smartsheet_mokapipe_complete 0.0.1
# Generated by dx-app-wizard.
#
# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# See https://wiki.dnanexus.com/Developer-Portal for documentation and
# tutorials on how to modify this file.
#
# DNAnexus Python Bindings (dxpy) documentation:
#   http://autodoc.dnanexus.com/bindings/python/current/

import os
import dxpy
import subprocess
import requests
import datetime

@dxpy.entry_point('main')
def main(NGS_run):
	'''update smartsheet to say demultiplexing is complete (add the completed date and calculate the duration (in days) and if met TAT)'''
	
	################define smartsheet variables#################
	# download the smartsheet api key from 001_auth
	# parse all the files in authentication_project
	for file in dxpy.find_data_objects(classname="file", project="project-FQqXfYQ0Z0gqx7XG9Z2b4K43"):
		#create a dxlink to each file and then run dx describe to get properties, such as filename
		description =  dxpy.describe(dxpy.dxlink(file["id"],project_id=file["project"]))
		# if the filename is smartsheet_api_token
		if description["name"] == "smartsheet_api_token":
				# download the file.
				dxpy.download_dxfile(dxpy.dxlink(file["id"],project_id=file["project"]),"smartsheet_api_token")

	# read and assign api key to variable
	API_KEY=open('/home/dnanexus/smartsheet_api_token','r')
	for line in API_KEY:
		smartsheet_api_key=line

	# smartsheet sheet ID
	smartsheet_sheetid=2798264106936196

	#columnIds
	ss_title=6197963270711172
	ss_description=3946163457025924
	ss_samples=957524288530308
	ss_status=8449763084396420
	ss_priority=4790588387157892
	ss_assigned=2538788573472644
	ss_received=6723667267741572
	ss_completed=4471867454056324
	ss_duration=6519775204534148
	ss_metTAT=4267975390848900

	# requests information
	headers={"Authorization": "Bearer "+smartsheet_api_key,"Content-Type": "application/json"}
	url='https://api.smartsheet.com/2.0/sheets/'+str(smartsheet_sheetid)

	#variables to capture
	rownumber="0"
	smartsheet_now = ""


	################Read the sheet to find the row with MokaPipe and inprogress #####################
	# build url to read sheet to
	sheet="https://api.smartsheet.com/2.0/sheets/"+str(smartsheet_sheetid)

	#get row
	r = requests.get(sheet, headers=headers)
	#read response in json
	response= r.json()
	#for each row
	for row in  response['rows']:
		# loop through the list of columns
		print row['cells']
		#if  and NGS_run in row['cells']:
		if NGS_run in str(row['cells']) and "u'displayValue': u'MokaPipe', u'columnId': "+str(ss_description)+" in str(row['cells'])":
			print "MATCH"
			rownumber= row['id']

	print rownumber
	################################### update row###################################
	#url to read row
	row_url="https://api.smartsheet.com/2.0/sheets/"+str(smartsheet_sheetid)+"/rows/"+str(rownumber)
	
	# read url
	r = requests.get(row_url, headers=headers)
	
	#read response in json
	response= r.json()
	print response
	
	# for each column
	for col in response["cells"]:
		# look for the columns containing the date recieved
	    	if int(col["columnId"]) == ss_received:
			# capture received
			recieved=datetime.datetime.strptime(col['value'], '%Y-%m-%d')
	
	# take current timestamp
	smartsheet_now = str('{:%Y-%m-%d}'.format(datetime.datetime.utcnow()))
	now=datetime.datetime.strptime(smartsheet_now, '%Y-%m-%d')
	
	#calculate the number of days taken (add one so if same day this counts as 1 day not 0)
	duration = (now-recieved).days+1
	
	# set flag to show if TAT was met.
	TAT=1
	if duration > 4:
	    TAT=0

	#build payload used to update the row
	payload = '{"id":"'+str(rownumber)+'", "cells": [{"columnId":"'+ str(ss_duration)+'","value":"'+str(duration)+'"},{"columnId":"'+ str(ss_metTAT)+'","value":"'+str(TAT)+'"},{"columnId":"'+ str(ss_status)+'","value":"Complete"},{"columnId": '+str(ss_completed)+', "value": "'+str(smartsheet_now)+'"}]}' 
	
	#build url to update row
	url=url+"/rows"
	update_OPMS = requests.request("PUT", url, data=payload, headers=headers)
    
   
dxpy.run()
