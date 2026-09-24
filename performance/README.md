# Performance tests

Install Apache JMeter 5.6.3, start the stack, then run
`bash scripts/run_performance.sh`. The script executes 24 groups: two services,
four tile scenarios and three concurrency levels (1/10/50), with 20 loops per
virtual user. `multi_z10` rotates across four neighboring tiles using a JMeter
CSV Data Set. Raw `.jtl` files are ignored by Git; analyzed summaries and
figures are generated from real runs only.
