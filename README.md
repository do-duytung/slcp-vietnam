# slcp-vietnam
Inventories of Short-lived Climate Pollutants (black carbon, tropospheric ozone, methane, PM2.5) in Vietnam

This project collect data of air pollutants in Vietnam for public research and study.
We welcome contributions of all kinds to improve this project.
# Crontab
```
* * * * python3 /home/ec2-user/purpleair_download.py
* * * * python3 /home/ec2-user/aqicn_download.py
*/3 * * * python3 /home/ec2-user/kttv_download.py
0 * * * cp KTTV.csv aqicn_data.csv purpleair.csv slcp-vietnam/data
0 * * * cd slcp-vietnam && git add data/*.csv && git commit -m "Update daily data" && git push
```     

 
