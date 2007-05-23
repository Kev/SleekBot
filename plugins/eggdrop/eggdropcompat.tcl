### These initial functions are the ones which eggdrop provides and which we therefore must do too

set eggdrop_time_bindings [list]
set eggdrop_join_bindings [list]
set eggdrop_part_bindings [list]
set eggdrop_msg_bindings [list]
set eggdrop_pub_bindings [list]
set eggdrop_pubm_bindings [list]
set eggdrop_utimer [list]
set eggdrop_timer [list]

set eggdrop_message_queue [list]

proc setudef {param1 param2} {
  puts "setudef"
}

proc putloglev {level channel text} {
  puts "log $level $channel : $text"
}


proc putlog {text} {
  puts "log     : $text"
}

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



proc channels {} {
  puts "channels"
  return "psi-test@conference.doomsong.co.uk"
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

#utimer <seconds> <tcl-command>
#    Description: executes the given Tcl command after a certain number of seconds have passed
#    Returns: a timerID
#    Module: core
proc utimer {seconds command} {
  puts "utimer: $seconds $command"
  global eggdrop_utimer
  array set timer {}
  set timer(TIME) $seconds
  set timer(PROC) $command
  set timer(ID) [rand 65536]
  lappend eggdrop_utimer [array get timer]
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

proc isbotnick {nick} {
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

#userlist [flags]
#    Returns: a list of users on the bot. You can use the flag matching system here ([global]{&/|}[chan]{&/|}[bot]). '&' specifies "and"; '|' specifies "or".
#    Module: core
proc userlist {args} {
  return {};
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

