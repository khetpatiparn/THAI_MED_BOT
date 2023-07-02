import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from .semantic import get_input_symptom

class ActionAskSymptom(Action):

    def name(self) -> Text:
        return "action_ask_symptom"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptom")
        if symptoms:
            result = get_input_symptom(symptoms)
            dispatcher.utter_message(text="{}".format(result))
            # Do something with the result if needed
        else:
            dispatcher.utter_message(text="No symptoms provided.")
        # dispatcher.utter_message(text="{}".format(symptoms)) # ['ปวดหัว', 'ตัวร้อน']
    
        return []
# ฉันรู้สึกปวดหัวและตัวร้อนเล็กน้อย
# ฉันอยากทราบอาการของฉัน

# class ActionSaySymptom(Action): # บอกอาการผ่าน API

#     def name(self) -> Text:
#         return "action_tell_symptom"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         symptoms = tracker.get_slot("symptom") # รับ slot
#         result = semantic.search(symptoms) # เรียกใช้งานฟังก์ชัน search(symptoms) จากไฟล์ semanticsearch.py
#         message = format_result(result)  # ทำการจัดรูปแบบข้อความผลลัพธ์ที่ได้
#         dispatcher.utter_message(text=message)
#         return []

# class ActionSaySymptom2(Action): # บอกอาการผ่าน API

#     def name(self) -> Text:
#         return "action_tell_symptom2"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         symptom = tracker.get_slot("symptom") # รับ slot 
#         if not symptom: # หาก user ไม่ได้บอกสิ่งที่เกี่ยวข้องกับอาการ
#             dispatcher.utter_message(text="ขออภัยนะครับ...เราไม่ทราบอาการของคุณ.")
#         else: # หาก user บอกอาการมา
#             # 1.เรียกใช้งาน api
#             data = CallApi() # ตอนนี้ data
#             # 2 คัดแยกข้อมูลที่ได้
#             message = FilterData(data, theshold = 70)
#             dispatcher.utter_message(text = message)
            
#         return []


# def CallApi(url = "http://127.0.0.1:5000/predict"):
#     response = requests.get(url)
#     return response.json()
#     """
#         {62: {'name': 'Common cold', 'th_name': 'ไข้หวัด', 'score': 0.7517},
#         141: {'name': 'Norovirus Infection',
#             'th_name': 'การติดเชื้อท้องเสียโนโรไวรัส (Norovirus)',
#             'score': 0.7351},
#         180: {'name': 'Systemic Lupus Erythematosus (SLE)',
#             'th_name': 'เอสแอลอี (SLE) - โรคแพ้ภูมิตัวเอง - ลูปัส',
#             'score': 0.7058},
#         198: {'name': 'Zika Virus and Pregnancy',
#             'th_name': 'โรคไข้ซิกากับการตั้งครรภ์',
#             'score': 0.6892}}
#     """

# def FilterData(data, theshold = 70):
#     # 1 กรองตัดเลขด้านหน้าออก
#     for idx, item in enumerate(data.values()):
#     # 2. คัดแยกโรคที่ได้ตามค่า theshold
#     # 2.1 ถ้าหาก score มากกว่า theshold ให้คืนข้อมูลที่มีค่า score สูงที่สุด
#         if (item["score"] * 100) >=  theshold:
#             if idx == 0:
#                 return item
#     # 2.2 ถ้าหาก score น้อยกว่า theshold ให้คืน message กลับไปที่ user ว่าขอข้อมูลเพิ่ม
#         elif (item["score"] * 100) < theshold:
#             message = "เราขอทราบอาการของคุณเพิ่มเติมเพื่อการวิเคราะห์ผลที่แม่นยำขึ้น."
#             return message