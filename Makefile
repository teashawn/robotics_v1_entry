setup:
	pip install -r requirements.txt
	./download_data.sh

run-small:
	python3 main.py \
		--input data/small/input.bin \
		--output data/small/output.bin

run-big:
	python3 main.py \
		--input data/big/input.bin \
		--output data/big/output.bin
