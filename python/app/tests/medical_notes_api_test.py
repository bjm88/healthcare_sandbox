import unittest
import requests


class TestMedicalNoteApi(unittest.TestCase):

    def test_medical_notes_api(self):

        # MedNote ids already loaded to db
        md_id_maternity_ultrasound_ob = "8daefb13-ea72-4985-aa99-25cb90bc0ba0"

        url = "http://healthsandboxc-api-dev.healthsandbox.org:5001/api/medical_notes/load?mn_id=" + \
            md_id_maternity_ultrasound_ob
        resp = requests.get(
            url=url)
        print("Medical Hosts Load resp:" + str(resp))
        self.assertTrue(resp.status_code == 200)
        json = resp.json()

        self.assertTrue(len(json["data"]) > 0)


if __name__ == '__main__':
    unittest.main()
