import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class CallExternalAPI(Action):
    def name(self) -> Text:
        return "action_call_external_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        url ="https://api.aiforthai.in.th/emonews/prediction"
        headers = {"apikey":"JAkIkqoUcnO0LUNCW94pELzrvYpcYj15"}
        params = {"text":"นักวิจัยออสเตรเลียเผยสาเหตุฉลามโจมตีมนุษย์"} #intent
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        dispatcher.utter_message(text="ข้อมูลจาก API: {}".format(data))

        return []

# def HealthCheck():
#     AskSymptoms()
#     TellDisease()

# def AskSymptoms():
#     # 1.รับค่ามาจาก intent จาก User
#     intent_msg_from_user = tracker.get_intent_of_lastest_message()
#     # 2.ดึงค่า slot และ entity

#     # 3.เอา intent เข้า SemanticSearchFunction()
#     # SemanticSearchFunction()
#     mood, prob_mood = SentimentAnalysisFunction(intent_msg_from_user)
#     if (prob_mood >= 0.5):
#         return mood
#     else:
#         # ถามใหม่
    


# # def SemanticSearchFunction(intent_msg_from_user):
# #     pass

# def SentimentAnalysisFunction(intent_msg_from_user = "นักวิจัยออสเตรเลียเผยสาเหตุฉลามโจมตีมนุษย์"):
#     # 1.ดึงข้อมูลจาก api มาเรียกใช้งาน
#     url ="https://api.aiforthai.in.th/emonews/prediction"
#     headers = {"apikey":"JAkIkqoUcnO0LUNCW94pELzrvYpcYj15"}
#     params = {"text": intent_msg_from_user}
#     response = requests.get(url, params=params, headers=headers)
#     data = response.json()

#     result = data['result']
#     # ค่า str อารมณ์มากสุด
#     max_value = max(result, key=result.get)
#     # 2.เอาค่าไปใช้
#     return max_value,  result[max_value]

# def TellDisease(mood):
#     return dispatcher.utter_message(text=mood)

##################################################
# 2. ดึง entity มาเก็บใน slots 
# class ValidateSymtomsForm(FormValidationAction):

#     def name(self) -> Text:
#         return "validate_symtoms_form"

#     def validate_pizza_size(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         # เงื่อนไขต่างๆในการใส่slot
            
#         return {"symtoms": slot_value}