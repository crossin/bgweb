#Make the current promotion system more interesting & useful

# Introduction #
1.  randomly record user visits from xiaonei  then promote them to the Ad image.
2.  Allow change the Ad picture for specific events


# Details #

//how it works
Interesting Part
1. user visit from xiaonei will be randomly recorded and add to a table
2. the table will currently have a fixed size about 10 people ids.
3. cron deamons will spider these user's avatars and compose them with default background
4. the ad display will always get its display from dynamic urls

userful part // allow for Ad picture change for specific
1. there must be a table holding the images
2. have admin console to enable this change .

Ad system currently asks for these changes.