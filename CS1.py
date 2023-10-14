from CSPsolver import CSPSolver
import time


class CS1SectionsCSP:

    def __init__(self, students, num_leaders, times):
        self.students = students  # Array list of students
        self.num_students = len(students)
        self.num_leaders = num_leaders
        self.times = times  # Array of time blocks

    # solver function that passes the problem to the CSP solver and prints the result
    def solve(self):

        # creating an array of variables
        variables = [x for x in range(self.num_students)]

        # list of all coordinates in the board which is all possible domains
        domains = [y for y in range(1, len(self.times) + 1)]

        domain_dictionary = {}  # to store each student's available times
        student_to_var = {}  # stores student names to variable name

        for var, student in enumerate(self.students):
            domain_dictionary[var] = student[2]
            student_to_var[student[0]] = var

        student_conflicts = {}  # to store any students a student can't work with
        for var, student in enumerate(self.students):
            if len(student) == 4:
                if var not in student_conflicts:
                    student_conflicts[var] = set()
                for student_name in student[3]:
                    student_var = student_to_var[student_name]
                    student_conflicts[var].add(student_var)
                    if student_var not in student_conflicts:
                        student_conflicts[student_var] = set()
                        student_conflicts[student_var].add(var)

        print(student_conflicts)

        def is_consistent(assignment, curr_var):
            print(assignment)
            # check if it is a leader
            if curr_var < self.num_leaders:
                return True

            #  first check if the student is matched to a time with leaders in it
            leader_assignments = assignment[0: self.num_leaders]
            if assignment[curr_var] not in leader_assignments:
                print('False because not valid leader time')
                return False

            # constraints on who can work with who
            if curr_var in student_conflicts:
                print("here")
                conflicts = student_conflicts[curr_var]
                print(conflicts)
                for c in conflicts:
                    if assignment[c] == assignment[curr_var]:
                        print('False because student conf')
                        return False

            # gender balancing constraint
            # at least num_students/2*num_leaders - 1 students of each gender in each section
            if -1 not in assignment:
                time_to_females = {}
                time_to_males = {}
                for student_var, time in enumerate(assignment):
                    if self.students[student_var][1] == "M":
                        time_to_males[time] = time_to_males.get(time, 0) + 1
                    else:
                        time_to_females[time] = time_to_females.get(time, 0) + 1

                min_required = max((self.num_students / (self.num_leaders * 2)) - 1, 2)
                print(min_required)

                for t in time_to_males:
                    if 0 < time_to_males[t] < min_required :
                        print('False because gender')
                        return False

                for t in time_to_females:
                    if 0 <time_to_females[t] < min_required:
                        print('False because gender')
                        return False

            return True

        # Creating the solver
        csp = CSPSolver(len(variables), domain_dictionary, is_consistent)

        # Solve the CSP
        solution = csp.solve()

        # Printing the solution
        print("---------------------------------------")
        print("Solution for Student problem:")

        # Saving solution
        result = ""

        if solution:
            print(solution)
            time_to_students = {}
            time_to_leaders = {}
            for idx, time_block in enumerate(solution):
                student = self.students[idx]
                if idx < self.num_leaders:
                    if time_block not in time_to_leaders:
                        time_to_leaders[time_block] = ""
                    time_to_leaders[time_block] += student[0] + "(" + student[1] + ") "
                else:
                    if time_block not in time_to_students:
                        time_to_students[time_block] = []
                    time_to_students[time_block].append(student[0] + "(" + student[1] + ")")
            for time_block in time_to_leaders:
                print('At time', self.times[time_block], ":")
                result += ('At time ' + self.times[time_block] + ":\n")
                print('Leaders are:', time_to_leaders[time_block])
                result+= ('Leaders are: '+ time_to_leaders[time_block] + "\n")
                print('Students are:')
                result+= ('Students are:\n')
                if time_block in time_to_students:
                    for student in time_to_students[time_block]:
                        print(student)
                        result += (student + "\n")
                print("-------------")
                result+= "-------------\n"

        else:
            print("No solution found.")
            result+= "No solution found."

        return result

# test code
if __name__ == "__main__":
    students = [
        ["Nitya", "F", [0, 1, 2, 3]],
        ["Max", "M", [1, 2]],
        ["Sam", "M", [0, 3]],
        ["Patty", "F", [0, 1, 2, 3]],
        ["Matt", "M", [1, 2, 3]],
        ["Cosh", "F", [2, 3], ["Claire"]],
        ["Collin", "M", [2, 3]],
        ["Claire", "F", [2, 3]],
    ]
    test_1 = CS1SectionsCSP(students, 3,
                            ["4:30-5:30 Thursday", "4:30-5:30 Friday", "6:30-7:30 Friday", "5:30-6:30 Saturday"])
    start = time.time()
    test_1.solve()
    end = time.time()
    print("The time of execution of test 1 with no inference :",
          (end - start) * 10 ** 3, "ms")
    print("---------------------------------------")
    print()
