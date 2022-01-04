"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 150126070
Name: Pavithra Subramaniyam
Email:xgpasu@tuni.fi

In this program, implemented a data structure
containing information about the courses offered
by a university. The program will help a student
to select suitable courses to enroll.
"""
# chosen data structure is 'dict in list in dict'

ADD = "a"
CREDITS = "c"
DELETE = "d"
PRINT = "p"
PRINT_DEPARTMENT = "r"
QUIT = "q"


def choose_function():
    """Read a choice from the user and return it."""

    input_line = ''
    choice = ''

    valid_input = True
    # Read input, while it is valid.
    while valid_input:
        print()

        msg = "["+ADD.upper()+"]dd / " + "[" + CREDITS.upper()+"]redits / "+"["+DELETE.upper()+"]elete / "+"[" \
              + PRINT.upper()+"]rint all / p"+"["+PRINT_DEPARTMENT.upper()+"]int department / "+"["+QUIT.upper()+"]uit"
        print(msg)
        input_line = input("Enter command: ").split(" ")    # Read input, split them on separator and store in a list
        choice = str(input_line[0])                         # Read first index in the list and store in the choice

        # Checking whether input (format) for add function have three strings and user input is one among the predefined
        if (choice == "a" and len(input_line) > 3) or choice in (CREDITS, PRINT, PRINT_DEPARTMENT, DELETE, QUIT):
            valid_input = False
        else:
            print("Invalid command!")

    # Returns function command read from the user input and the whole user input 
    return choice, input_line


def add_data(course_registry, department_name, course_name, credit_points):
    """Add a new department/course to course registry."""

    course_name_dict = {}

    # Add department to the course registry (dictionary)
    if department_name not in course_registry:
        course_name_dict.update({course_name: credit_points})  # add new course details in the course_name_dictionary
        course_registry[department_name] = [course_name_dict]  # add dictionary to course registry dictionary
        print()
        print(f"Added department {department_name} with course {course_name}")

    else:
        # Add the course associated with the department to the course registry,
        # if the course is missing from the department.
        if course_name not in department_name:
            course_name_dict.update({course_name: credit_points})     # add new course details in the dictionary
            course_registry[department_name].append(course_name_dict)  # add new course details to list in dictionary
            print()
            print(f"Added course {course_name} to department {department_name}")


def credits_info(course_registry, department_name):
    """Calculating the total credits for the given department"""

    # print if the department not found
    if department_name not in course_registry:
        print()
        print("Department not found!")

    else:
        # Since it is a nested data structure, creating a new dictionary to move
        # the multiple dictionaries inside the list to one dictionary.
        dict_of_dictionaries = {}

        # Calculating the length of the given department
        total_departments = len(course_registry[department_name])
        for course_name in range(total_departments):
            dict_of_dictionaries.update(course_registry[department_name][course_name])

        # Getting the values from the created dictionary
        course_credits = dict_of_dictionaries.values()

        # Calculating the sum of the values in dictionary
        total_credits = sum(course_credits)

        # Printing the total credits
        print()
        print(f"Department {department_name} has to offer {total_credits} cr.")


def delete(course_registry, department_name, course_name=""):
    """ Deleting the department name/course name from the course registry."""

    # execute when user wants to delete the department
    if course_name == "":
        # inform the user if the department not in the course registry
        if department_name not in course_registry:
            print()
            print(f"Department {department_name} not found!")

        else:
            # Deleting the department name from the course registry
            course_registry.pop(department_name)          # Popping the given department name from the course registry
            print()
            print(f"Department {department_name} removed.")

    else:                   # execute when user wants to delete a course from the department
        no_of_dept = len(course_registry[department_name])
        for i in range(no_of_dept):
            # Deleting the course name from the given department
            for key in (course_registry[department_name][i]).keys():
                if key == course_name:
                    (course_registry[department_name][i]).pop(key)        # Popping the given course name from
                    print()                                               # the list in the course registry (dictionary)
                    print(f"Department {department_name} course {course_name} removed.")
                    return                                          # End the function if the course name is deleted

            if i == no_of_dept - 1:                 # Search the course name till the end of the list and inform
                print()                             # the user if the course name not in the list
                print(f"Course {course_name} from {department_name} not found!")


def print_data(course_registry):
    """Print the course data. Does nothing, if there is no data."""

    print()
    # Print the course registry. A nested loop is needed, because the data structure is nested.
    for department_name in sorted(course_registry):
        # Since it is a nested data structure, creating a new dictionary to move
        # the multiple dictionaries inside the list to one dictionary.
        dict_of_dictionaries = {}
        # Print the department name.
        print(f"*{department_name}*")
        no_of_course_in_dept = len(course_registry[department_name])
        for course_name in range(no_of_course_in_dept):
            dict_of_dictionaries.update(course_registry[department_name][course_name])

        for course_name in sorted(dict_of_dictionaries):
            # Print the course and its credits related to the named department.
            print(f"{course_name} : {dict_of_dictionaries[course_name]} cr")


def print_department(course_registry, department_name):
    """Print a particular department and its credits."""

    print()
    if department_name not in course_registry:
        # print the given below text if the department not found
        print("Department not found!")
    else:
        # Since it is a nested data structure, creating a new dictionary to move
        # the multiple dictionaries inside the list to one dictionary.
        dict_of_dictionaries = {}

        # Print the department name.
        print(f"*{department_name}*")
        no_of_course_in_dept = len(course_registry[department_name])
        for course_name in range(no_of_course_in_dept):
            # list-in-dict is converted to new dictionary to print as required
            dict_of_dictionaries.update(course_registry[department_name][course_name])

        for course_name in sorted(dict_of_dictionaries):
            # Print the course and its credits related to the named department.
            print(f"{course_name} : {dict_of_dictionaries[course_name]} cr")


def load_data(file):

    """loading the course details from a text file. Each line of the file has
    data of one course. The format of a line is as follows:
    "department name;1st key=1st value;2nd key=2nd value;...;nth key=nth value"
    The facts (key-value pairs) related to a course and the number of facts
    may vary. The file is assumed to be correctly formatted."""

    # Initialize the a dictionary for the course registry.
    course_registry = {}
    try:
        # Try to open the file for the reading of the movie data.
        file_line = open(file, mode="r")

        # Populate the dictionary, until the file has been processed.
        # A nested loop is needed, because the data structure is nested.
        for line in file_line:

            # Split the line into names and facts.
            data_fields = line.split(";")

            # The input file should contain exactly three fields
            if len(data_fields) != 3:
                print("Error in file!")
                course_registry = {}
                return course_registry

            # Adding the course details in list
            department_name = data_fields[0]
            course_name = data_fields[1]
            credit_points = int(data_fields[2])

            # Add the credits in nested dictionary
            if department_name not in course_registry:
                course_name = {course_name: credit_points}
                course_registry[department_name] = [course_name]
            else:
                course_name = {course_name: credit_points}
                course_registry[department_name].append(course_name)

        # Close the file.
        file_line.close()

    except OSError:
        # Make a note of an error.
        print("Error opening file!")

    # returning the dictionary
    return course_registry


def processing_input(command, input_line):
    """ Function to read the input in a single line and return them to diff functions as per the requirement"""

    if command == 'a':
        # Calculating the number of the strings in the given input line list
        no_of_input_str = len(input_line)-1

        # Separating the department name
        department = str(input_line[1])

        # Separating the course name from the given string
        empty_string = ""
        for i in range(2, no_of_input_str):
            if empty_string == "":
                course_name = input_line[i]
                empty_string = course_name
            else:
                course_name = empty_string+" " + input_line[i]
                empty_string = course_name
        course_name = str(empty_string)

        # Separating the credits from the given string
        credits_in = int(input_line[no_of_input_str])

        # returning the department name, course name and credits to main
        return department, course_name, credits_in

    elif command == 'd':

        # Calculating the number of the strings in the given input line list
        no_of_input_str = len(input_line)

        # Separating the department name
        department = str(input_line[1])
        empty_string = ""

        # Separating the course name from the given string
        for i in range(2, no_of_input_str):
            if empty_string == "":
                course_name = input_line[i]
                empty_string = course_name
            else:
                course_name = empty_string + " " + input_line[i]
                empty_string = course_name
        course_name = str(empty_string)

        # returning the department name, course name to main
        return department, course_name

    elif command == 'c' or 'r':

        # Separating the department name
        department = str(input_line[1])

        # returning the department name to main
        return department


def main():
    # get a file which contains the course data.
    file_name = input("Enter file name: ")

    # Try to load the course data.
    course_data = load_data(file_name)

    # Do not continue, if the data could not be loaded.
    if course_data == {}:
        return

    # Call functions until the user has had enough.
    do_the_loop = True
    while do_the_loop:
        # Decide which function has to be executed
        choice, input_data = choose_function()
        if choice == ADD:
            # process from user input and get the arguments to the function
            department_n, course_n, credit_info = processing_input(choice, input_data)
            add_data(course_data, department_n, course_n, credit_info)
        elif choice == CREDITS:
            # process from user input and get the arguments to the function
            department_n = processing_input(choice, input_data)
            credits_info(course_data, department_n)
        elif choice == DELETE:
            # process from user input and get the arguments to the function
            department_n, course_n = processing_input(choice, input_data)
            delete(course_data, department_n, course_n)
        elif choice == PRINT:
            print_data(course_data)
        elif choice == PRINT_DEPARTMENT:
            # process from user input and get the arguments to the function
            department_n = processing_input(choice, input_data)
            print_department(course_data, department_n)
        elif choice == QUIT:
            print("Ending program.")
            do_the_loop = False


if __name__ == "__main__":
    main()
