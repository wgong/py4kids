# coding: utf-8

import os, sys, time, random 
import os.path
import requests
import codecs
import pandas as pd
from pandas import ExcelWriter
import xml.etree.ElementTree as ET

# add new service to this list when implemented
LIST_OF_SERVICES = ["CustomerMatchingService"]

def dataframe_to_html_table(df):
    html_str = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
    padding: 15px;
    }
    table#wen tr:nth-child(even) {
        background-color: #eee;
    }
    table#wen tr:nth-child(odd) {
       background-color: #fff;
    }
    table#wen th {
        background-color: blue;
        color: white;
    }
    </style>
    </head>
    <body>
    <h3>Service Tester Report</h2>
    %s
    
    <p> Contact <a href="mailto:wen.gong@gmail.com">
    wen.gong@gmail.com</a> for question on this report.
    </body>
    </html>    
    """
    table_str = "<table id='wen'>"
    th_str = "<tr>"
    th_str += "".join(["<th>{}</th>".format(c) for c in df.columns])
    th_str += "</tr>"
    table_str += th_str
    
    for ix in range(df.shape[0]):
        tr_str = "<tr>"
        tr_str += "".join(["<td><a href='{}'>{}</a></td>".format(str(df.iloc[ix][c]),str(df.iloc[ix][c])) if c in ['Request_XML','Response_XML'] else "<td>{}</td>".format(str(df.iloc[ix][c])) for c in df.columns])
        tr_str += "</tr>"
        table_str += tr_str
        
    table_str += "</table>"
    return html_str % table_str



dictPayload = {
    'verify' : False,
    'headers' : {'Content-Type': 'text/xml;charset=UTF-8'}
}

dictMatchStatus = {
	'Y' : "MATCH",
	'N' : "NO_MATCH",
	'Q' : "QUESTIONABLE"
}


def test_CustomerMatchingService(df_config_1, filename_data):

	filename, file_ext = os.path.splitext(filename_data)
	filename_result = filename + '-result' + file_ext
	filename_html = filename + '-result' + '.html'

	p_endPointURL = df_config_1['endPointURL']
	p_username = df_config_1['username']
	p_password = df_config_1['password']
	p_wait_time_sec = df_config_1['wait_time_sec']

	p_request_template = df_config_1['request_template']
	with codecs.open(p_request_template, 'r') as f:
		req_xml_template = f.read()
	
	# begin processing
	df_req_data = pd.read_excel(filename_data,keep_default_na = False)
	# df_req_data.head()

	print('[test_CustomerMatchingService]***********************************************************')
	print("[test_CustomerMatchingService] Testing %s requests ... " % df_req_data.shape[0])
	print('[test_CustomerMatchingService]***********************************************************')
	match_results = []
	for ix in range(df_req_data.shape[0]):
		print("\n[test_CustomerMatchingService] TestCase# : %s ..." % (ix+1))
		

		tm = time.localtime()
		t_start_sec = time.mktime(tm)
		t_start_str = '%d-%02d-%02d %02d:%02d:%02d'%(tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
		p_TimeStamp = '%d%02d%02d%02d%02d%02d'%(tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
		#print("request submitted at ", t_start_str)

		p_TestCaseID = df_req_data.iloc[ix]['TESTCASEID']
		p_TransactionID = int(p_TestCaseID * 1e15) + int(p_TimeStamp)


		req_xml = req_xml_template.format(
			TransactionID = p_TransactionID,
			MatchToken = df_req_data.iloc[ix]['MatchToken'],
			PartyName = df_req_data.iloc[ix]['ACCOUNT_NAME'],
			DUNSNumber = df_req_data.iloc[ix]['DUNS_NUMBER'],
			Address1 = df_req_data.iloc[ix]['ADDRESS1'],
			Address2 = df_req_data.iloc[ix]['ADDRESS2'],
			City = df_req_data.iloc[ix]['CITY'],
			County = df_req_data.iloc[ix]['COUNTY'],
			State = df_req_data.iloc[ix]['STATE'],
			Province = df_req_data.iloc[ix]['PROVINCE'],
			PostalCode = df_req_data.iloc[ix]['POSTAL_CODE'],
			Country = df_req_data.iloc[ix]['COUNTRY']
		)

		filename_req_xml = "req-{TestCaseID}-{TimeStamp}.xml".format(TestCaseID=p_TestCaseID, TimeStamp=p_TimeStamp )
		filename_res_xml = "res-{TestCaseID}-{TimeStamp}.xml".format(TestCaseID=p_TestCaseID, TimeStamp=p_TimeStamp )


		with open(filename_req_xml, "wb") as fi:
			fi.write(req_xml.encode('utf-8'))

		if ix:
			time.sleep(p_wait_time_sec) 
			
		res_xml = requests.post(
				p_endPointURL, 
				auth=(p_username, p_password), 
				headers=dictPayload['headers'], 
				verify=dictPayload['verify'], 
				data=req_xml.encode('utf-8')
			)

		tm = time.localtime()
		t_stop_sec = time.mktime(tm)
		t_stop_str = '%d-%02d-%02d %02d:%02d:%02d'%(tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
		#print("response received at ", tm_str)

		elapsed_time = t_stop_sec-t_start_sec
		print("[test_CustomerMatchingService]  ... Call completed in %f sec" % elapsed_time)
		p_status = None
		
		if res_xml.text:
			with codecs.open(filename_res_xml, "w", "utf-8-sig") as f:
				f.write(res_xml.text)
				
			res_tree = ET.parse(filename_res_xml)
			root = res_tree.getroot()
			
			# parse status
			for stat in root.iter('STATUS'):
				p_status = stat.text
				break		

			if p_status is None:
				p_match_result = 'Service call failed'
			elif not p_status in dictMatchStatus:
				p_match_result = 'Matching Status='+p_status+' undefined'
			else:
				p_match_result = dictMatchStatus[p_status]
			
			p_PARTY_NUMBER = ''
			if p_status=='Y':
				for tmp in root.iter('PARTY_NUMBER'):
					p_PARTY_NUMBER = tmp.text
					break
					
			p_MATCHRULE = ''
			if p_status=='Y':
				for tmp in root.iter('MATCHRULE'):
					p_MATCHRULE = tmp.text
					break		
			
			
		match_results.append((p_TestCaseID, p_match_result, p_PARTY_NUMBER, p_MATCHRULE \
			, filename_req_xml, filename_res_xml,  elapsed_time, p_TransactionID))

	# merge match-results	
	df_results = pd.DataFrame(columns=['TESTCASEID','Match Result', 'Match RegID' , 'Match Rule'\
		, 'Request_XML','Response_XML', 'Elapsed Time (sec)', 'Batch_ID'], data=match_results)
	df_req_data = pd.merge(df_req_data,df_results, on='TESTCASEID')

	# write match_results to html
	with codecs.open(filename_html, 'w', "utf-8-sig") as f:
		f.write(dataframe_to_html_table(df_req_data))
		
	# write match_results to spreadsheet
	writer = ExcelWriter(filename_result)
	df_req_data.to_excel(writer, header=True, index=False)
	# Close the Pandas Excel writer.
	writer.save()

	print('[test_CustomerMatchingService]***********************************************************')
	print("[test_CustomerMatchingService] Results are found in:\n\t%s\n\t%s\n " % (filename_html, filename_result))
	print('[test_CustomerMatchingService]***********************************************************')


def main():

	if len(sys.argv) < 4:
		print("Missing Inputs")
		print("Usage: python sys.argv[0] <service_name> <config_file> <data_file>")
		exit(1)

	#p_service_name = "CustomerMatchingService"
	p_service_name    = sys.argv[1]
	filename_config   = sys.argv[2]
	filename_data     = sys.argv[3]
	
	if not p_service_name in LIST_OF_SERVICES:
		print("%s tester not implemented" % p_service_name)
		exit(1)

	if not os.path.exists(filename_config):
		print("Config file %s not found" % filename_config)
		exit(1)

	if not os.path.exists(filename_data):
		print("Data file %s not found" % filename_data)
		exit(1)
		

	df_config = pd.read_excel(filename_config, keep_default_na = False)
	try:
		df_config_1 = df_config[df_config.service_name == p_service_name].iloc[0]
	except:
		print("service name %s not found in config file %s" % (p_service_name, filename_config))
		exit(1)
	
	#p_service_name = "CustomerMatchingService"
	if p_service_name == "CustomerMatchingService":
		test_CustomerMatchingService(df_config_1, filename_data)

	
	exit(0)


if __name__ == "__main__":
    main()
