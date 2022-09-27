#! /bin/bash

rm -f ./cookies.txt
touch ./cookies.txt
if [ ! -e "facenet_keras_weights.h5" ]
then
	wget --load-cookies ./cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ./cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1_IlFKQxEJbyKe5AItTbfX8YtJ7X96NMB' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1_IlFKQxEJbyKe5AItTbfX8YtJ7X96NMB" -O facenet_keras_weights.h5 && rm -rf ./cookies.txt
fi
