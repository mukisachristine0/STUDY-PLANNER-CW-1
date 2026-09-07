# Smart Study Planner

import os

DATA_FILE = "study_log.txt"


def classify_session(duration):
    # Decide if a session is Short, Medium or Long.
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def load_sessions():
    sessions = []

    if not os.path.exists(DATA_FILE):
        return sessions  # first run, no file yet

    with open(DATA_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            parts = line.split("|")
            if len(parts) != 4:
                continue  # skip a bad line instead of crashing

            subject, topic, date, duration_text = parts
            try:
                duration = float(duration_text)
            except ValueError:
                continue

            session = {
                "subject": subject,
                "topic": topic,
                "date": date,
                "duration": duration,
            }
            sessions.append(session)

    return sessions


def save_sessions(sessions):
    with open(DATA_FILE, "w") as file:
        for session in sessions:
            line = session["subject"] + "|" + session["topic"] + "|" + session["date"] + "|" + str(session["duration"])
            file.write(line + "\n")


def get_positive_duration():
    while True:
        text = input("Duration in minutes: ")
        try:
            duration = float(text)
        except ValueError:
            print("Please enter a number.")
            continue
        if duration <= 0:
            print("Duration must be greater than zero.")
            continue
        return duration


def add_session(sessions):
    print("\nAdd a Study Session")
    subject = input("Subject: ")
    topic = input("Topic covered: ")
    date = input("Date or day: ")
    duration = get_positive_duration()

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)

    classification = classify_session(duration)
    print(f"Session saved: {subject} - {topic} ({duration:.0f} min, {classification})")


def view_sessions(sessions):
    print("\nAll Study Sessions")
    if len(sessions) == 0:
        print("No study sessions have been logged yet.")
        return

    print(f"{'No.':<4}{'Subject':<15} {'Topic':<22} {'Duration':<9} {'Type':<8}")

    count = 1
    for session in sessions:
        classification = classify_session(session["duration"])
        duration_text = f"{session['duration']:.0f} min"
        print(f"{count:<4}{session['subject']:<15} {session['topic']:<22} {duration_text:<9} {classification:<8}")
        count += 1


def search_by_subject(sessions):
    print("\nSearch Sessions by Subject")
    subject_to_find = input("Enter subject to search for: ")

    matches = []
    for session in sessions:
        if session["subject"].lower() == subject_to_find.lower():
            matches.append(session)

    if len(matches) == 0:
        print(f"No sessions found for subject '{subject_to_find}'.")
        return

    print(f"{'No.':<4}{'Topic':<22} {'Duration':<9} {'Type':<8}")

    total_minutes = 0
    count = 1
    for session in matches:
        classification = classify_session(session["duration"])
        duration_text = f"{session['duration']:.0f} min"
        print(f"{count:<4}{session['topic']:<22} {duration_text:<9} {classification:<8}")
        total_minutes += session["duration"]
        count += 1

    print(f"Total time spent on {subject_to_find}: {total_minutes:.0f} minutes ({total_minutes / 60:.2f} hours)")


def study_statistics(sessions):
    print("\nStudy Statistics")
    if len(sessions) == 0:
        print("No sessions logged yet.")
        return

    total_minutes = 0
    for session in sessions:
        total_minutes += session["duration"]
    print(f"Total time studied overall: {total_minutes:.0f} minutes ({total_minutes / 60:.2f} hours)")

    # add up the total time for each subject
    subject_totals = {}
    for session in sessions:
        subject = session["subject"]
        if subject in subject_totals:
            subject_totals[subject] += session["duration"]
        else:
            subject_totals[subject] = session["duration"]

    print("\nTime studied per subject:")
    for subject in subject_totals:
        minutes = subject_totals[subject]
        print(f"  {subject:<15}{minutes:.0f} min ({minutes / 60:.2f} hrs)")

    # find the subject with the least total time
    weakest_subject = None
    lowest_minutes = None
    for subject in subject_totals:
        minutes = subject_totals[subject]
        if lowest_minutes is None or minutes < lowest_minutes:
            weakest_subject = subject
            lowest_minutes = minutes
    print(f"\nWeakest area: {weakest_subject} ({lowest_minutes:.0f} min)")

    # find the longest single session
    longest_session = sessions[0]
    for session in sessions:
        if session["duration"] > longest_session["duration"]:
            longest_session = session
    print(f"Longest session: {longest_session['subject']} - {longest_session['topic']} "
          f"({longest_session['duration']:.0f} min, {classify_session(longest_session['duration'])})")


def display_menu():
    print("\nSMART STUDY PLANNER")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")


def main():
    sessions = load_sessions()

    print("Welcome to the Smart Study Planner!")
    if len(sessions) > 0:
        print(f"Loaded {len(sessions)} saved session(s).")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Sessions saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
