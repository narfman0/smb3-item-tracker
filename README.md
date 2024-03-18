smb3itemtracker
===============

UI to handle tracking inventory in SMB3

All the code and assets were made by Lui_!
narfman0 just uselessly packaged it :)

Installation
------------

Navigate to the most recent versioned release here:

https://github.com/narfman0/smb3-item-tracker/tags

Download the zip and extract to your favorite directory.

Configuration
-------------

If a `settings.ini` file exists alongside the exe, it will be read to configure
the tool to the user's liking. The first line must start with `[default]`

Available settings:

`big_buttons` default=false. In this UI, we can use the bigger sized buttons for
everything!

`skip_prompts` default=true. We can warn user's when restarting runs if they
really want to remove everything.

`starting_items` default=. We can prepopulate the UI with a comma separated
list of items we for sure get, for example, in warpless, we can put
`whistle,star,pwing` since we always get those items in that order.

See the settings.ini file in project or this a example:

```
[default]
big_buttons = false
skip_prompts = true
starting_items = whistle,star,pwing
```

License
-------

Copyright (c) 2023 Lui_, narfman0

See LICENSE for details
