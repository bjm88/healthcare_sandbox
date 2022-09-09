from ..common.database_utils import DatabaseManager
from ..common.models.medical_note import MedicalNote

def load_medical_note(mn_id):
    if mn_id is None:
        return None

    db_session = DatabaseManager.get_db_session()
    mn = db_session.query(MedicalNote).filter_by(id=mn_id).one_or_none()
    db_session.close()
    return mn

