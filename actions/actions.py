import random
import pandas as pd
import numpy as np
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, UserUtteranceReverted, AllSlotsReset
from .semantic import get_input_symptom, embed_text
import ast

"""# Data loading"""
data = pd.read_csv("/home/patiparn/rasa_thainlp/rasatest/actions/sepSymptom.csv")
data["symptom"] = data["symptom1"].apply(ast.literal_eval)
data['embed'] = [np.array(embed_text(text)) for text in data['symptom']]

SYMPTOMS_DATABASE = []

class ActionAskSymptom(Action):

    def name(self) -> Text:
        return "action_ask_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptoms = tracker.get_slot("symptom") # รับ slot => ["ปวดหัว", "ตัวร้อน"]

        if not symptoms: # ในตอนแรก slot จะไม่มีการเก็บค่า เริ่มต้นเป็น None เราก็ให้แสดงข้อความอื่นแทน
            dispatcher.utter_message(text="เริ่มบอกอาการของคุณมาได้เลยย")

        else: # หลังจากได้ค่าที่มาจาก slots 
            # 1. เรียกใช้งานฟังก์ชัน search(symptoms) จากไฟล์ semantic
            result_from_input = get_input_symptom(symptoms, data)

            # 2 คัดแยกข้อมูลที่ได้
            item_or_message, is_valid= FilterData(result_from_input, symptoms, theshold = 76)
            if (is_valid == True):
                dispatcher.utter_message(text="{}".format(item_or_message))
            
            elif (is_valid == False):
                dispatcher.utter_message(text="{}".format(item_or_message))
        return []

# ฉันรู้สึกปวดหัวและตัวร้อนเล็กน้อย
# ฉันอยากทราบอาการของฉัน
# ฉันรู้สึกเจ็บคอ

def FilterData(result_from_input,symptoms, theshold):
    # 1 กรองตัดเลขด้านหน้าออก
    for idx, item in enumerate(result_from_input.values()):

    # 2. คัดแยกโรคที่ได้ตามค่า theshold
    # 2.1 ถ้าหาก score มากกว่า theshold ให้คืนข้อมูลที่มีค่า score สูงที่สุด
        if (item["score"] * 100) >=  theshold:
            if idx == 0:
                message = "คุณน่าจะมีอาการ "
                return message + item["th_name"], True
            
    # 2.2 ถ้าหาก score น้อยกว่า theshold ให้คืน message กลับไปที่ user ว่าขอข้อมูลเพิ่ม
        elif (item["score"] * 100) < theshold:
            message = message_for_more_symptoms(symptoms)
            return message, False
        
def message_for_more_symptoms(symptoms):
    concat = ", ".join(symptoms)
    messages = [
        "คุณมีอาการอะไรอื่นร่วมด้วยหรือไม่",
        "นอกจาก {} แล้วมีอาการอื่นอีกไหม".format(concat)
            ]
    random_message = random.choice(messages)
    return random_message


class ActionAskMoreSymptom(Action):

    def name(self) -> Text:
        return "action_ask_more_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.get_latest_entity_values("symptom")
        myvalue = list(entities) # ['หน้าแดง']
        slots_current = tracker.get_slot("symptom") # ['ปวดหัว', 'ตัวร้อน']
        total_symptom = slots_current + myvalue
        dispatcher.utter_message(text="มี{}ร่วมด้วยนะครับ".format(','.join(myvalue)))
        return [SlotSet(key = "symptom", value = total_symptom)]

