# Database Update Manager.
import mysql.connector
import requests
from tqdm import tqdm

#THE DATABASE UPDATE CLASS

class updateManager():



	def __init__(self): # Connecting to the MySQL service
		self.mydb = mysql.connector.connect(host='localhost',user='admin',passwd='admin')
		self.state_data_endpoint = 'https://api.covid19india.org/data.json'
		self.district_data_endpoint = 'https://api.covid19india.org/state_district_wise.json'
		self.country_endpoint = 'https://api.covid19api.com/summary'


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
		self.cursor.execute("DELETE FROM country_stats")
		mydb.commit()

		jsonData = self.pullJSONData(self.state_data_endpoint) #UPDATING STATEWISE INFORMATION


		print("[PROGRESS]")
		for d_id in tqdm(range(1,len(jsonData['statewise']))):
			state = jsonData['statewise'][d_id]['state']
			active = jsonData['statewise'][d_id]['active']
			confirmed = jsonData['statewise'][d_id]['confirmed']
			recovered = jsonData['statewise'][d_id]['recovered']
			deaths = jsonData['statewise'][d_id]['deaths']
			source = "www.covid19india.org"

			self.cursor.execute("INSERT INTO state_stats VALUES(%s,%s,%s,%s,%s,%s)",(state, int(active), int(confirmed),int(recovered), int(deaths), source))

		jsonData = self.pullJSONData(self.district_data_endpoint)

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

		jsonData = self.pullJSONData(self.country_endpoint)

		print("[PROGRESS]")

		for country_id in tqdm(range(0,len(jsonData['Countries']))):
			country = jsonData['Countries'][country_id]['Country']
			NewConfirmed = jsonData['Countries'][country_id]['NewConfirmed']
			TotalConfirmed = jsonData['Countries'][country_id]['TotalConfirmed']
			NewDeaths = jsonData['Countries'][country_id]['NewDeaths']
			TotalDeaths = jsonData['Countries'][country_id]['TotalDeaths']
			NewRecovered = jsonData['Countries'][country_id]['NewRecovered']
			TotalRecovered = jsonData['Countries'][country_id]['TotalRecovered']
			source = 'https://api.covid19api.com/summary'

			self.cursor.execute("INSERT INTO country_stats VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(country,int(NewConfirmed),int(TotalConfirmed),int(NewDeaths),int(TotalDeaths),int(NewRecovered),int(TotalRecovered),source))

		print("[CHECKING FOR OLD INDICES]")
		self.cursor.execute("SHOW INDEX FROM district_stats")
		d_index = self.cursor.fetchall()
		if(d_index != None):
			print("[CLEARING OLD INDEX]")
			self.cursor.execute("DROP INDEX district_index on district_stats")
		self.cursor.execute("SHOW INDEX FROM country_stats")
		c_index = self.cursor.fetchall()
		if(c_index != None):
			print("[CLEARING OLD INDEX]")
			self.cursor.execute("DROP INDEX country_index on country_stats")

		print("[BUILDING NEW INDICES]")
		self.cursor.execute("CREATE INDEX district_index ON district_stats(district)")
		self.cursor.execute("CREATE INDEX country_index ON country_stats(country)")
		print("[FINALIZING]")
		mydb.commit()
		print("[UPDATE SUCCESSFUL]")

if(__name__ == "__main__"):
    	um = updateManager()
    	um.updateDB()
