If you wish to download the repository and run the code, make sure to have the necessary libraries:
    - customtkinter, tkinter, requests
Otherwise, I've provided the .exe file to test it out on your device.

Made some final draft adjustments. The following features have been added

1. Cloud Database
    - My app no longer connects to my personal DB
    - I migrated my database to Oracle Cloud, so my demo can work from anywhere
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
    - The restrictions are that you can't make any actions that would normally UPDATE or INSERT any values to my database.
