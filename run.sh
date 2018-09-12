#!/bin/bash

#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################

##### CONSTANTS #####

NO_COLOR='\033[0m' 			# No Color
DARK_GRAY="\033[1;30m"		# Dark Gray
RED="\033[0;31m"			# Red

##### FUNCTIONS #####

fprint()
{
	printf -- "$3"
	
	if [ "$2" = "1" ]; then
		printf -- "$1"
	else
		printf -- "$1\n"
	fi
	
	printf "${NO_COLOR}"
}

dfprint()
{
	if [ "$debug" = "1" ]; then
		fprint "$1" "$2" $DARK_GRAY
	fi
}

err()
{
	fprint "ERROR: $1" 0 $RED
}

usage()
{
    echo "usage: autom8 [[[command] [--app \"[app arguments]\"] [--web \"[web arguments]\"]] | [-h | --help]]"
}

m8_start()
{
	fprint "\nStarting Autom8 App"
	sudo python /home/admin/autom8/app/autom8/main.py $1
	
	fprint "\nStarting Autom8 Web"
}

m8_update()
{
	fprint "Checking for updates..."
}

##### MAIN #####

debug=0
appArgs=""
webArgs=""
command="start"

while [ "$1" != "" ]; do
    case $1 in
        --app )           		shift
                                appArgs=$1
                                ;;
        --web )           		shift
                                webArgs=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        --debug )           	debug=1
                                ;;
        start )           		command="start"
                                ;;
        update )           		command="update"
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

dfprint "\nRunning in Debug mode!\n" 0
dfprint "command = $command" 0
dfprint "appArgs = $appArgs" 0
dfprint "webArgs = $webArgs" 0

case $command in
	start )			m8_start "$appArgs"
					;;
	update )		m8_update
					;;
	* )				err "$command is an invalid command!"
					usage
					exit 1
esac

fprint "\nDone\n"
exit