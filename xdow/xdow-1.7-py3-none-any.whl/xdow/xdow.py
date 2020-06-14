from bs4 import BeautifulSoup
from requests import Session as session
import requests
import js2py
from bs4.element import Tag as bs_tag
import sys
from urllib.parse import urlparse
#from pyppeteer import launch

s = session()
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://www.google.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}



def returnphjs(jstext):
    qualites = """ 
    
        all_data = []

        if (typeof(quality_720p) !== "undefined"){
            all_data.push(quality_720p)
        }

        if (typeof(quality_1080p) !== "undefined"){
            all_data.push(quality_1080p)
        }

        if (typeof(quality_240p) !== "undefined"){
            all_data.push(quality_240p)
        }

        if (typeof(quality_480p) !== "undefined"){
            all_data.push(quality_480p)
        }


        return all_data    
            
                                """
    jstext = jstext.replace('<script type="text/javascript">','')

    redunt_data = jstext.find('playerObjList.playerDiv')

    jstext = jstext[:redunt_data]
    jstext = jstext + qualites
    jstext = 'function getlink() {' + jstext
    jstext = jstext + '}'
    return jstext


def return_page_source(link):
    with s:
        s.headers = headers
        try:
            response = s.get(link)
        except:
            print("Can not establish connection with pornhub")
            sys.exit(0)
        pg_source = response.text

        # with open('../resp.html', 'w', encoding='utf-8') as f:
        #     f.write(pg_source)

        return pg_source


async def render_page(link):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(link)
    await page.waitFor(5000)
    await page.screenshot({'path': 'example.png'})
    page_source = await page.evaluate('() => document.body.innerHTML')
    await browser.close()
    return page_source


def download_file(link,filename):
    r = requests.head(link)
    file_size = int(r.headers['Content-Length'])
    file_size = int(file_size)

    downloaded = 0
    response = requests.get(link, stream=True)
    handle = open(f'{filename}.mp4', "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            downloaded += int(len(chunk))
            handle.write(chunk)

            done = int((downloaded / file_size) * 50)
            # input(f'{downloaded},{file_size}')
            sys.stdout.write("\r[{}{}] {}/{} kb".format('=' * done, ' ' * (50 - done), int(downloaded / 1024),
                                                        int(file_size / 1024)))
            sys.stdout.flush()
    handle.close()


def phub(link):
    pg_source = return_page_source(link)
    soup = BeautifulSoup(pg_source, 'html.parser')
    all_js = soup.find_all('script', {'type': 'text/javascript'})
    js = ''
    for js in all_js:
        if 'var flashvars' in js.text or 'var flashvars' in str(js):
            ojs = js.text
            if len(ojs) == 0:
                ojs = str(js)
            else:
                pass
    js = ojs

    if isinstance(js, bs_tag):
        print("slow internet connection.Exiting...")
        sys.exit(0)

    newjs = returnphjs(js)
    fun_all_links = js2py.eval_js(newjs)
    all_links = fun_all_links()
    dict_quality = dict()
    video_title = soup.find('div',{'class':'title-container'}).findNext('span',{'class':'inlineFree'}).text
    for link in all_links:
        if '480P' in link:
            dict_quality['480'] = link
        if '720P' in link:
            dict_quality['720'] = link
        if '1080P' in link:
            dict_quality['1080'] = link
        if '240P' in link:
            dict_quality['240'] = link

    print("Quality Found : ")

    key = [key for key in (dict_quality.keys())]
    print(key)

    to_download = input("Please enter quality ,e.g 480 : ")

    while True:
        try:
            link_to_down = dict_quality[to_download]
            break
        except KeyError:
            print("Bad Choice Choose again")
            to_download = input("Please enter quality ,e.g 480 : ")
            continue
        except KeyboardInterrupt:
            sys.exit(0)
    download_file(link_to_down,filename=video_title)



def classifier():
    link = None
    try:
        link = sys.argv[1]
    except:
        print("Need valid video link")
        sys.exit(0)

    parsedurl = urlparse(link)
    domain = parsedurl.netloc
    if 'pornhub' in domain:
        phub(link)
    else:
        print('Invalid video link')


if __name__ == '__main__':
    phub('https://www.pornhub.com/view_video.php?viewkey=ph5d164e727f368')