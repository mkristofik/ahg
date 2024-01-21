from collections import defaultdict
import csv
from datetime import date


def start_of_program_year(yearsAgo=0):
    """June 1st of the 'yearsAgo' program year."""
    today = date.today()
    if today.month >= 6:
        return date(today.year - yearsAgo, 6, 1)
    else:
        return date(today.year - yearsAgo - 1, 6, 1)


def load_service_projects():
    """Map {girl : (date, event)} for service projects in the current program year."""
    projects = defaultdict(list)
    with open('data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hours = row['Service Hours']
            if not hours or float(hours) <= 0:
                continue
            eventDate = date.fromisoformat(row['Date'])
            if eventDate < start_of_program_year():
                continue
            projects[row['Name']].append((eventDate, row['Event']))

    for events in projects.values():
        events.sort()
    return projects


class Roster:
    def __init__(self):
        self._gradeLevels = dict(self._load_from_file())

    def names(self):
        return self._gradeLevels.keys()

    def start_of_unit(self, girl):
        """June 1st of the year the girl started in her current unit."""
        grade = self._gradeLevels[girl]
        if grade >= 9:  # Patriot
            return start_of_program_year(grade - 9)
        elif grade >= 7:  # Pioneer
            return start_of_program_year(grade - 7)
        elif grade >= 4:  # Explorer
            return start_of_program_year(grade - 4)
        else:  # Tenderheart
            return start_of_program_year(grade - 1)

    def _load_from_file(self):
        with open('roster.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row:
                    continue
                yield (row['name'], int(row['grade']))
