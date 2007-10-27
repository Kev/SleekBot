#/bin/sh
#This runner script is useful for keeping a bot up to date and running.
#When running from this script, you can issue a /die to the bot and have
# it perform a clean restart from scratch with the latest version.
echo "If you want to pass parameters, please wrap them in quotes."
while true;
	do
	if [ -x `which svn` ]
		then
		svn up
	fi
	./sleekbot.py $1
done