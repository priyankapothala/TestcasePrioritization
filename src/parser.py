import re
from testcase import TestCase

class Parser:
    tot_stmts = re.compile(r"^\s+(#####|[0-9]+):\s+[0-9]+:.*")
    exe_stmts = re.compile(r"^\s+[0-9]+:\s+[0-9]+:.*")
    tot_branches = re.compile(r"^branch\s+[0-9]+.*") #matches (branch num taken || branch num never executed)
    exe_branches = re.compile(r"^branch\s+[0-9]+\s+taken\s+[1-9][0-9]*.*") #matches (branch num taken)
    stmt_line_num = re.compile(r"^\s+[0-9]+:\s+([0-9]+):.*") # line number matches group 1

    def __init__(self,benchmark,path):
        self.benchmark = benchmark
        self.coverage_path = path 
        self.test_cases = []

    def parse(self,num,filepath):
        branch_count = 0
        stmt_count = 0
        statements = set()
        branches = set()
        line_num = 1
        with open(filepath, 'r') as reader:
            for line in reader.readlines():
                #if the line matches the statement regex increment the stmt count
                if self.tot_stmts.match(line):
                    stmt_count+=1
                    if self.exe_stmts.match(line): #if the statement is executed add the statement line number
                        stmt_num = int(self.stmt_line_num.match(line).group(1))
                        statements.add(stmt_num)

                #if the line matches the branch regex increment the branch count
                elif self.tot_branches.match(line):
                    branch_count+=1
                    if self.exe_branches.match(line): #if the statement is executed add the branch line number
                        branches.add(line_num)
                line_num+=1
        self.test_cases.append(TestCase(num,stmt_count,branch_count,statements,branches))
        return self.test_cases