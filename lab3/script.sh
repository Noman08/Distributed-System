for i in `seq 1 5`; do 
    for ip in `seq 1 8`; do
        curl -d 'entry=t'${i} -X 'POST' "http://10.1.0.${ip}:80/board" &
    done
done