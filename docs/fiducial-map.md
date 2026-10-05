# Fiducial map for the Dining Room

Which fiducial (AprilTag) is where, so you can decide which tags your autonomous routine should look for. The ID numbers here are the same numbers `find_tag(id)` and `visible_tag_ids()` use in `src/main.py`.

**Source:** *Byte to Bite Field Drawings*, document GAMFLDR01, revision dated August 23 2026: the fiducial map on page 7, the table layout on page 30, and the wall and table drawings on pages 69-83 and 156-158. If BEST publishes a newer revision, check this page against it. The official drawings decide any disagreement.

A real field is built by volunteers from lumber, so expect positions to be off by a fraction of an inch or more. Use these numbers to plan, then measure what the camera actually reports on a real field.

## The map

Looking down on the field, drawn the same way round as the official map. The corner labels are the ones printed on that map.

```
   BLUE corner                                        RED corner

        +--        ======[ 9 ]======[10 ]======        --+
        |                                                |
      [20]                                             [11]
        |        ( 0 )        ( 1 )        ( 2 )         |
        |                                                |
      [19]                                             [12]
        |        ( 3 )        ( 4 )        ( 5 )         |
        |                                                |
      [18]                                             [13]
        |        ( 6 )        ( 7 )        ( 8 )         |
        |                                                |
      [17]                                             [14]
        |                                                |
        +--        ======[16 ]======[15 ]======        --+

   YELLOW corner                                      GREEN corner

   ( n )  fiducial lying flat on a table top, facing up
   [ n ]  fiducial on a wall, facing into the Dining Room
   ====   short wall        |   long wall
```

The four gaps at the corners, between the ends of the short walls and the long walls, are the entrances. Each is 24 inches wide.

## ID list

There are 21 fiducials, IDs 0 to 20, all from the Circle21h7 family.

| IDs | Where | Order |
| --- | ----- | ----- |
| 0 - 8 | One on each of the nine tables | Left to right, starting with the row nearest the red-blue side: 0 1 2, then 3 4 5, then 6 7 8. Table 4 is the centre of the Dining Room. |
| 9, 10 | Short wall on the red-blue side | 9 is nearer the blue corner, 10 nearer the red corner |
| 11 - 14 | Long wall on the red-green side | 11 is nearest the red corner, 14 nearest the green corner |
| 15, 16 | Short wall on the yellow-green side | 15 is nearer the green corner, 16 nearer the yellow corner |
| 17 - 20 | Long wall on the blue-yellow side | 17 is nearest the yellow corner, 20 nearest the blue corner |

The wall IDs run clockwise around the room, starting at 9.

## Positions

All measurements are in inches. They are measured from the centre of the Dining Room, which is the centre of table 4:

- **x** is positive towards the red-green long wall (right on the map).
- **y** is positive towards the red-blue short wall (up on the map).

The inside of the Dining Room is 132 by 132. Each wall's inside face is 66 from the centre.

### Tables

| ID | x | y |
| -- | --- | --- |
| 0 | -36 | 36 |
| 1 | 0 | 36 |
| 2 | 36 | 36 |
| 3 | -36 | 0 |
| 4 | 0 | 0 |
| 5 | 36 | 0 |
| 6 | -36 | -36 |
| 7 | 0 | -36 |
| 8 | 36 | -36 |

- A table top is 12 by 12, and the fiducial is centred on it.
- The gap between neighbouring tables is 24, and so is the gap between an outer table and the wall. That is the space the robot has to drive through.
- The table top is about 3 5/8 above the floor (3 1/2 legs plus a 1/8 top). The fiducial faces straight up, so the camera has to look down at it to see it.
- Each table fiducial is placed with its top edge, the edge with the ID number, towards the red-blue side.

### Walls

| ID | Wall | x | y |
| -- | ---- | --- | --- |
| 9 | Short, red-blue side | -18 | 66 |
| 10 | Short, red-blue side | 18 | 66 |
| 11 | Long, red-green side | 66 | 54 |
| 12 | Long, red-green side | 66 | 18 |
| 13 | Long, red-green side | 66 | -18 |
| 14 | Long, red-green side | 66 | -54 |
| 15 | Short, yellow-green side | 18 | -66 |
| 16 | Short, yellow-green side | -18 | -66 |
| 17 | Long, blue-yellow side | -66 | -54 |
| 18 | Long, blue-yellow side | -66 | -18 |
| 19 | Long, blue-yellow side | -66 | 18 |
| 20 | Long, blue-yellow side | -66 | 54 |

- Wall fiducials are upright, with the ID number at the top.
- Neighbouring fiducials on the same wall are 36 apart.
- No wall fiducial lines up with a row or column of tables. Tables are at -36, 0 and 36; wall fiducials are at -54, -18, 18 and 54. Each wall fiducial sits halfway between two table lines, or between a table line and the wall. So a robot centred on a wall fiducial is in the middle of an aisle, not pointed at a table.
- The centre of each wall fiducial is 9 above the bottom edge of the wall panel. The panel is 18 tall, so that is about 9 above the floor.

## Size of a fiducial

The inner area of a printed fiducial measures 4.25 across. The square drawn for the sticker on the wall drawings is 8.5 across.

## What was read and what was worked out

Read directly from the drawings:

- Every ID and which wall or table it is on (page 7).
- The 132 by 132 inside size and the 24 gaps around the tables and at the entrances (pages 30 and 69).
- Short wall fiducials 18 either side of the wall's centre, 9 above the bottom of the panel (page 70).
- Long wall fiducials 18 and 54 from one end of each wall half, 9 above the bottom of the panel (pages 77 and 78).
- Table top 12 by 12 with the fiducial centred, legs 3 1/2 tall (pages 156-158).

Worked out from those, so worth checking with a tape measure on a real field:

- **The x and y numbers.** The drawings give gaps and sizes, not coordinates.
- **Long wall positions.** The 18 and 54 are measured from the end of each half that has the bolt holes. This page takes that to be the end where the two halves join in the middle of the wall, which puts the four fiducials evenly 36 apart, as they appear on the map. The drawings do not say so in words.
- **Height above the floor.** This assumes the bottom of the wall panel sits at floor level.

Still unknown:

- **Whether the AI Vision Sensor reports ID 0.** The VEX SDK notes suggest tag IDs start at 1, and table 0 uses ID 0. See `TODO.md`.
- **How far away the camera can read a fiducial of this size.** Test it with a printed one.
