source "plugins/eggdrop/support.tcl"
source "plugins/eggdrop/eggdropcompat.tcl"
source "scripts/bmotion/bMotion.tcl"

puts "second time"
second_tick
puts "minute time"
minute_tick
puts "event time"
process_time 1 1 1 1 2007
