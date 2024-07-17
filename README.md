# slcp-vietnam
Inventories of Short-lived Climate Pollutants (black carbon, tropospheric ozone, methane, PM2.5) in Vietnam

This project collect data of air pollutants in Vietnam for public research and study.
We welcome contributions of all kinds to improve this project.

# Publication
Do, T. D., & Kita, K. (2022). Variations of short-lived climate pollutants in Hanoi, Vietnam. In Interlocal Adaptations to Climate Change in East and Southeast Asia: Sharing Lessons of Agriculture, Disaster Risk Reduction, and Resource Management (pp. 129-133). Cham: Springer International Publishing.
Link PDF: https://library.oapen.org/bitstream/handle/20.500.12657/53329/1/978-3-030-81207-2.pdf#page=140

# Crontab
```
* * * * python3 /home/ec2-user/purpleair_download.py
* * * * python3 /home/ec2-user/aqicn_download.py
*/3 * * * python3 /home/ec2-user/kttv_download.py
0 * * * cp KTTV.csv aqicn_data.csv purpleair.csv slcp-vietnam/data
0 * * * cd slcp-vietnam && git add data/*.csv && git commit -m "Update daily data" && git push
```     

 
