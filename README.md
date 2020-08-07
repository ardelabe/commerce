# commerce

# COMMERCE

# 0. INTRODUCTION
This project follows the specifications of problem set 2 of cs50w (edx) - and the full funcions developed can be obtained in this page: https://cs50.harvard.edu/web/2020/projects/2/commerce/
The next topics are particular registry of the problems that I faced and the way I solved and, also, some notations to remember important things that I figured in the process. 

# 1. MODELS
First, I defined a string name to User and I went to python3 manage.py shell to add data and see some output - it was nice to see those things working.
And "AbstractUser" is a predefined class that exists in django.contrib.auth.models that is VERY useful.
When I tried to compile with a class with a ForeignKey before define the class witch this key as Primary I got an error of "not defined". 
Quando cria o password pelo py, ele fica com os caracteres originais registrados - IMPORTANTE.
Remember, that with $ sqlite filename.sql is possible to run queryes on terminal. 
Dealing with data in python shell, the id doesn't show up until I saved the data in db. 
With these observations, looks like the django-db relation is working fine. 

# 2. CREATE LISTING
*FIXING MODEL PROBLEMS*
To insert data by web interface, it is needed to register the models in admin.py. The admin interface adds a "s" (for plural) - if the model and the registry in admin.py was in plural - it gets double "s". It's not nice - so keep it in mind. 
I moved the structures in models.py - took me a while to make it work. Seems like it is better to see if the db is working in /admin than SQLite or py-shell. It was working fine in these two but I got errors in /admin. Defining the name that does not figure in class also breaks the website. 
I think I don't understood completely what means "many to many" - maybe I should more search on this topic. 
I made some other changes in models.py.

*WORKING ON CREATE LISTING*
20200729 - I used **data = Product.objects.all()** to take all data of object "Product" form imported model "Product", saved into "data". Took "data" and passed to .html in context, assigning the name "product". In .html I managed this data by inserting attributes of model (.id and .title). At this point, the create.html displays forms to input info to register product and to register auction. 
**attribute: variable inside an object with notation .something** / **method: function inside an object with notation .something()**

# 3. NEW BEGINNING
20200804. This is a second try. I got stuck in my first attempt to make this project work. So, those observations of the first attempt are aplicable.
20200805. I created the models. This time I stayed with the project description and I don't made a product table separated from auction. I dont' know why, but now migration doesn't create a relational table because of the foreign key (users) in auctions. I'm more confidant that it will work better now. With this, requisite **MODELS** where recriated.
20200806. Gave listings.html acess by passing Auction data with **Auction.objects.all()** in views.py. Managed this data with the attribute **.title**. As I had imagined without that extra table with ids, the **CREATE LISTING** worked perfectly. There is one observation: the option to load an image is not developed - I'll return to this later (I have no idea how to implement).

# 4. ACTIVE LISTINGS PAGE
***BUG REPORT*** Sending form without data is crashing the website. 
***Reminder*** Need to put "no image" as alt url to images in html (operate wit .css file).
20200807. For the Active Listings Page task I altered the auctions model to store image url (a default url of the internet was provided). The entire auction data was already passing to Active Listings to display. I copied the code to home (addeded a link in layout to home too). And altered the loop to display the info that the problem asked to.