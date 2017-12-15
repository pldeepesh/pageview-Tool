#!/usr/bin/python

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date,timedelta,datetime
import psycopg2 as con

# try:
#   conn = con.connect(user='root',password='deepesh',host='localhost',database='test')
#   cursor = conn.cursor()
#   print('database connection succesful')
# except:
#   print('database connection was not established')

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'Google Analytics API-e0fe33a51543.json'
# start_date = (date.today()-timedelta(days=1)).isoformat()
# end_date = (date.today()-timedelta(days=1)).isoformat()
row_format = "{:>30}"*2+"{:>20}"*2
start_date = '2017-11-01'
end_date = '2017-11-30'

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics,viewId,expression):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': viewId,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression':'ga:pageviews'}],
          'dimensions': [{'name':'ga:pagePath'}],
          "dimensionFilterClauses": [
        {
          "filters": [
            {
              "dimensionName": "ga:pagePath",
              "operator": "PARTIAL",
              "expressions": expression
            }
          ]
        }
      ]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print (header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print ('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print (metricHeader.get('name') + ': ' + value)
    print('\n')


def print_table(response,property,expression):
  pageviews = response['reports'][0]['data']['totals'][0]['values'][0]
  

  # row_format = "{:>20}"*7
  # print(row_format.format('Property','Date Range','Sessions','Page Views','Users','New Users'))
  # print(row_format.format(column_headers))
  
  print(row_format.format(property,start_date+'-'+end_date,expression,pageviews))
  # cursor.execute("insert into google_analytics(product,start_date,end_date,sessions,users,new_users,page_views,bounce_rate,avg_time,time_stamp) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now())",(property,start_date,end_date,sessions,users,New_users,pageviews,bouncerate,time_on_page))
  # conn.commit()

def main(property,viewId,expression):
  analytics = initialize_analyticsreporting()
  response = get_report(analytics,viewId,expression[0])
  # print("depresion : "+response['reports'][0]['data']['totals'][0]['values'][0])

  # print(property+":")
  print('\n')
  # print_response(response)
  print_table(response,property,expression[0])

if __name__ == '__main__':

  input_keywords = open('keywords.txt','r')
  for i in input_keywords.readline():
    temp=[]
    temp.append(i)
    list_of_expressions.append(temp)
  input_keywords.close()

  # for i in range(0,len(list_of_expressions)):
  #   for j in list_of_expressions[i]:
  #     list_of_expressions[i][0]=j.replace(' ','-')


  list_of_expressions=[['Stress'],
['Fatigue'],
['Anxiety'],
['Happiness'],
['Depression'],
['Anger'],
['memory'],
['Hair'],
['Dandruff'],
['Bald'],
['Digest'],
['Constipation'],
['Bloating'],
['Bowel'],
['Acidity'],
['Diarrhoea'],
['Foot'],
['Feet'],
['heel'],
['Chest congestion'],
['asthma'],
['copd'],
['respiratory'],
['lung-disease']]

  list_of_view_ids = {
 #  'Brazil':'118205422',
	# 'Indonesia':'102733486',
	'Health-feed':'114815181',
	# 'Singapore':'83567831',
	# 'Philippines':'96537958',
	# 'India-DCH':'122840343',
	'Consult':'108073511',
	# 'Diagnostics':'133763520',
	# 'Diagnostics-Neo':'142593269',
	# 'Providers':'151968134',
	# 'order':'119302994',
	# 'Practo-Pedia':'139887700',
	# 'fabric-amp':'152853517',
	'consult-amp':'152395833',
	'Healthfeed-amp':'120575261'
	# 'Neo-amp':'158429376',
	# 'PractoPedia-amp':'149564271'
	}

  print(row_format.format('Property','Date Range','KW','Page Views'))

  for key in list_of_view_ids:
    for i in list_of_expressions:
      main(key,list_of_view_ids[key],i)
  





