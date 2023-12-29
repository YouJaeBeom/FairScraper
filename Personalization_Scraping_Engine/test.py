import requests

cookies = {
    'MUID': '290786FD3ED36DE4297A95A13FFB6CCF',
    'SRCHD': 'AF=NOFORM',
    'SRCHUID': 'V=2&GUID=340C9C8FC16A45F785E5F121EACE9A44&dmnchg=1',
    'ABDEF': 'V=13&ABDV=13&MRNB=1690725545206&MRB=0',
    'MUIDB': '290786FD3ED36DE4297A95A13FFB6CCF',
    'NAP': 'V=1.9&E=1cb0&C=1H1qDq7dsQ2o9G4kRxqYTrzYnMqxIMT7vr5J3l6OJyykeBAqZnJHmA&W=1',
    'MMCASM': 'ID=158D3CDD81FB467E9EE7B30A2CF81702',
    '_UR': 'QS=0&TQS=0&cdxcls=0',
    'MicrosoftApplicationsTelemetryDeviceId': 'a4bf9f07-cab4-4891-a48a-f3ff1240118b',
    '_clck': '1rfyxig|2|fgo|0|1410',
    '_BINGNEWS': 'SW=1085&SH=1283',
    'ipv6': 'hit=1701962537652&t=4',
    '_Rwho': 'u=d',
    'ai_session': 'Y+sbbSlBziAoWBgAaXnGis|1701958938301|1701958938301',
    '_HPVN': 'CS=eyJQbiI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0xMi0wN1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyMCwiVG9iYnMiOjB9',
    '_EDGE_S': 'SID=04DEFC45C5B162D61346EFA5C437632D&mkt=ko-kr',
    'USRLOC': 'HS=1&ELOC=LAT=37.626922607421875|LON=127.0882339477539|N=%EC%84%9C%EC%9A%B8%20%EC%84%9C%EC%9A%B8|ELT=6|',
    'WLS': 'C=&N=',
    'SRCHUSR': 'DOB=20230728&T=1701958935000&TPC=1701958955000',
    'ANIMIA': 'FRE=1',
    '_RwBf': 'r=0&ilt=2&ihpd=0&ispd=2&rc=6&rb=0&gb=0&rg=200&pc=3&mtu=0&rbb=0&g=0&cid=&clo=0&v=2&l=2023-12-07T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-12-07T14:25:01.2391623+00:00&rwred=0&wls=&wlb=&wle=&ccp=&lka=0&lkt=0&aad=0&TH=',
    '_SS': 'SID=04DEFC45C5B162D61346EFA5C437632D&R=6&RB=0&GB=0&RG=200&RP=3',
    'SRCHHPGUSR': 'SRCHLANG=ko&BRW=HTP&BRH=T&CW=960&CH=1298&SCW=1402&SCH=3041&DPR=2.0&UTC=540&DM=1&PV=14.0.0&HV=1701959102&WTS=63837555823&PRVCW=960&PRVCH=1298&IG=5CC85A3D165C4945876FB0CE182E52CB&CIBV=1.1366.6',
}

headers = {
    'authority': 'www.bing.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'MUID=290786FD3ED36DE4297A95A13FFB6CCF; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=340C9C8FC16A45F785E5F121EACE9A44&dmnchg=1; ABDEF=V=13&ABDV=13&MRNB=1690725545206&MRB=0; MUIDB=290786FD3ED36DE4297A95A13FFB6CCF; NAP=V=1.9&E=1cb0&C=1H1qDq7dsQ2o9G4kRxqYTrzYnMqxIMT7vr5J3l6OJyykeBAqZnJHmA&W=1; MMCASM=ID=158D3CDD81FB467E9EE7B30A2CF81702; _UR=QS=0&TQS=0&cdxcls=0; MicrosoftApplicationsTelemetryDeviceId=a4bf9f07-cab4-4891-a48a-f3ff1240118b; _clck=1rfyxig|2|fgo|0|1410; _BINGNEWS=SW=1085&SH=1283; ipv6=hit=1701962537652&t=4; _Rwho=u=d; ai_session=Y+sbbSlBziAoWBgAaXnGis|1701958938301|1701958938301; _HPVN=CS=eyJQbiI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6OCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0xMi0wN1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyMCwiVG9iYnMiOjB9; _EDGE_S=SID=04DEFC45C5B162D61346EFA5C437632D&mkt=ko-kr; USRLOC=HS=1&ELOC=LAT=37.626922607421875|LON=127.0882339477539|N=%EC%84%9C%EC%9A%B8%20%EC%84%9C%EC%9A%B8|ELT=6|; WLS=C=&N=; SRCHUSR=DOB=20230728&T=1701958935000&TPC=1701958955000; ANIMIA=FRE=1; _RwBf=r=0&ilt=2&ihpd=0&ispd=2&rc=6&rb=0&gb=0&rg=200&pc=3&mtu=0&rbb=0&g=0&cid=&clo=0&v=2&l=2023-12-07T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2023-12-07T14:25:01.2391623+00:00&rwred=0&wls=&wlb=&wle=&ccp=&lka=0&lkt=0&aad=0&TH=; _SS=SID=04DEFC45C5B162D61346EFA5C437632D&R=6&RB=0&GB=0&RG=200&RP=3; SRCHHPGUSR=SRCHLANG=ko&BRW=HTP&BRH=T&CW=960&CH=1298&SCW=1402&SCH=3041&DPR=2.0&UTC=540&DM=1&PV=14.0.0&HV=1701959102&WTS=63837555823&PRVCW=960&PRVCH=1298&IG=5CC85A3D165C4945876FB0CE182E52CB&CIBV=1.1366.6',
    'referer': 'https://www.bing.com/search?q=russia+ukraine+war&filters=ex1%3a%22ez5_19662_19662%22&qs=HS&sc=10-0&cvid=2C962994F16745C380D82221C07B9C5E&FORM=000017&sp=1&lq=0&qpvt=russia+ukraine+war',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"120.0.6099.71"',
    'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.71", "Google Chrome";v="120.0.6099.71"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://www.bing.com/search?q=russia+ukraine+war&filters=ex1%3a%22ez5_19663_19663%22&qs=HS&sc=10-0&cvid=2C962994F16745C380D82221C07B9C5E&FORM=000017&sp=1&lq=0&qpvt=russia+ukraine+war',
    cookies=cookies,
    headers=headers,
)

print(response.text)