This is the Main Readme for this Project: 

To initiate all our clients and servers see below:
1. Run three clients with seperate client details by running our python files with the command line argument python3 client.py --t=1
Alternate the t value from t {1,2,3} to run each unique client ie --t=2

2. Run the server using python3 server.py


Test Case 1: Hospital Server remains online, Client sends SOS through server.
1. Initiate all three clients and server.
2. Enter coords "4 4" into coordinate input to ensure all clients connect to same server.
3. Put clients t=1 and t=2 into Listening mode, using "L"
4. Input "R" into client t=3 to enter the Elderly Client menu (U/S)
5. Input "S" to send an SOS signal through the hospital system to the server.

Test Case 2: Client sends SOS through clients
1. Update Client list with U function on t=3.
2. Close Hosptial Server
3. Now press S again, Client will attempt to contact other clients, if online these clients will iterate through their client list and send on the details.
This demonstrates the semi decentralised nature of our network, allowing clients to still communicate if the central medical server goes down.
