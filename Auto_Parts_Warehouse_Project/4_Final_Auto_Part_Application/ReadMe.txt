If you wish to download the repository and run the code, make sure to have the necessary libraries:
    - customtkinter, tkinter, requests
Otherwise, I've provided the .exe file to test it out on your device.

If either choice is not viable, I have provided a video of myself using all three features
Demo Link 1: https://youtu.be/TuX8qcJ62LY
Demo Link 2: https://youtu.be/-sRb5uhVIMs
Demo Link 3: https://youtu.be/2Gb8JoRZysY

For more information about how my Database was structured, go here
Link: https://github.com/Cephuez/PastProjects/tree/main/Auto_Parts_Warehouse_Project/1_Auto_Part_Database

Made some final draft adjustments. The following features have been added

1. Cloud Database
    - My app no longer connects to my personal DB
    - I migrated my database to Oracle Cloud, so my application can work from anywhere
2. Backend API Architecture
    - All database calls are now handle through FastAPI backend service, instead of my GUI having direct access to the database
    - The API is hosted through Render. This allows me more control between the app and my database
3. Security and Access Control
    - Sensitive data like Oracle wallet credentials and connection settings are stored in a private repository
    - Access to my application is now handled through tokens
    - Whenever a user logs in, they are given a token that gives them access to my API
    - I've added two seperate roles
        - Demo users have some restricted permission 
        - Workers(Admin) have full access to the application
4. Demo Testing (I've added a PDF file with the login info and explanation)
    - Anyone now have access to my application by logging in
    - The restrictions prevent you from making changes to my database like INSERT and UPDATE, which happens often with full privileges.
