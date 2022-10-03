from ...common.database_utils import DatabaseManager
from ...common.models.medical_note import MedicalNote
from collections import Counter
import logging
import re
import pandas as pd
logger = logging.getLogger(__name__)


def derive_medical_notes_metadata():
    db_session = DatabaseManager.get_db_session()

    print(f"MedicalNote metadata post processor...")
    medNotes = db_session.query(MedicalNote)\
        .filter(MedicalNote.transcription != None) \
        .filter(MedicalNote.entity_extraction != None) \
        .filter(MedicalNote.derived_data == None) \
        .filter(MedicalNote.medical_specialty.in_((" Discharge Summary", " Emergency Room Reports", " Obstetrics / Gynecology"))) \
        .order_by(MedicalNote.create_dttm.asc()) \
        .limit(5000).all()
     
    if medNotes:
        for mn in medNotes:
            if len(mn.transcription) > 5 and len(mn.entity_extraction) > 5:
                result = derive_medical_note_metadata(mn)
                if result is not None:
                    mn.derived_data = result
                    print("Medical note " + str(mn.id) + " updated with derived data: "+ str(result))
                    db_session.add(mn)
                    db_session.commit()
                    print(f"Updated MedicalNote with derived_data: {result}")

        return mn
    db_session.close()


def derive_medical_note_metadata(mn):
    try:
        response = {}
        derive_base_image(mn, response)
        derive_key_phrases(mn, response)
        derive_vitals_and_metrics(mn, response)
    except Exception as ex:
        logger.exception(
            "Error: Couldn't derive metadata for Medical note " + str(mn.id) + ", error=" + str(ex))
        return None
    else:
        return response

def derive_base_image(md, response):
    if md.medical_specialty.lower().strip() in ["obstetrics / gynecology", "ob/gyn", "obgyn"]:
        if "pregnancy" in md.transcription.lower().strip() or "pregnancy" in md.keywords.lower().strip() or "ultrasound of pelvis" in md.keywords.lower().strip():
            # ex: looking for 8 weeks gestational age
            num_weeks_pregnant = None
            regex_result = re.search(r".*(\d)+ weeks .*(gestational).*", md.transcription)
            if regex_result:
                num_weeks_pregnant = regex_result.group(1)
            else:
                #see if entity extraction has it
                for e in md.entity_extraction:
                    if e["Type"] == "ACUITY" and e["Category"] == "MEDICAL_CONDITION" and "weeks" in e["Text"]:
                        s = e["Text"].split(" ")
                        num_weeks_pregnant = s[0]

            if num_weeks_pregnant is not None:
                response["num_weeks_pregnant"] = num_weeks_pregnant
                num_weeks_pregnant = re.sub("[^\d\.]", "", num_weeks_pregnant)
                x = int(num_weeks_pregnant)
                if x <= 7:
                    response["base_image"] = "pregnancy_early"
                elif x > 7 and x <= 12:
                    response["base_image"] = "pregnancy_t1"
                elif x > 12 and x <= 32:
                    response["base_image"] = "pregnancy_t2"
                else :
                        response["base_image"] = "pregnancy_t3"

def derive_key_phrases(md, response):
    anatomy_words = []
    for e in md.entity_extraction:
        if e["Category"] == "ANATOMY" and e["Type"] == "SYSTEM_ORGAN_SITE":
            anatomy_words.extend(e["Text"].split(" "))
    
    condition_words = []
    for e in md.entity_extraction:
        if e["Category"] == "MEDICAL_CONDITION" and e["Type"] == "DX_NAME":
            condition_words.extend(e["Text"].split(" "))


    freq_dict_anatomy = {}
    for aw in anatomy_words:
        if freq_dict_anatomy.get(aw, None) is None:
            freq_dict_anatomy[aw] = 0
        freq_dict_anatomy[aw] += 1

    freq_dict_conditions = {}
    for cw in condition_words:
        if freq_dict_conditions.get(cw, None) is None:
            freq_dict_conditions[cw] = 0
        freq_dict_conditions[cw] += 1

    ac=Counter(freq_dict_anatomy)
    response["anatomy_stats"] = ac.most_common()
    cc=Counter(freq_dict_conditions)
    response["condition_stats"] = cc.most_common()

    #response["anatomy_stats"] = pd.DataFrame(list(freq_dict_anatomy.items()), columns= ['word','count']).sort_values('count').to_json()
    #response["condition_stats"] = pd.DataFrame(list(freq_dict_conditions.items()), columns= ['word','count']).sort_values('count').to_json()


def derive_vitals_and_metrics(md, response):

    if md.medical_specialty.lower().strip() in ["obstetrics / gynecology", "ob/gyn", "obgyn"]:
        if "pregnancy" in md.transcription.lower().strip() or "pregnancy" in md.keywords.lower().strip() or "ultrasound of pelvis" in md.keywords.lower().strip():
            pregnancyMeasurements = {}
            # examples
            # BPD: 3.5cm consistent with 16 weeks, 6 days gestation
            # HC: 12.0cm consistent with 16 weeks, 4 days
            for m in ["BPD", "HC", "AC", "FL"]:
                print("searching " + str(m) + "...")
                regex_result = re.search(r".*" + m +": (\d+.\d+)cm .*", md.transcription)
                if regex_result:
                    measurementCm = regex_result.group(1)
                    pregnancyMeasurements[m] = measurementCm
            response["pregnancyMeasurements"] = pregnancyMeasurements

if __name__ == "__main__":
    derive_medical_notes_metadata()
