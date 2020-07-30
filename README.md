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




Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a 
A title for the listing, 
B  a text-based description, 
C and what the starting bid should be. 
D Users should also optionally be able to provide a URL for an image for the listing and
E /or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
