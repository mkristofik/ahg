"""Who has qualified for the HUGS patch this year?"""

import ahg
import csv
from datetime import date


def hugs_patches():
    with open('badge_book.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'HUGS' not in row['name']:
                continue
            yield (row['user_name'], date.fromisoformat(row['completed_on']))


if __name__ == '__main__':
    projects = ahg.load_service_projects()

    # If you have a HUGS patch while in your current unit, and you earn it
    # again, you get a rocker.
    roster = ahg.Roster()
    rockerCandidates = set()
    for girl, awardDate in hugs_patches():
        if awardDate >= roster.start_of_unit(girl):
            rockerCandidates.add(girl)

    for girl in roster.names():
        events = projects[girl]
        if len(events) < 3:
            continue
        if girl in rockerCandidates:
            print(girl, '(*)')
        else:
            print(girl)
        for edate, ename in events:
            print(edate, ename, sep='\t')
        print()
