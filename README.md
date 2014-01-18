# pypodcatcher
## Developpement information
 * Curent version: 0.3 might be slightly buggy
 * License: WTF Public License v2
 * Author: Thomas Maurice <tmaurice59@gmail.com>

## Using the script
Once you've downloaded the script, you can simply invoke
the script via the commandline by typing :
    ./pypodcatcher.py -f feedlist -c config

In the ```<feedlist>``` file, you just have to put
the URLs of the XML podcast feeds, one by line.
The ```<conf>``` file has a very simple syntax, for
exemple if you want to download all the podcast in
a ~/podcast directory you just write:
    Directory ~/podcast

In the file.

## Save formats
You may want to save the podcast according to a specific file
tree within your ~/podcast (or whatever) directory. To do that
you can declare a FileFormat variable in the ```<conf>``` file.
The FileFormat variable is a path which will be appended to the
Directory variable. It will be parsed and the variable part (marked
as %C, %T, %M and so on) will be replaced as it follows:
 * %C : Channel, will be replaced by the radio show name
 * %Y : The year of the podcast
 * %M : The month of the podcast
 * %D : A YYYY-MM-DD datestring
 * %T : The title of the podcast

So for example I want to save my podcasts in the ~/podcast directory,
have a directory per radio broadcast, within this directory sort
the podcasts by year and month and finally save the podcast with the
day it came out plus it's title, my config file will be:

    Directory ~/podcasts
    FileFormat %C/%Y %M/%D %T

As simple as that :)
