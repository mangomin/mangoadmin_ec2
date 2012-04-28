init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests

performance:
	python -m cProfile -o performance.prof tests/performance.py
	/usr/local/bin/runsnake tblrec.prof

lineprof:
	kernprof.py -v -l tests/performance.py
