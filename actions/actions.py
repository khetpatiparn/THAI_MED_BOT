import random
import pandas as pd
import numpy as np
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, UserUtteranceReverted, AllSlotsReset
from .semantic_search import get_input_symptom, embed_text
import ast

"""# Data loading"""
data = pd.read_csv("/home/patiparn/rasa_thainlp/thai_med_bot/actions/sepSymptom.csv")
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
            dispatcher.utter_message(text = message_begin_list())

        else: # หลังจากได้ค่าที่มาจาก slots 
            # 1. เรียกใช้งานฟังก์ชัน search(symptoms) จากไฟล์ semantic
            result_from_input = get_input_symptom(symptoms, data)

            # 2 คัดแยกข้อมูลที่ได้
            item_or_message, is_valid= FilterData(result_from_input, symptoms, theshold = 72)
            if (is_valid == True):
                dispatcher.utter_message(text="{}".format(item_or_message)) # บอกอาการ
            
            elif (is_valid == False):
                dispatcher.utter_message(text="{}".format(item_or_message)) # ขออาการเพิ่มเติม
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
                message = tell_disease_message_list()
                return message + item["th_name"], True
            
    # 2.2 ถ้าหาก score น้อยกว่า theshold ให้คืน message กลับไปที่ user ว่าขอข้อมูลเพิ่ม
        elif (item["score"] * 100) < theshold:
            message = message_for_more_symptoms(symptoms)
            return message, False
       
def message_for_more_symptoms(symptoms):
    concat = ", ".join(symptoms)
    messages = [
        "เรามีอาการอะไรอื่นนอกจากนี้ร่วมด้วยหรือป่าว",
        "นอกจาก{}แล้วมีอาการอื่นอีกรึป่าว".format(concat),
        "มีอะไรนอกจาก{}บ้างรึป่าว".format(concat),
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
        dispatcher.utter_message(text=tell_more_symptom_message__list(myvalue))
        return [SlotSet(key = "symptom", value = total_symptom)]

def message_begin_list():
    messages = [
        "ได้เลย ลองบอกอาการของคุณมาหน่อยสิ",
        "เข้าใจแล้วหล่ะ บอกอาการของคุณมาหน่อยสิ",
        "อาการมันเป็นอย่างไรหรอครับ",
        "เราอยากรู้อาการของคุณ ช่วยบอกให้ฉันรู้หน่อยสิ"
        ]
    random_message = random.choice(messages)
    return random_message

def tell_more_symptom_message__list(myvalue):
    messages = [
        "มี{}ร่วมด้วยนะครับ".format(','.join(myvalue)),
        "มี{}ด้วย...แบบนี้นี่เองงง".format(','.join(myvalue)),
        ]
    random_message = random.choice(messages)
    return random_message

def tell_disease_message_list():
    messages = [
        "เราคิดว่าคุณน่าจะมีอาการ",
        "คุณอาจจะเป็น",
        "คุณเข้าข่ายอาการ"
        ]
    random_message = random.choice(messages)
    return random_message

# ปรับ theshold ลงเมื่อยังหาค่าไม่ได้ซัก 3 ตัว
def adjust_theshold(result_from_input):
    if result_from_input:
        pass

# ให้ bot เริ่มต้นบทสนทนาใหม่ได้
def start_over_bot():
    pass

# ให้มีการเก็บค่าเอาไว้ใน database เผื่อเอาใช้เรียกใช้อีกรอบ
class CheckSymptomDatabase(Action):

    def name(self) -> Text:
        return "check_symptom_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get exist slot value
        exist_slot = tracker.get_slot("symptom")
        
        return[]

    