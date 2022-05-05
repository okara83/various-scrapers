import requests
from bs4 import BeautifulSoup
import re
import bleach
import json
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
count=1
page = "https://www.winemag.com/?s=&drink_type=wine&page="
for i in range(1,14151):
    final_json={}
#     with open("wine_enthusiast_total_bottles-"+str(len(final_json))+"_last_page-"+str(i-1)+".json","w") as file:
#         json.dump(final_json,file)
    try:
        spec = page + str(i) + "&search_type=reviews"
        spec = "".join(requests.get(spec, headers=headers).text.split("\n"))
        spec = spec.replace("&#8211;","-")
        soup = BeautifulSoup(spec,'lxml')
        #print(spec)
        [tagstring.extract() for tagstring in soup('li', class_='search-results-ad')] 
        [tagstring.extract() for tagstring in soup('li', class_='review-advert')] 


        filtered_content = soup.find('div', class_='results')
        #filtered_content = re.findall(r"<a\shref=\"#\">[\d+\+-]<>.*?data-bucket-label=\"[^<>\.]\">\s*\n",spec,re.DOTALL)
        print(len(filtered_content))
        #print(type(filtered_content))
        allthem = re.findall(r"<li\sclass=\"review-item\">\s*<a\sclass=\"review-listing\srow\"\s[^<>]+?href=\"([^<>]+?)\".*?<h3\sclass=\"title\">([^<>]+?)<.*?<span\sclass=\"appellation\">([^<>]+?)</span>.*?\"excerpt\">(.*?)</div>.*?\"rating\"><strong>([\d\.]+?)</strong>",str(filtered_content),re.DOTALL)
        for j in allthem:
            #print(allthem,"\n\n")
            new_page = requests.get(j[0],headers=headers).text
            description = ""
            descript = re.search("<p\sclass=\"description\">(.*?)</p>", new_page, re.DOTALL)
            if descript:
                description=descript[1]
            primary = re.search(r"ul\sclass=\"primary-info\">(.*?)</ul>",new_page, re.DOTALL)
            price="NA"
            designation="NA"
            variety= "NA"
            winery= "NA"
            if primary:
                primary_info=" ".join(primary[1].split("\n")).replace("\n"," ")
                prices = re.search(r"<span>(\$\d+[^<>]*?)<",primary_info,re.DOTALL)
                if prices:
                    price = prices[1]
                designations = re.search(r"<span>Designation</span>.*?\</div>.*?\"info.*?\">.*?<span><span>([^<>]*?)<",primary_info,re.DOTALL)
                if designations:
                    designation = designations[1]
                varietys = re.search(r"<span>Variety</span>.*?varietals[^<>]+?>(.*?)<",primary_info,re.DOTALL)
                if varietys:
                    variety = varietys[1]
                appellations = re.search(r"<span>Appellation</span>.*?<div\sclass=\"info[^<>]+?>.*?<span><a\shref=[^<>]+?>(.*?)<",primary_info,re.DOTALL)
                if appellations:
                    appellation = appellations[1]
                winerys = re.search(r"<span>Winery</span>.*?<span><span><?a?.*?>?(.*?)<?/?a?>?</span></span>",primary_info,re.DOTALL)
                if winerys:
                    winery = winerys[1]

            alc = "NA"
            bottle_sz="NA"
            category = "NA"
            date_published = "NA"
            av_user_rating = "NA"
            secondary = re.search(r"ul\sclass=\"secondary-info\">(.*?)</ul>",new_page, re.DOTALL)
            if secondary:
                secondary_info= " ".join(secondary[1].split("\n")).replace("\n"," ")
                alc_con = re.search(r"<span>([0-9\.%]+?)</span>",secondary_info,re.DOTALL)
                if alc_con:
                    alc = alc_con[1]
                bottle_szs = re.search(r"<span>([0-9]+?\s?[mlML]+?)</span>",secondary_info,re.DOTALL)
                if bottle_szs:
                    bottle_sz= bottle_szs[1]
                categorys = re.search(r"<span>Category</span>.*?<div\sclass=.*?<span><span>(.*?)</span></span>",secondary_info,re.DOTALL)
                if categorys:
                    category= categorys[1]
                av_user_ratings = re.search(r"span\sid=\"user-rating\">(.*?)<",secondary_info,re.DOTALL)
                if av_user_ratings:
                    av_user_rating= av_user_ratings[1]
                date_publisheds = re.search(r"<span>Category</span>.*?>(\d{1,2}/\d{1,2}/\d{2,4})<",secondary_info,re.DOTALL)
                if date_publisheds:
                    date_published=date_publisheds[1]
            newst_soup = BeautifulSoup(new_page,'lxml')
            related_wines = []
            find_related = newst_soup.find('div', class_='related-wines')
            #print(find_related)
            if find_related  !="" and find_related !=None:
                find_related = " ".join(str(find_related).split("\n"))
                related_wines = re.findall(r"<h3\sclass=\"title\">(.*?)</h3>",find_related,re.DOTALL)
                
            final_json[j[1]] = {"url": j[0], "name":j[1], "score":j[4], "appellation":j[2],"excerpt":j[3].replace("\xa0"," ").strip(),"description":description, "price":price,"designation":designation,"variety":variety, "alcohol_content":alc,"bottle_size":bottle_sz,"category":category,"date_published":date_published,"average_user_rating":av_user_rating,"winery":winery, "related_wines":related_wines}
#             with open("wines/wine_enthusiast_total_bottles-"+str(len(final_json))+"_last_page-"+str(i-1)+".json","w") as file:
#                 json.dump(final_json,file)
            print(count,i)
            count+=1
            #print(final_json)
        with open("wines/wine_enthusiast_total_bottles-"+str(len(final_json))+"_last_page-"+str(i-1)+".json","w") as file:
            json.dump(final_json,file)
    except:
        with open("wines/wine_enthusiast_total_bottles-"+str(len(final_json))+"_last_page-"+str(i-1)+".json","w") as file:
             json.dump(final_json,file)
        break
with open("wines/wine_enthusiast_total_bottles-"+str(len(final_json))+"_last_page-"+str(i-1)+".json","w") as file:
    json.dump(final_json,file)