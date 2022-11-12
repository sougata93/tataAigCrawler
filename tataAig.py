from bs4 import BeautifulSoup
import requests
import re
from playwright.sync_api import sync_playwright
import os


url="https://www.tataaig.com/public-disclosures"
domain="https://www.tataaig.com"

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
res=requests.get(url,headers=headers)

urlFilter='.*.pdf$'
year=['2021-22','2022-23']
count=0


def run(FY,Q):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        # Click text=Public Disclosures >> nth=1
        if FY=='22_23':
            page.locator("text=Public Disclosures").nth(1).click()

        # page.locator("text=Public Disclosures").nth(2).click()
        # page.locator("text=Public Disclosures").nth(3).click()
        # page.locator("text=Public Disclosures").nth(4).click()

            return page.content()
        if FY=='21_22':
            print('hi')
    
            page.locator("#model div:has-text(\"2022-23\")").nth(1).click()
                    # Click #react-select-model-option-1 div:has-text("2021-22")
            page.locator("#react-select-model-option-1 div:has-text(\"2021-22\")").click()
            if Q=='q1':
                    page.locator(".subHeading").first.click()
                    return page.content()
            if Q=='q2':
                    page.locator("div:nth-child(2) > div:nth-child(2) > div > .subHeading").click()
                    return page.content()
            if Q=='q3':
                    page.locator("div:nth-child(3) > div:nth-child(2) > div > .subHeading").click()
                    return page.content()
            if Q=='q4':
                    page.locator("div:nth-child(4) > div:nth-child(2) > div > .subHeading").click()
                    return page.content()
def tata(FY,Q):

    data=run(FY,Q)

    if data==None:
        return
    soup=BeautifulSoup(data,'lxml')

    yearText=soup.find('div',class_='select-field__single-value css-1aghscs-singleValue')
    yearText=yearText.text
    print(yearText)
    t=soup.find('div',class_='container borderBottom pb-5')
    x=t.find_all('div',class_='py-4')
    count=0
    for i in x: 
        q=i.find('div',class_='subHeading0 mb-3')
        q=q.text
        print(q)

        if Q in q.lower():
            tableData=soup.find('div',class_='card-body contentClass1 accordionBodyPadding')
            # d=tableData.find('div',class_='collapse show')
            tbody = tableData.find('tbody')
        # print(tbody.text)
            for r in tbody.find_all('tr'):

                count=0
                reftext=''

                for rd in r.find_all('td'):
                    if count<2:
                        reftext=reftext+" "+rd.text
                        count=count+1
        
                    link=rd.find('a')

                    if link!=None:
                        path=link.get('href')
                        print(path)
                        print('hi')
            
                        if(re.search(urlFilter,path)):
                            print(path)
                            pdfData=requests.get(path)
                            # open("tata_"+yearText+q+reftext+".pdf", 'wb').write(pdfData.content)
                            p=os.path.join('22_23',"tata_"+q+reftext+".pdf")
                            open(p, 'wb').write(pdfData.content)

                

tata('22_23','q1')
# tata('21_22','q1')
# tata('21_22','q2')
# tata('21_22','q3')
# tata('21_22','q4')


        