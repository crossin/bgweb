# Introduction #
everytime I try to revise sth related with media stuff, I spend a lot of time read the manual first,
write some code, and succeed. then after a while I foget all. today this thing happened again.
so I will write the detailed explanation here in case I forget next time.
> | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | || | | | | | | | | | | | | | | | | | ||
|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|


&lt;link rel="stylesheet" type="text/css" href="{{ MEDIA\_URL }}combined-ltr.css" /&gt;




&lt;script type="text/javascript" src="{{ MEDIA\_URL }}combined-{{ LANGUAGE\_CODE }}.js"&gt;



&lt;/script&gt;




&lt;script type="text/javascript" src="{{ MEDIA\_URL }}combined-content.js"&gt;



&lt;/script&gt;


| after rendering | | | | | | | | | | | | | | | | | | | | |  | | | | | | | | | | | | | | | | | | ||



&lt;link rel="stylesheet" type="text/css" href="/generated\_media/media/1/content-xlayout.css" /&gt;




&lt;script type="text/javascript" src="/generated\_media/media/1/combined-en.js"&gt;



&lt;/script&gt;




&lt;script type="text/javascript" src="/generated\_media/media/1/combined-content.js"&gt;



&lt;/script&gt;



so the LANGUAGE\_CODE is set in the settings.py as en %%% the MEDIA\_URL is /generated\_media/media/1/

actually combine the media is a good stuff should be done, but this media util actually makes one hardly understood
> | specified combine media | | | | | | | | | | | | | | | | | | | || | | | | | | | | | | | | | | | | | ||
|:------------------------|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|:|
COMBINE\_MEDIA = {
> > 'combined-%(LANGUAGE\_DIR)s.js': (
      1. See documentation why site\_data can be useful:
      1. http://code.google.com/p/app-engine-patch/wiki/MediaGenerator
      1. .site\_data.js',
      1. jquery.min.js',
> > ),
> > 'combined-%(LANGUAGE\_DIR)s.css': (
      1. global/look.css',
> > ),
settings.add\_app\_media( 'combined-%(LANGUAGE\_DIR)s.css' , 'content/layout.css')

> | generated combined media  | | | | | | | | | | | | | | | | | | | |  | | | | | | | | | | | | | | | | | | ||
combined-ltr.css
combined-rtl.css
combined-ltr.js
combined-rtl.js

one can never  understood %(LANGUAGE\_DIR)s the fuck how it functions actually it generate two files for this combine, cool down, cool down, maybe when in i18 applications we need different .......
yes maybe it's useful


see figured it again.WTF


# Details #

# Combine media files
COMBINE\_MEDIA = {
  1. Create a combined JS file which is called "combined-en.js" for English,
  1. "combined-de.js" for German, and so on
> 'combined-%(LANGUAGE\_CODE)s.js': (
    1. Integrate bla.js from "myapp/media" folder
    1. You don't write "media" because that folder is used automatically
> > 'myapp/bla.js',
    1. Integrate morecode.js from "media" under project root folder
> > 'global/morecode.js',

> ),
  1. Create a combined CSS file which is called "combined-ltr.css" for
  1. left-to-right text direction
> 'combined-%(LANGUAGE\_DIR)s.css': (
> > 'myapp/style.css',
    1. Load layout for the correct text direction
> > 'global/layout-%(LANGUAGE\_DIR)s.css',

> ),
}

continue to find what the stupid util do on 'helping' us.
##### inner settings related with media #####
MEDIA\_URL = '/media/%d/'
ADMIN\_MEDIA\_PREFIX = '%sadmin\_media/'

# Add start markers, so apps can insert JS/CSS at correct position
def add\_app\_media(combine, 