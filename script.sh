java -jar ./Lavalink.jar &

sleep 10

python3 ./main.py &

wait -n

exit $?
