## TODO: (not necessarily in order)

### Code Review
1. √ revive the contact page to better obfuscate email from bot scrapers


### Fixes
1. ckeditor 5 available https://pypi.org/project/django-ckeditor-5/
2. √ django debug toolbar setup https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#

### Infrastructure
1. √ create real database for posts
2. √ create file system database for uploaded files for blog posts

   https://github.com/jschneier/django-storages
   
    a. minio for file storage?
   
    https://django-minio-storage.readthedocs.io/en/latest/
   
    https://docs.min.io/community/minio-object-store/operations/checklists.html
   
    https://blog.marco.ninja/notes/technology/django/django-local-s3/
4. set up raid drives on server comp?
5. √ figure out a good domain name and buy it

### MVP
1. √ update blog post text type to allow uploaded images
   - out ~tinymce~ - can't get image uploading working
2. √ look into blog features created by zinnia

   https://github.com/Fantomas42/django-blog-zinnia
   --not interested
4. √ create real admin user
5. √ create post list view


### Content
1. write first posts:

   a. √ rebuilding my 3d printer? - Almost done, want review from alex

   b. building this website?

   c. about me page
2. √ revamp contact page

    a. √ include captcha
       https://github.com/django-recaptcha/django-recaptcha

    b. clean up styles
   
    √ Change contact page to mailto link "`<a href="mailto:john@example.com">John</a>`"
3. √ refine banner styles
4. √ reconsider if icons are desired.

    a. ~~maybe make an image cropping tool in the creation form and just have one uploaded image?~~
   
    b. banners and icons as the same image but styled differently?
5. √ refine post view style
6. √ refine post short text length
7. √ Make footer
   
    a. Free icons with attribution

    https://www.flaticon.com/packs/social-16


### Stretch Goals
1. implement 2fa on admin site
   
   https://github.com/jazzband/django-two-factor-auth
2. implement analytics
   
   https://github.com/jazzband/django-analytical
   
    a. metrics view in admin site
3. figure out post ranking with analytics
4. endless pagination for post list view
   
   https://github.com/shtalinberg/django-el-pagination
5. Include robots.txt to block AI training crawlers

    a. get updated list of ai robots from this repo

       https://github.com/ai-robots-txt/ai.robots.txt/tree/main

       tested on script to auto pull
    b. need to append sitemap to list
6. tags pages need fleshing out. currently not exposed on site and only handled internally
7. customize 404 page

   https://learndjango.com/tutorials/customizing-django-404-and-500-error-pages