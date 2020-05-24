import os
import re
import shutil
import csv
import filecmp

def run_testsuites(benchmarks,criteria_types,prioritization_methods):
    dir_pattern = re.compile(r"^v[0-9]+$")
    for benchmark in benchmarks:
        benchmark_path = os.path.join("../benchmarks",benchmark)
        os.chdir(benchmark_path)
        if os.path.exists('testruns'):
            shutil.rmtree('testruns')
        os.mkdir('testruns')
        for criteria in criteria_types:
            for method in prioritization_methods:
                for subdir, dirs, files in os.walk(os.getcwd()):
                    for dir in dirs:
                        if dir_pattern.match(dir):
                            filename = dir+'/testruns/'+criteria+'-'+method+'-output.txt'
                            if not os.path.exists(os.path.dirname(filename)):
                                os.mkdir(os.path.dirname(filename))
                            if os.path.exists(filename):
                                os.remove(filename)
                            with open(filename, 'w'): pass
                with open(os.path.join('testsuites',criteria+'-'+method+'.txt'), 'r') as reader:
                    for line in reader.readlines():
                        os.system('./'+benchmark+' '+line.strip()+' >> ./testruns/'+criteria+'-'+method+'-output.txt 2>&1') 
                        for subdir, dirs, files in os.walk(os.getcwd()):
                            for dir in dirs:
                                if dir_pattern.match(dir):
                                    os.system('./'+dir+'/'+benchmark+' '+line.strip()+' >> ./'+dir+'/testruns/'+criteria+'-'+method+'-output.txt 2>&1')
        os.chdir('..')
    os.chdir('..')

def expose_faults(cur_dir,benchmarks,criteria_types,prioritization_methods):
    dir_pattern = re.compile(r"^v[0-9]+$")
    os.chdir(cur_dir)
    with open('expose_faults.csv', 'w', newline='') as csvfile:
        fieldnames = ['benchmark', 'criteria', 'method', 'faults_exposed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for benchmark in benchmarks:
            benchmark_path = os.path.join("../benchmarks",benchmark)
            for criteria in criteria_types:
                for method in prioritization_methods:
                    benchmark_run = os.path.join(benchmark_path,'testruns/'+criteria+'-'+method+'-output.txt')
                    faults = 0
                    for subdir, dirs, files in os.walk(benchmark_path):
                        for dir in dirs:
                            if dir_pattern.match(dir):
                                faulty_run = os.path.join(benchmark_path,dir,'testruns/'+criteria+'-'+method+'-output.txt')
                                #print('benchmark run',benchmark_run,'faulty run',faulty_run)
                                if not filecmp.cmp(benchmark_run,faulty_run):
                                    faults+=1
                            #shutil.rmtree(fault_run_path)
                    writer.writerow({'benchmark': benchmark, 'criteria':criteria, 'method': method,'faults_exposed':faults})
            #shutil.rmtree(os.path.join(benchmark_path,'testruns'))