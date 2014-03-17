smarthus
========

Control lights with a Tellstick Duo, Angular, Bootstrap and Flask

I wanted to play with the Tellstick Duo and at the same time learn
some Angular and Bootstrap.

I found [tellcore-py] (https://github.com/erijo/tellcore-py) a
Python wrapper to Telldus Core, so I needed a lightweight Python
web framework that could talk to the Tellstick Duo. After a bit of
Googeling I found my way to [Flask] (http://flask.pocoo.org/docs/).

__Disclamer:__
This project was slapped together in an afternoon. Seasoned Python,
Angular and Bootstrap developers may hurt their eyes looking at
this code. Hopefully the code will improve over time. Yes, I know
you should not have all the code in one html-file... :)


Setting up
----------
I've been using Linux Mint while developing. So, if you're using
another OS you're going to have to do some Googeling. Of course
you don't have to install node, npm and finally bower just to
install Angular and Bootstrap. Just download them manually and
update the links in the code in that case.

### Telldus Core ###
Download and install [Telldus Core Library]
(http://developer.telldus.com/wiki/TellStickInstallationUbuntu)


### tellcore-py ###
Install the [Python wrapper]
(https://github.com/erijo/tellcore-py) for Telldus Core.

    pip install tellcore-py

If you don't have pip installed:

    sudo apt-get install python-pip

### Flask ###
Either have a look at the detailed installation instructions for
[Flask] (http://flask.pocoo.org/docs/), or just:

    pip install Flask

### Angular and Bootstrap ###
Install [Bower] (http://bower.io) if you don't have it and (node
if you don't have that).

    npm -g install bower

Then use it to install [AngularJS] (http://angularjs.org/) and
[Bootstrap] (http://getbootstrap.com/)

    bower install angular
    bower install bootstrap

### Configuring the receivers ###
I found the instructions on how to set up [tellstick.conf]
(http://developer.telldus.com/wiki/TellStick_conf) a bit dry, but
after a bit of trial and error I was able to use `tdtool` to
control my receivers.

After listing the devices in tellstick.conf i used tdtool to learn
the receiver to listen to the correct "house" and "unit". So for
example I chose to use the house code "22222001" and unit "1" for
the first receiver unit "2" for the second and so on.

    device {
      id = 1
      name = "Office Lamp"
      protocol = "arctech"
      model = "selflearning-switch:nexa"
      parameters {
        house = "22222001"
        unit = "1"
      }
    }

Everytime you change tellstick.conf you have to restart the
Telldus daemon:

    sudo /etc/init.d/telldusd restart

I've used [Nexa Receivers]
(http://www.nexa.se/PE3-komplett-set.htm) and they enter a short
learning period when you put the receiver into the wall socket.
During that period run `tdtool` to learn the reciver. For instance
to learn the device with id = 1 that it should listen to the house
code "22222001" and unit = "1" as specified in the tellstick.conf
above, run:

    tdtool --learn 1

You should now be able to switch the receiver on and off using:

    tdtool --on 1
    tdtool --off 1

The Nexa receivers can listen to up to three codes so you can still
learn them to use the remote that is included. This way you can
operate the receiver both from the remote and the Tellstick Duo.

Running the app
---------------
Just start the Flask server by running:

    python smarthus.py

and point your browser to http://localhost:5000
