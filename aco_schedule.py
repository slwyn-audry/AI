import random

# Define the parameters
num_ants = 10
num_iterations = 10
pheromone_decay = 0.1
alpha = 1
beta = 5

# Define the problem-specific data
school_hours_start = 7
school_hours_end = 20
school_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

subjects = {
    'CC303-M': 3,
    'CS321L-M': 3,
    'CS322-M': 2,
    'CS341L-M': 3,
    'CS342-M': 2,
    'CS361L-M': 3,
    'CS362-M': 2,
    'CS383-M': 3,
    'CSE3-M': 3,
    'CSE4-M': 3
}

professors = {
    'DOLLY': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'available_hours_start': 7,
        'available_hours_end': 20,
        'available_subjects': ['CS341L-M', 'CS342-M']
    },
    'JANLEE': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'available_hours_start': 10,
        'available_hours_end': 20,
        'available_subjects': ['CS321L-M', 'CS322-M', 'CS383-M']
    },
    'EDWARD': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'available_hours_start': 7,
        'available_hours_end': 17,
        'available_subjects': ['CS361L-M', 'CS362-M']
    },
    'YANIE': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'available_hours_start': 10,
        'available_hours_end': 17,
        'available_subjects': ['CC303-M']
    },
    'ENRICK': {
        'available_days': ['Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20,
        'available_subjects': ['CSE3-M']
    },
    'BENJIE': {
        'available_days': ['Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20,
        'available_subjects': ['CSE4-M']
    }
}

classrooms = {
    'ROOM CS301': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20
    },
    'ROOM CS302': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20
    }
}

sections = {
    'BSCS 3AB': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20,
        'max_subjects_per_day': 10
    },
    'BSCS 3CD': {
        'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'available_hours_start': 7,
        'available_hours_end': 20,
        'max_subjects_per_day': 10
    }
}

# Initialize the pheromone matrix
num_days = len(school_days)
num_hours = school_hours_end - school_hours_start + 1

pheromone_matrix = [
    [[5.0] * num_hours for _ in range(len(classrooms))] for _ in range(len(subjects))
]

# Initialize the best solution and its corresponding fitness
best_solution_3AB = {}
best_solution_3CD = {}
best_fitness_3AB = float('inf')
best_fitness_3CD = float('inf')
best_list = {}

# Initialize a dictionary to keep track of scheduled hours for each classroom
classroom_schedule = {classroom: set() for classroom in classrooms}

# Define a helper function to check if a classroom is available at a given time slot
def is_classroom_available(classroom, day, hour, subject_duration):
    for h in range(hour, hour + subject_duration):
        if h in classroom_schedule[classroom] or h < school_hours_start or h >= school_hours_end:
            return False
    return True

# Define a helper function to update the scheduled hours for a classroom
def update_classroom_schedule(classroom, hour, subject_duration):
    for h in range(hour, hour + subject_duration):
        classroom_schedule[classroom].add(h)

def is_available(subject, professor, classroom, section, day, hour):
    subject_duration = subjects[subject]
    if (
        day in professors[professor]['available_days'] and
        hour >= professors[professor]['available_hours_start'] and
        hour < professors[professor]['available_hours_end'] - subject_duration + 1 and
        subject in professors[professor]['available_subjects'] and
        day in classrooms[classroom]['available_days'] and
        hour >= classrooms[classroom]['available_hours_start'] and
        hour < classrooms[classroom]['available_hours_end'] - subject_duration + 1 and
        day in sections[section]['available_days'] and
        hour >= sections[section]['available_hours_start'] and
        hour < sections[section]['available_hours_end'] - subject_duration + 1 and
        is_classroom_available(classroom, day, hour, subject_duration)
    ):
        # Check for overlapping schedules in BSCS 3AB
        for subj, (prof, cl, sec, d, h) in best_solution_3AB.items():
            if h <= hour < h + subjects[subj] and d == day and cl == classroom:
                return False
        
        # Check for overlapping schedules in BSCS 3CD
        for subj, (prof, cl, sec, d, h) in best_solution_3CD.items():
            if h <= hour < h + subjects[subj] and d == day and cl == classroom:
                return False
        
        return True
    
    return False

# Main ACO loop for BSCS 3AB
for _ in range(num_iterations):
    # Initialize the ant solutions
    ant_solutions_3AB = []
    
    # Construct solutions for each ant
    for _ in range(num_ants):
        solution = {}
        
        # Assign subjects to professors, classrooms, sections, days, and hours
        for subject in subjects:
            available_slots = []
            for professor in professors:
                for classroom in classrooms:
                    for section in sections:
                        for day in school_days:
                            for hour in range(school_hours_start, school_hours_end + 1):
                                if is_available(subject, professor, classroom, 'BSCS 3AB', day, hour):
                                    available_slots.append((professor, classroom, 'BSCS 3AB', day, hour))
            
            if available_slots:
                probabilities = []
                
                # Calculate the probabilities based on pheromone levels and heuristic information
                for slot in available_slots:
                    professor, classroom, section, day, hour = slot
                    pheromone_level = pheromone_matrix[list(subjects.keys()).index(subject)][list(classrooms.keys()).index(classroom)][hour - school_hours_start]
                    probability = pheromone_level**alpha
                    probabilities.append((slot, probability))
                
                # Select the slot based on the probabilities
                total_probability = sum(p[1] for p in probabilities)
                probabilities = [(p[0], p[1]/total_probability) for p in probabilities]
                selected_slot, _ = random.choices(probabilities)[0]
                professor, classroom, section, day, hour = selected_slot
                
                solution[subject] = (professor, classroom, section, day, hour)
        
        # Add the solution to the ant solutions
        ant_solutions_3AB.append(solution)
    
    # Update the pheromone matrix for BSCS 3AB
    for i, classroom in enumerate(classrooms):
        for j in range(num_hours):
            for k, subject in enumerate(subjects):
                for ant_solution in ant_solutions_3AB:
                    if subject in ant_solution:
                        _, _, _, day, hour = ant_solution[subject]
                        if hour == hour and day == day:
                            pheromone_matrix[k][i][j] += pheromone_decay / best_fitness_3AB
    
    # Update the best solution for BSCS 3AB
    for ant_solution in ant_solutions_3AB:
        fitness = len(ant_solution)
        if fitness < best_fitness_3AB:
            best_solution_3AB = ant_solution
            best_fitness_3AB = fitness

# Main ACO loop for BSCS 3CD
for _ in range(num_iterations):
    # Initialize the ant solutions
    ant_solutions_3CD = []
    
    # Construct solutions for each ant
    for _ in range(num_ants):
        solution = {}
        
        # Assign subjects to professors, classrooms, sections, days, and hours
        for subject in subjects:
            available_slots = []
            for professor in professors:
                for classroom in classrooms:
                    for section in sections:
                        for day in school_days:
                            for hour in range(school_hours_start, school_hours_end + 1):
                                if is_available(subject, professor, classroom, 'BSCS 3CD', day, hour):
                                    available_slots.append((professor, classroom, 'BSCS 3CD', day, hour))
            
            if available_slots:
                probabilities = []
                
                # Calculate the probabilities based on pheromone levels and heuristic information
                for slot in available_slots:
                    professor, classroom, section, day, hour = slot
                    pheromone_level = pheromone_matrix[list(subjects.keys()).index(subject)][list(classrooms.keys()).index(classroom)][hour - school_hours_start]
                    probability = pheromone_level**alpha
                    probabilities.append((slot, probability))
                
                # Select the slot based on the probabilities
                total_probability = sum(p[1] for p in probabilities)
                probabilities = [(p[0], p[1]/total_probability) for p in probabilities]
                selected_slot, _ = random.choices(probabilities)[0]
                professor, classroom, section, day, hour = selected_slot
                
                solution[subject] = (professor, classroom, section, day, hour)
        
        # Add the solution to the ant solutions
        ant_solutions_3CD.append(solution)
    
    # Update the pheromone matrix for BSCS 3CD
    for i, classroom in enumerate(classrooms):
        for j in range(num_hours):
            for k, subject in enumerate(subjects):
                for ant_solution in ant_solutions_3CD:
                    if subject in ant_solution:
                        _, _, _, day, hour = ant_solution[subject]
                        if hour == hour and day == day:
                            pheromone_matrix[k][i][j] += pheromone_decay / best_fitness_3CD
    
    # Update the best solution for BSCS 3CD
    for ant_solution in ant_solutions_3CD:
        fitness = len(ant_solution)
        if fitness < best_fitness_3CD:
            best_solution_3CD = ant_solution
            best_fitness_3CD = fitness


# Print the best solution for BSCS 3AB
print("Best solution for BSCS 3AB:")
for subject, (professor, classroom, section, day, hour) in best_solution_3AB.items():
    print(f"{subject}: Professor {professor}, Classroom {classroom}, Section {section}, {day} at {hour}:00-{hour+subjects[subject]}:00")

# Print the best solution for BSCS 3CD
print("Best solution for BSCS 3CD:")
for subject, (professor, classroom, section, day, hour) in best_solution_3CD.items():
    print(f"{subject}: Professor {professor}, Classroom {classroom}, Section {section}, {day} at {hour}:00-{hour+subjects[subject]}:00")