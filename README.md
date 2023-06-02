# WICKED ACADIA

Live: https://wicked-acadia.onrender.com/

![Wicked Acadia Homepage](/static//images/homepage.jpg)

### About Wicked Acadia

One of the finest ways to rejuvenate and reconnect with oneself is to spend time in nature. Maine's reputation for natural beauty makes it a popular destination for nature enthusiasts. Wicked Acadia offers Nature Lovers to plan their trip to Acadia National Park (ANP) and see all that Maine has to offer.  Users can access alerts to stay informed, locate visitor centers, browse through events to enhance their experience, and explore places and activities with similar interests. In this app, users can sign-up safely and save data to view later. The app has organized file system that users can find saved data easily. 

## Getting Started

### Tech Stack 

This simple app created with Python(Python 3.10.6), Flask as Backend, Javascript as Frontend. SQLAlchhemy-Postgres was used to create databases. Users passwords will be hashed using Bcrpyt. All of the forms were created using WTForms.

### Installing Dependencies 
To install dependencies:
```sh
 pip3 install r requirements.txt
```

### Testing

Wicked Acadia has an extensive testing suite that covers various aspects of the application, including model testing, API route testing, and view testing. These tests ensure the reliability and correctness of the codebase. To run the tests, follow the instructions below:

To run unittests:

```sh
python -m unittest tests/test_model.py
```

To run the tests views functions, set the FLASK_ENV environment variable to production and run the command:

```sh
FLASK_ENV=production python -m unittest tests/test_restful_api.py
FLASK_ENV=production python -m unittest tests/test_user_view.py
FLASK_ENV=production python -m unittest tests/test_view_api_external.py
```
These commands will execute the respective test files and validate the functionality of the views functions within the Wicked Acadia application.

### Data Collection

**Wicked Acadia** will based on data from [National Park Service's API](https://www.nps.gov/subjects/developer/api-documentation.htm). API offers data and content about National Parks, and related to each park it offers data about events, places, thingstodo, alert, and visitor center The data will be taken from API accordingly. 

### Database schema 

![Database Schema](/static//images/capstone1-schema.jpg)

This database schema is designed to store information about users and their favorite/bookmark places to visit, events, and activities.The schema consists of several tables, each with its own purpose.

The users table stores information about website users, such as their username, email, password, firstname and lastname. This table will likely be populated with data as users register on the website.

As users save data to their favorites and bookmarks, the selected data from external APIs will be stored in their own corresponding tables in the database, such as events data being saved to the events table. User model has a one-to-many relationship with the Activity, Event, and Place models, through the bookmarks and favorites association table. 

Overall, this database schema is designed to store and manage data related to users and their favorite and bookmarked places to visit, events, and activities on the website. It enables the website to retrieve and display relevant data to users, as well as store user preferences and track their interactions with the site.


### Website Flow

The homepage of Wicked Acadia provides users with a brief overview of ANP and displays the latest alerts and visitor center information with directions. Users have the option to sign-up or log in using WTForms. The "remember me?" feature keeps users signed in for 30 days or until their cookies are cleared. The "Forgot Password?" feature sends a recovery token to the user's email for password recovery if the password is forgotten. Once logged in, users can save data into their profile to view later. Data that was retrieved from API will be saved in database as users add data to their favorite/bookmark list.

Wicked Acadia has three main categories: Activities, Events, and Places, and all information about ANP is obtained from the National Park API. API calls are made in the backend using OOP (Object Oriented Programming) to promote modularity and code reusability. By using OOP-Python, the code is organized into modular objects, each encapsulating its own data and functionality. Users can add data to their favorites and bookmarks list by clicking on the heart and bookmark icons, respectively, without refreshing the page. This functionality is achieved using Vanilla Javascript in front-end and Flask-RestfulAPI as the back-end to send data to the backend.

On the user profile page, users can view and edit their profile information, or delete profile, and view their favorites and bookmarked lists which can be categorized for ease of use. Users can also search within their favorites and bookmarks to retrieve data.

### Further Study

As the creator of Wicked Acadia, I am continuously exploring ways to improve the app and provide a better experience for users. Here are some ideas for further study and potential enhancements:

1. Implementing Flask Blueprints to divide the app into modular components or modules. This approach organizes the codebase, improves maintainability, and allows for better scalability as the application grows. 

1. Implement a feature that allows users to leave reviews and ratings for activities, events, and places within Acadia National Park.

1. Enchancing user profiles by implementing user profile picture upload feature, and social media links