# hacker-hunt-backend

Backend repo for second build week focused on Computer Science. The goal of the project is to efficiently traverse an island maze, collect treasure, solve puzzles, unearth powerful artifacts and more. Glory and riches await the victors!

### Backend role

As the backend developer, you will be implementing an automated traversal server. By sending POST requests to our LambdaMUD Island server and processing the response, your server will allow your team to move and collect treasure at all hours of the day and night. The teams with efficient traversal and treasure collection algorithms will find themselves prosperous.

## Implementation

Servers API endpoints are build with Pythons Flask and connected to a MongoDB database.

Backend architecture is designed to utilize all four team members to explore the map. This is achieved by syncing the game map, stored in DB, across all players.

**Map traversal algorithm** - the player traverses the map (Graph data structure) with Depth-First-Traversal, until it hits a dead end - room with only one exit. Then it starts Breath-First-Search to find the shortest path to next unexplored room from DFT.

The player will update the map on every move, check for treasures, picks them up, check for special rooms (name changer, shrine) and does actions according to the room. If players inventory is full, he will be **automagically** traversed back to shop, where he sells items and traverses back to the room where he started.

Player movement will always check if he already explored rooms around him, to effectively utilize the `wise_explore` request to make his movement as efficient as possible.
