import pandas as pd
import numpy as np
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, UserUtteranceReverted, AllSlotsReset
from .semantic_search import get_input_symptom, embed_text
from .module import  *
import ast

"""# Data loading"""
data = pd.read_csv("/home/patiparn/rasa_thainlp/thai_med_bot/actions/sepSymptom.csv")
data["symptom"] = data["symptom1"].apply(ast.literal_eval)
data['embed'] = [np.array(embed_text(text)) for text in data['symptom']]

SYMPTOMS_DATABASE = set() # เก็บเป็น set

class ActionAskSymptom(Action):

    def name(self) -> Text:
        return "action_ask_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptoms = tracker.get_slot("symptom") # รับ slot => ["ปวดหัว", "ตัวร้อน"]

        SYMPTOMS_DATABASE.update(set(tracker.get_latest_entity_values("symptom"))) # เพิ่มค่า symptoms ที่สกัดได้เก็บไว้ใน Database

        if not symptoms: # ในตอนแรก slot จะไม่มีการเก็บค่า เริ่มต้นเป็น None เราก็ให้แสดงข้อความอื่นแทน
            dispatcher.utter_message(text = message_begin_list())

        else: # หลังจากได้ค่าที่มาจาก slots 
            # 1. เรียกใช้งานฟังก์ชัน search(symptoms) จากไฟล์ semantic
            result_from_input = get_input_symptom(symptoms, data)

            # 2 คัดแยกข้อมูลที่ได้
            item_or_message, is_valid= FilterData(result_from_input, symptoms, theshold = 72) #72 for work # 77 for test
            if (is_valid == True):
                dispatcher.utter_message(text="{}".format(item_or_message)) # บอกอาการ
                return [SlotSet(key = "symptom", value = None)]
            
            elif (is_valid == False):
                dispatcher.utter_message(text="{}".format(item_or_message)) # ขออาการเพิ่มเติม
        return []

class ActionAskMoreSymptom(Action):

    def name(self) -> Text:
        return "action_ask_more_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.get_latest_entity_values("symptom")
        myvalue = list(entities) # ['หน้าแดง']

        SYMPTOMS_DATABASE.update(set(myvalue)) # เพิ่มค่า symptoms ที่สกัดได้เก็บไว้ใน Database
        
        slots_current = tracker.get_slot("symptom") # ['ปวดหัว', 'ตัวร้อน']
        total_symptom = slots_current + myvalue
        dispatcher.utter_message(text=tell_more_symptom_message__list(myvalue))
        return [SlotSet(key = "symptom", value = total_symptom)]


# ให้มีการเก็บค่าเอาไว้ใน database => SYMPTOMS_DATABASE เผื่อเอาใช้เรียกใช้อีกรอบ
class ActionCheckSymptomDatabase(Action):

    def name(self) -> Text:
        return "action_check_symptom_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=str(SYMPTOMS_DATABASE))
        return[]

# เคลียร์ slot หลังจากจบ conversation
# class ActionClearSymptomSlots(Action):

#     def name(self) -> Text:
#         return "action_clear_symptom_slots"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(response = "utter_thank_for_help")
#         return [SlotSet(key = "symptom", value = None)]
    
# สร้างคำพูดที่เอาไว้จบการสนทนาแล้วสามารถถามบอทใหม่
# class ActionStartOver(Action):

#     def name(self) -> Text:
#         return "action_start_over"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(response = )
#         return []