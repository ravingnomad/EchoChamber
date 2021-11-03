# Echo Chamber
Personal project that transfers files between two computers, or one computer and a phone.


# Download Instructions
1. Download the code in a zip file.

2. Extract the entire file directory into two separate computers. One will serve as the client side of the program, and the other will serve as the server side of the program.


# How to Use
1. Open the 'main.py' file on both server and client computers and change the 'serverIPAddress' variable, located at the bottom,  so that it holds a valid IP Address of the server machine represented as a string.

2. Initially, on the server computer, there will be no user info for the computer to access. So run the 'main.py' file and enter in valid user info and then have it wait for a client to connect to it.

3. Run 'main.py' on the client side and allow it to connect to the server side.

NOTE: Keep all files in one place on each computer because the server side and client side can only access files that are in the same directory as 'echoChamberClient.py' and 'echoChamberServer.py'.


# Uninstallation
Delete the downloaded/extracted files.