import sys

from ...common.database_utils import DatabaseManager
from ...common.models.medical_note import MedicalNote
import boto3
import logging
logger = logging.getLogger(__name__)

def nlu_medical_notes(extraction_type):
    if extraction_type is None:
        extraction_type = "Entity"

    db_session = DatabaseManager.get_db_session()
    aws_mc_client = boto3.client('comprehendmedical')

    print(f"MedicalNote nlu processor...")
    medNotes = db_session.query(MedicalNote)\
        .filter(MedicalNote.transcription != None) \
        .filter(MedicalNote.entity_extraction == None) \
        .filter(MedicalNote.medical_specialty.in_((" Discharge Summary", " Emergency Room Reports", " Obstetrics / Gynecology"))) \
        .order_by(MedicalNote.create_dttm.asc()) \
        .limit(5000).all()

    if medNotes:
        for mn in medNotes:
            if len(mn.transcription) > 5:
                result = detect_medical_entities(aws_mc_client, mn.transcription)
                if result is not None:
                    mn.entity_extraction = result

                    db_session.add(mn)
                    db_session.commit()
                    print(f"Updated MedicalNote with entity_extraction: {result}")

        return mn
    db_session.close()

def detect_medical_entities(aws_mc_client, text):
        try:
            response = aws_mc_client.detect_entities(
                Text=text)
        except Exception as ex:
            logger.exception("Error: Couldn't detect entities, error=" + str(ex))
            return None
        else:
            return response.get("Entities", None)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: nlu_medical_notes.py <extraction type, ie entity> ")
        exit(1)

    extraction_type = sys.argv[1] if sys.argv else "entity"
    nlu_medical_notes(extraction_type)
