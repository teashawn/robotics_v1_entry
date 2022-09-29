# robotics_v1_entry

## Requirements

- Python>=3.8.10
- Make

The solution also relies on [NumPy](https://numpy.org/) and some test data. To
get both run:
```bash
make setup
```

## Running

To run the solution with the small test case, type the following in your
teminal:
```bash
make run-small
```

To run the solution with the big test case, type the following:
```bash
make run-big
```

To run the solution with an arbritrary data set, type this:
```bash
python3 main.py \
	--input path/to/input/file \
	--output path/to/output/file
```
