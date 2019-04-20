from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
import os
import os.path
import sys
import zipfile
import hashlib
import json
import datetime
import urllib2
import random
import base64
import hmac
import time

secret_id = 'AKIDWyFKIK1mkXCg6NQL2XqxxqX2LRPBIBOP'
secret_key = '1qTt7E9sOiqlkYAi5FDze7f2DCf097wk'
cdn_refresh_url = "cdn.api.qcloud.com/v2/index.php"
bucket = "moka-1253928017"
region = 'ap-guangzhou'
token = ''
config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region, Token=token)
client = CosS3Client(config)

ch='1'
nowGroup='1'

if len(sys.argv) >= 2:
    ch=sys.argv[1]
    nowGroup=sys.argv[2]

rootDir="../"
updateDir=rootDir+"build_res/update/ch"+ch+"/"

def upload(file_name,remote_dir_name):
	with open(updateDir + file_name, 'rb') as fp:
		response = client.put_object(
    		Bucket=bucket,
    		Body=fp,
    		Key=remote_dir_name+file_name,
    		StorageClass='STANDARD',
    		CacheControl='no-cache',
    		ContentDisposition=file_name
    		)
		print response['ETag']

def refresh_cdn(remote_dir):
    time_str = str(int(time.time()))
    nonce = str(random.randint(100000000,999999999))
    rear = "&dirs.0=" + remote_dir

    want_sign_str = "Action=RefreshCdnDir"+"&Nonce=" + nonce +"&SecretId=" + secret_id + "&Timestamp=" + time_str + rear;
    url = cdn_refresh_url + "?" + want_sign_str

    signature = hmac.new(secret_key,"GET"+cdn_refresh_url + "?" + want_sign_str,hashlib.sha1).digest();
    url = "https://" + url + "&Signature=" + urllib2.quote(base64.b64encode(signature))
    print("refresh request => "+url)
    response = urllib2.urlopen(url)
    data = response.read()
    data = json.loads(data)
    print("refresh cdn result:")
    if data['code'] == 0:
        print(data['codeDesc'])
    else:
        print(data['message'])

remote_dir = 'ddz-client-update/ch' + ch + '/'

upload("game_1.0."+nowGroup+".zip",remote_dir)
upload("project.manifest",remote_dir)
upload("version.manifest",remote_dir)

refresh_cdn("http://"+bucket+".file.myqcloud.com/"+remote_dir)
