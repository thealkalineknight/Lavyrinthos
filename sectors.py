class Sector:
    class Sector0:
        x1 = 0
        y1 = 0
        x2 = 10
        y2 = 10
        max = max(x2 - x1, y2 - y1)
        waypoints = []

    class Sector1:
        x1 = 0
        y1 = 0
        x2 = 20
        y2 = 20
        max = max(x2 - x1, y2 - y1)
        waypoints = [(14, 16), (7, 10),
                     (5, 10), (1, 10), (1, 18), (5, 18), (5, 10),
                     (7, 10), (18, 10), (20, 11), (19, 13),
                     (18, 10), (7, 10)]

        class SSector1:
            x1 = 0
            y1 = 0
            x2 = 8
            y2 = 20
            max = max(x2 - x1, y2 - y1)

        class SSector2:
            x1 = 8
            y1 = 9
            x2 = 20
            y2 = 9
            max = max(x2 - x1, y2 - y1)

        class SSector3:
            x1 = 8
            y1 = 9
            x2 = 20
            y2 = 20
            max = max(x2 - x1, y2 - y1)

#         waypoints = [(14, 16.5), (7.5, 10.5),
#                      (5.5, 10.5), (1.5, 10.5), (1.5, 18.5), (5.5, 18.5), (5.5, 10.5),
#                      (7.5, 10.5), (18, 10), (20, 11.5), (19, 13),
#                      (18, 10), (7.5, 10.5)]
