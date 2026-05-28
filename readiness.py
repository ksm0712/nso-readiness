from calendar import monthrange
from datetime import date

from date_format import format_date


TRAINING_MONTHS = {
    "RGM": 6,
    "ARGM": 3,
    "Supervisor": 3,
    "Team Member": 1,
}

ROLE_FIELDS = {
    "RGM": ("need_rgm", "hired_rgm"),
    "ARGM": ("need_argm", "hired_argm"),
    "Supervisor": ("need_sup", "hired_sup"),
    "Team Member": ("need_tm", "hired_tm"),
}


def add_months(start_date, months):
    month_number = start_date.month + months
    year = start_date.year + (month_number - 1) // 12
    month = (month_number - 1) % 12 + 1
    day = min(start_date.day, monthrange(year, month)[1])
    return date(year, month, day)


def read_date(date_text):
    if not date_text:
        return None
    return date.fromisoformat(date_text)


def format_role_list(roles):
    unique_roles = sorted(set(roles))
    if len(unique_roles) == len(ROLE_FIELDS):
        return "all roles"
    return ", ".join(unique_roles)


def get_readiness(store, hires, today=None):
    if today is None:
        today = date.today()

    target_open = read_date(store["target_open"])
    if target_open is None:
        return {
            "status": "Behind",
            "summary": "No target opening date is saved, so readiness cannot be confirmed.",
            "details": [],
        }

    details = []
    missing_roles = []
    late_roles = []
    latest_finish = None
    all_needed_hired = True
    all_training_done = True

    for role, fields in ROLE_FIELDS.items():
        need_field, hired_field = fields
        needed = store[need_field]
        hired_count = store[hired_field]
        role_hires = [hire for hire in hires if hire["role"] == role]
        missing = max(0, needed - hired_count)

        if missing > 0:
            all_needed_hired = False
            missing_roles.append(f"{missing} {role}")

        training_months = TRAINING_MONTHS[role]
        role_finish_dates = []

        for hire in role_hires[:needed]:
            start_date = read_date(hire["start_date"]) or today
            finish_date = add_months(start_date, training_months)
            role_finish_dates.append(finish_date)
            if finish_date > today:
                all_training_done = False
            if finish_date > target_open:
                late_roles.append(role)

        counted_without_details = max(0, min(hired_count, needed) - len(role_hires))
        for i in range(counted_without_details):
            finish_date = add_months(today, training_months)
            role_finish_dates.append(finish_date)
            all_training_done = False
            if finish_date > target_open:
                late_roles.append(role)

        for i in range(missing):
            finish_date = add_months(today, 1 + training_months)
            role_finish_dates.append(finish_date)
            if finish_date > target_open:
                late_roles.append(role)

        if role_finish_dates:
            role_latest_finish = max(role_finish_dates)
            latest_finish = role_latest_finish if latest_finish is None else max(latest_finish, role_latest_finish)
            details.append(f"{role}: {hired_count} of {needed} hired. Earliest full readiness: {format_date(role_latest_finish)}.")
        else:
            details.append(f"{role}: {hired_count} of {needed} hired.")

    if all_needed_hired and all_training_done:
        return {
            "status": "Ready",
            "summary": "Ready for opening. All required positions are hired and training is complete.",
            "details": details,
        }

    if late_roles:
        late_role_names = format_role_list(late_roles)
        if missing_roles:
            missing_text = ", ".join(missing_roles)
            summary = f"At risk for opening. Need to hire: {missing_text}. Training will miss the target date for {late_role_names}."
        else:
            summary = f"At risk for opening. Hiring is complete, but training will miss the target date for {late_role_names}."
        return {
            "status": "Behind",
            "summary": summary,
            "details": details,
        }

    if all_needed_hired:
        finish_text = latest_finish if latest_finish else target_open
        summary = f"On track for opening. Hiring is complete and training is expected to finish by {format_date(finish_text)}."
    else:
        missing_text = ", ".join(missing_roles)
        finish_text = latest_finish if latest_finish else target_open
        summary = f"On track, but hiring is not finished. Need to hire: {missing_text}. If hiring starts now, training can finish by {format_date(finish_text)}."

    return {
        "status": "On Track",
        "summary": summary,
        "details": details,
    }
