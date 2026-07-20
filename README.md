## TODO: (not necessarily in order)

### Infrastructure
1. set up raid drives on server comp
2. set up ddclient to handle dynamic dns


### Feature Wishlist
1. implement 2fa on admin site
   
   https://github.com/jazzband/django-two-factor-auth
2. implement analytics
   
   https://github.com/jazzband/django-analytical
   
    a. metrics view in admin site
3. figure out post ranking with analytics
4. endless pagination for post list view
   
   https://github.com/shtalinberg/django-el-pagination
5. Create custom module for robots.txt that stores content in the database and autpmatically pulls a new list when data gets stale, ~1 month

    a. get updated list of ai robots from this repo

       https://github.com/ai-robots-txt/ai.robots.txt/tree/main

       tested on script to auto pull
6. tags pages need fleshing out. currently not exposed on site and only handled internally
7. customize 404 page

   https://learndjango.com/tutorials/customizing-django-404-and-500-error-pages
8. implement the admin file browser
   
   https://django-filebrowser.readthedocs.io/en/latest/quickstart.html