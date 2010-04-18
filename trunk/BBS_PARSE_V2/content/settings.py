from ragendja.settings_post import settings

settings.add_app_media('combined-content.js',
    #'content/ga.js',
    'content/bundle.js', 
    #'content/scripts/jquery.timeago.js',              
    
    # ...
)
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css', 
    'content/layout.css',
)

settings.add_app_media('content-xlayout.css',
    'content/xlayout.css',
)