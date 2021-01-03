rm -rf logs
docker cp cc_outputservice_1:/logs ./logs
rm -rf input_instance.txt
tr ' ' '\n' < ./logs/gunicorn-access.log  | sort  | uniq -c  | sort -rn  | awk '{print $2"@"$1"\n"}'  >> input_instance.txt
