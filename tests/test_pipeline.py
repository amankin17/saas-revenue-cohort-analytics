import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pipeline import plus_month,make_data,database,kpi,cohorts
class TestMetrics(unittest.TestCase):
    def test_month_increment(self): self.assertEqual(plus_month('2026-12',1),'2027-01')
    def test_deterministic(self): self.assertEqual(make_data(8),make_data(8))
    def test_churn_and_mrr(self):
        conn=database([(1,'2026-01','2026-03',100),(2,'2026-02',None,50)])
        self.assertEqual(kpi(conn,'2026-02')['mrr'],150)
        self.assertEqual(kpi(conn,'2026-03')['mrr'],50)
        self.assertEqual(kpi(conn,'2026-03')['logo_churn'],0.5)
        self.assertEqual(cohorts(conn,'2026-03')[0]['retention'],0)
if __name__=='__main__': unittest.main()
