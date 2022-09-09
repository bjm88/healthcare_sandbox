from sqlalchemy import Column, Integer, String, Text, text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from ..database_utils import DatabaseManager
from sqlalchemy.dialects.postgresql import UUID


class MedicalNote(DatabaseManager.Base):

    __tablename__ = "medical_notes"

    id = Column(UUID(as_uuid=True),
                primary_key=True, server_default=text("gen_random_uuid()"))
    create_dttm = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    description = Column(String(500), nullable=True)
    medical_specialty = Column(String(500), nullable=True)
    sample_name = Column(String(500), nullable=True)
    keywords = Column(Text(), nullable=True)
    transcription = Column(Text(), nullable=True)
    entity_extraction = Column(JSONB, nullable=True)
    org_id = Column(Integer, nullable=True)
    external_id = Column(String(255), nullable=True, index=True)
    source = Column(String(500), nullable=True)

    def __str__(self):
        return "<MedicalNote(id='%s', medical_specialty='%s' keywords='%s'>" % (self.id, self.medical_specialty, self.keywords)

    def as_dict(self):
        _obj = dict()
        _obj["id"] = self.id
        _obj["medical_specialty"] = self.medical_specialty
        _obj["keywords"] = self.keywords
        _obj["description"] = self.description
        _obj["transcription"] = self.transcription
        _obj["entity_extraction"] = self.entity_extraction
        return _obj
