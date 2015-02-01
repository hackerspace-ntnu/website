# Infoscreen setup at raspberry pi

We used the a [guide](http://blogs.wcode.org/2013/09/howto-boot-your-raspberry-pi-into-a-fullscreen-browser-kiosk/) for this setup.

First we need to install packages needed:

	$ sudo apt-get update
	$ sudo apt-get dist-upgrade
	$ sudo apt-get install matchbox chromium x11-xserver-utils ttf-mscorefonts-installer xwit sqlite3 libnss3
	$ sudo reboot
	
To detect resolution we set the frambuffer up by adding this to /boot/config.txt

	# 1900x1200 at 32bit depth, DMT mode
	disable_overscan=1
	framebuffer_width=1900
	framebuffer_height=1200
	framebuffer_depth=32
	framebuffer_ignore_alpha=1
	hdmi_pixel_encoding=1
	hdmi_group=2
	
Add this to /etc/rc.local to detect screen and start the kiosk.

	# Wait for the TV-screen to be turned on...
	while ! $( tvservice --dumpedid /tmp/edid | fgrep -qv 'Nothing written!' ); do
		bHadToWaitForScreen=true;
		printf "===> Screen is not connected, off or in an unknown mode, waiting for it to become available...\n"
		sleep 1;
	done;

	printf "===> Screen is on, extracting preferred mode...\n"
	_DEPTH=32;
	eval $( edidparser /tmp/edid | fgrep 'preferred mode' | tail -1 | sed -Ene 's/^.+(DMT|CEA) \(([0-9]+)\) ([0-9]+)x([0-9]+)[pi]? @.+/_GROUP=\1;_MODE=\2;_XRES=\3;_YRES=\4;/p' );

	printf "===> Resetting screen to preferred mode: %s-%d (%dx%dx%d)...\n" $_GROUP $_MODE $_XRES $_YRES $_DEPTH
	tvservice --explicit="$_GROUP $_MODE"
	sleep 1;

	printf "===> Resetting frame-buffer to %dx%dx%d...\n" $_XRES $_YRES $_DEPTH
	fbset --all --geometry $_XRES $_YRES $_XRES $_YRES $_DEPTH -left 0 -right 0 -upper 0 -lower 0;
	sleep 1;

	printf "===> Start Kiosk \n"
	
	# Start the kiosk
	su - pi -c 'startx' &
	
Then you need to add this to the file .xinitrc in /home/pi.


	#!/bin/sh
	while true; do

		# Clean up previously running apps, gracefully at first then harshly
		killall -TERM chromium 2>/dev/null;
		killall -TERM matchbox-window-manager 2>/dev/null;
		sleep 2;
		killall -9 chromium 2>/dev/null;
		killall -9 matchbox-window-manager 2>/dev/null;

		# Clean out existing profile information
		rm -rf /home/pi/.cache;
		rm -rf /home/pi/.config;
		rm -rf /home/pi/.pki;

		# Generate the bare minimum to keep Chromium happy!
		mkdir -p /home/pi/.config/chromium/Default
		sqlite3 /home/pi/.config/chromium/Default/Web\ Data "CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR); INSERT INTO meta VALUES('version','46'); CREATE TABLE keywords (foo INTEGER);";

		# Disable DPMS / Screen blanking
		xset -dpms
		xset s off

		# Reset the framebuffer's colour-depth
		fbset -depth $( cat /sys/module/*fb*/parameters/fbdepth );
	
		# Hide the cursor (move it to the bottom-right, comment out if you want mouse interaction)
		xwit -root -warp $( cat /sys/module/*fb*/parameters/fbwidth ) $( cat /sys/module/*fb*/parameters/fbheight )
	
		# Start the window manager (remove "-use_cursor no" if you actually want mouse interaction)
		matchbox-window-manager -use_titlebar no -use_cursor no &
	
		# Start the browser (See http://peter.sh/experiments/chromium-command-line-switches/)
		chromium --disable-translate --app=http://hackerspace.idi.ntnu.no/infoscreen/bigscreen/index.html
	
	done;

Then restart the pi and you are ready to go.
