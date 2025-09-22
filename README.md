## TODO: (note necessarily in order)

### Infrastructure
1. create real database for posts
2. create file system database for uploaded files for blog posts

   https://github.com/jschneier/django-storages
   
    a. minio for file storage?
   
    https://django-minio-storage.readthedocs.io/en/latest/
   
    https://docs.min.io/community/minio-object-store/operations/checklists.html
   
    https://blog.marco.ninja/notes/technology/django/django-local-s3/
4. set up raid drives on server comp?
5. figure out a good domain name and buy it

### MVP
1. √ update blog post text type to allow uploaded images
   out ~tinymce~ - can't get image uploading working
2. √ look into blog features created by zinnia

   https://github.com/Fantomas42/django-blog-zinnia
   --not interested
4. create real admin user
5. √ create post list view


### Content
1. write first posts:

   a. rebuilding my 3d printer?

   b. building this website?

   c. about me page
3. √ revamp contact page
    a. include captcha
       https://github.com/django-recaptcha/django-recaptcha
    b. clean up styles~~ scrap contact page
   
    √ Change contact page to mailto link "`<a href="mailto:john@example.com">John</a>`"
4. √ refine banner styles
5. √ reconsider if icons are desired.

    a. maybe make an image cropping tool in the creation form and just have one uploaded image?
   
    b. banners and icons as the same image but styled differently?
7. √ refine post view style
8. refind post short text length
9. Make footer

### Stretch Goals
1. implement 2fa on admin site
   
   https://github.com/jazzband/django-two-factor-auth
3. implement analytics
   
   https://github.com/jazzband/django-analytical
   
    a. metrics view in admin site
5. figure out post ranking with analytics
6. endless pagination for post list view
   
   https://github.com/shtalinberg/django-el-pagination
