"""Who did National Day of Service, who gets the patch, and who gets the rocker?"""

import ahg


# National Day of Service project in the current program year
# Have the National Day of Service patch since start of unit?
# If yes, rocker
if __name__ == '__main__':
    projects = ahg.load_service_projects()
    roster = ahg.Roster()
    badges = ahg.Badges()
    patches = []
    rockers = []
    for girl in roster.names():
        if not any('National' in eventName for _, eventName in projects[girl]):
            continue
        if badges.has_national_day_of_service(girl, roster.start_of_unit(girl)):
            rockers.append(girl)
        else:
            patches.append(girl)

    print('PATCHES')
    for girl in patches:
        print(girl)
    print('\nROCKERS')
    for girl in rockers:
        print(girl)
