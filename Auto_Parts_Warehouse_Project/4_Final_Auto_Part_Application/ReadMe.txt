Made some final draft adjustments. The following features has been added

1. App no longer connects to my personal database. I've set up a database online using Oracle Cloud
2. To keep sensitive data secured:
    - I've made sure to secure Oracle's connection data secured in a private repository
    - Using Render, I'm hosting API calls in this private repository so no user can try to access it
    - To prevent users from willingly using my API, I've added Tokens giving to users only if they log in 
    - Since this is a DEMO, I've attached an account that allows you to sign into the app, but with the exception of making any modification to the database like UPDATE and INSERT
