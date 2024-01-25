# AHG Utilities

## Court of Awards Agenda

- From TroopTrack dashboard page, click on Achieve > Print Agenda by Unit.
- Save file as **award_agenda_by_scout.pdf** to this directory.
- Run `python agenda.py`.
- Open **agenda.html** in a browser, copy and paste to Google Docs.

## Badge Analysis

Before getting started, create `roster.csv` in this directory containing all the
girls' grade levels, Tenderheart and above.  Pathfinders do not earn badges.

```
name,grade
Wilma Flinstone,3
Jane Jetson,8
Betty Rubble,6
...
```

- From TroopTrack dashboard page, click on Manage > Reports > Badge Book.
- Right-click on CSV, save file as **badge_book.csv** to this directory.
- Click on Manage > Reports > Participation Book.
- Left-click Options, right-click CSV, save file as **data.csv** to this
directory.

### HUGS Patches

- Run `python hugs.py`.
- Output shows all girls who have completed three or more service projects in
the current program year.
    - Need to review if the service projects meet the HUGS requirements.
    - Girls who already have the HUGS patch in their current unit will be
      highlighted (they get a rocker instead).

### National Day of Service

- Run `python national.py`
- Output shows all girls who participated in the National Day of Service for the
  current program year.
    - Girls who already have the patch receive a rocker instead.

### Incomplete Badges

- Run `python incomplete.py`
- Shows all badges that were started in a girl's current unit but not yet
  finished.
