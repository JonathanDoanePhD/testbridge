import json,pathlib,unittest,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from testbridge import retrieve,run_simulation,validate,SimulatedSMU
PLAN=dict(device='2N7000',vds=48,vgs=0,temperature=25,limit=1,compliance=100,settling=1,samples=20,connections=True)
class Tests(unittest.TestCase):
 def test_missing_limit(self):self.assertTrue(validate({**PLAN,'limit':''}))
 def test_nan(self):self.assertTrue(validate({**PLAN,'limit':float('nan')}))
 def test_unsafe_bias(self):self.assertTrue(validate({**PLAN,'vgs':5}))
 def test_noninteger_samples(self):self.assertTrue(validate({**PLAN,'samples':3.5}))
 def test_no_connection_confirmation(self):self.assertTrue(validate({**PLAN,'connections':False}))
 def test_faults(self):
  for scenario,status in [('nominal','PASS'),('leaky','FAIL'),('fixture','FAIL'),('compliance','INVALID: compliance')]:
   with self.subTest(scenario=scenario):
    r=run_simulation(PLAN,scenario);self.assertEqual(r['status'],status);self.assertEqual(r['trace'][-1],'OUTPUT OFF')
 def test_reproducibility(self):self.assertEqual(run_simulation(PLAN),run_simulation(PLAN))
 def test_retrieval(self):self.assertEqual(retrieve('IGSS gate leakage')[0]['id'],'igss')
 def test_no_evidence(self):self.assertEqual(retrieve('xyzzy qqqq'),[])
 def test_protocol(self):
  s=SimulatedSMU();s.enable()
  with self.assertRaises(RuntimeError):s.connect()
 def test_browser_python_parity(self):
  root=pathlib.Path(__file__).resolve().parents[1];report=json.loads((root/'dist/evaluation.json').read_text())
  for method in report['methods']:
   for row in method['rows']:
    self.assertEqual([c['id'] for c in retrieve(row['query'],method['method'])],row['hits'])
if __name__=='__main__':unittest.main()
