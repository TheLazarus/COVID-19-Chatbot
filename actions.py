from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import mysql.connector
from tqdm import tqdm
import sys


try:
    mydb = mysql.connector.connect(host='localhost',user='admin',passwd='admin')
    cursor = mydb.cursor()
except:
    print("Cannot Connect to the Database")
    sys.exit()

class ActionQueryCoronaLocation(Action):

    def name(self) -> Text:
        return "action_query_corona_location"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

             cursor = mydb.cursor()
             try:
                 entities = tracker.latest_message['entities']
                 for entity in entities:
                     if(entity['entity'] == 'location'):
                         location = entity['value']
            except:
                dispatcher.utter_message('I am not able to understand what you are trying to say')

             cursor.execute("USE CoronaVirus")
             cursor.execute("SELECT * from state_stats WHERE state=%s",(location,))
             result = cursor.fetchall()
             if(len(result) == 0):
                 cursor.execute("SELECT * from district_stats WHERE district=%s",(location,))
                 result = cursor.fetchall()
                 if(len(result) != 0):
                     for row in result:
                         dispatcher.utter_message("-----------------\n[District] : "+location+"\n[State] : "+row[1]+"\n[Active Cases] :"+str(row[2])+"\n[Confirmed Cases] :"+str(row[3])+"\n[TotalRecovered] :"+str(row[4])+"\n[Total Deaths] :"+str(row[5]))
                 else:
                     cursor.execute("SELECT * from country_stats WHERE country=%s",(location,))
                     result = cursor.fetchall()
                     if(len(result) != 0):
                         for row in result:
                             dispatcher.utter_message("------------------\n[Country] : "+location+"\n[New Confirmed Cases] :"+str(row[1])+"\n[Total Confirmed Cases] : "+str(row[2])+"\n[New Deaths] :"+str(row[3])+"\n[Total Deaths] :"+str(row[4])+"\n[New Recovered] :"+str(row[5])+"\n[Total Recovered] :"+str(row[6])+"\n[Source] :"+row[7])
                     else:
                         dispatcher.utter_message("I was not able to find any information about the provided location.")
             else:
                 for row in result:
                     dispatcher.utter_message("-----------------\n[State] :"+row[0]+"\n[Active Cases] :"+str(row[1])+"\n[Confirmed Cases] :"+str(row[2])+"\n[Total Recovered] :"+str(row[3])+"\n[Total Deaths] :"+str(row[4])+"\n[Source] :"+row[5])


             return []



#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
