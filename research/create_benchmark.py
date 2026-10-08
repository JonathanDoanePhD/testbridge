import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
groups=[
('idss',['What does IDSS measure?','Find the zero gate voltage drain current condition.','How should off-state drain leakage be tested?']),
('idss',['What is the 2N7000 drain leakage limit at 48 V?','Which bias is specified for 2N7000 off-state leakage?','Does the 2N7000 IDSS row specify a maximum current?']),
('igss',['What conditions define IGSS?','Find the gate-body leakage condition.','What voltage is used to measure gate leakage?']),
('igss',['Is IGSS measured at zero drain voltage?','Which terminal current is gate leakage?','What is the 2N7000 gate leakage limit?']),
('threshold',['What is the threshold voltage condition?','What current defines VGS(th) for 2N7000?','Find Vth rather than off-state leakage.']),
('rating',['What is the drain-source absolute maximum rating?','Can the maximum rating be used as the leakage test voltage?','What is the maximum rated drain voltage?']),
('settling',['How do I determine settling time?','Why does the reading need time to stabilize?','What sets the delay before low-current acquisition?']),
('settling',['What causes a transient after a bias change?','How does shunt capacitance affect settling?','How can I choose a delay from a current-versus-time plot?']),
('guard',['How does guarding reduce leakage?','Why use triax for fixture leakage?','Can insulation leakage contaminate the device reading?']),
('guard',['What does a guard do in a low-current circuit?','Which technique reduces fixture leakage?','How do I separate parasitic insulation leakage?']),
('shield',['Why does movement near the setup change current?','How do I reduce electrostatic interference?','When should sensitive circuitry be shielded?']),
('shield',['Where is the shield connected in the 4200A-SCS example?','What should I do about electrostatic coupling?','Does shielding help with nearby charged objects?']),
('offset',['How do I measure system offset without the DUT?','Can I measure a baseline before connecting the device?','How do I isolate background current from cables?']),
('offset',['Should I add fixtures progressively during offset checks?','How do I check background leakage at the test bias?','How should I characterize open circuit offset?']),
('filter',['What is the filtering versus speed tradeoff?','How does averaging affect throughput?','Can additional delay reduce noise but slow testing?']),
('drift',['Why does zero drift change with temperature?','Why is thermal stability needed?','What can warmup and temperature changes do to offset?']),
('generated',['Can input bias contribute to measured current?','Why does moving a cable generate current?','What are triboelectric error currents?']),
('verify',['How do I verify my noise floor?','How do I verify the instrument against its specification?','Why characterize system leakage before very small currents?']),
('breakdown',['How is breakdown voltage measured?','Is an avalanche sweep the same as fixed-bias leakage?','What defines the stopping current in breakdown testing?']),
('hv',['What does the high voltage safety note require?','Where should exposed high-voltage conductors be enclosed?','Does this demo implement a physical interlock?'])]
rows=[]
for gi,(gold,qs) in enumerate(groups):
 for j,q in enumerate(qs):rows.append(dict(id=f'q{gi+1:02}-{j+1}',group=f'g{gi+1:02}',query=q,relevant=[gold],origin='author-written synthetic development query'))
(root/'dist/benchmark.json').write_text(json.dumps(rows,indent=2))
print(len(rows),'queries;',len(groups),'paraphrase groups')
