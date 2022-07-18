#!/usr/bin/env python3

#Gotta Import our dependencies!
import requests
import json
import base64
import hmac
import hashlib
import datetime, time

url = "https://api.sandbox.gemini.com" #Target API for Gemini (This is a REST API)

gemini_api_key = "master-SECRETAPIKEY" #You need a Gemini API Key. Instructions: https://docs.gemini.com/rest-api/?python#private-api-invocation

gemini_api_secret = "APISECRET".encode() #You need a Gemini API Secret. This is available when you generate an API Key. See above link for instructions.

#Available Address Types that can be added are: bitcoin, ethereum, bitcoincash, litecoin, zcash, filecoin, dogecoin, tezos, solana, or polkadot
#Be sure to structure your csv/text file as Network,Address eg:ethereum,0x3833a5db28340a6C3C35FeF532A2CFC6277A03eF

f = "./addresslist.txt" #This file needs to be in the same directory or you need to update the file path

#Lets open the file up and read it line by line.
with open(f, 'r') as reader:
	for line in reader:
		fields = line.strip().split(',') #We need to strip and separate each line so that only our indexed fields (0=Network, 1=Address) are left over.
		
		#print(fields) #Uncomment the Print statement for troubleshooting your CSV file entries. 
		
	#Remember you can add any variable as a filed (Like "Label")
	#label = fields.index(2) #and change "label": "API_Added_Address to "label": = label, I added these below as examples
		
	network = fields[0] #eg:ethereum,0x3833a5db28340a6C3C35FeF532A2CFC6277A03eF "ethereum" is Index 0!
	addressline = fields[1] #eg:ethereum,0x3833a5db28340a6C3C35FeF532A2CFC6277A03eF <<<<<<<<<This is Index 1!
	timestamp = datetime.datetime.now() #Timestamps are important for logging.
	payload_nonce = time.time() #Gemini uses a NONCE thats based on the current time. its a required post of the "POST" request.
	payload =  {
		"request": "/v1/approvedAddresses/"+network.lower()+"/request", #Endpoint request requires the network variable. This is the REST API Endpoint we are POSTing our request to.
		"nonce": payload_nonce,
		"address": addressline,
		"label": "API_Added_Address",
		#"label": = label, #Uncomment if you want to add custom labels for each address. It should be the third item in your csv: eg:ethereum,0x3833a5db28340a6C3C35FeF532A2CFC6277A03eF, My_Label
		"account": "primary" #See Gemini API Reference for more details on defining accounts. This too can be another index field in your CSV if you want.
	}
	encoded_payload = json.dumps(payload).encode()
	b64 = base64.b64encode(encoded_payload)
	signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest() #Gemini expects and encoded and signed B64 Payload so we do that with a little magic.
	path = "/v1/approvedAddresses/"+network.lower()+"/request" #Make sure you add the path to the API Request

  #Make sure we set the proper headers according to the Gemini
	request_headers = {
		'Content-Type': "text/plain",
		'Content-Length': "0",
		'X-GEMINI-APIKEY': gemini_api_key,
		'X-GEMINI-PAYLOAD': b64,
		'X-GEMINI-SIGNATURE': signature,
		'Cache-Control': "no-cache"
		}
	
	#We define our response variables here.
	response = requests.post(url + path, headers=request_headers, verify=False)
	
	#We check to see if we got a 200 response or if we got an error code. If we get an error we print the entire output for debugging.
	if response.status_code == 200:
		api_response = response.status_code
	
		#We print it out here.
		print(api_response)
		print(timestamp)
		print(response._content)
	else:
		print(response.status_code)
		print(response.raw)
		print(timestamp)
