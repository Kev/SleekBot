### These are the TCL functions called from the eggdrop compatability plugin.
# It would be much easier to not try and emulate eggdrop, but who really cares? :)  prefixed with eggsupp_ (eggdrop support)


proc eggsupp_process_join {nick hostmask handle channel} {
	global eggdrop_join_bindings
	puts "Join event $nick $hostmask $handle $channel"
	foreach tmpbinding $eggdrop_join_bindings {
		if {$tmpbinding == ""} {
			continue
		}
		array set binding $tmpbinding
		#puts "Join command: $binding(CHANNEL) $binding(MASK) $binding(PROC)"
		if {[eggsupp_channel_matches $channel $binding(CHANNEL)] && [eggsupp_hostmask_matches $hostmask $binding(MASK)]} {
			puts "Running: $binding(PROC) $nick $hostmask $handle $channel"
			eval {$binding(PROC) $nick $hostmask $handle $channel}
		}
	}
}

proc eggsupp_process_part {nick hostmask handle channel} {
	global eggdrop_part_bindings
	puts "Part event $nick $hostmask $handle $channel"
	foreach tmpbinding $eggdrop_part_bindings {
		if {$tmpbinding == ""} {
			continue
		}
		array set binding $tmpbinding
		#puts "Join command: $binding(CHANNEL) $binding(MASK) $binding(PROC)"
		if {[eggsupp_channel_matches $channel $binding(CHANNEL)] && [eggsupp_hostmask_matches $hostmask $binding(MASK)]} {
			puts "Running: $binding(PROC) $nick $hostmask $handle $channel"
			eval {$binding(PROC) $nick $hostmask $handle $channel}
		}
	}
}

#checks if the supplied host matches the host mask
proc eggsupp_hostmask_matches {host mask} {
	return 1
	if {$mask == "*!*@*"} {
		return 1
	}
	if {$mask == $host} {
		return 1
	}
	#FIXME: we also need to support partial wildcards
	return 0
}

#checks if the supplied channel matches the channel mask
proc eggsupp_channel_matches {channel mask} {
	return 1
	if {$mask == "*"} {
		return 1
	}
	if {$mask == $channel} {
		return 1
	}
	#FIXME: we also need to support partial wildcards
	return 0
}

proc eggsupp_process_nick {} {

}

proc eggsupp_process_pub {nick hostmask handle channel text} {
	set command [lindex $text 0]
	set rest [lreplace $text 0 0]
	#if pub is matched, pubm must not be
	global eggdrop_pubm_bindings
	global eggdrop_pub_bindings
	puts "Pub event $nick $hostmask $handle $channel"
	set done 0
	foreach tmpbinding $eggdrop_pub_bindings {
		if {$tmpbinding == ""} {
			continue
		}
		array set binding $tmpbinding
		puts "pub command: $binding(COMMAND) $binding(PROC) checking against '$command' (with '$rest')"
		if {$binding(COMMAND) == $command} {
			puts "Running: $binding(PROC) $nick $hostmask $handle $channel $text"
			eval {$binding(PROC) $nick $hostmask $handle $channel $rest}
			set done 1
		}
	}

	if {$done == 1} {
		return
	}

	foreach tmpbinding $eggdrop_pubm_bindings {
		if {$tmpbinding == ""} {
			continue
		}
		array set binding $tmpbinding
		#puts "pubm command: $binding(CHANNEL) $binding(MASK) $binding(PROC)"
		if {[eggsupp_channel_matches $channel $binding(CHANNEL)] && [eggsupp_hostmask_matches $hostmask $binding(MASK)]} {
			puts "Running: $binding(PROC) $nick $hostmask $handle $channel $text"
			eval {$binding(PROC) $nick $hostmask $handle $channel $text}
		}
	}  
}



proc eggsupp_process_msg {} {
#msg and msgm
#these are private messages
}

proc eggsupp_process_time {minute hour day month year } {
  global eggdrop_time_bindings
  puts "Time event $minute $hour $day $month $year"
  foreach tmpbinding $eggdrop_time_bindings {
    if {$tmpbinding == ""} {
      continue
    }
    array set binding $tmpbinding
    #puts "time command: $binding(MINUTE)"
    #puts "time command: $binding(MINUTE) $binding(HOUR) $binding(DAY) $binding(MONTH) $binding(YEAR) $binding(PROC)"
    if {$binding(MINUTE) == $minute || $binding(MINUTE) == "*"} {
      if {$binding(HOUR) == $hour || $binding(HOUR) == "*"} {
        if {$binding(DAY) == $day || $binding(DAY) == "*"} { 
          if {$binding(MONTH) == $month || $binding(MONTH) == "*"} {
            if {$binding(YEAR) == $year || $binding(YEAR) == "*"} {
              eval {$binding(PROC) $minute $hour $day $month $year}
            }
          }
        }
      }
    }
  }
}


#This is called (approximately!) every second. While it'll be called for the correct number of seconds which have passed, there's no guarantee of regularity
proc eggsupp_second_tick {args} {
  global eggdrop_utimer
  #puts "Second tick"
  for {set i 0} {$i < [llength eggdrop_utimer]} {incr i} {
    set item [lindex $eggdrop_utimer $i]
    if {$item == ""} {
      continue
    }
    array set timer $item 
    #puts "timer(TIME) is $timer(TIME)"
    set timer(TIME) [expr {$timer(TIME)-1}]
    if {$timer(TIME) == 0} {
      puts "Timer expired, running '$timer(PROC)'"
      eval {$timer(PROC)}
      killutimer $timer(ID)
      incr i -1
    } else {
      #puts "Timer for command '$timer(PROC)' still has $timer(TIME) to run"
      lset eggdrop_utimer $i [array get timer]
    }
  }
}

#This is called (approximately!) every minute. While it'll be called for the correct number of minutes which have passed, there's no guarantee of regularity
proc eggsupp_minute_tick {args} {
  global eggdrop_timer
  #puts "Second tick"
  for {set i 0} {$i < [llength eggdrop_timer]} {incr i} {
    set length  [llength eggdrop_timer]
    set item [lindex $eggdrop_timer $i]
    if {$item == ""} {
      continue
    }
    array set timer $item
    puts "minute loop $length $item"
    puts "timer(TIME) is $timer(TIME)"
    set timer(TIME) [expr {$timer(TIME)-1}]
    if {$timer(TIME) == 0} {
      puts "Timer expired, running '$timer(PROC)'"
      eval {$timer(PROC)}
      killtimer $timer(ID)
      irc i -1
    } else {
      #puts "Timer for command '$timer(PROC)' still has $timer(TIME) to run"
      lset eggdrop_timer $i [array get timer]
    }
  }
}

#This returns the next message on the queue, or "" if it's empty
proc eggsup_get_message_queue {} {
	global eggdrop_message_queue
	set num [llength $eggdrop_message_queue]
	#puts "Checking message queue: $num message(s) left"
	if {[llength $eggdrop_message_queue] < 1} {
		#puts "Empty queue, returning ''"
		return ""
	}
	set message [lindex $eggdrop_message_queue 0]
	set eggdrop_message_queue [lreplace $eggdrop_message_queue 0 0]
	puts "Returning $message"
	return $message
}