import random

class Prioritize:

    def __init__(self,test_cases):
        self.test_cases = test_cases

    def select(self,criteria,method):
        self.criteria = criteria
        if method=="random":
            return self.random_coverage()
        elif method=="total":
            return self.total_coverage()
        elif method=="additional":
            return self.additional_coverage()

    def random_coverage(self):
        random_test_cases = list(self.test_cases)
        random.shuffle(random_test_cases)
        return self.select_tests(random_test_cases)

    def total_coverage(self):
        sorted_test_cases = []
        if self.criteria == "statement":
            sorted_test_cases = sorted(self.test_cases, key=lambda x: x.covered_statements, reverse=True)
        elif self.criteria == "branch":
            sorted_test_cases = sorted(self.test_cases, key=lambda x: x.covered_branches, reverse=True)

        return self.select_tests(sorted_test_cases)

    def additional_coverage(self):
        selected_tests = []
        total = set()
        covered = set()

        # computing total lines covered by all testcases
        for test_case in self.test_cases:
            coverage_info = test_case.get_coverage(self.criteria)
            total.update(coverage_info['lines'])
					
        temp_test_cases = list(self.test_cases)
        # (i) select a test case that yields the greatest additional coverage; and 
        # (ii) then adjust the coverage information on subsequent test cases to indicate their coverage of statements/branches not yet covered
        while len(covered) < len(total):
            #sort the uncovered test cases based on # uncovered statements 
            selected_test_case = self.select_max_coverage(total,covered,temp_test_cases)
            selected_tests.append(selected_test_case)
            coverage_info = selected_test_case.get_coverage(self.criteria)
            covered.update(coverage_info["lines"])
	
        #print(len(covered),len(total))      
        return selected_tests

    def select_max_coverage(self,total,covered,test_cases):
        # select the test case that yields the greatest additional coverage
        uncovered = total.difference(covered)
        max_covered = 0
        selected_test_index = 0
        for index in range(len(test_cases)):
            coverage_info = test_cases[index].get_coverage(self.criteria)
            count = len(uncovered.intersection(coverage_info["lines"]))
            if count > max_covered:
                max_covered = count
                selected_test_index = index
        return test_cases.pop(selected_test_index)

    def select_tests(self,test_cases):
        selected_tests = []
        total = set()
        covered = set()

        for test_case in test_cases:
            coverage_info = test_case.get_coverage(self.criteria)
            total.update(coverage_info['lines'])

        for test_case in test_cases:
            if len(covered) >= len(total):
                break
            coverage_info = test_case.get_coverage(self.criteria)
            if len(covered.union(coverage_info["lines"])) == len(covered):
                continue
            covered.update(coverage_info["lines"])
            selected_tests.append(test_case)

        #print(len(covered),len(total))
        return selected_tests