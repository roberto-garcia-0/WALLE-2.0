# revert terminal back to black when command exits
handle_exit() {
    echo -ne '\e]11;#000000\e\\'
    exit 0
}

trap handle_exit SIGINT

# flash the terminal between white and yellow
while :
do
    echo -ne '\e]11;#ffffff\e\\'
    sleep 1
    echo -ne '\e]11;#ffff00\e\\'
    sleep 1
done