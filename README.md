# L6_L7_37 — Irrigation Scheduler

Lab 6: Code and Branch Coverage

## About

A small Python module that decides when a field zone needs watering, how much water it needs and builds a schedule within a water budget.

## Files

| File | Description |
|------|-------------|
| `irrigation_scheduler.py` | The module under test |
| `test_irrigation_scheduler.py` | Starter test file |
| `CodeCoverageTest_37_irrigation_scheduler.py` | Tests focused on executable-line coverage |
| `BranchCoverageTest_37_irrigation_scheduler.py` | Tests covering both outcomes of each decision |

## Run coverage

From this directory, install the test dependencies if needed:

```powershell
python -m pip install pytest coverage
```

Measure line coverage:

```powershell
python -m coverage run --data-file=.coverage-line --source=irrigation_scheduler -m pytest -q CodeCoverageTest_37_irrigation_scheduler.py
python -m coverage report --data-file=.coverage-line -m
```

Measure branch coverage:

```powershell
python -m coverage run --branch --data-file=.coverage-branch --source=irrigation_scheduler -m pytest -q BranchCoverageTest_37_irrigation_scheduler.py
python -m coverage report --data-file=.coverage-branch -m
```

The line-focused tests exercise every executable application line. The branch-focused
tests cover both outcomes of each decision and loop. The coverage data files are kept
separate so the two reports can be generated independently.
