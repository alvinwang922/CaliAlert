from twilio.rest import Client
from collections import defaultdict


from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("calialert-firebase-adminsdk-2wgqz-70c2fa06a9.json")
    
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
            self.call_dict[doc.to_dict()['zip']].append(doc.to_dict()['phoneNumber'])
        
    def numbers_to_call(self, area_code: str or list(str)) -> list:
        return_list = []
        if type(area_code) == str:
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
            
if __name__ == '__main__':
    t = Twilio()
    print(t.call_dict)
    t.sms_func(t.numbers_to_call('94555'), 'h i  b u r w i n im pha si n g in  n o  u t of e x ist en ce')
    # Import database module.
    
    
    # db = firebase.database()
    # print(db.child('/users').get().val()
          
    # Import database module.

        