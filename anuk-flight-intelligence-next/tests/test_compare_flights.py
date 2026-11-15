import unittest
from scripts.compare_flights import compare

BASE={"airline":"TEST","flight_number":"T100","origin":"GLA","destination":"LHR",
      "departure_local":"08:00","arrival_local":"09:20","operating_days":[1,2,3],
      "effective_from":"2027-03-28","effective_to":"2027-10-30","aircraft_type":"A320",
      "source_name":"Synthetic test","source_url":"","captured_at":"2026-11-01T00:00:00Z"}
class CompareTests(unittest.TestCase):
    def test_no_change(self): self.assertEqual(compare([BASE],[dict(BASE)]),[])
    def test_time_change(self):
        b=dict(BASE); b["departure_local"]="08:30"
        out=compare([BASE],[b]); self.assertEqual(out[0]["change_type"],"Schedule changed")
        self.assertEqual(out[0]["changes"][0]["field"],"departure_local")
    def test_missing_requires_review(self):
        out=compare([BASE],[]); self.assertEqual(out[0]["verification_status"],"review_required")
    def test_added(self):
        out=compare([],[BASE]); self.assertEqual(out[0]["change_type"],"Flight added")
if __name__=="__main__": unittest.main()
