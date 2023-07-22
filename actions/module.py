import random
######################### filter data zone ######################
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

# ปรับ theshold ลงเมื่อยังหาค่าไม่ได้ซัก 3 ตัว
def adjust_theshold(result_from_input):
    if result_from_input:
        pass

# ให้ bot เริ่มต้นบทสนทนาใหม่ได้
def start_over_bot():
    pass
        
######################### message zone #######################
def message_for_more_symptoms(symptoms):
    concat = ", ".join(symptoms)
    messages = [
        "เรามีอาการอะไรอื่นนอกจากนี้ร่วมด้วยหรือป่าว",
        "นอกจาก{}แล้วมีอาการอื่นอีกรึป่าว".format(concat),
        "มีอะไรนอกจาก{}บ้างรึป่าว".format(concat),
            ]
    random_message = random.choice(messages)
    return random_message

def message_begin_list():
    messages = [
        "ได้เลย ลองบอกอาการของคุณมาหน่อยสิ",
        "เข้าใจแล้วหล่ะ บอกอาการของคุณมาหน่อยสิ",
        "อาการมันเป็นอย่างไรหรอครับ",
        "เราอยากรู้อาการของคุณ ช่วยบอกให้ฉันรู้หน่อยสิ"
        ]
    random_message = random.choice(messages)
    return random_message

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