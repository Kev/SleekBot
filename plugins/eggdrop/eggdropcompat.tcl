#These are variables set by eggdrop:
#Value: the current nickname the bot is using (for example: "Valis", "Valis0", etc.)
set botnick "erk"
#Value: the current nick!user@host that the server sees (for example: "Valis!valis@crappy.com")
set botname "erk!erk@erk"
#Value: the current server's real name (what server calls itself) and port bot is connected to (for example: "irc.math.ufl.edu:6667") Note that this does not nececerilly match the servers internet address.
set server "fakeircmucserver"
#Value: the current server's internet address (hostname or IP) and port bot is connected to. This will correspond to the entry in server list (for example: "eu.undernet.org:6667"). Note that this does not necessarily match the name server calls itself.
set serveraddress "fake.address:6667"
#Value: current bot version "1.1.2+pl1 1010201 pl1"; first item is the text version, second item is a numerical version, and any following items are the names of patches that have been added
set version "1.6.0 1060000"
#Value: the current numeric bot version (for example: "1010201"). Numerical version is in the format of "MNNRRPP", where:
#    M major release number
#   NN minor release number
#    RR sub-release number
#    PP patch level for that sub-release
set numversion 1060000
#Value: the unixtime value for when the bot was started
set uptime 10
#Value: the unixtime value for when the bot connected to its current server
set server-online 1
#Value: the last command binding which was triggered. This allows you to identify which command triggered a Tcl proc.
set lastbind ""
#Value: 1 if bot's nick is juped(437); 0 otherwise
set isjuped 0
#Value: the value of the HANDLEN define in src/eggdrop.h
set handlen ""
#Value: the filename of the config file Eggdrop is currently using
set config "eggdropbot.py"

### These initial functions are the ones which eggdrop provides and which we therefore must do too
### The complete list of available eggdrop commands is available from http://www.eggheads.org/support/egghtml/1.6.18/tcl-commands.html - by the time we're finished here, hopefully we'll implement them all
set eggdrop_time_bindings [list]
set eggdrop_join_bindings [list]
set eggdrop_part_bindings [list]
set eggdrop_msg_bindings [list]
set eggdrop_pub_bindings [list]
set eggdrop_pubm_bindings [list]
set eggdrop_topc_bindings [list]
set eggdrop_kick_bindings [list]
set eggdrop_utimer [list]
set eggdrop_timer [list]

set eggdrop_message_queue [list]


###1. Output commands

#putserv <text> [options]
#    Description: sends text to the server, like '.dump' (intended for direct server commands); output is queued so that the bot won't flood itself off the server.
#    Options:
#        -next: push messages to the front of the queue
#        -normal: no effect
#    Returns: nothing
#    Module: server
proc putserv {text args} {
	puts "putserv: '$text $args'"
	global eggdrop_message_queue
	lappend eggdrop_message_queue $text
}

#puthelp <text> [options]
#    Description: sends text to the server, like 'putserv', but it uses a different queue intended for sending messages to channels or people.
#    Options:
#        -next: push messages to the front of the queue
#        -normal: no effect
#    Returns: nothing
#    Module: server
proc puthelp {text args} {
	puts "puthelp: '$text $args'"
	global eggdrop_message_queue
	lappend eggdrop_message_queue $text
}

#putquick <text> [options]
#    Description: sends text to the server, like 'putserv', but it uses a different (and faster) queue.
#    Options:
#        -next: push messages to the front of the queue
#        -normal: no effect
#    Returns: nothing
#    Module: server
proc putquick {text args} {
	puts "putquick: '$text $args'"
	global eggdrop_message_queue
	lappend eggdrop_message_queue $text
}
#putkick <channel> <nick,nick,...> [reason]
#    Description: sends kicks to the server and tries to put as many nicks into one kick command as possible.
#    Returns: nothing
#    Module: irc
proc putkick {channel nicks reason} {
	puts "putkick: '$channel $nicks $reason'"
}
#putlog <text>
#    Description: sends text to the bot's logfile, marked as 'misc' (o)
#    Returns: nothing
#    Module: core
proc putlog {text} {
	puts "putlog: '$text'"
}
#putcmdlog <text>
#    Description: sends text to the bot's logfile, marked as 'command' (c)
#    Returns: nothing
#    Module: core
proc putcmdlog {text} {
	puts "putcmdlog: '$text'"
}
#putxferlog <text>
#    Description: sends text to the bot's logfile, marked as 'file-area' (x)
#    Returns: nothing
#    Module: core
proc putxferlog {text} {
	puts "putxferlog: '$text'"
}

#putloglev <level(s)> <channel> <text>
#    Description: sends text to the bot's logfile, tagged with all of the valid levels given. Use "*" to indicate all log levels.
#    Returns: nothing
#    Module: core
proc putloglev {level channel text} {
  puts "log $level $channel : $text"
}

#dumpfile <nick> <filename>
#    Description: dumps file from the help/text directory to a user on IRC via msg (one line per msg). The user has no flags, so the flag bindings won't work within the file.
#    Returns: nothing
#   Module: core
proc dumpfile {nick filename} {
	puts "dumpfile $nick $filename"
}

#queuesize [queue]
#    Returns: the number of messages in all queues. If a queue is specified, only the size of this queue is returned. Valid queues are: mode, server, help.
#    Module: server
proc queuesize {queue} {
	puts "queuesize $queue"
	return 0
	#FIXME - parameters
}

#clearqueue <queue>
#    Description: removes all messages from a queue. Valid arguments are: mode, server, help, or all.
#    Returns: the number of deleted lines from the specified queue.
#    Module: server
proc clearqueue {queue} {
	puts "clearqueue $queue"
	return 0
}

### 2. User record manipulation commands

#    countusers
#        Returns: number of users in the bot's database
#        Module: core
#    validuser <handle>
#        Returns: 1 if a user by that name exists; 0 otherwise
#        Module: core
#    finduser <nick!user@host>
#        Description: finds the user record which most closely matches the given nick!user@host
#        Returns: the handle found, or "*" if none
#        Module: core
#    userlist [flags]
#        Returns: a list of users on the bot. You can use the flag matching system here ([global]{&/|}[chan]{&/|}[bot]). '&' specifies "and"; '|' specifies "or".
#        Module: core
#    passwdok <handle> <pass>
#        Description: checks the password given against the user's password. Check against the password "" (a blank string) or "-" to find out if a user has no password set.
#        Returns: 1 if the password matches for that user; 0 otherwise
#        Module: core
#    getuser <handle> <entry-type> [extra info]
#        Description: an interface to the new generic userfile support. Valid entry types are:
#            BOTFL
#            returns the current bot-specific flags for the user (bot-only)
#            BOTADDR
#            returns a list containing the bot's address, telnet port, and relay port (bot-only)
#            HOSTS
#            returns a list of hosts for the user
#            LASTON
#            returns a list containing the unixtime last seen and the last seen place. LASTON #channel returns the time last seen time for the channel or 0 if no info exists.
#            INFO
#            returns the user's global info line
#            XTRA
#            returns the user's XTRA info
#            COMMENT
#            returns the master-visible only comment for the user
#            EMAIL
#            returns the user's e-mail address
#            URL
#            returns the user's url
#            HANDLE
#            returns the user's handle as it is saved in the userfile
#            PASS
#            returns the user's encrypted password
#        Returns: info specific to each entry-type
#        Module: core
#    setuser <handle> <entry-type> [extra info]
#        Description: this is the counterpart of getuser. It lets you set the various values. Other then the ones listed below, the entry-types are the same as getuser's.
#            HOSTS
#            if used with no third arg, all hosts for the user will be cleared. Otherwise, *1* hostmask is added :P
#            LASTON
#            This setting has 3 forms. "setuser <handle> LASTON <unixtime> <place>" sets global LASTON time, "setuser <handle> LASTON <unixtime>" sets global LASTON time (leaving the place field empty), and "setuser <handle> LASTON <unixtime> <channel>" sets a users LASTON time for a channel (if it is a valid channel).
#            PASS
#            sets a users password (no third arg will clear it)
#        Returns: nothing
#        Module: core
#    chhandle <old-handle> <new-handle>
#        Description: changes a user's handle
#        Returns: 1 on success; 0 if the new handle is invalid or already used, or if the user can't be found
#        Module: core
#    chattr <handle> [changes [channel]]
#        Description: changes the attributes for a user record, if you include any. Changes are of the form '+f', '-o', '+dk', '-o+d', etc. If changes are specified in the format of <changes> <channel<, the channel-specific flags for that channel are altered. You can now use the +o|-o #channel format here too.
#        Returns: new flags for the user (if you made no changes, the current flags are returned). If a channel was specified, the global AND the channel-specific flags for that channel are returned in the format of globalflags|channelflags. "*" is returned if the specified user does not exist.
#        Module: core
#    botattr <handle> [changes [channel]]
#        Description: similar to chattr except this modifies bot flags rather than normal user attributes.
#        Returns: new flags for the bot (if you made no changes, the current flags are returned). If a channel was specified, the global AND the channel-specific flags for that channel are returned in the format of globalflags|channelflags. "*" is returned if the specified bot does not exist.
#        Module: core
#    matchattr <handle> <flags> [channel]
#        Returns: 1 if the specified user has the specified flags; 0 otherwise
#        Module: core
#    adduser <handle> [hostmask]
#        Description: creates a new user entry with the handle and hostmask given (with no password and the default flags)
#        Returns: 1 if successful; 0 if the handle already exists
#        Module: core
#    addbot <handle> <address>
#        Description: adds a new bot to the userlist with the handle and bot address given (with no password and no flags)
#        Returns: 1 if successful; 0 if the bot already exists
#        Module: core
#    deluser <handle>
#        Description: attempts to erase the user record for a handle
#        Returns: 1 if successful, 0 if no such user exists
#        Module: core
#    delhost <handle> <hostmask>
#        Description: deletes a hostmask from a user's host list
#        Returns: 1 on success; 0 if the hostmask (or user) doesn't exist
#        Module: core
#    addchanrec <handle> <channel>
#        Description: adds a channel record for a user
#        Returns: 1 on success; 0 if the user or channel does not exist
#        Module: channels
#    delchanrec <handle> <channel>
#        Description: removes a channel record for a user. This includes all associated channel flags.
#        Returns: 1 on success; 0 if the user or channel does not exist
#        Module: channels
#    haschanrec <handle> <channel>
#        Returns: 1 if the given handle has a chanrec for the specified channel; 0 otherwise
#        Module: channels
#    getchaninfo <handle> <channel>
#        Returns: info line for a specific channel (behaves just like 'getinfo')
#        Module: channels
#    setchaninfo <handle> <channel> <info>
#        Description: sets the info line on a specific channel for a user. If info is "none", it will be removed.
#        Returns: nothing
#        Module: channels
#    newchanban <channel> <ban> <creator> <comment> [lifetime] [options]
#        Description: adds a ban to the ban list of a channel; creator is given credit for the ban in the ban list. lifetime is specified in minutes. If lifetime is not specified, ban-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent ban.
#        Options:
#            sticky: forces the ban to be always active on a channel, even with dynamicbans on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    newban <ban> <creator> <comment> [lifetime] [options]
#        Description: adds a ban to the global ban list (which takes effect on all channels); creator is given credit for the ban in the ban list. lifetime is specified in minutes. If lifetime is not specified, global-ban-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent ban.
#        Options:
#            sticky: forces the ban to be always active on a channel, even with dynamicbans on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    newchanexempt <channel> <exempt> <creator> <comment> [lifetime] [options]
#        Description: adds a exempt to the exempt list of a channel; creator is given credit for the exempt in the exempt list. lifetime is specified in minutes. If lifetime is not specified, exempt-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent exempt. The exempt will not be removed until the corresponding ban has been removed. For timed bans, once the time period has expired, the exempt will not be removed until the corresponding ban has either expired or been removed.
#        Options:
#            sticky: forces the exempt to be always active on a channel, even with dynamicexempts on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    newexempt <exempt> <creator> <comment> [lifetime] [options]
#        Description: adds a exempt to the global exempt list (which takes effect on all channels); creator is given credit for the exempt in the exempt list. lifetime is specified in minutes. If lifetime is not specified, exempt-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent exempt. The exempt will not be removed until the corresponding ban has been removed.
#        Options:
#            sticky: forces the exempt to be always active on a channel, even with dynamicexempts on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    newchaninvite <channel> <invite> <creator> <comment> [lifetime] [options]
#        Description: adds a invite to the invite list of a channel; creator is given credit for the invite in the invite list. lifetime is specified in minutes. If lifetime is not specified, invite-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent invite. The invite will not be removed until the channel has gone -i.
#        Options:
#            sticky: forces the invite to be always active on a channel, even with dynamicinvites on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    newinvite <invite> <creator> <comment> [lifetime] [options]
#        Description: adds a invite to the global invite list (which takes effect on all channels); creator is given credit for the invite in the invite list. lifetime is specified in minutes. If lifetime is not specified, invite-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent invite. The invite will not be removed until the channel has gone -i.
#        Options:
#            sticky: forces the invite to be always active on a channel, even with dynamicinvites on
#            none: no effect
#        Returns: nothing
#        Module: channels
#    stick <banmask> [channel]
#        Description: makes a ban sticky, or, if a channel is specified, then it is set sticky on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    unstick <banmask> [channel]
#        Description: makes a ban no longer sticky, or, if a channel is specified, then it is unstuck on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    stickexempt <exemptmask> [channel]
#        Description: makes an exempt sticky, or, if a channel is specified, then it is set sticky on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    unstickexempt <exemptmask> [channel]
#        Description: makes an exempt no longer sticky, or, if a channel is specified, then it is unstuck on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    stickinvite <invitemask> [channel]
#        Description: makes an invite sticky, or, if a channel is specified, then it is set sticky on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    unstickinvite <invitemask> [channel]
#        Description: makes an invite no longer sticky, or, if a channel is specified, then it is unstuck on that channel only.
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killchanban <channel> <ban>
#        Description: removes a ban from the ban list for a channel
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killban <ban>
#        Description: removes a ban from the global ban list
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killchanexempt <channel> <exempt>
#        Description: removes an exempt from the exempt list for a channel
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killexempt <exempt>
#        Description: removes an exempt from the global exempt list
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killchaninvite <channel> <invite>
#        Description: removes an invite from the invite list for a channel
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    killinvite <invite>
#        Description: removes an invite from the global invite list
#        Returns: 1 on success; 0 otherwise
#        Module: channels
#    ischanjuped <channel>
#        Returns: 1 if the channel is juped, and the bot is unable to join; 0 otherwise
#        Module: channels
#    isban <ban> [channel]
#        Returns: 1 if the specified ban is in the global ban list; 0 otherwise. If a channel is specified, that channel's ban list is checked as well.
#        Module: channels
#    ispermban <ban> [channel]
#        Returns: 1 if the specified ban is in the global ban list AND is marked as permanent; 0 otherwise. If a channel is specified, that channel's ban list is checked as well.
#        Module: channels
#    isexempt <exempt> [channel]
#        Returns: 1 if the specified exempt is in the global exempt list; 0 otherwise. If a channel is specified, that channel's exempt list is checked as well.
#        Module: channels
#    ispermexempt <exempt> [channel]
#        Returns: 1 if the specified exempt is in the global exempt list AND is marked as permanent; 0 otherwise. If a channel is specified, that channel's exempt list is checked as well.
#        Module: channels
#    isinvite <invite> [channel]
#        Returns: 1 if the specified invite is in the global invite list; 0 otherwise. If a channel is specified, that channel's invite list is checked as well.
#        Module: channels
#    isperminvite <invite> [channel]
#        Returns: 1 if the specified invite is in the global invite list AND is marked as permanent; 0 otherwise. If a channel is specified, that channel's invite list is checked as well.
#        Module: channels
#    isbansticky <ban> [channel]
#        Returns: 1 if the specified ban is marked as sticky in the global ban list; 0 otherwise. If a channel is specified, that channel's ban list is checked as well.
#        Module: channels
#    isexemptsticky <exempt> [channel]
#        Returns: 1 if the specified exempt is marked as sticky in the global exempt list; 0 otherwise. If a channel is specified, that channel's exempt list is checked as well.
#        Module: channels
#    isinvitesticky <invite> [channel]
#        Returns: 1 if the specified invite is marked as sticky in the global invite list; 0 otherwise. If a channel is specified, that channel's invite list is checked as well.
#        Module: channels
#    matchban <nick!user@host> [channel]
#        Returns: 1 if the specified nick!user@host matches a ban in the global ban list; 0 otherwise. If a channel is specified, that channel's ban list is checked as well.
#        Module: channels
#    matchexempt <nick!user@host> [channel]
#        Returns: 1 if the specified nick!user@host matches an exempt in the global exempt list; 0 otherwise. If a channel is specified, that channel's exempt list is checked as well.
#        Module: channels
#    matchinvite <nick!user@host> [channel]
#        Returns: 1 if the specified nick!user@host matches an invite in the global invite list; 0 otherwise. If a channel is specified, that channel's invite list is checked as well.
#        Module: channels
#    banlist [channel]
#        Returns: a list of global bans, or, if a channel is specified, a list of channel-specific bans. Each entry is a sublist containing: hostmask, comment, expiration timestamp, time added, last time active, and creator. The three timestamps are in unixtime format.
#        Module: channels
#    exemptlist [channel]
#        Returns: a list of global exempts, or, if a channel is specified, a list of channel-specific exempts. Each entry is a sublist containing: hostmask, comment, expiration timestamp, time added, last time active, and creator. The three timestamps are in unixtime format.
#        Module: channels
#    invitelist [channel]
#        Returns: a list of global invites, or, if a channel is specified, a list of channel-specific invites. Each entry is a sublist containing: hostmask, comment, expiration timestamp, time added, last time active, and creator. The three timestamps are in unixtime format.
#        Module: channels
#    newignore <hostmask> <creator> <comment> [lifetime]
#        Description: adds an entry to the ignore list; creator is given credit for the ignore. lifetime is how many minutes until the ignore expires and is removed. If lifetime is not specified, ignore-time (usually 60) is used. Setting the lifetime to 0 makes it a permanent ignore.
#        Returns: nothing
#        Module: core
#    killignore <hostmask>
#        Description: removes an entry from the ignore list
#        Returns: 1 if successful; 0 otherwise
#        Module: core
#    ignorelist
#        Returns: a list of ignores. Each entry is a sublist containing: hostmask, comment, expiration timestamp, time added, and creator. The timestamps are in unixtime format.
#        Module: core
#    isignore <hostmask>
#        Returns: 1 if the ignore is in the list; 0 otherwise
#        Module: core
#    save
#        Description: writes the user and channel files to disk
#        Returns: nothing
#        Module: core
#    reload
#        Description: loads the userfile from disk, replacing whatever is in memory
#        Returns: nothing
#        Module: core
#    backup
#        Description: makes a simple backup of the userfile that's on disk. If the channels module is loaded, this also makes a simple backup of the channel file.
#        Returns: nothing
#        Module: core
#    getting-users
#        Returns: 1 if the bot is currently downloading a userfile from a sharebot (and hence, user records are about to drastically change); 0 if not
#        Module: core





proc setudef {param1 param2} {
  puts "setudef"
}

proc putlog {text} {
  puts "log     : $text"
}




proc channels {} {
  puts "channels"
  return "sleek@conference.psi-im.org"
}

proc channel {command name args} {
  puts "channel $command $name $args"
  return true 
}

set _rand [pid]
    # random returns a value in the range 0..range-1
proc rand {range} {
    global _rand
    set period 233280
    set _rand [expr ($_rand * 9301 + 49297) % $period]
    return [expr int(($_rand/double($period)) * $range)]

}


proc isbotnick {nick} {
  if {$nick == "Iono"} {
    return 1
  }
  if {$nick == "BoreDa"} {
    return 1
  }
  return 0
}

proc matchattr {handle flags args} {
  set channel args
  return 1
}

#chandname2name <channel-dname>
#    Description: these two functions are important to correctly support !channels. The bot differentiates between channel description names (chan dnames) and real channel names (chan names). The chan dnames are what you would normally call the channel, such as "!channel". The chan names are what the IRC server uses to identify the channel. They consist of the chan dname prefixed with an ID; such as "!ABCDEchannel".
#    For bot functions like isop, isvoice, etc. you need to know the chan dnames. If you communicate with the server, you usually get the chan name, though. That's what you need the channame2dname function for.
#    If you only have the chan dname and want to directly send raw server commands, use the chandname2name command.
#    For non-!channels, chan dname and chan name are the same.
#    Module: irc
proc chandname2name {channel_dname} {
	return $channel_dname
}



#userlist [flags]
#    Returns: a list of users on the bot. You can use the flag matching system here ([global]{&/|}[chan]{&/|}[bot]). '&' specifies "and"; '|' specifies "or".
#    Module: core
proc userlist {args} {
  return {};
}

#validuser <handle>
#Returns: 1 if a user by that name exists; 0 otherwise
#Module: core
proc validuser {handle} {
	return 0
}

#loadhelp <helpfile-name>
# Description: attempts to load the specified help file from the help/ directory.
# Returns: nothing
# Module: core
proc loadhelp {helpfile_name} {

}

###9. Miscellaneous commands


#bind <type> <flags> <keyword/mask> [proc-name]
#    Description: You can use the 'bind' command to attach Tcl procedures to certain events. flags are the flags the user must have to trigger the event (if applicable). proc-name is the name of the Tcl procedure to call for this command (see below for the format of the procedure call). If the proc-name is omitted, no binding is added. Instead, the current binding is returned (if it's stackable, a list of the current bindings is returned).
#    Returns: name of the command that was added, or (if proc-name was omitted), a list of the current bindings for this command
#    Module: core
proc bind {type flags keywordmask procname} {
  puts "binding: $type $flags $keywordmask $procname"
  eval {bind_$type $flags $keywordmask $procname}
}

#TIME (stackable)
#bind time <flags> <mask> <proc>
#proc-name <minute> <hour> <day> <month> <year>
#  Description: allows you to schedule procedure calls at certain times. mask matches 5 space separated integers of the form: "minute hour day month year". minute, hour, day, month have a zero padding so they are exactly two characters long; year is extended to four characters in the same way. flags are ignored.
proc bind_time {flags keywordmask procname} {
  global eggdrop_time_bindings
  array set binding {}
  set time $keywordmask
  set binding(PROC) $procname
  set binding(MINUTE) [lindex $time 0]
  set binding(HOUR) [lindex $time 1]
  set binding(DAY) [lindex $time 2]
  set binding(MONTH) [lindex $time 3]
  set binding(YEAR) [lindex $time 4]
  lappend eggdrop_time_bindings [array get binding]
}

#JOIN (stackable)
#bind join <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel>
#Description: triggered by someone joining the channel. The mask in the bind is matched against "#channel nick!user@host" and can contain wildcards.
#Module: irc
proc bind_join {flags keywordmask procname} {
  global eggdrop_join_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(CHANNEL) [lindex $keywordmask 0]
  set binding(MASK) [lindex $keywordmask 1]
  lappend eggdrop_join_bindings [array get binding]
}

#PART (stackable)
#bind part <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <msg>
#Description: triggered by someone leaving the channel. The mask is matched against "#channel nick!user@host" and can contain wildcards. If no part message is specified, msg will be set to "".
#New Tcl procs should be declared as
#  proc partproc {nick uhost hand chan {msg ""}} { ... }
#for compatibility.
#  Module: irc
proc bind_part {flags keywordmask procname} {
  global eggdrop_part_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(CHANNEL) [lindex $keywordmask 0]
  set binding(MASK) [lindex $keywordmask 1]
  lappend eggdrop_part_bindings [array get binding]
}

#TOPC (stackable)
#bind topc <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <topic>
#Description: triggered by a topic change. mask can contain wildcards and is matched against '#channel <new topic>'.
#  Module: irc
proc bind_topc {flags keywordmask procname} {
  global eggdrop_topc_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(CHANNEL) [lindex $keywordmask 0]
  set binding(MASK) [lindex $keywordmask 1]
  lappend eggdrop_topc_bindings [array get binding]
}

##KICK (stackable)
#bind kick <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <target> <reason>
#Description: triggered when someone is kicked off the channel. The mask is matched against '#channel target' where the target is the nickname of the person who got kicked (can contain wildcards). The proc is called with the nick, user@host, and handle of the kicker, plus the channel, the nickname of the person who was kicked, and the reason; flags are ignored.
#Module: irc
proc bind_kick {flags keywordmask procname} {
  global eggdrop_kick_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(CHANNEL) [lindex $keywordmask 0]
  set binding(MASK) [lindex $keywordmask 1]
  lappend eggdrop_kick_bindings [array get binding]
}

#MSG
#bind msg <flags> <command> <proc>
#procname <nick> <user@host> <handle> <text>
#Description: used for /msg commands. The first word of the user's msg is the command, and everything else becomes the text argument.
#Module: server
proc bind_msg {flags keywordmask procname} {

}

#PUB
#bind pub <flags> <command> <proc>
#procname <nick> <user@host> <handle> <channel> <text>
#Description: used for commands given on a channel. The first word becomes the command and everything else is the text argument.
#Module: irc
proc bind_pub {flags keywordmask procname} {
  global eggdrop_pub_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(COMMAND) $keywordmask
  lappend eggdrop_pub_bindings [array get binding]

}

#PUBM (stackable)
#bind pubm <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <text>
#Description: just like MSGM, except it's triggered by things said on a channel instead of things /msg'd to the bot. The mask is matched against the channel name followed by the text and can contain wildcards. Also, if a line triggers a PUB bind, it will not trigger a PUBM bind.
#Module: irc
proc bind_pubm {flags keywordmask procname} {
  global eggdrop_pubm_bindings
  array set binding {}
  set binding(PROC) $procname
  set binding(CHANNEL) [lindex $keywordmask 0]
  set binding(MASK) [lindex $keywordmask 1]
  lappend eggdrop_pubm_bindings [array get binding]
}

#SIGN (stackable)
#bind sign <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <reason>
#Description: triggered by a signoff, or possibly by someone who got netsplit and never returned. The signoff message is the last argument to the proc. Wildcards can be used in the mask, which is matched against '#channel nick!user@host'.
#Module: irc
proc bind_sign {flags keywordmask procname} {

}

#DCC
#bind dcc <flags> <command> <proc>
#procname <handle> <idx> <text>
#Description: used for partyline commands; the command is the first word and everything else becomes the text argument. The idx is valid until the user disconnects. After that, it may be reused, so be careful about storing an idx for long periods of time.
#Module: core
proc bind_dcc {flags keywordmask procname} {

}

#NICK (stackable)
#bind nick <flags> <mask> <proc>
#procname <nick> <user@host> <handle> <channel> <newnick>
#Description: triggered when someone changes nicknames. The mask is matched against '#channel newnick' and can contain wildcards. Channel is "*" if the user isn't on a channel (usually the bot not yet in a channel).
#Module: irc
proc bind_nick {flags keywordmask procname} {

}

#MODE (stackable)
#bind mode <flags> <mask> <proc>
#proc-name <nick> <user@host> <handle> <channel> <mode-change> <victim>
#
#Description: mode changes are broken down into their component parts before being sent here, so the <mode-change> will always be a single mode, such as "+m" or "-o". victim will show the argument of the mode change (for o/v/b/e/I) or "" if the set mode does not take an argument. Flags are ignored. The bot's automatic response to a mode change will happen AFTER all matching Tcl procs are called. The mask will be matched against '#channel +/-modes' and can contain wildcards.
#If it is a server mode, nick will be "", user@host is the server name, and handle is *.
#Note that "victim" was added in 1.3.23 and that this will break Tcl scripts that were written for pre-1.3.23 versions and use this binding. An easy fix (by guppy) is as follows (example):

#Old script looks as follows:
#  bind mode - * mode_proc
#    proc mode_proc {nick uhost hand chan mc} { ... }
#
#    To make it work with 1.3.23+ and stay compatible with older bots, do:
#
#      bind mode - * mode_proc_fix
#        proc mode_proc_fix {nick uhost hand chan mc {victim ""}} {
#          if {$victim != ""} {append mc " $victim"}
#          mode_proc $nick $uhost $hand $chan $mc
#        }
#        proc mode_proc {nick uhost hand chan mc} { ... }

#Module: irc
proc bind_mode {flags keywordmask procname} {

}

#CTCP (stackable)
#bind ctcp <flags> <keyword> <proc>
#proc-name <nick> <user@host> <handle> <dest> <keyword> <text>
#Description: dest will be a nickname (the bot's nickname, obviously) or channel name. keyword is the ctcp command (which can contain wildcards), and text may be empty. If the proc returns 0, the bot will attempt its own processing of the ctcp command.
#Module: server
proc bind_ctcp {flags keywordmask procname} {

}

#BOT
#bind bot <flags> <command> <proc>
#proc-name <from-bot> <command> <text>
#Description: triggered by a message coming from another bot in the botnet. The first word is the command and the rest becomes the text argument; flags are ignored.
#Module: core
proc bind_bot {flags keywordmask procname} {

}

#LINK (stackable)
#bind link <flags> <mask> <proc>
#proc-name <botname> <via>
#Description: triggered when a bot links into the botnet. botname is the botnetnick of the bot that just linked in; via is the bot it linked through. The mask is checked against the botnetnick of the bot that linked and supports wildcards. flags are ignored.
#Module: core
proc bind_link {flags keywordmask procname} {

}


#    unbind <type> <flags> <keyword/mask> <proc-name>
#        Description: removes a previously created bind
#        Returns: name of the command that was removed
#        Module: core
#    binds [type/mask]
#        Returns: a list of Tcl binds, each item in the list is a sublist of five elements: {<type> <flags> <name> <hits> <proc>}
#        Module: core
#    logfile [<modes> <channel> <filename>]
#        Description: creates a new logfile, which will log the modes given for the channel listed. If no logfile is specified, a list of existing logfiles will be returned. "*" indicates all channels. You can also change the modes and channel of an existing logfile with this command. Entering a blank mode and channel ("") makes the bot stop logging there.
#        Returns: filename of logfile created, or, if no logfile is specified, a list of logfiles such as: {mco * eggdrop.log} {jp #lame lame.log}
#        Module: core
#    maskhost <nick!user@host>
#        Returns: masked hostmask for the string given ("n!u@1.2.3.4" -> "*!u@1.2.3.*", "n!u@lame.com" -> "*!u@lame.com", "n!u@a.b.edu" -> "*!u@*.b.edu")
#        Module: core
#utimer <seconds> <tcl-command>
#    Description: executes the given Tcl command after a certain number of seconds have passed
#    Returns: a timerID
#    Module: core
proc utimer {seconds command} {
  global eggdrop_utimer
  set numtimers1 [kllength eggdrop_utimer]
  #puts "utimer called, before $numtimers1 active timers: \n $eggdrop_utimer"
  puts "utimer: $seconds $command"

  array set timer {}
  set timer(TIME) $seconds
  set timer(PROC) $command
  set timer(ID) [rand 65536]
  lappend eggdrop_utimer [array get timer]

  set numtimers [kllength eggdrop_utimer]
  #puts "putting on the utimer queue $command $seconds $timer(ID) $numtimers timers now active"
  #puts "utimer called, after $numtimers1 active timers: \n $eggdrop_utimer"
  set indexthing [lindex $eggdrop_utimer 1]
  #puts "first index: '$indexthing'"
  return $timer(ID)
}

#timer <minutes> <tcl-command>
#    Description: executes the given Tcl command after a certain number of minutes have passed
#    Returns: a timerID
#    Module: core
proc timer {minutes command} {
  puts "timer: $minutes $command"
  global eggdrop_timer
  array set timer {}
  set timer(TIME) $minutes
  set timer(PROC) $command
  set timer(ID) [rand 65536]
  lappend eggdrop_timer [array get timer]
  return $timer(ID)
}

#timers
#    Returns: a list of active minutely timers. Each entry in the list contains the number of minutes left till activation, the command that will be executed, and the timerID.
#    Module: core
proc timers {} {
  global eggdrop_timer
  set timerlist [list]
  for {set i 0} {$i < [llength eggdrop_timer]} {incr i} {
     set item [lindex $eggdrop_timer $i]
     if {$item == ""} {
       continue
     }
     array set timer $item
     set command $timer(PROC)
     set timerID $timer(ID)
     set time $timer(TIME)
     lappend timerlist [list $time $command $timerID]
  }
  return timerlist
}

#utimers
#    Returns: a list of active secondly timers. Each entry in the list contains the number of minutes left till activation, the command that will be executed, and the timerID.
#    Module: core
proc utimers {} {
  global eggdrop_utimer
  set timerlist [list]
  for {set i 0} {$i < [llength eggdrop_utimer]} {incr i} {
     array set timer [lindex $eggdrop_utimer $i]
     set command $timer(PROC)
     set timerID $timer(ID)
     set time $timer(TIME)
     lappend timerlist [list $time $command $timerID]
  }
  return timerlist
}

#killtimer <timerID>
#    Description: removes a minutely timer from the list
#    Returns: nothing
#    Module: core
proc killtimer {timerID} {
  global eggdrop_timer
  for {set i 0} {$i < [llength eggdrop_timer]} {incr i} {
    array set timer [lindex $eggdrop_timer $i]
    if {$timer(ID) == $timerID} {
      set eggdrop_timer [lreplace eggdrop_timer $i $i]
    }
  }
}


#killutimer <timerID>
#    Description: removes a secondly timer from the list
#    Returns: nothing
#    Module: core
proc killutimer {timerID} {
  global eggdrop_utimer
  for {set i 0} {$i < [llength eggdrop_utimer]} {incr i} {
    array set timer [lindex $eggdrop_utimer $i]
    if {$timer(ID) == $timerID} {
      set eggdrop_utimer [lreplace eggdrop_utimer $i $i]
      incr i -1
    }
  }
}
#    unixtime
#        Returns: a long integer which represents the number of seconds that have passed since 00:00 Jan 1, 1970 (GMT).
#        Module: core
proc unixtime {} {
	global current_unixtime
	return current_unixtime
}

#    duration <seconds>
#        Returns: the number of seconds converted into years, weeks, days, hours, minutes, and seconds. 804600 seconds is turned into 1 week 2 days 7 hours 30 minutes.
#        Module: core
#    strftime <formatstring> [time]
#        Returns: a formatted string of time using standard strftime format. If time is specified, the value of the specified time is used. Otherwise, the current time is used.
#        Module: core
#    ctime <unixtime>
#        Returns: a formatted date/time string based on the current locale settings from the unixtime string given; for example "Fri Aug 3 11:34:55 1973"
#        Module: core
#    myip
#        Returns: a long number representing the bot's IP address, as it might appear in (for example) a DCC request
#        Module: core
#    rand <limit>
#        Returns: a random integer between 0 and limit-1
#        Module: core
#    control <idx> <command>
#        Description: removes an idx from the party line and sends all future input to the Tcl command given. The command will be called with two parameters: the idx and the input text. The command should return 0 to indicate success and 1 to indicate that it relinquishes control of the user back to the bot. If the input text is blank (""), it indicates that the connection has been dropped. Also, if the input text is blank, never call killdcc on it, as it will fail with "invalid idx".
#        Returns: nothing
#        Module: core
#    sendnote <from> <to[@bot]> <message>
#        Description: simulates what happens when one user sends a note to another
#        Returns:
#            0
#            the send failed
#            1
#            the note was delivered locally or sent to another bot
#            2
#            the note was stored locally
#            3
#            the user's notebox is too full to store a note
#            4
#            a Tcl binding caught the note
#            5
#            the note was stored because the user is away
#        Module: core
#    link [via-bot] <bot>
#        Description: attempts to link to another bot directly. If you specify a via-bot, it tells the via-bot to attempt the link.
#        Returns: 1 if the link will be attempted; 0 otherwise
#        Module: core
#    unlink <bot>
#        Description: attempts to unlink a bot from the botnet
#        Returns: 1 on success; 0 otherwise
#        Module: core
#    encrypt <key> <string>
#        Returns: encrypted string (using the currently loaded encryption module), encoded into ASCII using base-64
#        Module: encryption
#    decrypt <key> <encrypted-base64-string>
#        Returns: decrypted string (using the currently loaded encryption module)
#        Module: encryption
#    encpass <password>
#        Returns: encrypted string (using the currently loaded encryption module)
#        Module: encryption
#    die [reason]
#        Description: causes the bot to log a fatal error and exit completely. If no reason is given, "EXIT" is used.
#        Returns: nothing
#        Module: core
#    unames
#        Returns: the current operating system the bot is using
#        Module: core
#    dnslookup <ip-address/hostname> <proc> [[arg1] [arg2] ... [argN]]
#        Description: This issues an asynchronous dns lookup request. The command will block if dns module is not loaded; otherwise it will either return immediately or immediately call the specified proc (e.g. if the lookup is already cached).
#        As soon as the request completes, the specified proc will be called as follows: <proc> <ipaddress> <hostname> <status> [[arg1] [arg2] ... [argN]]
#        status is 1 if the lookup was successful and 0 if it wasn't. All additional parameters (called arg1, arg2 and argN above) get appended to the proc's other parameters.
#        Returns: nothing
#        Module: core
#    md5 <string>
#        Returns: the 128 bit MD5 message-digest of the specified string
#        Module: core
#    callevent <event>
#        Description: triggers the evnt bind manually for a certain event. For example: callevent rehash.
#        Returns: nothing
#        Module: core
#    traffic
#        Returns: a list of sublists containing information about the bot's traffic usage in bytes. Each sublist contains five elements: type, in-traffic today, in-traffic total, out-traffic today, out-traffic total (in that order).
#        Module: core
#    modules
#        Returns: a list of sublists containing information about the bot's currently loaded modules. Each sublist contains three elements: module, version, and dependencies. Each dependency is also a sublist containing the module name and version.
#        Module: core
#    loadmodule <module>
#        Description: attempts to load the specified module.
#        Returns: "Already loaded." if the module is already loaded, "" if successful, or the reason the module couldn't be loaded.
#        Module: core
#    unloadmodule <module>
#        Description: attempts to unload the specified module.
#        Returns: "No such module" if the module is not loaded, "" otherwise.
#        Module: core
#    loadhelp <helpfile-name>
#        Description: attempts to load the specified help file from the help/ directory.
#        Returns: nothing
#        Module: core
#    unloadhelp <helpfile-name>
#        Description: attempts to unload the specified help file.
#        Returns: nothing
#        Module: core
#    reloadhelp
#        Description: reloads the bot's help files.
#        Returns: nothing
#        Module: core
#    restart
#        Description: rehashes the bot, kills all timers, reloads all modules, and reconnects the bot to the next server in its list.
#        Returns: nothing
#        Module: core
#    rehash
#        Description: rehashes the bot
#        Returns: nothing
#        Module: core
#    stripcodes <strip-flags> <string>
#        Description: strips specified control characters from the string given. strip-flags can be any combination of the following:
#            b
#            remove all boldface codes
#            c
#            remove all color codes
#            r
#            remove all reverse video codes
#            u
#            remove all underline codes
#            a
#            remove all ANSI codes
#            g
#            remove all ctrl-g (bell) codes
#        Returns: the stripped string
#        Module: core
