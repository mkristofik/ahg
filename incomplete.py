import ahg


if __name__ == '__main__':
    roster = ahg.Roster()
    for girl in roster.names():
        allUndone = list(roster.incomplete_badges(girl))
        if not allUndone:
            continue
        # TODO: produce html output so the girls' names are bolded
        print(girl)
        for badge in allUndone:
            print(badge)
        print()
