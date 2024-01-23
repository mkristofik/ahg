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

    def grade_level(self, girl):
        return self._gradeLevels[girl]

    def start_of_unit(self, girl):
        """June 1st of the year the girl started in her current unit."""
        grade = self.grade_level(girl)
        if grade >= 7:  # Pioneer/Patriot
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


class Badges:
    def __init__(self):
        self._completed = defaultdict(list)  # {girl : (date, badge name)}
        self._incomplete = defaultdict(list)  # {girl : badge name}

        for badge in self._load_from_file():
            if badge['date']:
                self._completed[badge['girl']].append((badge['date'], badge['name']))
            else:
                self._incomplete[badge['girl']].append(badge['name'])

    def has_national_day_of_service(self, girl, unitStartDate):
        return self._has_badge(girl, unitStartDate, 'National')

    def has_hugs_patch(self, girl, unitStartDate):
        return self._has_badge(girl, unitStartDate, 'HUGS')

    def all_incomplete(self, girl, grade):
        unit = self._current_unit_tag(grade)
        others = self._other_unit_tags(grade)
        for badge in self._incomplete[girl]:
            if any(tag in badge for tag in others):
                continue
            yield badge.removesuffix(unit)

    def _has_badge(self, girl, unitStartDate, partialName):
        for badgeDate, badgeName in self._completed[girl]:
            if badgeDate < unitStartDate:
                continue
            if partialName in badgeName:
                return True
        return False

    def _current_unit_tag(self, grade):
        if grade >= 7:
            return ' (Pi/Pa)'
        elif grade >= 4:
            return ' (E)'
        else:
            return ' (T)'

    def _other_unit_tags(self, grade):
        if grade >= 7:  # Pioneer/Patriot
            return ['(T)', '(E)']
        elif grade >= 4:  # Explorer
            return ['(T)', '(Pi/Pa)']
        else:  # Tenderheart
            return ['(E)', '(Pi/Pa)']

    def _load_from_file(self):
        with open('badge_book.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pct = row['percent_complete']
                if not pct or int(pct) == 0:
                    continue
                completionDate = row['completed_on']
                if completionDate:
                    completionDate = date.fromisoformat(completionDate)
                elif 'Level Award' in row['achievement_type']:
                    continue
                yield {
                        'girl': row['user_name'],
                        'name': row['name'],
                        'date': completionDate
                        }
