from bs4 import BeautifulSoup
import requests
import time
from csv import writer
def find_jobs():
    html_text = requests.get('https://m.timesjobs.com/jobskill/python-jobs').text
    soup = BeautifulSoup(html_text,'lxml')
    jobs = soup.find_all('li')
    with open(f'Webscrape_2\posts\JOBS.csv','w') as f:
        thewriter = writer(f)
        header = ['Company name', 'Required Skills','Publishing Date','More Info']
        thewriter.writerow(header)
        
        for index, job in enumerate(jobs):
            try:
                published_date = job.find('span', class_ = 'posting-time').text
                company_name = job.find('h4').text
                skills_req = job.find('a').text
                more_info = job.find('h3').a['href']
            except AttributeError:
                published_date = '1404'
                company_name = '404'
                skills_req = '404'
                more_info = '404'

            if '1404' in published_date:
                continue
            else:
                pass
            info = [company_name,skills_req,published_date,more_info]
            thewriter.writerow(info)





if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 60
        print('waiting for a min')
        time.sleep(time_wait)

