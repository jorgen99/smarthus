# installing on a raspberry pi 4 with Ubuntu 20.04 LTS 64bit.

This is a brain dump of what I did to get my Tellstick-Duo up
and running.

I had problems with installing telldus-core from Telldus apt-rpository.
I got error messages about not having support for arm64

So, I downloaded the source and tried to compile it.
http://download.telldus.com/TellStick/Software/telldus-core/telldus-core-2.1.2.tar.gz

Following this guide:
http://developer.telldus.com/wiki/TellStickInstallationSource

libconfuse0 can't be installed in new versions of Ubuntu. At the moment
the current is libconfuse2
    
    sudo apt install build-essential cmake ibftdi1 libftdi-dev libconfuse2 libconfuse-dev
    cmake .
    make

I got some error messages about "pthread" when make was compiling. After
some Googling I found this post. The second link is to the first answer.

https://stackoverflow.com/questions/1620918/cmake-and-libpthread

https://stackoverflow.com/a/29871891/5264

I think the code from the post should go in to the file CMakeLists.txt.
I had some problems with what to replace my_app with and after fiddling
around with cmake and make it finally did build without errors. I'm
not sure why it started to work all of a sudden...

    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_package(Threads REQUIRED)
    target_link_libraries(my_app Threads::Threads)

After compiling was done:

    sudo make install

I copied the code from this repo: conf/telldusd to /etc/init.d/

    sudo cp ./conf/telldusd /etc/init.d/

I had to modify the path to telldusd in the init.d-script to where
telldusd got installed by 'make install'

Create soft links to /etc/init.d/telldusd in the rc{0..6}.d folders

    for i in {0,1,6}; do sudo ln -s /etc/init.d/telldusd /etc/rc$i.d/K20telldusd; done
    for i in {2..5}; do sudo ln -s /etc/init.d/telldusd /etc/rc$i.d/S20telldusd; done

Copy tellstick.conf to /etc

    sudo cp ./conf/tellstick.conf /etc/

Start the daemon

    sudo /etc/init.d/telldusd start

Try turning on and off one of the configured devices to see if it's working:

    tdtool --on <device_id_from_tellstick.conf>
    tdtool --off <device_id_from_tellstick.conf>

## Installing tellcore-py

    pip install tellcore-py

install flask

    pip install flask

run flask app

    python smarthus.py

run event listener app

    python tellstick_events.py

