from collections import defaultdict
from pypdf import PdfReader
import re


levels = ('Pathfinder', 'Tenderheart', 'Explorer', 'Pioneer', 'Patriot')
lineinfo = []


def page_visitor(text, cm, tm, font_dict, font_size):
    x = tm[4]
    y = tm[5]
    words = text.strip()
    if words:
        lineinfo.append((y, x, words))


# Yields lists of words that appear on each line
def parse_page(page):
    lineinfo.clear()
    page.extract_text(visitor_text=page_visitor)
    curY = 0
    curRow = []

    # Words that appear at the same Y coordinate are physically on the same
    # line.  This accounts for the pdf not being rendered in line order.
    for line in sorted(lineinfo):
        yPos = line[0]
        words = line[2]
        if yPos != curY:
            if curRow:
                yield curRow
                curRow.clear()
            curY = yPos
        if yPos == curY:
            curRow.append(words)
    if curRow:
        yield curRow


def is_unit_heading(row):
    if len(row) != 1:
        return False
    return row[0] in levels


def extract_badges(page):
    patchName = ''  # Catholic faith awards are split over multiple rows

    for row in parse_page(page):
        # Skip title
        if 'Agenda for Next Award Ceremony' in row:
            continue
        # Skip the row headings
        if 'Purchased' in row and 'Awarded' in row:
            continue

        if is_unit_heading(row):
            yield ('unit', row[0])
        elif len(row) == 1:
            if 'Faith Award' in row[0]:
                patchName = row[0]
            elif 'Patch' in row[0]:
                patchName += ' ' + row[0]
                # Shorten a bit for readability
                patchName = re.sub('- .+ -', '-', patchName)
                yield ('badge', patchName)
                patchName = ''
            else:
                yield ('girl', row[0])
        elif patchName:  # in the middle of a faith award
            patchName += ' ' + row[0]
        else:
            # Remove unit indicator from badge name
            badge = re.sub(r'\(.+\)', '', row[0]).strip()
            if badge.isupper():
                badge = badge.capitalize()
            if len(row) > 1 and 'Level Award' in row[1]:
                if 'Joining Award' in badge:
                    yield ('joining', badge)
                else:
                    yield ('level', badge)
            elif len(row) > 1 and 'Sports Pin' in row[1]:
                yield ('badge', badge + ' pin')
            else:
                if 'Rocker:' in badge:
                    badge = re.sub(r'Rocker: (.+)', r'\1 Rocker', badge)
                yield ('badge', badge)


def print_joining_awards(f, names):
    print('<h3>Joining Awards</h3>', file=f)
    for n in names:
        print(n + '<br />', file=f)


def print_pathfinder_beads(f, girls):
    print('<h3>Pathfinder: Beads</h3>', file=f)
    for girl in girls:
        print('<b>' + girl['name'] + ':</b> ', end='', file=f)
        beads = []
        if girl['steppingStones'] > 1:
            beads.append('{} Stepping Stones beads'.format(girl['steppingStones']))
        elif girl['steppingStones'] == 1:
            beads.append('1 Stepping Stone bead')
        if girl['attendanceBeads'] > 1:
            beads.append('{} blue attendance beads'.format(girl['attendanceBeads']))
        elif girl['attendanceBeads'] == 1:
            beads.append('1 blue attendance bead')
        if girl['serviceBeads'] > 1:
            beads.append('{} white service beads'.format(girl['serviceBeads']))
        elif girl['serviceBeads'] == 1:
            beads.append('1 white service bead')
        if girl['bibleVerseBeads'] > 1:
            beads.append('{} red Bible verse beads'.format(girl['bibleVerseBeads']))
        elif girl['bibleVerseBeads'] == 1:
            beads.append('1 red Bible verse bead')
        print(', '.join(beads) + '<br />', file=f)


def print_badges(f, badges):
    for lvl in levels:
        if lvl == 'Pathfinder':
            print_pathfinder_beads(f, badges[lvl])
        else:
            print('<h3>' + lvl + ': Badges and Service Stars</h3>', file=f)
            for girl in badges[lvl]:
                print('<b>' + girl['name'] + ':</b> ', end='', file=f)
                badgesToPrint = list(girl['badges'])
                if girl['serviceStars'] > 1:
                    badgesToPrint.append('{} service stars'.format(girl['serviceStars']))
                elif girl['serviceStars'] == 1:
                    badgesToPrint.append('1 service star')
                print(', '.join(badgesToPrint) + '<br />', file=f)


def print_level_awards(f, levelAwards):
    awardNames = {
            'Pathfinder': 'Fanny Crosby',
            'Tenderheart': 'Sacagawea',
            'Explorer': 'Ida Scudder',
            'Pioneer': 'Harriet Tubman',
            'Patriot': 'Abigail Adams'
            }
    print('<h3>Level Awards</h3>', file=f)
    for lvl in levels:
        if lvl not in levelAwards:
            continue
        print('<h4>' + lvl, awardNames[lvl], 'Level Award</h4>', file=f)
        for name in levelAwards[lvl]:
            print(name + '<br />', file=f)


if __name__ == '__main__':
    levelAwards = defaultdict(list)
    joiningAwards = []
    badges = defaultdict(list)
    reader = PdfReader('award_agenda_by_scout.pdf')

    curUnit = ''
    curGirl = {}
    for page in reader.pages:
        for itemType, title in extract_badges(page):
            if itemType == 'unit':
                curUnit = title
            elif itemType == 'girl':
                if curGirl:
                    badges[curGirl['unit']].append(curGirl)
                curGirl = {
                        'unit': curUnit,
                        'name': title,
                        'badges': [],
                        'serviceStars': 0,
                        'steppingStones': 0,
                        'attendanceBeads': 0,
                        'serviceBeads': 0,
                        'bibleVerseBeads': 0
                        }
            elif itemType == 'joining':
                joiningAwards.append(curGirl['name'])
            elif itemType == 'level':
                levelAwards[curUnit].append(curGirl['name'])
            elif itemType == 'badge':
                if title == 'Service Star':
                    curGirl['serviceStars'] += 1
                elif title == 'AHG Logo Bead':
                    curGirl['steppingStones'] += 1
                elif title == 'Blue Round Bead':
                    curGirl['attendanceBeads'] += 1
                elif title == 'White Star Bead':
                    curGirl['serviceBeads'] += 1
                elif title == 'Red Heart Bead':
                    curGirl['bibleVerseBeads'] += 1
                else:
                    curGirl['badges'].append(title)
    # Don't forget the last girl on the last page
    badges[curGirl['unit']].append(curGirl)

    with open('agenda.html', 'w') as f:
        print_joining_awards(f, joiningAwards)
        print_badges(f, badges)
        print_level_awards(f, levelAwards)
