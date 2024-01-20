"""Who has qualified for the HUGS patch this year?"""

from collections import defaultdict
import csv
from datetime import date


def start_of_program_year(yearsAgo=0):
    today = date.today()
    if today.month >= 6:
        return date(today.year - yearsAgo, 6, 1)
    else:
        return date(today.year - yearsAgo - 1, 6, 1)


def start_of_unit(grade):
    if grade >= 9:  # Patriot
        return start_of_program_year(grade - 9)
    elif grade >= 7:  # Pioneer
        return start_of_program_year(grade - 7)
    elif grade >= 4:  # Explorer
        return start_of_program_year(grade - 4)
    else:  # Tenderheart
        return start_of_program_year(grade - 1)


def last_name(girl):
    if 'Caballero' in girl:  # Caballero Segura family has double last name
        return girl.split()[1:]
    else:
        return girl.split()[-1]


def get_service():
    with open('data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hours = row['Service Hours']
            if not hours or float(hours) <= 0:
                continue
            eventDate = date.fromisoformat(row['Date'])
            if eventDate < start_of_program_year():
                continue
            yield (row['Name'], row['Event'], eventDate)


def hugs_patches():
    with open('badge_book.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'HUGS' not in row['name']:
                continue
            yield (row['user_name'], date.fromisoformat(row['completed_on']))


def load_roster():
    with open('roster.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            yield (row['name'], int(row['grade']))

            
if __name__ == '__main__':
    projects = defaultdict(list)
    for girl, event, eventDate in get_service():
        projects[girl].append((eventDate, event))

    # If you have a HUGS patch while in your current unit, and you earn it
    # again, you get a rocker.
    grades = dict(load_roster())
    rockerCandidates = set()
    for girl, awardDate in sorted(list(hugs_patches()), key=lambda x: last_name(x[0])):
        if awardDate >= start_of_unit(grades[girl]):
            rockerCandidates.add(girl)

    for girl in sorted(projects, key=lambda x: last_name(x)):
        events = projects[girl]
        if len(events) < 3:
            continue
        if girl in rockerCandidates:
            print(girl, '(*)')
        else:
            print(girl)
        for edate, ename in sorted(events):
            print(edate, ename, sep='\t')
        print()
