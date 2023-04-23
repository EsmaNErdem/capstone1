# WICKED ACADIA

### About Wicked Acadia

One of the finest ways to rejuvenate and reconnect with oneself is to spend time in nature. Maine's reputation for natural beauty makes it a popular destination for nature enthusiasts. Wicked Acadia offers Nature Lovers to plan their trip to Acadia National Park (ANP) and see all that Maine has to offer.  Users can access alerts to stay informed, locate visitor centers, browse through events to enhance their experience, and explore places and activities with similar interests. In this app, users can sign-up safely and save data to view later. The app has organized file system that users can find saved data easily. 

## Getting Started

### Tech Stack 

This simple app created with Python(Python 3.10.6), Flask as Backend, Javascript as Frontend. SQLAlchhemy-Postgres was used to create databases. Users passwords will be hashed using Bcrpyt. 

### Installing Dependencies

To install dependencies
```sh
 pip3 install r requirement.txt
```

### Data Collection

**Wicked Acadia** will based on data from [National Park Service's API](https://www.nps.gov/subjects/developer/api-documentation.htm). API offers data and content about National Parks, and related to each park it offers data about events, places, thingstodo, alert, and visitor center The data will be taken from API accordingly. 

### Database schema 

![Database Schema](/static//images/capstone1-schema.jpg)

This database schema is designed to store information about users and their favorite/bookmark places to visit, events, and activities.The schema consists of several tables, each with its own purpose.

The users table stores information about website users, such as their username, email, password, firstname and lastname. This table will likely be populated with data as users register on the website.

The favorites table stores information about a user's favorite places to visit, events, and activities. This table has a category column that indicates which category the favorite belongs to,  so we can allow users to view saved items by categories later and an item_id column that is a foreign key to the appropriate category table (i.e., places, events, or activities) based on the value of the category column. This table will be populated with data as users add favorites to their lists.

The favorites table stores information about a user's favorite places to visit, events, and activities. Its functionality is similiar to favorites table. This database allows users to save content in orginazed manner to make callback easy. 

Overall, this database schema is designed to store and manage data related to users and their favorite and bookmarked places to visit, events, and activities on the website. It enables the website to retrieve and display relevant data to users, as well as store user preferences and track their interactions with the site.


### Website Flow
The homepage of Wicked Acadia provides users with a brief overview of ANP and displays the latest alerts and visitor center information with directions. Users have the option to sign-up or log in using WTForms. The "remember me?" feature keeps users signed in for 30 days or until their cookies are cleared. The "Forgot Password?" feature sends a recovery token to the user's email for password recovery if the password is forgotten. Once logged in, users can save data into their profile. 

Wicked Acadia has three main categories: Activities, Events, and Places, and all information about ANP is obtained from the National Park API. API calls are made in the backend using ORM-Python. Users can add data to their favorites and bookmarks list by clicking on the heart and bookmark icons, respectively, without refreshing the page. This functionality is achieved using Vanilla Javascript and Flask-RestfulAPI to send data to the backend.

On the user profile page, users can view and edit their profile information, or delete profile, and view their favorites and bookmarked lists which can be categorized for ease of use. Users can also search within their favorites and bookmarks to retrieve data.
