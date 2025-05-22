#!/bin/bash

if [ $# -ne 2 ]; then
          echo "Usage: $0 <input_file> <output_file>"
            exit 1
fi

input_file="$1"
output_file="$2"

awk '
function format_time(sec, usec) {
  while (usec >= 1000000) {
              usec -= 1000000
                  sec += 1
                    }
                      return sprintf("(%d.%06d)", sec, usec)
              }

              NR == 1 {
                match($0, /\(([0-9]+)\.([0-9]+)\)/, m)
                  base_sec = m[1] + 0
                    base_usec = m[2] + 0
            }
            {
                      curr_usec = base_usec + (NR - 1)
                        curr_time = format_time(base_sec, curr_usec)

                          # Replace the CAN ID (3 hex digits before ##) with 000
                             line = $0
                               sub(/\([0-9]+\.[0-9]+\)/, curr_time, line)
                                 sub(/[0-9A-Fa-f]{3}##/, "000##", line)

                                   print line
                                   }
                                   ' "$input_file" > "$output_file"
