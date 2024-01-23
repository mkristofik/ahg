import ahg


if __name__ == '__main__':
    roster = ahg.Roster()
    badges = ahg.Badges()
    for girl in roster.names():
        allUndone = list(badges.all_incomplete(girl, roster.grade_level(girl)))
        if not allUndone:
            continue
        # TODO: produce html output so the girls' names are bolded
        print(girl)
        for badge in allUndone:
            print(badge)
        print()
