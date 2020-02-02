from twilio.rest import Client
from collections import defaultdict
import naturaldisasterparse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

disaster_dict = {
  "wildfire": "ALERT: FIRE \nWildfire reported nearby. Be ready to evacuate.\n For up to date info:\n https://www.fire.ca.gov/incidents/",
  "earthquake14": "ALERT: EARTHQUAKE\nMagnitude: 4.1\nDROP, COVER, AND HOLD ON\nHide beneath a table or cover your head with your arms\nhttps://www.ready.gov/earthquakes",
  "earthquake67": "ALERT: EARTHQUAKE\nMagnitude: 6.7\nDROP, COVER, AND HOLD ON\nHide beneath a table or cover your head with your arms\nhttps://www.ready.gov/earthquakes",
  "flood": "ALERT: FLOODING\nFlooding reported in your area. Be cautious when traveling.\nNEVER drive through a flooded road. Stay home if possible.",
  'coronavirus': 'ALERT: CORONAVIRUS\nWear a facemask\nWash your hands\nMonitor your sypmtoms\nAvoid sharing foods and liquids.'
}
cred = credentials.Certificate("calialert-firebase-adminsdk-2wgqz-70c2fa06a9.json")
# firebase_admin.initialize_app(cred)



db = firestore.client()

class Twilio():
    account_sid = 'AC256d2fc18b15ba880d3222d578211f49'
    auth_token = '183b346a01f4d52591f7277e861fc4b5'
    phone_num = '+18026764021'
    call_dict = defaultdict(list)
    
    def __init__(self):
        self.from_firestore_populate()
        self.zip_store()
        self.client = Client(self.account_sid, self.auth_token)
        
    def zip_store(self):
        with open('states.json', 'r') as json_file:
            self.state_zip = json.load(json_file)
            
    def city_locate(self, zip_code):
        for key in self.state_zip.keys():
            for city in self.state_zip[key]:
                for zips in city:
                    if zips == zip_code:
                        return (city, zips)

            
    def from_firestore_populate(self):
        docs = db.collection(u'users').stream()
        for doc in docs:
            if doc.to_dict()['phoneNumber'] not in doc.to_dict()['zip']:
                self.call_dict[doc.to_dict()['zip']].append(doc.to_dict()['phoneNumber'])
        
    def numbers_to_call(self, area_code: str or list(str)) -> list:
        return_list = []
        if area_code == 'all':
            for key in self.call_dict.keys():
                return_list.append(self.call_dict[key])
            return [item for sublist in return_list for item in sublist]
        elif type(area_code) == str:
            return_list = self.call_dict[area_code]
        elif type(area_code) == list:
            for code in area_code:
                return_list.append(self.call_dict[code])
        return return_list
    
    def sms_func(self, numbers_to_message: list, message):
        for number in numbers_to_message:
            try:
                self.client.messages.create(
                    body = message,
                    from_ = self.phone_num,
                    to = number
                )
            except:
                print('Blacklisted Number:', number)
                
    def read_json(self, file):
        with open(file, "r") as read_file:
            data = json.load(read_file)
        return data
    
    def search_bool(self, collect, key, val) -> bool:
        docs = db.collection(collect).stream()
        for doc in docs:
            if key == 'admin':
                if doc.to_dict()['phoneNumber'] == doc.to_dict()['zip']:
                    return_zip = doc.to_dict()['zip']
                    _ref = db.collection(collect).document(doc.id)
                    _ref.update({
                        u'phoneNumber': firestore.DELETE_FIELD,
                        u'zip': firestore.DELETE_FIELD
                    })
                    db.collection(collect).document(doc.id).delete()
                    return return_zip
            if doc.to_dict()['phoneNumber'] == key and doc.to_dict()['zip'] == val:
                _ref = db.collection(collect).document(doc.id)
                _ref.update({
                    u'phoneNumber': firestore.DELETE_FIELD,
                    u'zip': firestore.DELETE_FIELD
                })
                db.collection(collect).document(doc.id).delete()
                return True
        return False
            
    def return_text(self):
        pass
            
if __name__ == '__main__':
    t = Twilio()
    w = naturaldisasterparse.get_result('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2020-02-01&maxlatitude=42.010122&minlatitude=32.467133&maxlongitude=-113.881617&minlongitude=-124.718872&minmagnitude=2')    
    # while True:
    #     x = t.search_bool(u'users','admin','')
    #     if x == 'admin':
    #         print('admin')
    while True:
        if t.search_bool(u'users','','earthquake14'):
            t.sms_func(t.numbers_to_call('all'), disaster_dict['earthquake14'])
            break
        elif t.search_bool(u'users','','wildfire'):
            t.sms_func(t.numbers_to_call('all'), disaster_dict['wildfire'])
            break
        elif t.search_bool(u'users','','earthquake67'):
            t.sms_func(t.numbers_to_call('all'), disaster_dict['earthquake67'])
            break
        elif t.search_bool(u'users','','flood'):
            print('flood')
            t.sms_func(t.numbers_to_call('all'), disaster_dict['flood'])
            break
        elif t.search_bool(u'users','','coronavirus'):
            t.sms_func(t.numbers_to_call('all'), disaster_dict['coronavirus'])
            break
        # elif x:
        #     print('x')
        #     while True:
        #         if t.search_bool(u'users','','earthquake14'):
        #             t.sms_func(t.numbers_to_call(x), disaster_dict['earthquake14'])
        #             print('earthquakeyayy')
        #             break
        # elif x == 'quit':
        #     print('quit')
        #     break