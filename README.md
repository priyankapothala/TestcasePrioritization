# Effectiveness of Different Test Case Prioritization Methods Based on Coverage Criteria

## Project Structure

```
project-thebugsters
├── run.sh
├── benchmarks
    ├── compile.sh
├── src
    ├── main.py
    ├── parser.py
    ├── prioritize.py
    ├── testcase.py
    ├── faults.py
    ├── expose_faults.csv
```

## Dependencies 
-   Python 3

## Steps to run

- Execute ``run.sh`` in the project directory using the following command. 

```sh
$ chmod +x run.sh
$ ./run.sh
```
``run.sh`` compiles each bechmark program and it's faulty versions and generates coverage information using ``compile.sh``. It then executes ``main.py`` to select the testsuites using prioritization methods and finds the faults exposed by each testsuite

## Testsuites

Testsuites for each benchmark program are present in the **testsuites** folder under the respective benchmark program directory

For example, testsuites of printtokens are present in the **testsuites** folder under *printtokens* directory as shown below

```
├── benchmarks
    ├── printtokens
        ├── testsuites
            ├── branch-additional.txt
            ├── branch-random.txt
            ├── branch-total.txt
            ├── statement-additional.txt
            ├── statement-random.txt
            ├── statement-total.txt
```
``expose_faults.csv`` in the src directory contains the the number of faults exposed after running the testsuites.