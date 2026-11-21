import json
from datetime import datetime, timedelta
from pathlib import Path

# ==========================================
# MEETING SCHEDULER ASSISTANT
# Three-Function Python Agent
# ==========================================

DATE_FORMAT = "%Y-%m-%d %H:%M"
MEETING_DURATION = 60  # Minutes
SLOTS_PER_PERSON = 10
TIMEZONE = "Asia/Kolkata"


# FUNCTION 1: COLLECT PREFERRED TIMES

def collect_preferred_times():
    print("\n===== MEETING SCHEDULER AGENT =====")

    while True:
        try:
            count = int(input("Number of participants: "))
            if count >= 2:
                break
            print("Enter at least 2 participants.")
        except ValueError:
            print("Please enter a valid number.")

    participants = {}

    for i in range(count):
        while True:
            name = input(
                f"\nEnter participant {i + 1} name: "
            ).strip()

            if name and name not in participants:
                break

            print("Name must be unique and non-empty.")

        print(f"\nEnter 10 preferred times for {name}")
        print("Format: YYYY-MM-DD HH:MM")
        print("Example: 2026-11-05 10:00")
        print("Timezone: Asia/Kolkata")
        print("Each slot represents a 60-minute meeting.")

        preferred_times = []

        while len(preferred_times) < SLOTS_PER_PERSON:
            slot_text = input(
                f"Slot {len(preferred_times) + 1}: "
            ).strip()

            try:
                slot = datetime.strptime(
                    slot_text, DATE_FORMAT
                )

                if slot <= datetime.now():
                    print("Enter a future date and time.")
                    continue

                if slot in preferred_times:
                    print("Duplicate slot. Try another.")
                    continue

                preferred_times.append(slot)

            except ValueError:
                print("Invalid format. Try again.")

        participants[name] = preferred_times

        print(f"Saved 10 preferred times for {name}.")

    return participants


# FUNCTION 2: FIND COMMON AVAILABLE SLOTS

def find_common_slots(participants):
    print("\n===== CHECKING COMMON SLOTS =====")

    all_availability = [
        set(times)
        for times in participants.values()
    ]

    common_slots = set.intersection(
        *all_availability
    )

    common_slots = sorted(common_slots)

    if common_slots:
        print("\nCommon available slots found:")

        for index, slot in enumerate(
            common_slots, start=1
        ):
            print(
                f"{index}. "
                f"{slot.strftime(DATE_FORMAT)}"
            )
    else:
        print("\nNo common available slots found.")
        print("Ask participants for new preferences.")

    return common_slots


# FUNCTION 3: SCHEDULE THE MEETING

def schedule_meeting(common_slots, participants):
    print("\n===== SCHEDULE MEETING =====")

    if not common_slots:
        print("Meeting cannot be scheduled.")
        return None

    meeting_title = input(
        "Enter meeting title: "
    ).strip()

    if not meeting_title:
        meeting_title = "Team Meeting"

    # Automatically choose earliest common slot
    start_time = common_slots[0]

    end_time = start_time + timedelta(
        minutes=MEETING_DURATION
    )

    meeting = {
        "title": meeting_title,
        "date": start_time.strftime("%Y-%m-%d"),
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
        "duration_minutes": MEETING_DURATION,
        "timezone": TIMEZONE,
        "participants": list(participants.keys()),
        "status": "Scheduled"
    }

    # Save meeting information to JSON
    file_path = Path("scheduled_meetings.json")

    meetings = []

    if file_path.exists():
        try:
            with file_path.open(
                "r", encoding="utf-8"
            ) as file:
                saved_data = json.load(file)

                if isinstance(saved_data, list):
                    meetings = saved_data

        except (json.JSONDecodeError, OSError):
            print("Could not read previous meetings.")
            print("Starting a new local schedule.")

    meetings.append(meeting)

    with file_path.open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(
            meetings,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n========== SUCCESS ==========")
    print("Meeting successfully scheduled!")
    print(f"Title: {meeting_title}")
    print(f"Date: {meeting['date']}")
    print(f"Start: {meeting['start_time']}")
    print(f"End: {meeting['end_time']}")
    print(f"Timezone: {TIMEZONE}")
    print(f"Participants: {', '.join(meeting['participants'])}")
    print("Saved to scheduled_meetings.json")
    print("=============================")

    return meeting


# ==========================================
# EXECUTE THE AGENT
# ==========================================

if __name__ == "__main__":

    participants = collect_preferred_times()

    common_slots = find_common_slots(
        participants
    )

    meeting = schedule_meeting(
        common_slots,
        participants
    )

    if meeting:
        print("\nAgent completed the scheduling task.")
    else:
        print("\nAgent stopped: No common time.")