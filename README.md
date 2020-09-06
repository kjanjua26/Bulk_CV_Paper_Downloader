# Bulk_CV_Paper_Downloader
A small script to bulk download all CVPR/ICCV/ECCV papers for different analysis or reading..


## Bulk Download CVPR
The code `bulk_download_cvpr.py` downloads the CVPR papers. It takes two command line arguments for now
1. Year - the year you want to download the paper of.
2. Path - the download path.

Running `python3 bulk_download_cvpr.py -h` returns:

```
usage: bulk_download_cvpr.py [-h] --year YEAR --path PATH [--conf CONF]

optional arguments:
  -h, --help   show this help message and exit
  --year YEAR  The year to download papers of
  --path PATH  The save path - to save papers in
  --conf CONF  The conference to download papers of
```

The conf flag is optional for now since it only works with CVPR for the moment. Extending to xCCV (x = E or I), will use the conf flag to download papers from a specific conference.
