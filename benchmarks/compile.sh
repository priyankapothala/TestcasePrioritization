#!/bin/bash
coveragefile="coverage.sh"
rm $coveragefile
touch $coveragefile
for benchmark in * ; do
	# -d checks if file exists and is a directory
	if [ -d $benchmark ]; then
		# compiling the benchmark program
		# run replace and totinfo with -lm flag
		cd $benchmark
		echo "cd $benchmark" >> ../$coveragefile
		echo "rm -rf coverage" >> ../$coveragefile
		if [ $benchmark = totinfo -o $benchmark = replace ]; then
			gcc -g -o $benchmark $benchmark.c -lm -Wno-return-type -fprofile-arcs -ftest-coverage
		else
			gcc -g -o $benchmark $benchmark.c -Wno-return-type -fprofile-arcs -ftest-coverage
		fi

		echo "mkdir coverage" >> ../$coveragefile
		inputfile='./universe.txt'
		test_num=1
		# reading each testinput in universe.txt
		while read -r testinput; do
			echo "mkdir coverage/$test_num" >> ../$coveragefile
			echo "./$benchmark $testinput" >> ../$coveragefile
			echo "gcov -b -c $benchmark" >> ../$coveragefile
			# move coverage file to the coverage directory
			echo "mv $benchmark.c.gcov coverage/$test_num" >> ../$coveragefile
			echo "rm $benchmark.gcda" >> ../$coveragefile
			((test_num++))
		done < $inputfile
		
		# compiling the faulty versions
		i=1
		while [ -d v$i ]; do
			cd v$i	
			# run replace and totinfo with -lm flag	
			if [ $benchmark = totinfo -o $benchmark = replace ]; then
				gcc -g -o $benchmark $benchmark.c -lm -Wno-return-type -fprofile-arcs -ftest-coverage
			else
				gcc -g -o $benchmark $benchmark.c -Wno-return-type -fprofile-arcs -ftest-coverage
			fi
			cd ..
			((i++))
		done
		echo "cd .." >> ../$coveragefile
		cd ..
	fi
done
