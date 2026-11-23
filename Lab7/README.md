# L6_L7_37 — Irrigation Scheduler

Lab 7: Fuzz Testing

## About

A small Python module that parses field zones, averages soil moisture and estimates water needs.

## Files

| File | Description |
|------|-------------|
| `irrigation_scheduler.py` | Validates and processes zone, moisture, and water inputs |
| `test_irrigation_scheduler.py` | Hypothesis properties and invalid-input tests |
| `Lab_7_FuzzTesting_Evidence.pdf` | Before-and-after command output report |

## Run Lab 7

Install the test dependencies if needed:

```powershell
python -m pip install pytest hypothesis
```

Run the application with the sample inputs:

```powershell
python irrigation_scheduler.py
```

Run the property-based and validation tests:

```powershell
python -m pytest -q test_irrigation_scheduler.py
```

The parsing functions raise `ValueError` for malformed inputs, non-finite numbers,
empty fields, nonpositive plot areas, and out-of-range moisture percentages.
