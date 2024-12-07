function auto() {
    python3 auto_proxy.py
    sleep 10
    TOKEN=$(cat token.txt)
    echo -e "$TOKEN" | python3 grass_desktop.py &
    GRASS_PID=$!
    echo "grass_desktop.py running with PID: $GRASS_PID"
}

function stop_grass() {
    if [ ! -z "$GRASS_PID" ]; then
        echo "Stopping grass_desktop.py with PID: $GRASS_PID"
        kill -9 $GRASS_PID
    else
        echo "No grass_desktop.py process found to stop."
    fi
}

while true; do
    echo "Starting auto process..."
    auto
    RANDOM_SLEEP=$((RANDOM % 60 * 60 * 24))
    sleep $RANDOM_SLEEP
    stop_grass
done
