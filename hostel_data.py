

def initialize_students():
    """
    Returns an initial list of student dictionaries.
    Pre-populated with sample records so the system is ready for testing immediately.
    """
    return [
        {
            "id": "ST101",
            "name": "Aarav Sharma",
            "course": "B.Tech CSE",
            "contact": "9876543210",
            "room_number": "101",
            "fee_total": 45000.0,
            "fee_paid": 45000.0,
            "fee_due": 0.0,
            "fee_status": "Paid",
            "meal_pref": "Veg",
            "late_entries": 0,
            "remarks": "Good conduct"
        },
        {
            "id": "ST102",
            "name": "Priya Patel",
            "course": "B.Tech AI-DS",
            "contact": "9812345678",
            "room_number": "101",
            "fee_total": 45000.0,
            "fee_paid": 30000.0,
            "fee_due": 15000.0,
            "fee_status": "Pending",
            "meal_pref": "Veg",
            "late_entries": 1,
            "remarks": "Late entry on 12-Nov (Gate passed at 10:25 PM)"
        },
        {
            "id": "ST103",
            "name": "Rohit Verma",
            "course": "B.Tech ECE",
            "contact": "9745612345",
            "room_number": "102",
            "fee_total": 45000.0,
            "fee_paid": 45000.0,
            "fee_due": 0.0,
            "fee_status": "Paid",
            "meal_pref": "Non-Veg",
            "late_entries": 0,
            "remarks": "Good conduct"
        },
        {
            "id": "ST104",
            "name": "Sneha Das",
            "course": "B.Tech Mechanical",
            "contact": "9654781230",
            "room_number": "103",
            "fee_total": 50000.0,
            "fee_paid": 25000.0,
            "fee_due": 25000.0,
            "fee_status": "Pending",
            "meal_pref": "Veg",
            "late_entries": 2,
            "remarks": "Warned regarding late library return after 10 PM"
        },
        {
            "id": "ST105",
            "name": "Ankit Singh",
            "course": "B.Tech Civil",
            "contact": "9512368740",
            "room_number": "104",
            "fee_total": 40000.0,
            "fee_paid": 40000.0,
            "fee_due": 0.0,
            "fee_status": "Paid",
            "meal_pref": "Non-Veg",
            "late_entries": 0,
            "remarks": "Good conduct"
        }
    ]


def initialize_rooms():
    """
    Returns a dictionary of hostel rooms with capacity, occupants, and floor.
    Ensures capacity constraints are respected during room allocation.
    """
    return {
        "101": {"type": "Double Sharing", "capacity": 2, "occupants": ["ST101", "ST102"], "floor": 1},
        "102": {"type": "Double Sharing", "capacity": 2, "occupants": ["ST103"], "floor": 1},
        "103": {"type": "Single Deluxe",  "capacity": 1, "occupants": ["ST104"], "floor": 1},
        "104": {"type": "Triple Sharing", "capacity": 3, "occupants": ["ST105"], "floor": 1},
        "105": {"type": "Triple Sharing", "capacity": 3, "occupants": [], "floor": 1},
        "201": {"type": "Double Sharing", "capacity": 2, "occupants": [], "floor": 2},
        "202": {"type": "Single Deluxe",  "capacity": 1, "occupants": [], "floor": 2},
        "203": {"type": "Double Sharing", "capacity": 2, "occupants": [], "floor": 2}
    }


def initialize_complaints():
    """
    Returns an initial list of student grievances and maintenance tickets.
    """
    return [
        {
            "id": 1,
            "student_id": "ST102",
            "category": "Plumbing",
            "description": "Geyser heating rod faulty in 1st Floor Washroom",
            "cost_to_fix": 1500.0,
            "status": "Pending"
        },
        {
            "id": 2,
            "student_id": "ST104",
            "category": "Internet",
            "description": "Wi-Fi access point in corridor dropping packets",
            "cost_to_fix": 1200.0,
            "status": "Pending"
        },
        {
            "id": 3,
            "student_id": "ST103",
            "category": "Electrical",
            "description": "Study table tube light flickering",
            "cost_to_fix": 400.0,
            "status": "Resolved"
        }
    ]

# 2. INPUT VALIDATION HELPER FUNCTIONS

def get_valid_integer(prompt, min_val=None, max_val=None):
    """
    Prompts the user for an integer until a valid integer within the optional
    [min_val, max_val] range is entered.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f" [!] Input error: Value must be at least {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f" [!] Input error: Value cannot exceed {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print(" [!] Invalid input! Please enter a valid whole number.")


def get_valid_float(prompt, min_val=0.0):
    """
    Prompts the user for a floating-point number (e.g. for currency/fees).
    """
    while True:
        user_input = input(prompt).strip()
        try:
            val = float(user_input)
            if val < min_val:
                print(f" [!] Input error: Value must be at least {min_val}. Try again.")
                continue
            return val
        except ValueError:
            print(" [!] Invalid input! Please enter a valid decimal number.")


def get_non_empty_string(prompt):
    """
    Ensures the user cannot press Enter on an empty line for important text.
    """
    while True:
        text = input(prompt).strip()
        if len(text) > 0:
            return text
        print(" [!] This field cannot be left blank. Please enter some text.")


def get_valid_phone(prompt):
    """
    Validates that a 10-digit mobile contact number is provided.
    """
    while True:
        phone = input(prompt).strip()
        if len(phone) == 10 and phone.isdigit():
            return phone
        print(" [!] Please enter a valid 10-digit numeric mobile number.")

# 3. LOOKUP & QUERY HELPERS

def find_student_by_id(students, student_id):
    """
    Searches the students list for a student matching the given ID.
    Returns the student dictionary if found, else None.
    """
    target = student_id.strip().upper()
    for student in students:
        if student["id"].upper() == target:
            return student
    return None


def get_vacant_rooms(rooms):
    """
    Returns a list of room numbers that still have capacity for more occupants.
    """
    vacant = []
    for room_no, data in rooms.items():
        if len(data["occupants"]) < data["capacity"]:
            vacant.append(room_no)
    return vacant

# 4. STUDENT & ROOM MANAGEMENT FUNCTIONS (CRUD OPERATIONS)

def add_student(students, rooms):
    """
    Collects student details, checks for duplicate IDs, allocates a vacant room,
    and appends the new record to the students list.
    """
    print("\n" + "=" * 55)
    print("           NEW STUDENT ADMISSION & REGISTRATION")
    print("=" * 55)

    # 1. Unique ID validation
    while True:
        s_id = get_non_empty_string(" Enter Unique Student ID (e.g. ST106) [or '0' to Cancel]: ").upper()
        if s_id == '0':
            print(" [*] Admission cancelled.")
            return
        if find_student_by_id(students, s_id) is not None:
            print(f" [!] Error: Student ID '{s_id}' already exists in system. Please use a unique ID.")
        else:
            break

    # 2. General Details
    name = get_non_empty_string(" Enter Full Name: ")
    course = get_non_empty_string(" Enter Course/Branch (e.g. B.Tech CSE): ")
    contact = get_valid_phone(" Enter 10-Digit Contact Number: ")

    # 3. Meal Preference
    print("\n Meal Preference Options:")
    print("  1. Vegetarian (Veg)")
    print("  2. Non-Vegetarian (Non-Veg)")
    print("  3. Jain / Satvik")
    meal_choice = get_valid_integer(" Select Meal Preference (1-3): ", 1, 3)
    meal_mapping = {1: "Veg", 2: "Non-Veg", 3: "Jain"}
    meal_pref = meal_mapping[meal_choice]

    # 4. Fee Details
    fee_total = get_valid_float(" Enter Semester Hostel Fee (in Rs., e.g. 45000): ", min_val=1000.0)
    fee_paid = get_valid_float(" Enter Amount Paid Initially (in Rs.): ", min_val=0.0)
    if fee_paid > fee_total:
        print(f" [*] Paid amount exceeds total fee. Setting paid amount to total Rs. {fee_total:,.2f}")
        fee_paid = fee_total

    fee_due = fee_total - fee_paid
    fee_status = "Paid" if fee_due == 0.0 else "Pending"

    # 5. Room Allocation
    vacant_rooms = get_vacant_rooms(rooms)
    if not vacant_rooms:
        print("\n [!] WARNING: All hostel rooms are currently full!")
        print("     The student will be admitted to the waiting list without an assigned room.")
        allocated_room = "Waiting List"
    else:
        print("\n Currently Available / Vacant Rooms:")
        print(f" {'Room No':<10} {'Type':<18} {'Floor':<8} {'Capacity':<10} {'Occupied':<10}")
        print("-" * 58)
        for r_no in vacant_rooms:
            r_info = rooms[r_no]
            print(f" {r_no:<10} {r_info['type']:<18} {r_info['floor']:<8} {r_info['capacity']:<10} {len(r_info['occupants']):<10}")

        while True:
            allocated_room = get_non_empty_string("\n Enter Room Number to allocate from list above: ")
            if allocated_room in vacant_rooms:
                rooms[allocated_room]["occupants"].append(s_id)
                break
            else:
                print(f" [!] Invalid room choice or room is full. Choose from: {vacant_rooms}")

    # 6. Build Student Record
    new_student = {
        "id": s_id,
        "name": name,
        "course": course,
        "contact": contact,
        "room_number": allocated_room,
        "fee_total": fee_total,
        "fee_paid": fee_paid,
        "fee_due": fee_due,
        "fee_status": fee_status,
        "meal_pref": meal_pref,
        "late_entries": 0,
        "remarks": "Newly admitted student"
    }

    students.append(new_student)

    print("\n" + "-" * 55)
    print(f" [SUCCESS] Student '{name}' (ID: {s_id}) registered successfully!")
    print(f"           Allocated Room: {allocated_room} | Fees Due: Rs. {fee_due:,.2f}")
    print("-" * 55)


def view_all_students(students):
    """
    Displays all registered students in a formatted tabular structure.
    """
    print("\n" + "=" * 92)
    print("                              HOSTEL STUDENT MASTER DIRECTORY")
    print("=" * 92)

    if not students:
        print(" [!] No student records currently exist in the database.")
        print("=" * 92)
        return

    # Table Header
    print(f" {'ID':<8} {'Name':<18} {'Course':<15} {'Room':<8} {'Meal':<8} {'Due (Rs.)':<12} {'Status':<9} {'Late':<6}")
    print("-" * 92)

    # Table Rows
    for s in students:
        print(f" {s['id']:<8} {s['name'][:17]:<18} {s['course'][:14]:<15} {s['room_number']:<8} "
              f"{s['meal_pref']:<8} {s['fee_due']:<12,.2f} {s['fee_status']:<9} {s['late_entries']:<6}")

    print("-" * 92)
    print(f" Total Registered Students: {len(students)}")
    print("=" * 92)


def search_student(students):
    """
    Offers search options by ID, Name keyword, or Room Number.
    """
    print("\n" + "=" * 45)
    print("           SEARCH STUDENT RECORDS")
    print("=" * 45)
    print(" 1. Search by Student ID")
    print(" 2. Search by Student Name (Keyword match)")
    print(" 3. Search by Room Number")
    print(" 4. Back to Main Menu")
    print("-" * 45)

    choice = get_valid_integer(" Select search method (1-4): ", 1, 4)

    results = []

    if choice == 1:
        query_id = get_non_empty_string(" Enter Student ID to search: ").upper()
        found = find_student_by_id(students, query_id)
        if found:
            results.append(found)
    elif choice == 2:
        query_name = get_non_empty_string(" Enter Name keyword: ").lower()
        for s in students:
            if query_name in s["name"].lower():
                results.append(s)
    elif choice == 3:
        query_room = get_non_empty_string(" Enter Room Number: ")
        for s in students:
            if s["room_number"] == query_room:
                results.append(s)
    elif choice == 4:
        return

    # Display Results
    if not results:
        print("\n [!] No matching student records found.")
    else:
        print(f"\n Found {len(results)} matching record(s):")
        for s in results:
            print("\n " + "-" * 48)
            print(f" Student ID     : {s['id']}")
            print(f" Full Name      : {s['name']}")
            print(f" Course/Branch  : {s['course']}")
            print(f" Contact Mobile : {s['contact']}")
            print(f" Room Number    : {s['room_number']}")
            print(f" Meal Preference: {s['meal_pref']}")
            print(f" Total Fee      : Rs. {s['fee_total']:,.2f}")
            print(f" Fee Paid       : Rs. {s['fee_paid']:,.2f}")
            print(f" Fee Due        : Rs. {s['fee_due']:,.2f} ({s['fee_status']})")
            print(f" Late Entries   : {s['late_entries']} times (after 10 PM)")
            print(f" Remarks        : {s['remarks']}")
            print(" " + "-" * 48)


def update_student(students, rooms):
    """
    Allows updating student contact, course, meal preference, disciplinary remarks,
    or reallocating room without double booking.
    """
    print("\n" + "=" * 50)
    print("             UPDATE STUDENT RECORD")
    print("=" * 50)

    target_id = get_non_empty_string(" Enter Student ID to update (or '0' to Cancel): ").upper()
    if target_id == '0':
        return

    student = find_student_by_id(students, target_id)
    if not student:
        print(f" [!] Student with ID '{target_id}' not found.")
        return

    print(f"\n Selected: {student['name']} (ID: {student['id']}, Current Room: {student['room_number']})")
    print(" 1. Update Contact Mobile Number")
    print(" 2. Update Course/Branch")
    print(" 3. Change Meal Preference")
    print(" 4. Reallocate / Shift Room")
    print(" 5. Update Disciplinary Remarks")
    print(" 6. Cancel")

    ch = get_valid_integer("\n Choose field to update (1-6): ", 1, 6)

    if ch == 1:
        new_phone = get_valid_phone(" Enter new 10-digit phone number: ")
        student["contact"] = new_phone
        print(" [SUCCESS] Contact number updated successfully.")
    elif ch == 2:
        new_course = get_non_empty_string(" Enter new Course/Branch: ")
        student["course"] = new_course
        print(" [SUCCESS] Course updated successfully.")
    elif ch == 3:
        print(" 1. Veg | 2. Non-Veg | 3. Jain")
        m = get_valid_integer(" Choose new meal preference (1-3): ", 1, 3)
        mapping = {1: "Veg", 2: "Non-Veg", 3: "Jain"}
        student["meal_pref"] = mapping[m]
        print(f" [SUCCESS] Meal preference changed to {student['meal_pref']}.")
    elif ch == 4:
        # Reallocate room: remove from old room occupants, assign new vacant room
        old_room = student["room_number"]
        vacant_rooms = get_vacant_rooms(rooms)
        print(f"\n Current Room: {old_room}")
        print(f" Available Vacant Rooms: {vacant_rooms}")

        if not vacant_rooms:
            print(" [!] No vacant rooms available for shifting.")
            return

        new_room = get_non_empty_string(" Enter new Room Number from available list: ")
        if new_room in vacant_rooms:
            # Free up old room if was in one
            if old_room in rooms and target_id in rooms[old_room]["occupants"]:
                rooms[old_room]["occupants"].remove(target_id)
            # Add to new room
            rooms[new_room]["occupants"].append(target_id)
            student["room_number"] = new_room
            print(f" [SUCCESS] Student reallocated from Room {old_room} to Room {new_room}!")
        else:
            print(" [!] Invalid room choice or room is full.")
    elif ch == 5:
        new_rem = get_non_empty_string(" Enter new Disciplinary / Conduct Remark: ")
        student["remarks"] = new_rem
        print(" [SUCCESS] Disciplinary remarks updated.")
    elif ch == 6:
        print(" [*] Update cancelled.")


def delete_student(students, rooms):
    """
    Deletes a student record and frees their bed in their allocated room.
    """
    print("\n" + "=" * 50)
    print("           DELETE / EXPEL STUDENT RECORD")
    print("=" * 50)

    target_id = get_non_empty_string(" Enter Student ID to delete [or '0' to Cancel]: ").upper()
    if target_id == '0':
        return

    student = find_student_by_id(students, target_id)
    if not student:
        print(f" [!] Student with ID '{target_id}' not found.")
        return

    print(f"\n WARNING: You are about to permanently delete record for:")
    print(f" Name: {student['name']} | ID: {student['id']} | Room: {student['room_number']}")
    confirm = input(" Are you sure you want to proceed? (yes/no): ").strip().lower()

    if confirm in ["yes", "y"]:
        # Remove from room occupants list
        room_no = student["room_number"]
        if room_no in rooms and target_id in rooms[room_no]["occupants"]:
            rooms[room_no]["occupants"].remove(target_id)

        # Remove from students list
        students.remove(student)
        print(f" [SUCCESS] Student '{student['name']}' has been removed. Room {room_no} bed is now vacant.")
    else:
        print(" [*] Deletion cancelled.")

# 5. ROOM OCCUPANCY & TRACKING

def view_rooms(rooms):
    """
    Displays all rooms with capacity, occupant IDs, and vacancy status.
    Calculates overall hostel occupancy percentage.
    """
    print("\n" + "=" * 70)
    print("                       HOSTEL ROOM OCCUPANCY REPORT")
    print("=" * 70)

    total_capacity = 0
    total_occupied = 0

    print(f" {'Room':<8} {'Floor':<8} {'Room Type':<18} {'Capacity':<10} {'Occupied':<10} {'Occupants'}")
    print("-" * 70)

    for room_no, data in rooms.items():
        occ_count = len(data["occupants"])
        total_capacity += data["capacity"]
        total_occupied += occ_count

        occupants_str = ", ".join(data["occupants"]) if data["occupants"] else "[VACANT]"
        status_tag = f"{occ_count}/{data['capacity']}"
        if occ_count == data["capacity"]:
            status_tag += " (FULL)"

        print(f" {room_no:<8} {data['floor']:<8} {data['type']:<18} {data['capacity']:<10} {status_tag:<10} {occupants_str}")

    print("-" * 70)
    vacant_beds = total_capacity - total_occupied
    occupancy_pct = (total_occupied / total_capacity * 100) if total_capacity > 0 else 0

    print(f" Total Bed Capacity: {total_capacity} | Occupied Beds: {total_occupied} | Vacant Beds: {vacant_beds}")
    print(f" Overall Hostel Occupancy Rate: {occupancy_pct:.1f}%")
    print("=" * 70)

# 6. FEE MANAGEMENT & DUES AUDIT

def manage_fees(students):
    """
    Provides fee accounting: view defaulters, record payments, and audit summary.
    """
    print("\n" + "=" * 55)
    print("                 HOSTEL FEE MANAGEMENT DESK")
    print("=" * 55)
    print(" 1. View Fee Defaulters (Pending Dues)")
    print(" 2. Collect / Pay Student Fee Installment")
    print(" 3. Fee Collection Summary Report")
    print(" 4. Back to Main Menu")
    print("-" * 55)

    choice = get_valid_integer(" Select an option (1-4): ", 1, 4)

    if choice == 1:
        print("\n" + "-" * 70)
        print("                     STUDENTS WITH PENDING FEES")
        print("-" * 70)
        print(f" {'ID':<8} {'Name':<20} {'Room':<8} {'Total (Rs.)':<14} {'Due (Rs.)':<14}")
        print("-" * 70)
        defaulters = [s for s in students if s["fee_due"] > 0]
        if not defaulters:
            print(" [GOOD NEWS] All registered students have cleared their hostel fees!")
        else:
            for s in defaulters:
                print(f" {s['id']:<8} {s['name'][:19]:<20} {s['room_number']:<8} {s['fee_total']:<14,.2f} {s['fee_due']:<14,.2f}")
        print("-" * 70)

    elif choice == 2:
        s_id = get_non_empty_string("\n Enter Student ID paying fee: ").upper()
        student = find_student_by_id(students, s_id)
        if not student:
            print(f" [!] Student with ID '{s_id}' not found.")
            return

        print(f"\n Student: {student['name']} | Total Fee: Rs. {student['fee_total']:,.2f}")
        print(f" Already Paid: Rs. {student['fee_paid']:,.2f} | Remaining Due: Rs. {student['fee_due']:,.2f}")

        if student["fee_due"] <= 0:
            print(" [*] This student has already cleared all semester dues!")
            return

        payment = get_valid_float(f" Enter Payment Amount (Max Rs. {student['fee_due']:,.2f}): ", min_val=1.0)
        if payment > student["fee_due"]:
            print(f" [*] Entered amount exceeds due. Adjusting payment to exact due: Rs. {student['fee_due']:,.2f}")
            payment = student["fee_due"]

        student["fee_paid"] += payment
        student["fee_due"] -= payment
        if student["fee_due"] == 0.0:
            student["fee_status"] = "Paid"
        #Receipt 
        print("\n" + "-" * 50)
        print("                  FEE PAYMENT RECEIPT")
        print("-" * 50)
        print(f" Student Name : {student['name']} ({student['id']})")
        print(f" Amount Paid  : Rs. {payment:,.2f}")
        print(f" Remaining Due: Rs. {student['fee_due']:,.2f}")
        print(f" Fee Status   : {student['fee_status']}")
        print("-" * 50)

    elif choice == 3:
        total_billed = sum(s["fee_total"] for s in students)
        total_collected = sum(s["fee_paid"] for s in students)
        total_outstanding = sum(s["fee_due"] for s in students)

        print("\n" + "=" * 50)
        print("             HOSTEL FINANCIAL DUES AUDIT")
        print("=" * 50)
        print(f" Total Students Enrolled : {len(students)}")
        print(f" Total Hostel Fees Billed: Rs. {total_billed:,.2f}")
        print(f" Total Fees Collected    : Rs. {total_collected:,.2f}")
        print(f" Total Outstanding Dues  : Rs. {total_outstanding:,.2f}")
        collection_rate = (total_collected / total_billed * 100) if total_billed > 0 else 0
        print(f" Fee Collection Progress : {collection_rate:.1f}%")
        print("=" * 50)

# 7. NIGHT PATROL & LATE ENTRY REGISTER (AFTER 10 PM)

def record_late_entry(students):
    """
    Wardens use this function to log students returning past 10:00 PM curfew.
    Repeated late entries trigger disciplinary alerts.
    """
    print("\n" + "=" * 55)
    print("      NIGHT PATROL: LATE ENTRY LOGGING (AFTER 10 PM)")
    print("=" * 55)

    s_id = get_non_empty_string(" Enter Student ID returning late (or '0' to Cancel): ").upper()
    if s_id == '0':
        return

    student = find_student_by_id(students, s_id)
    if not student:
        print(f" [!] Student with ID '{s_id}' not found.")
        return

    time_str = get_non_empty_string(" Enter Arrival Time (e.g. 10:35 PM, 11:15 PM): ")
    reason = get_non_empty_string(" Enter Stated Reason (e.g. Library, Lab work, Traffic): ")

    student["late_entries"] += 1
    new_remark = f"Late entry logged at {time_str} (Reason: {reason})"
    student["remarks"] = new_remark

    print("\n" + "-" * 55)
    print(f" [LOGGED] Late arrival recorded for {student['name']}.")
    print(f" Total Late Entries this semester: {student['late_entries']}")

    # Disciplinary Escalation Threshold
    if student["late_entries"] >= 3:
        print(" [WARNING] Escalation! Student has 3 or more late entries.")
        print("           Action: Mandatory warning letter issued to local guardian.")
        student["remarks"] += " | ESCALATED TO CHIEF WARDEN & GUARDIAN"
    elif student["late_entries"] == 2:
        print(" [CAUTION] Second late entry recorded. One more will prompt guardian call.")
    print("-" * 55)


def view_late_entry_register(students):
    """
    Displays the log of all students with late entry infractions.
    """
    print("\n" + "=" * 75)
    print("                     HOSTEL LATE ENTRY REGISTER (AFTER 10 PM)")
    print("=" * 75)
    print(f" {'ID':<8} {'Name':<18} {'Room':<8} {'Late Count':<12} {'Latest Remarks'}")
    print("-" * 75)

    flagged = [s for s in students if s["late_entries"] > 0]
    if not flagged:
        print(" [EXCELLENT] No students have late entry infractions on record.")
    else:
        for s in flagged:
            print(f" {s['id']:<8} {s['name'][:17]:<18} {s['room_number']:<8} {s['late_entries']:<12} {s['remarks']}")
    print("-" * 75)
