import sys

# Import custom modular components
from hostel_data import (
    initialize_students,
    initialize_rooms,
    initialize_complaints,
    get_valid_integer,
    get_valid_float,
    get_non_empty_string,
    find_student_by_id,
    add_student,
    view_all_students,
    search_student,
    update_student,
    delete_student,
    view_rooms,
    manage_fees,
    record_late_entry,
    view_late_entry_register
)

from simulation import (
    initialize_game_state,
    display_warden_hud,
    run_daily_simulation,
    view_audit_report,
    check_game_status
)

# 1. COMPLAINT REGISTRATION HELPER

def register_new_complaint(complaints, students):
    """
    Allows wardens or students to file a new maintenance ticket.
    Appends the complaint to the shared complaints list used in the simulation.
    """
    print("\n" + "=" * 55)
    print("           REGISTER NEW STUDENT GRIEVANCE / TICKET")
    print("=" * 55)

    s_id = get_non_empty_string(" Enter Student ID lodging complaint (or '0' to Cancel): ").upper()
    if s_id == '0':
        return

    student = find_student_by_id(students, s_id)
    if not student:
        print(f" [!] Student ID '{s_id}' not found in registered records.")
        return

    print("\n Issue Category:")
    print(" 1. Plumbing & Washroom")
    print(" 2. Electrical & Lighting")
    print(" 3. Wi-Fi & Internet")
    print(" 4. Mess & Food Hygiene")
    print(" 5. Room Furniture & Carpentry")
    cat_choice = get_valid_integer(" Select Category (1-5): ", 1, 5)
    cat_map = {
        1: "Plumbing",
        2: "Electrical",
        3: "Internet",
        4: "Mess",
        5: "Carpentry"
    }
    category = cat_map[cat_choice]

    desc = get_non_empty_string(" Describe the issue in detail: ")
    est_cost = get_valid_float(" Enter Estimated Repair Cost (in Rs., e.g. 800): ", min_val=0.0)

    # Auto-generate next complaint ID
    next_id = len(complaints) + 1

    new_ticket = {
        "id": next_id,
        "student_id": s_id,
        "category": category,
        "description": desc,
        "cost_to_fix": est_cost,
        "status": "Pending"
    }

    complaints.append(new_ticket)
    print("\n" + "-" * 55)
    print(f" [SUCCESS] Complaint #{next_id} logged successfully for {student['name']} (Room {student['room_number']})!")
    print(f"           Category: {category} | Estimated Cost: Rs. {est_cost:,.2f}")
    print("           The ticket will appear in the next daily simulation round.")
    print("-" * 55)

# 2. STUDENT MANAGEMENT SUBMENU

def student_management_menu(students, rooms):
    """
    Dedicated submenu for complete CRUD operations on student records.
    """
    while True:
        print("\n" + "=" * 55)
        print("         STUDENT & ROOM RECORDS MANAGEMENT")
        print("=" * 55)
        print(" 1. Add / Register New Student")
        print(" 2. View All Registered Students")
        print(" 3. Search Student Records (by ID, Name, Room)")
        print(" 4. Update Student Details / Shift Room")
        print(" 5. Delete / Expel Student Record")
        print(" 6. Return to Main Menu")
        print("-" * 55)

        choice = get_valid_integer(" Choose an operation (1-6): ", 1, 6)

        if choice == 1:
            add_student(students, rooms)
        elif choice == 2:
            view_all_students(students)
        elif choice == 3:
            search_student(students)
        elif choice == 4:
            update_student(students, rooms)
        elif choice == 5:
            delete_student(students, rooms)
        elif choice == 6:
            break

# 3. NIGHT PATROL & DISCIPLINE SUBMENU

def night_patrol_menu(students):
    """
    Submenu for tracking hostel curfew, late arrivals after 10 PM, and warnings.
    """
    while True:
        print("\n" + "=" * 55)
        print("      NIGHT PATROL & CURFEW REGISTER (AFTER 10 PM)")
        print("=" * 55)
        print(" 1. Log Late Entry (Time, Student ID, Reason)")
        print(" 2. View Late Entry Master Register")
        print(" 3. Return to Main Menu")
        print("-" * 55)

        choice = get_valid_integer(" Choose an operation (1-3): ", 1, 3)

        if choice == 1:
            record_late_entry(students)
        elif choice == 2:
            view_late_entry_register(students)
        elif choice == 3:
            break

# 4. MAIN MENU LOOP & DRIVER

def main():
    """
    Main driver function initializing project data and driving the top-level menu.
    """
    # Initialize Core Application State
    students = initialize_students()
    rooms = initialize_rooms()
    complaints = initialize_complaints()
    game_state = initialize_game_state()

    print("\n" + "*" * 76)
    print("  WELCOME TO THE HOSTEL MANAGEMENT SYSTEM & WARDEN SIMULATION GAME")
    print("  Department of Computer Science & Engineering | B.Tech 1st Semester")
    print("*" * 76)

    while True:
        # Show top HUD summary
        display_warden_hud(game_state, len(students))

        print("\n MAIN NAVIGATION MENU:")
        print(" -------------------------------------------------------------")
        # Dynamic label based on simulation progress
        if not game_state["game_over"]:
            print(f" 1. [SIMULATION] Run Day {game_state['day']} Warden Operations (Food, Crisis, Patrol)")
        else:
            print(f" 1. [SIMULATION] Simulation Completed ({game_state['game_result']}) - View Audit")

        print(" 2. [STUDENTS]   Student Records Desk (Add, View, Search, Update, Delete)")
        print(" 3. [ROOMS]      Hostel Room Occupancy & Vacancy Status")
        print(" 4. [FEES]       Fee Payments, Dues Audit & Defaulters List")
        print(" 5. [GRIEVANCE]  Register New Student Complaint / Maintenance Ticket")
        print(" 6. [CURFEW]     Late Entry & Night Patrol Register (After 10:00 PM)")
        print(" 7. [AUDIT]      View Complete Financial & Satisfaction Audit Log")
        print(" 8. Exit Program")
        print(" -------------------------------------------------------------")

        choice = get_valid_integer(" Enter your choice (1-8): ", 1, 8)

        if choice == 1:
            if not game_state["game_over"]:
                run_daily_simulation(game_state, students, rooms, complaints)
            else:
                print("\n [!] The 7-day challenge has ended!")
                print(f"     Final Status: {game_state['game_result']}")
                is_over, res, msg = check_game_status(game_state)
                print(f"     Outcome: {msg}")
                print("     You can continue to manage records, fees, and rooms in the other menus.")
                view_audit_report(game_state)

        elif choice == 2:
            student_management_menu(students, rooms)

        elif choice == 3:
            view_rooms(rooms)

        elif choice == 4:
            manage_fees(students)

        elif choice == 5:
            register_new_complaint(complaints, students)

        elif choice == 6:
            night_patrol_menu(students)

        elif choice == 7:
            view_audit_report(game_state)

        elif choice == 8:
            print("\n" + "=" * 60)
            print(" Thank you for using the Hostel Management & Simulation System!")
            print("=" * 60 + "\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
