import requests, re, copy
from bs4 import BeautifulSoup, NavigableString, Comment
from urllib.parse import urlparse,urljoin
# from selenium import webdriver
# import time

def get_links():
    with open('urls.txt','r') as f:
        lines = f.readlines()
        links = [line.rstrip() for line in lines]
        return links

class SiteScrapper:
    """This will take care of all individual website link."""
    def __init__(self, url:str):
        self.url = url
        self.root_url = []
        self.getRootUrl()
        self.title = None
        self.page = None
        self.contents = None
        self.min_content = 20
        self.getPage()
        self.review_content = None
        # self.getContents()
        self.getContentsBody()

        self.inpage_links, self.internal_links, self.outbound_links = [],[],[]
        self.getLinks()
    
    def getRootUrl(self):
        url = urlparse(self.url)
        self.root_url = self.url.replace(url.path,"")
    
    def getPage(self):
        """This will make get request and collect whole page content."""
        print("Requesting:",self.url)
        source = requests.get(self.url).text
        # driver = webdriver.Chrome('G:\\Tools\\webdrivers\\chromedriver_win32\\chromedriver.exe')
        # driver.get(self.url)
        # time.sleep(10)
        # source = driver.page_source
        # driver.quit()
        # with open("content.html","w+",encoding='utf-8') as f:
        #     f.write(source)

        soup = BeautifulSoup(source,'html.parser')
        self.title = soup.title.text
        self.page = soup.html
        # Initialize the content
        self.contents = soup.new_tag("div")
    
    def getContentsBody(self):
        self.contents = copy.copy(self.page.body)
        self.removeGarbage()
        self.review_content = self.contents.get_text()
    
    def getContents(self):
        # step-1 filter (limit the source)
        # Find section tag
        contents = self.page.find('section')
        if not contents or self.ok():
            # Find Article tag
            contents = self.page.find('article')
            if not contents or self.ok():
                # find main tag or div id='main'
                contents = self.page.find('main') or self.page.find(id='body')
                if not contents or self.ok():
                    contents = self.page.body
        
        # step-2 filter (find what we need)
        contents = contents.findAll(['div','p','h2','h3','h4'])

        for c in contents:
            # Remove tag if contents is too short
            if self.contentLength(c.text) > 1 and c.text != " ":
                self.contents.append(c)
        
        self.removeGarbage()
        soup = BeautifulSoup("<br/>".join([str(tag) for tag in contents]),'html.parser')
        self.review_content = soup.get_text()
    
    def getContents2(self):
        tags = self.page.find_all(['p','h2','h3','h4'])
        count = 0
        for tag in tags:
            siblings = tag.next_siblings
            for sibling in siblings:
                if sibling.name == 'p':
                    count += 1
            if count > 5:
                self.contents = tag.parent
                break
        self.removeGarbage()
 
    def removeGarbage(self):
        # Garbage collection
        garbages = self.contents.findAll([
            'form','input','label','header','footer','aside','nav', 'button',
            'script','style','link','meta','noscript',
            'svg','desc'
            ])
        garbages += self.contents.find_all(class_=re.compile("nav"))
        garbages += self.contents.find_all(class_=re.compile("menuitems"))
        garbages += self.contents.find_all(class_=re.compile("sub-menu"))
        garbages += self.contents.find_all(class_=re.compile("main-header-w"))
        garbages += self.contents.find_all(class_=re.compile("mobile-header-w"))
        garbages += self.contents.find_all(class_=re.compile("footer"))
        garbages += self.contents.find_all(class_=re.compile("author"))
        garbages += self.contents.find_all(class_=re.compile("comment"))
        garbages += self.contents.find_all(class_=re.compile("social-"))
        garbages += self.contents.find_all(class_=re.compile("disclosure-"))
        garbages += self.contents.find_all(class_=re.compile("sr-only"))
        garbages += self.contents.find_all(class_=re.compile("newsletter"))
        garbages += self.contents.find_all(class_=re.compile("signup"))
        garbages += self.contents.find_all(class_=re.compile("top-profile-links-box"))
        garbages += self.contents.find_all(class_="page-sidebar")
        garbages += self.contents.find_all(class_=re.compile("icon"))
        garbages += self.contents.find_all(class_=re.compile("fa"))

        garbages += self.contents.find_all(id=re.compile("sidebar"))
        garbages += self.contents.findAll(attrs={'aria-hidden':'true'})
        # garbages += self.contents.find_all(string=lambda text: isinstance(text, Comment))

        anchors = self.contents.find_all('a')
        for a in anchors:
            if a.parent.name != 'p' and not a.find('img'):
                garbages.append(a)

        for tag in garbages:
            if not tag.decomposed:
                tag.decompose()
        
    def ok(self):
        return self.contentLength(self.contents.text) < self.min_content
    
    def getLinks(self):
        links = self.page.find_all('a')
        for link in links:
            href = link.get('href')
            href_type = self.getLinkType(href)
            if href_type=='inpage':
                self.inpage_links.append(self.url+href)
            elif href_type=='internal':
                if href.startswith('/'):
                    href = self.root_url + href
                elif not href.startswith('/'):
                    href = urljoin(self.root_url,href)
                self.internal_links.append(href)
            elif href_type=='external':
                self.outbound_links.append(href)
    
    def getLinkType(self, href):
        # Check if internal or external
        if href is not None:
            if href == '/' or href.startswith('#'):
                return "inpage"
            elif href.startswith(self.root_url) or href.startswith('/') or '/' not in href:
                # if href.startswith('/'):
                return "internal"
                
            else:
                return "external"
            # elif not href.startswith(self.root_url):
            #     return "external"
            # else:
            #     return "internal"
    
    def getImageAltText(self):
        images_alt_texts = []
        for image in self.contents.find_all('img'):
            text = image.get('alt')
            src = image.get('src')

            if text is not None and text != '':
                src_type = self.getLinkType(src)
                if src_type == 'internal':
                    src = self.root_url+src
                elif src_type == 'inpage':
                    src = self.url+src
                images_alt_texts.append({'src':src, 'alt':text})
        return images_alt_texts
    
    def getSubHeadings(self):
        # sub_headings = self.contents.findAll(['h2','h3','h4'])
        h1 = self.page.findAll('h1')
        h2 = self.page.findAll('h2')
        h3 = self.page.findAll('h3')
        h4 = self.page.findAll('h4')
        h1 = [" ".join(subheading.text.strip().split()) for subheading in h1]
        h2 = [" ".join(subheading.text.strip().split()) for subheading in h2]
        h3 = [" ".join(subheading.text.strip().split()) for subheading in h3]
        h4 = [" ".join(subheading.text.strip().split()) for subheading in h4]
        return {"h1":h1,"h2":h2,"h3":h3,"h4":h4}
        # return [" ".join(subheading.text.strip().split()) for subheading in sub_headings]

    def getImportant(self):
        texts = self.contents.find_all('strong')
        # print(texts)
    
    def contentLength(self, str):
        result = str.strip().split()
        return len(result)

    def getMetaDescription(self):
        meta = self.page.find('meta',attrs={'name':'description'})
        if meta is not None:
            return meta['content']
        else:
            return ''

    def getProducts(self,taglist=['h2','h3','h4']):
        tags = self.page.find_all(taglist)
        output = []
        pattern = re.compile(r'\d+[.]\s?')
        for tag in tags:
            # print(tag.text)
            content = pattern.sub("",tag.text).strip()
            if tag.has_attr('class'):
                classes = " ".join(tag['class'])
            else: classes = ''
            output.append({'name':tag.name, 'class':classes, 'content':content})
            # if len(tag.contents) == 1 and isinstance(tag.contents[0], NavigableString):
                # content = pattern.sub("",tag.contents[0])
                # output.append({'name':tag.name, 'content':content})
        return output



# Sc = SiteScrapper('https://nijhoom.com/top-bangladeshi-food/')  
# Sc.getProductsHtml()         