from collections import Counter
class CSPSolver:

    def __init__(self, num_variables, domains, is_consistent):
        self.num_variables = num_variables
        self.domains = domains  # A dictionary of available domains for each variable
        self.is_consistent = is_consistent  # Function to check if an assignment violates constraints

    # makes an initial assignment with -1s and initiates backtracking
    def solve(self):
        assignment = [-1 for _ in range(self.num_variables)]
        result = self.backtracking_search(assignment)
        return result

    # function to make an assignment for one variable, recurse and return the solution if one is found
    def backtracking_search(self, assignment):

        # All variables are assigned, we have reached a solution
        if -1 not in assignment:
            return assignment

        # get the variable we currently want to assign (the first unassigned variable
        curr_var = assignment.index(-1)

        # getting a list of values that can be assigned to this variable in sorted order
        values = self.get_values(assignment, self.domains[curr_var])

        # loop over all values and assign them and recurse until a solution is found
        for value in values:
            assignment[curr_var] = value  # assigning the current value
            if self.is_consistent(assignment, curr_var):  # if it does not violate constraints
                result = self.backtracking_search(assignment)  # recurse to assign other variables
                # if a solution is found
                if result is not None:
                    return result
            assignment[curr_var] = -1  # unassigning that variable to try a different value
        return None  # if no solution is found

    # this function is to balance the students out by first checking times that have the least students assigned
    # it returns the domain sorted by times which are least used first
    def get_values(self, assignment, domain):
        value_counts = Counter(assignment)
        sorted_domain = sorted(domain, key=lambda x: value_counts.get(x, 0))
        print("GET VALS")
        print(assignment)
        print(domain)
        print(sorted_domain)
        return sorted_domain

