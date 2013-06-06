#
# Regular cron jobs for the teapot package
#
0 4	* * *	root	[ -x /usr/bin/teapot_maintenance ] && /usr/bin/teapot_maintenance
