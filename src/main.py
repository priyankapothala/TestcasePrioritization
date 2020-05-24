#!/usr/bin/env python3

import os
import shutil
from parser import Parser
from prioritize import Prioritize
from faults import run_testsuites
from faults import expose_faults

def create_teststuite(benchmark, criteria, method, selected_tests):
    benchmarks_path = "../benchmarks/"+benchmark
    test_num = [int(test_case.num) for test_case in selected_tests] #getting the test case numbers
    line_num = 1
    test_inputs = []
    input_file_path = os.path.join(benchmarks_path,'universe.txt')
    with open(input_file_path, 'r') as reader:
        for line in reader.readlines():
            if line_num in test_num:
                test_inputs.append(line)
            line_num+=1
    #print('inputs',len(test_inputs))
    test_suite_path = os.path.join(benchmarks_path,'testsuites')
    test_input_path = os.path.join(test_suite_path,criteria+'-'+method+'.txt')
    with open(test_input_path,'w') as f:
        for test_input in test_inputs:
            f.write(test_input)

if __name__ == "__main__":
    benchmarks = ['printtokens','printtokens2','replace','schedule','schedule2','tcas','totinfo']
    criteria_types = ['statement','branch']
    prioritization_methods = ['random','total','additional']
    for benchmark in benchmarks:
        test_cases = []
        test_suite_path = os.path.join("../benchmarks",benchmark,'testsuites')
        if os.path.exists(test_suite_path):
            shutil.rmtree(test_suite_path)
        os.mkdir(test_suite_path)
        coverage_path = os.path.join("../benchmarks",benchmark,'coverage')
        parser = Parser(benchmark,coverage_path)
        for subdir, dirs, files in os.walk(coverage_path):
            for dir in sorted(dirs,key=int):
                filepath = os.path.join(subdir,dir+"/"+benchmark+".c.gcov")
                test_cases = parser.parse(dir,filepath)
        #print('--------------------------------------')
        #print("total: ", len(test_cases))
        prioritize = Prioritize(test_cases)
        for criteria in criteria_types:
            selected_tests = []
            for method in prioritization_methods:
                selected_tests = prioritize.select(criteria,method)
                print("BENCHMARK: "+benchmark+", CRITERIA: "+criteria+", METHOD: "+method+", SELECTED: ",len(selected_tests))
                create_teststuite(benchmark,criteria,method,selected_tests)

    cur_dir = os.getcwd()
    run_testsuites(benchmarks,criteria_types,prioritization_methods)
    expose_faults(cur_dir,benchmarks,criteria_types,prioritization_methods)


            

