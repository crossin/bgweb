from ragendja.settings_post import settings

settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'content/ga.js',
    'content/bundle.js',                   
    
    # ...
)
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',

    
    'content/layout.css',
    
    # ...
)