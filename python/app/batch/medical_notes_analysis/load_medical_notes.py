import sys

from ...common.database_utils import DatabaseManager
from ...common.models.medical_note import MedicalNote
from ...common.util.csv_parser import CSVUtil

def load_medical_notes(file):
    db_session = DatabaseManager.get_db_session()

    def medical_note_row_handler(row):
        print(f"MedicalNote load running for row: {row}")
        external_id = row.get("name", None)
        mn = None
        if external_id is not None:
            mn = db_session.query(MedicalNote).filter_by(
                external_id=external_id).one_or_none() 
        if mn is None:
            mn = MedicalNote()
            
        mn.description = row.get("description", None)
        mn.medical_specialty = row.get("medical_specialty", None)
        mn.sample_name = row.get("sample_name", None)
        mn.keywords = row.get("keywords", None)
        mn.transcription = row.get("transcription", None)
        mn.org_id = row.get("org_id", None)
        mn.external_id = row.get("external_id", None)
        mn.source = row.get("source", "mtsamples.com")

        db_session.add(mn)
        db_session.commit()

        print(f"Created or updated MedicalNote: {mn}")

        return mn

    CSVUtil.parse(file, medical_note_row_handler)
    db_session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: load_medical_notes.py <csv file> ")
        exit(1)

    csv_file = sys.argv[1]
    load_medical_notes(csv_file)
