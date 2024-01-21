"""Who has qualified for the HUGS patch this year?"""

import ahg


if __name__ == '__main__':
    projects = ahg.load_service_projects()
    roster = ahg.Roster()
    badges = ahg.Badges()

    # If you have a HUGS patch while in your current unit, and you earn it
    # again, you get a rocker.
    for girl in roster.names():
        events = projects[girl]
        if len(events) < 3:
            continue
        if badges.has_hugs_patch(girl, roster.start_of_unit(girl)):
            print(girl, '(*)')
        else:
            print(girl)
        for edate, ename in events:
            print(edate, ename, sep='\t')
        print()
