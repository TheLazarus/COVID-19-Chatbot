# Database Update Manager.
import mysql.connector
import requests
from tqdm import tqdm

#THE DATABASE UPDATE CLASS

class updateManager():



	def __init__(self): # Connecting to the MySQL service
		self.mydb = mysql.connector.connect(host='localhost',user='admin',passwd='admin')
		self.state_data_api = 'https://api.covid19india.org/data.json'
		self.district_data_api = 'https://api.covid19india.org/state_district_wise.json'


	def pullJSONData(self,api):

		jsonData_S = requests.get(api).json()
		return jsonData_S

	def updateDB(self): #UPDATING DATABASE
		print("\n\n\t\t\t\t\t\t\t----------------------- [Updating Database] -------------------------")
		mydb = self.mydb
		self.cursor = mydb.cursor()
		self.cursor.execute("use CoronaVirus")

		print("[FLUSHING OLD DATA]")
		self.cursor.execute("DELETE FROM state_stats")
		self.cursor.execute("DELETE FROM district_stats")
		mydb.commit()

		jsonData = self.pullJSONData(self.state_data_api) #UPDATING STATEWISE INFORMATION


		print("[PROGRESS]")
		for d_id in tqdm(range(1,len(jsonData['statewise']))):
			state = jsonData['statewise'][d_id]['state']
			active = jsonData['statewise'][d_id]['active']
			confirmed = jsonData['statewise'][d_id]['confirmed']
			recovered = jsonData['statewise'][d_id]['recovered']
			deaths = jsonData['statewise'][d_id]['deaths']
			source = "www.covid19india.org"

			self.cursor.execute("INSERT INTO state_stats VALUES(%s,%s,%s,%s,%s,%s)",(state, int(active), int(confirmed),int(recovered), int(deaths), source))

		jsonData = self.pullJSONData(self.district_data_api)

		print("[PROGRESS]")

		for state in tqdm(jsonData):
			if(state == "State Unassigned"):
				continue
			else:
				for district in jsonData[state]['districtData']:
					act = jsonData[state]['districtData'][district]['active']
					conf = jsonData[state]['districtData'][district]['confirmed']
					rec = jsonData[state]['districtData'][district]['recovered']
					died = jsonData[state]['districtData'][district]['deceased']

					self.cursor.execute("INSERT INTO district_stats VALUES(%s,%s,%s,%s,%s,%s)",(district,state,int(act),int(conf),int(rec),int(died)))

		print("[CLEARING OLD INDICES]")
		self.cursor.execute("DROP INDEX district_index on district_stats")
		print("[BUILDING NEW INDICES]")
		self.cursor.execute("CREATE INDEX district_index ON district_stats(district)")
		print("[FINALIZING]")
		mydb.commit()
		print("[UPDATE SUCCESSFUL]")

if(__name__ == "__main__"):
    	um = updateManager()
    	um.updateDB()
