This is a very old discontinued project.

I worked on heavily on it in 2023 when I first moved from Roblox to Python development.
I decided to release it after a while because I had moved on to my current 3D experiments in C++ and tried to maintain Lavryrinthos,
but this is a bit of a mess and had lots of things I would structure differently, so I just released it so see what happens.

It was based on a heavily modified version of this raycaster: https://github.com/StanislavPetrovV/DOOM-style-Game .
Plus music by https://soundcloud.com/spiderguaves .
Chicken from Heretic, big cow from DOOM 64, shotgun from DOOM '93, some stock images I heavily editied or drew all over, plus some of my (cough, old) original art.

Changes Included:
-Far clipping plane based on maximum visible distance (furthest rendered wall)

-Locks and keys, secrets, and gates.
-Two different weapons.
-Sprites with 8 different perspectives, 
-Configurable sprite starting angle, determining perspective angle and direction of the monster's FOV
-Different patrol routes based on map sector for boss types, switching routes if entering a new sector and if the player ran away.
-Different levels of boss awareness of player;
.If player not in any range, continue on route.
.If player within a near range, raycast FOV
.If player within FOV, pursue player
.If player no longer within FOV, timer will allow monster to follow player, even if behind a wall, for a short time limit, then return to patrol.

How to Play:
Controls: WASD move, mouse or left/right arrows to look, E to pick up, click to use; 
Cheat/Test Keys; L to drop power up, P to teleport near end in levels 1-2 ONLY.
There are currently 3 levels (crusades). Originally, there were going to be 2-4 levels per world, but the art took much longer than the actual programming. 
-Find the keys on the walls and hang them on the keystands.
-A powerup will drop that will allow the hero to attack the main boss.
-The boss (not programmed) would retreat and meet the player next level with reduced health and die in the final level of that world. Next world would have a new boss.
-This was designed to be an evasion/shooter game with labrynith puzzles. There was a lore reason for the power up system.

There is an image of a blender model in assets/conceptArt that was going to be converted into sprite sheets to replace the Chicken from Heretic as a common mob, but at that point, it did not seem like a smart idea to invest so much in this particular project. 
