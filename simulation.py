
import random
from hostel_data import get_valid_integer, get_valid_float, get_non_empty_string

# 1. SIMULATION STATE INITIALIZATION

def initialize_game_state():
    """
    Initializes the state dictionary for the 7-day Warden Management Challenge.
    """
    return {
        "day": 1,
        "max_days": 7,              # 7-day challenge for the semester simulation
        "budget": 50000.0,          # Starting reserve funds in Rupees 
        "satisfaction": 78,         # Starting satisfaction index (Scale: 0 to 100)
        "total_revenue": 0.0,
        "total_expenses": 0.0,
        "game_over": False,
        "game_result": "IN_PROGRESS",  # "IN_PROGRESS", "WON", "LOST_BUDGET", "LOST_SATISFACTION"
        "daily_logs": []
    }

# 2. STATUS HUD & SATISFACTION METER

def draw_satisfaction_bar(score, total_blocks=10):
    """
    Generates a visual ASCII satisfaction progress bar.
    """
    clamped_score = max(0, min(100, score))
    filled_blocks = int((clamped_score / 100) * total_blocks)
    empty_blocks = total_blocks - filled_blocks
    bar = "█" * filled_blocks + "░" * empty_blocks
    return f"[{bar}] {clamped_score}%"


def display_warden_hud(game_state, student_count):
    """
    Displays the top Heads-Up Display (HUD) showing current day, budget, and morale.
    """
    day = game_state["day"]
    max_days = game_state["max_days"]
    budget = game_state["budget"]
    sat = game_state["satisfaction"]

    # Mood text
    if sat >= 80:
        mood = "THRIVING (Students very happy)"
    elif sat >= 60:
        mood = "SATISFACTORY (Normal campus mood)"
    elif sat >= 40:
        mood = "UNREST (Grumbling & Complaints)"
    else:
        mood = "CRITICAL (Protest imminent!)"

    print("\n" + "=" * 76)
    print(f"  HOSTEL WARDEN DASHBOARD | DAY {day} of {max_days}")
    print("=" * 76)
    print(f"  Current Treasury Budget : Rs. {budget:,.2f}")
    print(f"  Student Satisfaction    : {draw_satisfaction_bar(sat)} -> {mood}")
    print(f"  Hostel Boarders Count   : {student_count} registered students")
    print("=" * 76)


def update_satisfaction(game_state, delta, reason=""):
    """
    Safely adjusts the satisfaction score within the 0 to 100 boundaries
    and informs the player of the change.
    """
    old_sat = game_state["satisfaction"]
    new_sat = old_sat + delta
    # Clamp between 0 and 100
    if new_sat > 100:
        new_sat = 100
    elif new_sat < 0:
        new_sat = 0

    game_state["satisfaction"] = new_sat
    sign = "+" if delta >= 0 else ""
    if reason:
        print(f" [*] Student Satisfaction changed: {sign}{delta}% ({reason}) -> Current: {new_sat}%")
    else:
        print(f" [*] Student Satisfaction changed: {sign}{delta}% -> Current: {new_sat}%")

# 3. DAILY SIMULATION PHASES

def phase_mess_decision(game_state, student_count):
    """
    Phase 1: Morning Mess & Food Quality Selection.
    Food quality directly impacts daily expenditure and student satisfaction.
    """
    print("\n" + "-" * 60)
    print(" [PHASE 1] MORNING MESS & MEAL MENU SELECTION")
    print("-" * 60)
    print(f" As Warden, you must approve today's 3-meal menu for {student_count} students:\n")

    cost_opt1 = 70.0 * student_count
    cost_opt2 = 140.0 * student_count
    cost_opt3 = 230.0 * student_count

    print(f" 1. Budget Austere Meal (Dal, Rice, Plain Roti)")
    print(f"    -> Daily Cost: Rs. {cost_opt1:,.2f} (Rs. 70/student) | Impact: -5% Satisfaction")
    print(f" 2. Balanced Nutritious Meal (Dal Makhani, Seasonal Sabzi, Paneer/Egg, Curd)")
    print(f"    -> Daily Cost: Rs. {cost_opt2:,.2f} (Rs. 140/student) | Impact: +2% Satisfaction")
    print(f" 3. Deluxe Grand Feast (Shahi Paneer, Biryani, Naan, Gulab Jamun/Ice Cream)")
    print(f"    -> Daily Cost: Rs. {cost_opt3:,.2f} (Rs. 230/student) | Impact: +7% Satisfaction")

    choice = get_valid_integer("\n Select Mess Plan for today (1-3): ", 1, 3)

    if choice == 1:
        chosen_cost = cost_opt1
        update_satisfaction(game_state, -5, "Students felt the food was too plain")
        menu_name = "Budget Austere Menu"
    elif choice == 2:
        chosen_cost = cost_opt2
        update_satisfaction(game_state, +2, "Students enjoyed a wholesome meal")
        menu_name = "Standard Balanced Menu"
    else:
        chosen_cost = cost_opt3
        update_satisfaction(game_state, +7, "Special feast cheered up the entire hostel")
        menu_name = "Deluxe Feast Menu"

    game_state["budget"] -= chosen_cost
    game_state["total_expenses"] += chosen_cost
    print(f" [FINANCE] Paid Rs. {chosen_cost:,.2f} to the hostel mess vendor.")
    return chosen_cost, menu_name


def phase_maintenance_event(game_state, day_number):
    """
    Phase 2: Afternoon Campus Maintenance Crisis / Event.
    Presents realistic hostel dilemmas with budget vs satisfaction trade-offs.
    """
    print("\n" + "-" * 60)
    print(" [PHASE 2] AFTERNOON CAMPUS MAINTENANCE DILEMMA")
    print("-" * 60)

    # 7 curated realistic events matching 1st semester college life
    events = [
        {
            "title": "Wi-Fi Router Meltdown During Lab Submissions",
            "desc": "The primary optical fiber router for Block A blew its power supply right before submission deadline!",
            "opt1_text": "Emergency express technician call & high-speed router replacement",
            "opt1_cost": 3200.0, "opt1_sat": +5,
            "opt2_text": "Apply temporary tape and reset old slow backup router",
            "opt2_cost": 800.0, "opt2_sat": -2,
            "opt3_text": "Advise students to use mobile hotspot until next week",
            "opt3_cost": 0.0, "opt3_sat": -8
        },
        {
            "title": "Mess RO Water Purifier Malfunction",
            "desc": "The main drinking water purifier in the dining hall is dispensing cloudy water with high TDS.",
            "opt1_text": "Install brand new certified industrial multi-stage RO filter",
            "opt1_cost": 4500.0, "opt1_sat": +6,
            "opt2_text": "Backwash and chemical flush the old candle filters",
            "opt2_cost": 1200.0, "opt2_sat": +1,
            "opt3_text": "Paste a notice: 'Drink tap water at own risk'",
            "opt3_cost": 0.0, "opt3_sat": -12
        },
        {
            "title": "Winter Geyser Element Burnout in Washrooms",
            "desc": "With morning temperatures dropping, both electric water heaters on the 1st floor have tripped.",
            "opt1_text": "Call electrical contractor for immediate heavy-duty geyser heating coils",
            "opt1_cost": 3800.0, "opt1_sat": +6,
            "opt2_text": "Fix one unit only; ask students to share the common washroom",
            "opt2_cost": 1500.0, "opt2_sat": -1,
            "opt3_text": "Postpone repair: 'Cold baths build immunity and discipline!'",
            "opt3_cost": 0.0, "opt3_sat": -10
        },
        {
            "title": "Sports & Recreation Equipment Request",
            "desc": "The hostel sports secretary brings a petition requesting new Table Tennis rackets and gym weights.",
            "opt1_text": "Approve purchase of premium TT kit, badminton set, and gym dumbbells",
            "opt1_cost": 5000.0, "opt1_sat": +9,
            "opt2_text": "Approve modest budget for 2 badminton rackets and shuttlecocks only",
            "opt2_cost": 1500.0, "opt2_sat": +3,
            "opt3_text": "Reject petition: 'Focus on your upcoming mid-semester examinations!'",
            "opt3_cost": 0.0, "opt3_sat": -5
        },
        {
            "title": "Sanitation, Pest Control & Mosquito Fumigation Drive",
            "desc": "Dengue alert issued by the municipal health department. Stagnant rainwater seen near block.",
            "opt1_text": "Hire professional pest control agency for complete chemical fogging & drains cleaning",
            "opt1_cost": 3000.0, "opt1_sat": +5,
            "opt2_text": "Purchase manual spray cans and have hostel sweepers spray outdoors",
            "opt2_cost": 900.0, "opt2_sat": +2,
            "opt3_text": "Do nothing; ask students to keep their window mosquito nets shut",
            "opt3_cost": 0.0, "opt3_sat": -6
        },
        {
            "title": "Study Room Air Conditioning & Inverter Battery Crisis",
            "desc": "Frequent power cuts during evening study hours are plunging the hostel reading room into darkness.",
            "opt1_text": "Purchase two high-capacity tubular inverter batteries with warranty",
            "opt1_cost": 6000.0, "opt1_sat": +8,
            "opt2_text": "Refill battery acid and install rechargeable LED emergency lanterns",
            "opt2_cost": 1800.0, "opt2_sat": +2,
            "opt3_text": "Advise students to study under solar streetlights or carry candles",
            "opt3_cost": 0.0, "opt3_sat": -9
        },
        {
            "title": "Hostel Weekend Cultural Eve & Open Mic Night",
            "desc": "Students request permission and small sponsorship to organize a weekend music and open-mic night.",
            "opt1_text": "Sponsor sound system rental, stage lights, and evening samosa snacks",
            "opt1_cost": 4200.0, "opt1_sat": +10,
            "opt2_text": "Grant venue permission in courtyard with hostel amplifier only (no snacks)",
            "opt2_cost": 500.0, "opt2_sat": +4,
            "opt3_text": "Deny permission to preserve strict silent hours",
            "opt3_cost": 0.0, "opt3_sat": -6
        }
    ]

    # Select event based on day index
    event = events[(day_number - 1) % len(events)]

    print(f" EVENT: {event['title']}")
    print(f" {event['desc']}\n")
    print(f" 1. [Proactive Response] {event['opt1_text']}")
    print(f"    -> Cost: Rs. {event['opt1_cost']:,.2f} | Impact: +{event['opt1_sat']}% Satisfaction")
    print(f" 2. [Budget Compromise]  {event['opt2_text']}")
    sign2 = "+" if event['opt2_sat'] >= 0 else ""
    print(f"    -> Cost: Rs. {event['opt2_cost']:,.2f} | Impact: {sign2}{event['opt2_sat']}% Satisfaction")
    print(f" 3. [Do Nothing]         {event['opt3_text']}")
    print(f"    -> Cost: Rs. 0.00 | Impact: {event['opt3_sat']}% Satisfaction")

    choice = get_valid_integer("\n Select your administrative action (1-3): ", 1, 3)

    if choice == 1:
        cost = event["opt1_cost"]
        update_satisfaction(game_state, event["opt1_sat"], "Effective maintenance resolution")
    elif choice == 2:
        cost = event["opt2_cost"]
        update_satisfaction(game_state, event["opt2_sat"], "Budget patch-up applied")
    else:
        cost = 0.0
        update_satisfaction(game_state, event["opt3_sat"], "Deferred maintenance caused frustration")

    game_state["budget"] -= cost
    game_state["total_expenses"] += cost
    print(f" [FINANCE] Maintenance expense incurred: Rs. {cost:,.2f}")
    return cost, event["title"]


def phase_resolve_complaints(game_state, complaints):
    """
    Phase 3: Student Grievance Resolution.
    Warden can inspect pending tickets and pay to clear them for bonus satisfaction.
    """
    print("\n" + "-" * 60)
    print(" [PHASE 3] STUDENT GRIEVANCE & COMPLAINTS DESK")
    print("-" * 60)

    pending = [c for c in complaints if c["status"] == "Pending"]

    if not pending:
        print(" [ALL CLEAR] No pending student complaints in the register today!")
        update_satisfaction(game_state, +2, "Clean complaint log boost")
        return 0.0

    print(f" Found {len(pending)} pending student complaint(s):")
    print(f" {'ID':<5} {'Student':<9} {'Category':<12} {'Cost (Rs.)':<12} {'Issue'}")
    print("-" * 60)
    for c in pending:
        print(f" #{c['id']:<4} {c['student_id']:<9} {c['category']:<12} {c['cost_to_fix']:<12,.2f} {c['description']}")
    print("-" * 60)

    print("\n As Warden, would you like to:")
    print(" 1. Resolve all pending complaints today (Spend funds for maximum morale)")
    print(" 2. Resolve one specific high-priority ticket")
    print(" 3. Postpone complaint resolution to tomorrow")

    choice = get_valid_integer(" Select choice (1-3): ", 1, 3)
    spent = 0.0

    if choice == 1:
        total_fix_cost = sum(c["cost_to_fix"] for c in pending)
        print(f" Total cost to clear all {len(pending)} complaints: Rs. {total_fix_cost:,.2f}")
        confirm = input(" Proceed with payment from hostel funds? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            game_state["budget"] -= total_fix_cost
            game_state["total_expenses"] += total_fix_cost
            spent = total_fix_cost
            for c in pending:
                c["status"] = "Resolved"
            boost = len(pending) * 4
            update_satisfaction(game_state, boost, "All pending complaints resolved!")
        else:
            print(" [*] Action cancelled.")

    elif choice == 2:
        ticket_id = get_valid_integer(" Enter Complaint ID to resolve: ")
        target = None
        for c in pending:
            if c["id"] == ticket_id:
                target = c
                break
        if target:
            if game_state["budget"] >= target["cost_to_fix"]:
                game_state["budget"] -= target["cost_to_fix"]
                game_state["total_expenses"] += target["cost_to_fix"]
                spent = target["cost_to_fix"]
                target["status"] = "Resolved"
                print(f" [SUCCESS] Complaint #{target['id']} resolved for Rs. {target['cost_to_fix']:,.2f}!")
                update_satisfaction(game_state, +5, f"Resolved ticket #{target['id']}")
            else:
                print(" [!] Insufficient budget to resolve this ticket.")
        else:
            print(f" [!] Pending complaint #{ticket_id} not found.")

    elif choice == 3:
        print(" [*] Complaints kept pending.")
        update_satisfaction(game_state, -2, "Unresolved complaints lingering")

    return spent


def phase_night_discipline(game_state, students):
    """
    Phase 4: Late-Night Patrol & Discipline Enforcement (Curfew at 10:00 PM).
    Simulates curfew gate-keeping, anti-ragging patrols, and noise complaints.
    """
    print("\n" + "-" * 60)
    print(" [PHASE 4] NIGHT PATROL & HOSTEL DISCIPLINE (POST 10:00 PM)")
    print("-" * 60)

    # Scenarios for nighttime wardens
    scenarios = [
        "LATE_ENTRY",
        "NOISE_DISTURBANCE",
        "ANTI_RAGGING_INSPECTION"
    ]
    # Pick one scenario randomly or cyclically
    scenario = random.choice(scenarios)

    if scenario == "LATE_ENTRY":
        print(" [ALERT] 11:15 PM - Two students arrive at the main hostel security gate")
        print("         well past the mandatory 10:00 PM curfew claiming heavy city traffic.\n")
        print(" 1. Strict Gate Policy: Lock the gate, mark entry register, and call local guardians.")
        print("    -> Impact: High discipline, -3% Satisfaction (students find it overly strict)")
        print(" 2. Spot Disciplinary Fine: Collect Rs. 250 late-fee per student into hostel treasury.")
        print("    -> Impact: +Rs. 500.00 to Budget, 0% Satisfaction change")
        print(" 3. Empathetic Warning: Let them enter with a formal verbal reprimand.")
        print("    -> Impact: +2% Satisfaction (students appreciate leniency)")

        ch = get_valid_integer(" Choose disciplinary action (1-3): ", 1, 3)
        if ch == 1:
            update_satisfaction(game_state, -3, "Strict night curfew enforcement")
        elif ch == 2:
            game_state["budget"] += 500.0
            game_state["total_revenue"] += 500.0
            print(" [FINANCE] Collected Rs. 500.00 in late disciplinary fines.")
        else:
            update_satisfaction(game_state, +2, "Leniency appreciated by students")

    elif scenario == "NOISE_DISTURBANCE":
        print(" [ALERT] 11:45 PM - Room 102 is blasting bass music celebrating a birthday")
        print("         during pre-exam quiet hours, provoking calls from neighboring rooms.\n")
        print(" 1. Confiscate Bluetooth speakers and levy Rs. 500 nuisance fine.")
        print("    -> Impact: +Rs. 500.00 to Budget, +2% Satisfaction (silent environment restored)")
        print(" 2. Personally visit room and politely instruct students to use earphones.")
        print("    -> Impact: +4% Satisfaction (friendly warden relationship)")
        print(" 3. Ignore the noise and let them celebrate.")
        print("    -> Impact: -5% Satisfaction (studious boarders irritated)")

        ch = get_valid_integer(" Choose disciplinary action (1-3): ", 1, 3)
        if ch == 1:
            game_state["budget"] += 500.0
            game_state["total_revenue"] += 500.0
            update_satisfaction(game_state, +2, "Quiet study hours restored")
        elif ch == 2:
            update_satisfaction(game_state, +4, "Gentle and respectful intervention")
        else:
            update_satisfaction(game_state, -5, "Noise disrupted sleep for studious students")

    elif scenario == "ANTI_RAGGING_INSPECTION":
        print(" [MANDATORY] 10:30 PM - Conducting routine surprise Anti-Ragging squad patrol")
        print("             across 1st and 2nd floor corridors as per Supreme Court / UGC guidelines.\n")
        print(" 1. Comprehensive Corridor Walkthrough with floor prefects (Provide tea/coffee to night guards).")
        print("    -> Cost: Rs. 600.00 | Impact: +6% Satisfaction (Junior students feel secure and safe)")
        print(" 2. Quick 5-minute visual check through corridor cameras.")
        print("    -> Cost: Rs. 0.00 | Impact: +1% Satisfaction")

        ch = get_valid_integer(" Choose inspection approach (1-2): ", 1, 2)
        if ch == 1:
            game_state["budget"] -= 600.0
            game_state["total_expenses"] += 600.0
            update_satisfaction(game_state, +6, "Safe and secure anti-ragging atmosphere")
        else:
            update_satisfaction(game_state, +1, "Basic surveillance check complete")

# 4. DAILY FINANCIAL SETTLEMENT & REVENUE

def phase_financial_settlement(game_state, student_count):
    """
    Phase 5: Night Accounting & Daily Fixed Overheads.
    Collects daily operational contribution from students and deducts overheads
    (security guard payroll, sanitization, electrical base bills).
    """
    print("\n" + "-" * 60)
    print(" [PHASE 5] NIGHT FINANCIAL RECONCILIATION & REVENUE")
    print("-" * 60)

    # Fixed daily overheads: Security, Housekeeping, Utilities
    fixed_overhead = 1200.0
    # Daily hostel fee amortization / incoming payments from boarders
    daily_revenue = 650.0 * student_count

    game_state["budget"] += daily_revenue
    game_state["budget"] -= fixed_overhead
    game_state["total_revenue"] += daily_revenue
    game_state["total_expenses"] += fixed_overhead

    print(f" Daily Hostel Dues Collected from {student_count} boarders: +Rs. {daily_revenue:,.2f}")
    print(f" Fixed Daily Operations (Sanitization & Guards) : -Rs. {fixed_overhead:,.2f}")
    net_daily = daily_revenue - fixed_overhead
    sign = "+" if net_daily >= 0 else ""
    print(f" Net Daily Operational Cashflow                 : {sign}Rs. {net_daily:,.2f}")
    print(f" Ending Day Treasury Balance                    : Rs. {game_state['budget']:,.2f}")

# 5. MAIN SIMULATION CONTROLLER (RUN 1 DAY)

def run_daily_simulation(game_state, students, rooms, complaints):
    """
    Executes one full turn (1 day) of the hostel warden simulation.
    Takes the player through the 5 phases, updates game state, logs progress,
    and checks win/lose conditions.
    """
    current_day = game_state["day"]
    max_days = game_state["max_days"]
    student_count = len(students)

    display_warden_hud(game_state, student_count)

    print(f"\n >>> STARTING HOSTEL OPERATIONS FOR DAY {current_day} OF {max_days} <<<")

    # Starting snapshot for daily log
    start_budget = game_state["budget"]
    start_sat = game_state["satisfaction"]

    # Phase 1: Mess
    mess_spent, menu_name = phase_mess_decision(game_state, student_count)

    # Phase 2: Maintenance Dilemma
    maint_spent, event_title = phase_maintenance_event(game_state, current_day)

    # Phase 3: Complaints
    complaints_spent = phase_resolve_complaints(game_state, complaints)

    # Phase 4: Night Discipline
    phase_night_discipline(game_state, students)

    # Phase 5: Finance Settlement
    phase_financial_settlement(game_state, student_count)

    # Compile Daily Log
    end_budget = game_state["budget"]
    end_sat = game_state["satisfaction"]

    log_entry = {
        "day": current_day,
        "menu": menu_name,
        "event": event_title,
        "net_funds_change": end_budget - start_budget,
        "closing_budget": end_budget,
        "closing_satisfaction": end_sat
    }
    game_state["daily_logs"].append(log_entry)

    print("\n" + "=" * 60)
    print(f"           DAY {current_day} DEBRIEFING COMPLETE")
    print("=" * 60)
    print(f" Final Treasury Balance: Rs. {end_budget:,.2f}")
    print(f" Final Satisfaction    : {draw_satisfaction_bar(end_sat)}")

    # Advance day counter
    game_state["day"] += 1

    # Check Game Status
    is_over, result, msg = check_game_status(game_state)
    if is_over:
        game_state["game_over"] = True
        game_state["game_result"] = result
        print("\n" + "*" * 65)
        print(f" [GAME OVER] {msg}")
        print("*" * 65)
    else:
        print(f" Tomorrow: Advance to Day {game_state['day']} of {max_days}.")

# 6. WIN / LOSS & STATUS VERIFICATION

def check_game_status(game_state):
    """
    Checks whether the warden has won, lost, or is still managing.
    Win Condition : Survived max_days with Budget > 0 and Satisfaction >= 70
    Loss Condition 1: Budget dropped to 0 or below (Bankrupt)
    Loss Condition 2: Satisfaction dropped below 40 (Student Protest/Strike)
    """
    budget = game_state["budget"]
    sat = game_state["satisfaction"]
    day = game_state["day"]
    max_days = game_state["max_days"]

    # Condition 1: Bankruptcy
    if budget <= 0.0:
        return True, "LOST_BUDGET", "BANKRUPT! The hostel ran out of funds to pay power, water, and vendor bills."

    # Condition 2: Student Rebellion
    if sat < 40:
        return True, "LOST_SATISFACTION", "STUDENT STRIKE! Boarders launched a massive dharna demanding a new warden!"

    # Condition 3: Completed challenge duration
    if day > max_days:
        if sat >= 70:
            return True, "WON", "VICTORY! You won the 'Best Hostel Administration Award'! Budget preserved and students happy!"
        else:
            return True, "SURVIVED_POOR", "SURVIVED: You kept the hostel running, but satisfaction finished below the 70% excellence benchmark."

    return False, "IN_PROGRESS", "Challenge Ongoing."


def view_audit_report(game_state):
    """
    Prints a detailed historical log of daily decisions, budget shifts, and satisfaction.
    """
    print("\n" + "=" * 75)
    print("                      HOSTEL SIMULATION AUDIT REPORT")
    print("=" * 75)
    print(f" Current Challenge Status: {game_state['game_result']}")
    print(f" Total Revenue Generated : Rs. {game_state['total_revenue']:,.2f}")
    print(f" Total Operational Spend : Rs. {game_state['total_expenses']:,.2f}")
    net = game_state['total_revenue'] - game_state['total_expenses']
    print(f" Net Treasury Position   : Rs. {net:,.2f}")
    print(f" Current Satisfaction    : {draw_satisfaction_bar(game_state['satisfaction'])}")
    print("-" * 75)

    if not game_state["daily_logs"]:
        print(" [!] No simulation rounds have been executed yet.")
    else:
        print(f" {'Day':<5} {'Mess Menu Plan':<22} {'Closing Budget':<18} {'Satisfaction'}")
        print("-" * 75)
        for log in game_state["daily_logs"]:
            print(f" {log['day']:<5} {log['menu'][:20]:<22} Rs. {log['closing_budget']:<14,.2f} {draw_satisfaction_bar(log['closing_satisfaction'])}")

    print("=" * 75)
