"""Who has started working on badges but not finished them yet?"""

import ahg
from collections import defaultdict
import webbrowser


if __name__ == '__main__':
    roster = ahg.Roster()
    incomplete = defaultdict(list)
    for girl in roster.names():
        for badge in roster.incomplete_badges(girl):
            incomplete[girl].append(badge)

    with open('incomplete.html', 'w') as f:
        for girl, badges in incomplete.items():
            print('<p><b>' + girl + '</b><br />', file=f)
            for badge in badges:
                print(badge + '<br />', file=f)
            print('</p>', file=f)

    webbrowser.open('incomplete.html', new=2)
