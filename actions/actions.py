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

        symptoms = tracker.get_slot("symptom") # รับ slot 
        
        if not symptoms: # ในตอนแรก slot จะไม่มีการเก็บค่า เริ่มต้นเป็น None เราก็ให้แสดงข้อความอื่นแทน
            dispatcher.utter_message(text="เริ่มบอกอาการของคุณมาได้เลยย")
        
        else: # หลังจากได้ค่าที่มาจาก slots แล้วเช่น ["ปวดหัว", "ตัวร้อน"]
            
            # 1. เรียกใช้งานฟังก์ชัน search(symptoms) จากไฟล์ semantic
            result_from_input = get_input_symptom(symptoms)
            '''
            {62: {'name': 'Common cold', 'th_name': 'ไข้หวัด', 'score': 0.7517}, 141: {'name':                                    
            'Norovirus Infection', 'th_name': 'การติดเชื้อท้องเสียโนโรไวรัส (Norovirus)',                                         
            'score': 0.7351}, 180: {'name': 'Systemic Lupus Erythematosus (SLE)', 'th_name':                                      
            'เอสแอลอี (SLE) - โรคแพ้ภูมิตัวเอง - ลูปัส', 'score': 0.7058}, 198: {'name': 'Zika                                    
            Virus and Pregnancy', 'th_name': 'โรคไข้ซิกากับการตั้งครรภ์', 'score': 0.6892}} 
            '''
            # 2 คัดแยกข้อมูลที่ได้
            message = FilterData(result_from_input, theshold = 85)
            dispatcher.utter_message(text="{}".format(message))
            
        return []

def FilterData(result_from_input, theshold):
    # 1 กรองตัดเลขด้านหน้าออก
    for idx, item in enumerate(result_from_input.values()):

    # 2. คัดแยกโรคที่ได้ตามค่า theshold
    # 2.1 ถ้าหาก score มากกว่า theshold ให้คืนข้อมูลที่มีค่า score สูงที่สุด
        if (item["score"] * 100) >=  theshold:
            if idx == 0:
                return item
            
    # 2.2 ถ้าหาก score น้อยกว่า theshold ให้คืน message กลับไปที่ user ว่าขอข้อมูลเพิ่ม
        elif (item["score"] * 100) < theshold:
            message = "เราขอทราบอาการของคุณเพิ่มเติมเพื่อการวิเคราะห์ผลที่แม่นยำขึ้น."
            return message

# ฉันรู้สึกปวดหัวและตัวร้อนเล็กน้อย
# ฉันอยากทราบอาการของฉัน