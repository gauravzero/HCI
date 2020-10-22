
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import requests

#sites=["https://nrega.nic.in/netnrega/home.aspx","https://www.usa.gov/","https://www.bits-pilani.ac.in/","https://www.isro.gov.in/","https://medium.com/"]
sites=["https://www.usa.gov/","https://www.bits-pilani.ac.in/","https://www.isro.gov.in/","https://medium.com/"]
final=pd.DataFrame()
for w in sites:
    browser= webdriver.Chrome()
    browser.accept_untrusted_certs = True

    browser.get(w)
    #browser.find_element_by_class_name('close').click()
    links=browser.find_elements(By.TAG_NAME,"a")
    browser.close()
    avglinktime=[0]*len(links)

    for t in range(5):
        browser= webdriver.Chrome()
        browser.accept_untrusted_certs = True
        browser.set_page_load_timeout(30)
        browser.maximize_window()
        browser.get(w)
        #browser.find_element_by_class_name('close').click()
        d=browser.title
        print(browser.title)
        print(browser.current_url)
        links=browser.find_elements(By.TAG_NAME,"a")
        k=[]
        print(len(links))
        for i in range(len(links)):
            k.append(links[i].get_attribute('href'))
        browser.close()
        c=0
        d=0
        a=[]
        b=[]
        dead=[]
        for i in k:
            try:
                browser= webdriver.Chrome()
                browser.accept_untrusted_certs = True
                x=time.time()
                browser.get(i)
                y=time.time()
                r=requests.head(i)
                a.append(y-x)
                b.append(r.status_code)
                if(r.status_code==404):
                    c+=1
                    dead.append("Y")
                else:
                    dead.append("N")
                browser.back()
            except TimeoutException:
                a.append(30)
                b.append(404)
                dead.append("Y")
                browser.back()

        avglinktime=[avglinktime[i]+a[i] for i in range(len(a))]
        browser.close()



    theavglinktime=[(avglinktime[i]/5) for i in range(len(avglinktime))]
    x=pd.DataFrame({'Website':w,'Link':k,'LinkLoad Time':theavglinktime,'Status':b,'Dead Links':dead})
    final=final.append(x)
    print(final)
    browser.close()
print(final)
final.to_csv('fivesites.csv')
