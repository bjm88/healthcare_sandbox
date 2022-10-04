
python3 -m app.batch.medical_notes_analysis.analyze_medical_notes

python3 -m app.batch.medical_notes_analysis.load_medical_notes app/data/test/fixtures/mtsamples.csv

python3 -m app.batch.medical_notes_analysis.nlu_medical_notes "entity"

python3 -m app.batch.medical_notes_analysis.derive_medical_note_metadata

