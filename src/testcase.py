class TestCase:
    total_statements = 0
    total_branches = 0
    covered_statements = 0
    covered_branches = 0
    statements = set()
    branches = set()
    
    def __init__(self,num,statement_count,branch_count,statements,branches):
        self.num = num #test case number in universe.txt
        self.total_statements = statement_count
        self.total_branches = branch_count
        self.statements = statements
        self.branches = branches
        self.covered_statements = len(statements)
        self.covered_branches = len(branches)

    def get_coverage(self,criteria):
        if criteria == "statement":
            return dict({"lines":self.statements,"count":self.total_statements})
        if criteria == "branch":
            return dict({"lines":self.branches,"count":self.total_branches})

    def __repr__(self):
        return "Num: "+str(self.num)+\
            "\nToatl Statement: "+str(self.total_statements)+\
            "\nTotal Branches: "+str(self.total_branches)+\
            "\nExe Statements: "+str(len(self.statements))+\
            "\nExe Branches: "+str(len(self.branches))+\
            "\nStatements: "+str(self.statements)+\
            "\nBranches: "+str(self.branches)