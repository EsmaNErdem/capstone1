
# WICKED ACADIA

### About Wicked Acadia

As the weather gets warmer, Maine is getting ready for another wondeful summer season.  One of the finest ways to rejuvenate and reconnect with oneself is to spend time in nature. Maine's reputation for natural beauty makes it a popular destination for nature enthusiasts. Wicked Acadia offers Nature Lovers to plan their trip to Acadia National Park (ANP) and experience all that Maine has to offer.  Users can access alerts to stay informed, locate visitor centers, browse through events to enhance their experience, and explore places and activities with similar interests.

---
### Expected users

This website is for anyone who wants to plan their trip in ANP. Even kids can view activies/events of their insterest to help plan family trip to ANP. 

---
### Data Collection

**Wicked Acadia** will based on data from [National Park Service's API](https://www.nps.gov/subjects/developer/api-documentation.htm). API offers data and content about National Parks, and related to each park it offers data about events, places, thingstodo, alert, vs... The data will be taken from API accordingly. 

---

### Database schema 

![Database Schema](/static//images/capstone1-schema.jpg)

This database schema is designed to store information about users and their favorite places to visit, events, and activities. The schema consists of several tables, each with its own purpose.

The users table stores information about website users, such as their username, email, and password. This table will likely be populated with data as users register on the website.

The favorites table stores information about a user's favorite places to visit, events, and activities. This table has a category column that indicates which category the favorite belongs to,  so we can allow users to view saved items by categories later and an item_id column that is a foreign key to the appropriate category table (i.e., places_to_visit, events, or activities) based on the value of the category column. This table will be populated with data as users add favorites to their lists.

Overall, this database schema is designed to store and manage data related to users and their favorite places to visit, events, and activities on the website. It enables the website to retrieve and display relevant data to users, as well as store user preferences and track their interactions with the site.

---

### API Errors

In case of an API error, we will use the try and catch method to handle the error gracefully. This method allows us to execute code that might cause an error within a try block, and then handle the error within a catch block.

If an error occurs, we will view a 404 page to the user if necessary. This will inform the user that the requested data is not available at the moment and provide them with an appropriate error message.

---

### Sensitive Data Storage

Only sensitive info that wil saved in database is user's password and it will be hashed using Bcrypt.

---

### User Flow

Wicked Acadia aims to provide a welcoming and user-friendly homepage that is easy to navigate. The homepage will contain brief information about Acadia National Park (ANP) along with quick links to visitor centers and up-to-date alerts to stay informed.

Users will have access to three primary data categories that will assist them in planning their trip to ANP. These categories will be accessible through the navbar, and each page will provide users with the ability to browse and explore relevant information. Additionally, users will be able to save their preferred data to view later.

Overall, Wicked Acadia strives to create a positive user experience by providing easy access to information about ANP and convenient tools to plan and organize a visit.




