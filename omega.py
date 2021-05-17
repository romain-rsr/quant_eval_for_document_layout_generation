




## webscraper indeed

import urllib.request
from bs4 import BeautifulSoup
import requests
from lxml import html
import requests

p_code="/home/paintedpalms/rdrive/taff/code"



import time

def get_posting_info(url_posting,option,k):

    sub_page = requests.get(url_posting)
    sub_soup = BeautifulSoup(sub_page.content, 'html.parser')

    company_name=""
    location=""
    contract_type=""
    contract_infos=[]
    job_description=""

    # get job title
    job_title=""
    nodes=sub_soup.find_all("h1")
    for n in nodes:
        s="jobsearch-JobInfoHeader-title"
        cl=n.get_attribute_list("class")
        if s in cl:
            job_title=n.get_text()

    # get company infos
    company_infos=[]
    nodes=sub_soup.find_all("div")
    for n in nodes:
        s="InlineCompanyRating"
        cl=n.get_attribute_list("class")
        if len(cl)>0:
            if cl[0] is not None:
                if s in cl[0]:
                    '''
                    txt=n.get_text()
                    company_name=txt.split("-")[0]
                    location=txt.split("-")[1]
                    '''                    
                    sub_nodes=n.findChildren()
                    for sn in sub_nodes:
                        txt=sn.get_text()
                        if txt not in company_infos and len(txt)>1:
                            company_infos.append(txt)

    # get contract infos
    contract_infos=[]
    nodes=sub_soup.find_all("div")
    for n in nodes:
        s="JobMetadataHeader-item"
        cl=n.get_attribute_list("class")
        if len(cl)>0:
            if cl[0] is not None:
                if s in cl[0]:
                    sub_nodes=n.findChildren()
                    for sn in sub_nodes:
                        txt=sn.get_text()
                        if txt not in contract_infos:
                            contract_infos.append(txt)

    # get job description
    job_description=""
    nodes=sub_soup.find_all("div")
    for n in nodes:
        s="jobDescriptionText"
        cl=n.get_attribute_list("class")
        #print(cl)
        if len(cl)>0:
            if cl[0] is not None:
                if s in cl[0]:
                    job_description=n.get_text()

    # get publication date
    pub_date=""
    nodes=sub_soup.find_all("div")
    for n in nodes:
        s="jobsearch-JobMetadataFooter"
        cl=n.get_attribute_list("class")
        if len(cl)>0:
            if cl[0] is not None:
                if s in cl[0]:
                    sub_nodes=n.findChildren()
                    for sn in sub_nodes:
                        txt=sn.get_text()
                        if "-" in txt and "continuer" not in txt:
                            pub_date=txt.split("-")[1]


    if option=="print":

        print("url_posting",url_posting)
        print("")
        print("job_title",job_title)
        print("")
        print("company_name",company_name)
        print("")
        print("location",location)
        print("")
        for ci in contract_infos:
            print("ci",ci)
            print("")
        print("job_description",job_description)
        print("")

    if option=="save":
        
        sep="\n\n"

        s=""
        s+="####################### url_posting"+sep+url_posting+sep
        s+="####################### job_title"+sep+job_title+sep
        #s+="#company_name"+sep+company_name+sep
        #s+="#location"+sep+location+sep
        s+="####################### company_infos"+sep
        for ci in company_infos:s+=ci+sep
        s+="####################### contract_infos"+sep
        for ci in contract_infos:s+=ci+sep
        s+="####################### job_description"+sep+job_description+sep
        s+="####################### pub_date"+sep+pub_date+" (scrap date "+get_simple_time_str().split("_")[0]+")"+sep

        company_name=""
        if len(company_infos)>0:
            company_name=company_infos[0]
        company_name=company_name.replace("/","_")
        company_name=company_name.replace(" ","_")
        
        #p="/home/paintedpalms/rdrive/taff/code/forecast"+"/"+get_simple_time_str()+"_"+job_title+".txt"
        #p="/home/paintedpalms/rdrive/taff/code/forecast"+"/"+get_simple_time_str()+"_"+get_random_id()+".txt"
        p="/home/paintedpalms/rdrive/taff/code/forecast"+"/"+get_simple_time_str()+"_"+get_trigram_count(k)+"_"+company_name+".txt"
        file=open(p,"w")
        file.write(s)
        file.close()

# get job posting urls
def get_posting_urls(soup):

    sub_urls=[]
    nodes=soup.find_all("a")

    for n in nodes:
        ok=0
        if isinstance(n.get_attribute_list("id"), list):
            for v in n.get_attribute_list("id"):
                if type(v)!=type(None):
                    if "jl_" in v or "sja" in v:ok=1
        if ok:
            ext_url=n.get_attribute_list("href")[0]
            new_url="https://fr.indeed.com"+ext_url
            print(new_url)
            sub_urls.append(new_url)
    return sub_urls


if 1==0:

    #url="https://fr.indeed.com/emplois?q=Deep+Learning&sort=date"
    #url="https://fr.indeed.com/emplois?q=Deep+Learning&sort=date&start=570"

    urls=[]
    pages=[]
    url_start="https://fr.indeed.com/emplois?q=Deep+Learning&sort=date"

    ##########
    start=30 #1
    end=57 #58
    ##########

    if start==0:
        urls.append(url_start)
        pages.append("start page")

    for k in range(max(start,1),end):
        page=str(k*10)
        url=url_start+"&start="+page
        print(url)
        urls.append(url)
        pages.append(page)

    #for url in urls:
    #url=urls[2]
    #if 1==1:
    k=0
    k_page=0
    for url in urls:

        m=60
        if k_page%7==0 and k_page>0:
            
            print("sleep for 1 hour",time.ctime())
            time.sleep(60*m)

        #time.sleep(20)
        print("\n\n\n\n\n--------------- page",pages[k_page],"\n\n\n\n\n")
        k_page+=1

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        sub_urls=get_posting_urls(soup)
        for url_posting in sub_urls:

            #time.sleep(20)
            print("next url posting ...")

            get_posting_info(url_posting,"save",k)
            k+=1


## webscraper

# public imports

import urllib.request
from bs4 import BeautifulSoup
import requests

class WebScrapper():

    def __init__(self):
        return None

    def get_images_from_url(url):
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        image_tags = soup.find_all('img')
        elem_urls = []
        for tag in image_tags:
            image_name = tag['src']
            image_url = url+'/'+image_name
            elem_urls.append(image_url)
        return elem_urls

## layout display


import random
import numpy as np

class clay():
    def __init__(self):
        return None

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        visual eval : display
#------------------------------------------------------------------------------------------------------------------------------------

def display_bboxes_and_images_rico(bboxes_rico,start,end):
    indexes=range(start,end)
    for i_sample in range(len(indexes)):
        print("-------------------",i_sample)
        bboxes=bboxes_rico[i_sample]
        img1=show_bboxes(bboxes,"",2560,1440)
        img2=get_rico_image(names[indexes[i_sample]])
        display(img2)
        display(img1)

def show_synth_sample1(sample):
    npa_bg=get_npa_sample(sample)
    display(get_image_from_npa(npa_bg))

# poor # sub : rasterize_sample
def show_synth_sample_quick(sample,saving_path,h,w):
    alpha=1/10
    
    '''
    if h==None:h=int(alpha*600)
    if w==None:w=int(alpha*300)
    '''

    #'''
    if h==None:600
    if w==None:300
    h=int(alpha*h)
    w=int(alpha*w)
    #'''
      
    
    npa_bg=get_npa_bg2(h,w)
    for i_asset in range(len(sample.assets)):
        asset=sample.assets[i_asset]
        '''
        if i_asset==0:r,g,b=255,100,100
        if i_asset==1:r,g,b=100,255,100
        if i_asset==2:r,g,b=100,100,255
        '''
        r,g,b=100,100,100
        if asset.type=="red":r,g,b=255,100,100
        if asset.type=="green":r,g,b=100,255,100
        if asset.type=="blue":r,g,b=100,100,255
        
        if asset.type=="text":r,g,b=100,255,100
        if asset.type=="image":r,g,b=100,100,255
        if asset.type=="logo":r,g,b=255,100,100
        if asset.type=="cta":r,g,b=100,255,255

        npa_bg=add_shape(npa_bg,int(asset.top*h/600),int(asset.left*w/300),int(asset.low*h/600),int(asset.right*w/300),r,g,b)
    #npa_bg=resize_image(npa_bg,100)
    
    img=get_image_from_npa(npa_bg)
    if saving_path=="":return img #display(img)
    if saving_path=="npa":return npa_bg
    if saving_path not in ["","npa"]:img.save(saving_path)

# show bboxes
def show_bboxes(bboxes,saving_path,h,w):
    # bbox : top,left,low,right
    npa_bg=get_npa_bg3(h,w)
    for bbox in bboxes:
        npa_bg=add_shape2(npa_bg,bbox[0],bbox[1],bbox[2],bbox[3],random.randint(0,255),random.randint(0,255),random.randint(0,255))
    npa_bg=resize_image(npa_bg,100)
    img=get_image_from_npa(npa_bg)
    if saving_path=="":return img
    if saving_path=="npa":return npa_bg
    if saving_path not in ["","npa"]:img.save(saving_path)

def show_synth_sample(sample,saving_path,h,w):

    if h==None:h=600
    if w==None:w=300
    npa_bg=get_npa_bg2(h,w)
    for i_asset in range(len(sample.assets)):
        asset=sample.assets[i_asset]
        '''
        if i_asset==0:r,g,b=255,100,100
        if i_asset==1:r,g,b=100,255,100
        if i_asset==2:r,g,b=100,100,255
        '''
        r,g,b=100,100,100
        if asset.type=="red":r,g,b=255,100,100
        if asset.type=="green":r,g,b=100,255,100
        if asset.type=="blue":r,g,b=100,100,255
        
        if asset.type=="text":r,g,b=100,255,100
        if asset.type=="image":r,g,b=100,100,255
        if asset.type=="logo":r,g,b=255,100,100
        if asset.type=="cta":r,g,b=100,255,255

        npa_bg=add_shape(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)

    npa_bg=resize_image(npa_bg,100)
    img=get_image_from_npa(npa_bg)
    if saving_path=="":return img #display(img)
    if saving_path=="npa":return npa_bg
    if saving_path not in ["","npa"]:img.save(saving_path)
    


# ajouter pour show rapidement synth samples
#def show_synth_sample3sample,saving_path,h,w):


# à corriger (à juste vérifier ?)
def show_synth_sample2(sample,saving_path,h,w):

    if 1==0:
        if h==None:h=600
        if w==None:w=300
        npa_bg=get_npa_bg2(h,w)
        for i_asset in range(len(sample.assets)):
            asset=sample.assets[i_asset]
            r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
            npa_bg=add_shape(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
    
    if 1==1:
        if h==None:h=600
        if w==None:w=300
        npa_bg=get_npa_bg3(h,w)
        for i_asset in range(len(sample.assets)):
            asset=sample.assets[i_asset]
            r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
            npa_bg=add_shape2(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
        npa_bg=resize_image(npa_bg,100)

    npa_bg=resize_image(npa_bg,100)
    img=get_image_from_npa(npa_bg)

    if saving_path=="":return img #display(img)
    if saving_path=="npa":return npa_bg
    if saving_path not in ["","npa"]:img.save(saving_path)
                
'''
def get_npa_sample(sample):
    npa_bg=get_npa_bg()
    for i_asset in range(len(sample.assets)):
        asset=sample.assets[i_asset]
        r,g,b=100,100,100
        if asset.type=="text":r,g,b=100,255,100
        if asset.type=="image":r,g,b=100,100,255
        if asset.type=="logo":r,g,b=255,100,100
        if asset.type=="cta":r,g,b=100,255,255
        npa_bg=add_shape(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
    return npa_bg
'''

def get_npa_bg():
    r,g,b=100,100,100
    npa_bg=np.zeros((600,300,4),dtype=np.uint8)
    for i in range(600):
        for j in range(300):
            npa_bg[i,j,0]=r
            npa_bg[i,j,1]=g
            npa_bg[i,j,2]=b
            npa_bg[i,j,3]=255
    return npa_bg

def get_npa_bg2(h,w):
    r,g,b=100,100,100
    npa_bg=np.zeros((h,w,4),dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            npa_bg[i,j,0]=r
            npa_bg[i,j,1]=g
            npa_bg[i,j,2]=b
            npa_bg[i,j,3]=255

    return npa_bg

def get_npa_bg3(h,w,option_color):
    if option_color==1:r,g,b=100,100,100
    if option_color==2:r,g,b=212,230,242 #129,198,245 # 175,210,233
    npa_bg=np.zeros((h,w,4),dtype=np.uint8)
    npa_bg[:,:,0]=r
    npa_bg[:,:,1]=g
    npa_bg[:,:,2]=b
    npa_bg[:,:,3]=255
    return npa_bg

def save_synth_sample_png(sample,saving_path): 
    npa_bg=get_npa_bg()
    for asset in sample.assets:
        r,g,b=200,200,200
        npa_bg=add_shape(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
    get_image_from_npa(npa_bg).save(saving_path,"PNG")

# left top width height + no type
def create_sample_from_boxes1(boxes):
    sample=clay() 
    sample.assets=[]
    for box in boxes:
        asset=clay()
        asset.left=box[0]
        asset.top=box[1]
        asset.width=box[2]
        asset.height=box[3]
        asset.right=asset.left+asset.width
        asset.low=asset.top+asset.height 
        asset.type="text"
        sample.assets.append(asset)
    return sample    


# left top width height + rico asset type
def create_sample_from_boxes2(boxes):
    sample=clay() 
    sample.assets=[]
    for box in boxes:
        asset=clay()
        asset.left=box[0]
        asset.top=box[1]
        asset.width=box[2]
        asset.height=box[3]
        asset.type=box[4]
        asset.right=asset.left+asset.width
        asset.low=asset.top+asset.height 
        sample.assets.append(asset)
    return sample  

def get_synth_sample_png(sample):
    npa_bg=get_npa_bg()
    for i_asset in range(len(sample.assets)):
        asset=sample.assets[i_asset]
        '''
        if i_asset==0:r,g,b=255,100,100
        if i_asset==1:r,g,b=100,255,100
        if i_asset==2:r,g,b=100,100,255
        '''
        r,g,b=100,100,100
        if asset.type=="text":r,g,b=100,255,100
        if asset.type=="image":r,g,b=100,100,255
        if asset.type=="logo":r,g,b=255,100,100
        if asset.type=="cta":r,g,b=100,255,255
        npa_bg=add_shape(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
    npa_bg=resize_image(npa_bg,100)
    return npa_bg

# get sample image npa from sample name
def get_screenshot_npa(file_name):
    root_path='/home/paintedpalms/rdrive/taff/data/automated_layout_real/pubs_madmix/segm2'
    image_path=root_path+'/'+file_name
    #image = PIL.Image.open(image_path, "r")
    image=Image.open(image_path, "r")
    npa = np.asarray(copy.copy(image))
    return npa
                       
def visual_eval(samples_test,samples_pred,names):
    for i_sample in range(len(samples_test)):
        visual_eval_single(samples_test[i_sample],samples_pred[i_sample],names[i_sample])

#def visual_eval_single(sample_test,sample_pred,name):
def visual_eval_single(sample_test,sample_pred,name,display_option):
    n_assets=3
    saving_path="results"
    npa=get_screenshot_npa(name)
    npa_bg=get_npa_bg()
    for i_asset in range(n_assets):
        # predicted asset + original asset
        asset_test=sample_test.assets[i_asset]
        asset_pred=sample_pred.assets[i_asset]
        top_new,left_new,low_new,right_new=asset_pred.top,asset_pred.left,asset_pred.low,asset_pred.right
        top_src,left_src,low_src,right_src=int(asset_test.top),int(asset_test.left),int(asset_test.low),int(asset_test.right)
        npa_asset=npa[top_src:low_src,left_src:right_src]
        npa_asset=resize_image(npa_asset,asset_pred.width)
        for i in range(len(npa_asset)):
            for j in range(len(npa_asset[0])):
                i_bg=top_new+i
                j_bg=left_new+j
                if 0<i_bg<600 and 0<j_bg<300:
                    npa_bg[i_bg,j_bg]=npa_asset[i,j]
    npa_sample=get_screenshot_npa(name)
    npa_couple=np.concatenate((npa_bg,npa_sample),axis=1)
    image_couple=get_image_from_npa(npa_couple)
    
    if display_option==1:display(image_couple)
    if display_option==2:image_couple.save(saving_path+'/'+str(i_sample)+'.png',"PNG")
                       
# show gan synth layouts
def show_gan_synth_layouts(c,samples_gan,i_epoch,save_option):
    for i_sample in range(min(len(samples_gan),100)):
        if save_option==0:p=""
        if save_option==1:p=c.results_folder+"/ep"+str(i_epoch)+"_sample"+str(i_sample)+".png"
        show_synth_sample(samples_gan[i_sample],p,None,None)

def save_visual_inputs_and_outputs(samples_test,names,folder_name):
    root_path='/home/paintedpalms/rdrive/taff/data/automated_layout_real/pubs_madmix/segm3'
    n_assets=3
    for i_sample in range(1):
        name=names[i_sample]
        saving_path=root_path+'/'+folder_name
        npa=get_screenshot_npa(name)
        npa_bg=get_npa_bg()
        for i_asset in range(n_assets):
            # predicted asset + original asset
            asset_test=samples_test[i_sample].assets[i_asset]
            top_src,left_src,low_src,right_src=int(asset_test.top),int(asset_test.left),int(asset_test.low),int(asset_test.right)
            npa_asset=npa[top_src:low_src,left_src:right_src]
            npa_asset=resize_image(npa_asset,asset_test.width)
            image_asset=get_image_from_npa(npa_asset)
            image_asset.save(saving_path+'/'+str(i_sample)+'_'+str(i_asset)+'.png',"PNG")
        npa_sample=get_screenshot_npa(name)
        image_sample=get_image_from_npa(npa_sample)
        image_sample.save(saving_path+'/'+str(i_sample)+'.png',"PNG")

## layout eval

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        public imports
#------------------------------------------------------------------------------------------------------------------------------------

# ok

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        quant eval : diversity
#------------------------------------------------------------------------------------------------------------------------------------

# measure diversity in samples generated by layout gan
def diversity_eval(samples):
    combinaisons=[]
    for sample in samples:
        combinaison=[]
        for asset in sample.assets:
            combinaison.append(asset.type)
        if combinaison not in combinaisons:combinaisons.append(combinaison)
    return len(combinaisons)#/max(1,len(samples))

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        quant eval : error
#------------------------------------------------------------------------------------------------------------------------------------




# eval samples concerned by general rules only
# ancien
def quant_eval(samples,str_option,w,h):

    #h=600
    #w=300
        
    top_overtakings=[]
    left_overtakings=[]
    right_overtakings=[]
    low_overtakings=[]
    overtakings=[]
    overlaps_btw_assets=[]
    
    n_samples=len(samples)
    n_assets=3
    n_samples_in_error=0
    n_assets_in_error=0
    
    # overlap or exceeding screen limits => error
    for sample in samples:
        prev_low=0
        sample_is_in_error=0
        for i_asset in range(n_assets):
            asset_is_in_error=0
            asset=sample.assets[i_asset]
            if i_asset==0 and asset.top<0:
                asset_is_in_error=1
                sample_is_in_error=1
                top_overtakings.append(0-asset.top)
            if i_asset==n_assets-1 and asset.low>h:
                asset_is_in_error=1
                sample_is_in_error=1
                low_overtakings.append(asset.low-h)
            if asset.left<0:
                asset_is_in_error=1
                sample_is_in_error=1
                left_overtakings.append(0-asset.left)
            if asset.right>w:
                asset_is_in_error=1
                sample_is_in_error=1
                right_overtakings.append(asset.right-w)
            if i_asset>0 and asset.top<prev_low:
                asset_is_in_error=1
                sample_is_in_error=1              
                overlaps_btw_assets.append(prev_low-asset.top)
                
            prev_low=asset.low
                
            n_assets_in_error+=asset_is_in_error
        n_samples_in_error+=sample_is_in_error
        
    for values in left_overtakings,top_overtakings,right_overtakings,low_overtakings:
        for v in values:overtakings.append(v)
        
    results={}
    results["overtakings"]={}
    results["overtakings"]["all"]=overtakings
    results["overtakings"]["left"]=left_overtakings
    results["overtakings"]["top"]=top_overtakings
    results["overtakings"]["right"]=right_overtakings
    results["overtakings"]["low"]=low_overtakings
    results["overlaps"]=overlaps_btw_assets
    results["n_samples"]=n_samples
    results["n_samples_in_error"]=n_samples_in_error
    results["n_assets"]=n_assets*n_samples
    results["n_assets_in_error"]=n_assets_in_error
    results["samples_in_error"]=n_samples_in_error/max(1,n_samples)
    results["assets_in_error"]=n_assets_in_error/max(1,(n_samples*n_assets))

    if 0==1:

        name="samples in error"
        
        if len(name)<=7:after_name="\t\t\t:"
        if len(name)>7:after_name="\t\t:"
        if len(name)>15:after_name="\t:"
    
    if 1==1:
        
        s=""
        
        s+="\n"
        s+="quant eval"+"\n"
        s+="\n"

   
        for k0 in results.keys():
 
            if type(results[k0])!=dict:
                if str_option==0:display_stats_line(k0,results[k0])
                if str_option==1:
                    if k0 in ["samples_in_error","assets_in_error"]:
                        s+=get_str_with_tabs(k0,results[k0],3)#+"\n"
                  
        for k0 in results.keys():
            if type(results[k0])==dict:
                for k1 in results[k0].keys():
                    if str_option==0:display_stats_line(k1,results[k0][k1])
                    if str_option==1:
                        if k1 in ["samples_in_error","assets_in_error"]:
                            s+=get_str_with_tabs(k1,results[k0][k1],3)#+"\n"
                            

    return s,n_samples_in_error/max(1,n_samples)
  
#------------------------------------------------------------------------------------------------------------------------------------
#                                                        quant eval : error
#------------------------------------------------------------------------------------------------------------------------------------

def quant_eval0(samples):
    m=0
    w=300
    h=600
    k=0
    k_bench=0
    ks=0
    s=0
    k_overlap=0
    for sample in samples:
        k_bench+=1
        i=0
        prev_low=0
        for asset in sample.assets:
            if i>0:prev_low=sample.assets[i-1].low
            next_top=h
            if i<2:next_top=sample.assets[i+1].top
            i+=1
            k_temp=k
            if asset.top<prev_low-m*2:
                k+=1
                s+=abs(asset.top-prev_low)
                k_overlap+=1
            '''
            if asset.low>next_top+m*2:
                k+=1
                s+=abs(asset.low)
                k_overlap+=1
            '''
            if asset.right>w+m:
                k+=1
                s+=abs(asset.right-w)
            if asset.low>h+m*2:
                k+=1
                s+=abs(asset.low-h)
            if asset.left<0-m:
                k+=1
                s+=abs(asset.left)
            '''
            if asset.top<0-m*2:
                k+=1
                s+=abs(asset.top)
            '''
            if k>k_temp:ks+=1
    if ks==0:print("eval",k_bench,k,s)
    if ks!=0:print("eval",k_bench,k,s/ks)

               
#features distributions (no error measurement !!!)

def init_stats(c):
    stats={}
    stats["lefts"]=[]
    stats["tops"]=[]
    stats["rights"]=[]
    stats["last lows"]=[]
    stats["lateral mids"]=[]
    stats["vertical mids"]=[]
    
    for i_asset in range(c.n_assets):
        stats[i_asset]={}
        for tp in c.types:
            stats[i_asset][tp]={}
            for ft in c.features:
                stats[i_asset][tp][ft]=[]
    return stats

def get_stats(c,samples):
    stats=init_stats(c)
    for i_sample in range(len(samples)):
        sample=samples[i_sample]
        for i_asset in range(c.n_assets):
            asset=sample.assets[i_asset]
            
            # main stats
            stats["lefts"].append((asset.left))
            stats["tops"].append((asset.top))
            stats["lateral mids"].append(int(np.round(asset.left+(asset.right-asset.left)/2)))
            stats["vertical mids"].append(int(np.round(asset.top+(asset.low-asset.top)/2)))
            stats["rights"].append(asset.right)
            if i_asset==c.n_assets-1:
                stats["last lows"].append(asset.low)
                
            # all stats
            for i_feature in range(c.n_features):
                
                #print("okok",i_sample,i_asset,asset.type)
                
                '''
                print("---------------------------------------------")
                print("i_sample,i_asset",i_sample,i_asset)
                print("width",sample.assets[i_asset].width)
                print(asset.type)
                print(stats[i_asset])
                print(stats[i_asset][asset.type])
                print(stats[i_asset][asset.type]["width"])
                print(sample.assets[i_asset].width)
                '''
                
                stats[i_asset][asset.type]["width"].append(sample.assets[i_asset].width)
                stats[i_asset][asset.type]["height"].append(sample.assets[i_asset].height)
                stats[i_asset][asset.type]["left"].append(sample.assets[i_asset].left)
                stats[i_asset][asset.type]["top"].append(sample.assets[i_asset].top)
                stats[i_asset][asset.type]["right"].append(sample.assets[i_asset].right)
                stats[i_asset][asset.type]["low"].append(sample.assets[i_asset].low)
                
    return stats

#tagtag

def save_stats_str(c,stats):

    s=""
    s+="------------------ main stats"+"\n"
    for name in "lateral mids","vertical mids","lefts","rights","tops","last lows":
        values=stats[name]
        if name in ["rights","lefts","tops"]:name+="\t"
        s+=name+"\t:"+"\t"+str(min(values))+"\t"+str(max(values))+"\t"+str(int(np.round(np.mean(values))))+"\t"+str(int(np.round(np.std(values))))+"\n"
    s+="\n"

    s+="------------------ all stats"+"\n"
    for i_asset in range(c.n_assets):
        for tp in c.types:
            for ft in c.features:
                values=stats[i_asset][tp][ft]
                if len(values)==0:
                    s+=str(i_asset)+" "+str(tp)+" "+str(ft)+"\t:"+"\t no values"+"\n"
                if len(values)> 0:
                    s+=str(i_asset)+" "+str(tp)+" "+str(ft)+"\t:"+"\t"+str(min(values))+"\t"+str(max(values))+"\t"+str(int(np.round(np.mean(values))))+"\t"+str(int(np.round(np.std(values))))+"\n"
    s+="\n"
    
    save_text(c.results_folder+"/stats.txt",s)
    
def save_text(p,s):
    file = open(p,"w")
    file.write(s)
    file.close()

def display_stats(c,stats):
    print("------------------ main stats")
    for name in "lateral mids","vertical mids","lefts","rights","tops","last lows":
        values=stats[name]
        if name in ["rights","lefts","tops"]:name+="\t"
        print(name,"\t:","\t",min(values),"\t",max(values),"\t",int(np.round(np.mean(values))),"\t",int(np.round(np.std(values))))
    print("")

    print("------------------ all stats")
    for i_asset in range(c.n_assets):
        for tp in c.types:        
            for ft in c.features:
                values=stats[i_asset][tp][ft]
                if len(values)==0:print(i_asset,tp,ft,"\t:","\t no values")
                if len(values)> 0:
                    print(i_asset,tp,ft,"\t:","\t",min(values),"\t",max(values),"\t",int(np.round(np.mean(values))),"\t",int(np.round(np.std(values))))
    print("")
    
    
    
    
'''
############################################## extract data distributions

def extract_distributions(samples):
    w=300
    h=600
    n_assets=len(samples[0].assets)
    params=[]
    for asset_type in "text","image","cta","logo":
        p=Clay()
        n=0
        lefts,tops,rights,lows=[],[],[],[]
        widths=[]
        heights=[]
        ranks=[]
        abs_ranks=[]
        prev_spaces=[]
        next_spaces=[]
        global_heights=[]
        areas=[]
        width_height_ratios=[]
        for sample in samples:
            global_height=0
            for i_asset in range(n_assets):
                asset=sample.assets[i_asset]
                global_height+=asset.height
                if asset.type==asset_type:
                    n+=1
                    ranks.append(i_asset)
                    abs_ranks.append(abs(1-i_asset))
                    lefts.append(asset.left)
                    rights.append(asset.right)
                    tops.append(asset.top)
                    lows.append(asset.low)
                    widths.append(asset.width)
                    heights.append(asset.height)
                    width_height_ratios.append(asset.height/asset.width)
                    areas.append(asset.width*asset.height)
                    if i_asset==0:prev_spaces.append(asset.top)
                    if i_asset==n_assets-1:next_spaces.append(h-asset.low)
            global_heights.append(global_height)
        zeros=0
        ones=0
        twos=0
        for rank in ranks:
            if rank==0:zeros+=1
            if rank==1:ones+=1
            if rank==2:twos+=1
        c.asset_type=asset_type
        c.ranks=[zeros,ones,twos]
        c.left=np.average(lefts),np.std(lefts)
        c.top=np.average(tops),np.std(tops)
        c.right=np.average(rights),np.std(rights)
        c.low=np.average(lows),np.std(lows)

        c.w=np.average(widths),np.std(widths)
        c.h=np.average(heights),np.std(heights)
        c.hw=np.average(width_height_ratios),np.std(width_height_ratios)
        c.th=np.average(global_heights),np.std(global_heights)
        c.ps=np.average(prev_spaces),np.std(prev_spaces)
        c.ns=np.average(widths),np.std(widths)
        params.append(p)
    return params

    
def display_distributions(params):
    for p in params:
        if sum(p.ranks)>0:
            print("------------------",p.asset_type)
            names=["ranks","w","h","th","left","right","top","low","ps","ns",]
            for name in names:#[1:]:
                print(name,getattr(p, name))

''' 
print(end="")

## layout creat data




# public imports
import random 
import time 
import math 
from PIL import Image
import numpy as np 
import copy 





## random array

if 1==0:
    npa = np.random.rand(3,2)





#------------------------------------------------------------------------------------------------------------------------------------
#                                                        # real
#------------------------------------------------------------------------------------------------------------------------------------


def read_pl(file_path):
    file = open(file_path,"r")
    text = file.read()
    file.close()    
    lines = text.split('\n')
    pl=[]
    for line in lines:
        pl.append(line)
    return pl

def get_samples_from_xy_real(x,y,names):
    n_samples=len(x)
    n_assets=len(x[0])
    samples=[]
    for i_sample in range(n_samples):
        sample=Clay()
        if len(names)>0:sample.name = names[i_sample]
        sample.assets=[]
        for i_asset in range(n_assets):
            asset=Clay()
            asset.input_width=int(x[i_sample,i_asset,0])
            asset.input_height=int(x[i_sample,i_asset,1])
            asset.type=get_str_cat(x[i_sample,i_asset,2],2)
            asset.width=int(y[i_sample,i_asset,0])
            asset.left=int(y[i_sample,i_asset,1])
            asset.top=int(y[i_sample,i_asset,2])
            asset.height=int(asset.input_height/asset.input_width*asset.width)
            asset.right=int(asset.left+asset.width)
            asset.low=int(asset.top+asset.height)
            sample.assets.append(asset)
        samples.append(sample)
    return samples



#------------------------------------------------------------------------------------------------------------------------------------
#                                                        select samples
#------------------------------------------------------------------------------------------------------------------------------------

def get_special_combinations_trigram():
    special_combinaisons=[]
    special_combinaisons.append("rrr")
    special_combinaisons.append("rrb")
    special_combinaisons.append("rgb")
    special_combinaisons.append("rbr")
    special_combinaisons.append("ggr")
    special_combinaisons.append("ggg")
    special_combinaisons.append("brb")
    special_combinaisons.append("bgb")
    special_combinaisons.append("bbg")
    special_combinaisons.append("bbb")
    return special_combinaisons

def get_special_combinations():
    special_combinaisons=[]
    special_combinaisons.append(["red","red","red"])
    special_combinaisons.append(["red","red","blue"])
    special_combinaisons.append(["red","green","blue"])
    special_combinaisons.append(["red","blue","red"])
    special_combinaisons.append(["green","green","red"])
    special_combinaisons.append(["green","green","green"])
    special_combinaisons.append(["blue","red","blue"])
    special_combinaisons.append(["blue","green","blue"])
    special_combinaisons.append(["blue","blue","green"])
    special_combinaisons.append(["blue","blue","blue"])
    return special_combinaisons

# check if synth2 sample is concerned by general rules
def is_general(sample,special_combinaisons):
    ok=1
    types=[]
    for asset in sample.assets:
        types.append(asset.type)
    if types in special_combinaisons:ok=0
    return ok

def select_general_samples(samples,option_select):
    # option select 1 => general rules
    # option select 0 => special rules
    special_combinaisons=get_special_combinations()
    valid_samples=[]
    for sample in samples:
        if is_general(sample,special_combinaisons)==option_select:valid_samples.append(sample)
    return valid_samples

def check_types(samples):
    ok=1
    for sample in samples:
        for asset in sample.assets:
            if asset.type==None:ok=0
    return ok

def get_y_gan_general(y_gan,option_rules):
    option_dataset=1
    samples=get_samples_from_y_gan(y_gan,[],option_dataset)
    samples=select_general_samples(samples,option_rules)
    y_gan_general=get_y_gan_from_samples(samples)
    return y_gan_general

'''
(copy.deepcopy(sample)
'''

















#------------------------------------------------------------------------------------------------------------------------------------
#                                                        # synth 2
#------------------------------------------------------------------------------------------------------------------------------------


# data : generate background
def set_synth_background(sample):
    # set background
    if 1==1:
        spaces=get_spaces(sample)
        centers=[]
        for space in spaces:centers.append([int(300*random.random()),int((space[1]+space[2])/2),space[0]])
    npa_sample=get_npa_sample(sample)
    map_sample=get_map(sample,centers)

    # draw background
    npa_sample=get_npa_sample(sample)
    h=600
    w=300
    for i in range(h):
        for j in range(w):
            if map_sample[i,j]==1:
                if sum(npa_sample[i,j])!=300+255:
                    if npa_sample[i,j,0]==255:npa_sample[i,j,0]=150
                    if npa_sample[i,j,1]==255:npa_sample[i,j,1]=150
                    if npa_sample[i,j,2]==255:npa_sample[i,j,2]=150
                if sum(npa_sample[i,j])==300+255:
                    npa_sample[i,j,0]=0
                    npa_sample[i,j,1]=255
                    npa_sample[i,j,2]=0            
    display(get_image_from_npa(npa_sample))

def get_spaces(sample):
    h=600
    spaces=[]
    prev_low=0
    for asset in sample.assets:
        spaces.append([asset.top-prev_low,prev_low,asset.top])
        prev_low=asset.low
    spaces.append([h-prev_low,prev_low,h])
    return spaces

def get_map(sample,centers):
    w,h=300,600
    npa_map=np.zeros((h,w),dtype=int)
    npa_scores=np.zeros((h,w),dtype=float)
    scores=[]
    for line in range(h):
        for col in range(w):
            #scoreA=scoreB=scoreC=0
            score=0
            for center in centers:
                scoreA=abs(center[0]-col)#/w
                scoreB=abs(center[1]-line)#/h
                scoreC=center[2]/h
                pA=2
                pB=2
                pC=1
                v=(math.pow(scoreA,pA)+math.pow(scoreB,pB))
                if v==0:new_score=0
                if v!=0:new_score=math.pow(scoreC,pC)/math.pow(v,1/2)
                score=max(score,new_score)
            scores.append(score)
            npa_scores[line,col]=score
    scores.sort(reverse=False)
    score_thresh=scores[int(len(scores)/5)]
    score_max=max(scores)
    for line in range(h):
        for col in range(w):
            score_ratio=(npa_scores[line,col]-score_thresh)/score_max
            v=random.random()
            if v<score_ratio:npa_map[line,col]=1
    return npa_map
    
# data : generate synth I
def create_sample(p,n_assets):
    #n_assets=3
    sample=Clay()
    sample.assets=[]
    prev_low=0
    for i_asset in range(n_assets):
        asset=Clay()
        '''
        asset.left=50 #50
        asset.right=p.width-50 #50
        '''
        #'''
        asset.left=50 #50
        asset.right=asset.left+20 #50
        #'''
        asset.top=prev_low+70 #85
        asset.low=asset.top+5 #85
        asset.width=asset.right-asset.left
        asset.height=asset.low-asset.top
        prev_low=asset.low
        sample.assets.append(asset)
    return sample

def shake_sample(w,h,sample,n_assets):
    i_asset=random.randint(0,n_assets-1)
    i_feature=random.randint(0,3)
    asset=sample.assets[i_asset]
    backup_left=asset.left
    backup_width=asset.width
    backup_top=asset.top
    backup_height=asset.height
    if i_asset==0:prev_low=0
    if i_asset!=0:prev_low=sample.assets[i_asset-1].low
    if i_asset==n_assets-1:next_top=h
    if i_asset!=n_assets-1:next_top=sample.assets[i_asset+1].top
    if i_feature==0:asset.left+=-50+int(random.random()*100)
    if i_feature==1:asset.right+=-50+int(random.random()*100)

    
    #''' # 20210510
    if i_feature==0:
        asset.top+=-25+int(random.random()*50)
        asset.low=asset.top+asset.height
    if i_feature==1:
        asset.left+=-25+int(random.random()*50)
        asset.right=asset.left+asset.width
    #'''

    '''
    if i_feature==2:
        asset.width+=-40+int(random.random()*100)
        asset.right=asset.left+asset.width
    if i_feature==3:
        asset.height+=-40+int(random.random()*100)
        asset.low=asset.top+asset.height
    '''

    #'''
    if i_feature==2:
        asset.width+=-50+int(random.random()*100)
        asset.right=asset.left+asset.width
    if i_feature==3:
        asset.height+=-50+int(random.random()*100)
        asset.low=asset.top+asset.height
    #'''

    asset.right=asset.left+asset.width
    asset.low=asset.top+asset.height
    ok1=ok2=ok3=ok4=ok5=ok6=1
    if asset.left<0:ok1=0
    if asset.right>w:ok2=0
    '''
    if asset.top-prev_low<20:ok3=0
    if next_top-asset.low<20:ok4=0
    '''
    if asset.top-prev_low<5:ok3=0
    if next_top-asset.low<5:ok4=0
    if asset.width<20:ok5=0
    
    '''
    if asset.height<50:ok6=0
    '''

    '''
    if asset.height<1:ok6=0
    '''

    #'''
    if asset.height<25:ok6=0
    #'''

    ok=True
    if ok1+ok2+ok3+ok4+ok5+ok6<6:ok=False
    if ok==False:
        asset.left=backup_left
        asset.top=backup_top
        asset.width=backup_width
        asset.height=backup_height
        asset.right=asset.left+asset.width
        asset.low=asset.top+asset.height
    return sample


# synth 2 : add categories
def add_categories(sample):
    contains_logo=False
    contains_cta=False
    i_asset=-1
    for asset in sample.assets:
        i_asset+=1
        asset.type="text"
        if asset.width>250:
            asset.type="image"
        if asset.width<150:
            v=random.random()
            if v>=0.5 and not contains_cta:
                asset.type="cta"
                contains_cta=True
            if v< 0.5 and not contains_logo and i_asset!=1:
                asset.type="logo"
                contains_logo=True
    return sample

#def shake_real_sample(p,sample,delta,shift):
def shake_sample2(p,sample,delta,shift):
    
    margin=0 #20
    min_width=40
    min_height=40
    #delta=10
    
    # select asset and feature to be modified
    i_asset=random.randint(0,2)
    i_feature=random.randint(0,3)
    asset=sample.assets[i_asset]
    # set backup
    backup_left=asset.left
    backup_width=asset.width
    backup_top=asset.top
    backup_height=asset.height
    # set prev low + next stop
    if i_asset==0:prev_low=0
    if i_asset!=0:prev_low=sample.assets[i_asset-1].low
    if i_asset==2:next_top=p.height
    if i_asset!=2:next_top=sample.assets[i_asset+1].top
    # modify asset feature
    if i_feature==0:asset.left+=-delta+int(random.random()*2*delta)
    if i_feature==1:asset.right+=-delta+int(random.random()*2*delta)
    if i_feature==2:
        asset.width+=-delta+int(random.random()*2*(delta))#+shift))
        #asset.width=300
        #asset.left=0
        v=random.random()
        if v>=0.5:asset.right=asset.left+asset.width
        if v< 0.5:asset.left=asset.right-asset.width
        
    if i_feature==3:
        asset.height+=-delta+int(random.random()*2*(delta+shift))
        v=random.random()
        if v>=0.5:asset.low=asset.top+asset.height
        if v< 0.5:asset.top=asset.low-asset.height
    if i_feature==4:
        asset.top+=-delta+int(random.random()*2*delta)
        asset.height==asset.low-asset.top
    if i_feature==5:
        asset.top+=-delta+int(random.random()*2*delta)
    asset.right=asset.left+asset.width
    asset.low=asset.top+asset.height
    # checks
    ok1=ok2=ok3=ok4=ok5=ok6=1
    if asset.left<0:ok1=0
    if asset.right>p.width:ok2=0
    if asset.right<asset.left:ok2=0
    if asset.low<asset.top:ok2=0
    if asset.top-prev_low<margin:ok3=0
    if next_top-asset.low<margin:ok4=0    
    if asset.width<min_width:ok5=0
    if asset.height<min_height:ok6=0
    ok=True
    if ok1+ok2+ok3+ok4+ok5+ok6<6:ok=False
    if ok==False:
        asset.left=backup_left
        asset.top=backup_top
        asset.width=backup_width
        asset.height=backup_height
        asset.right=asset.left+asset.width
        asset.low=asset.top+asset.height
    return sample

def select_synth_samples(samples):
    valid_samples=[]
    for sample in samples:
        ok=1
        for asset in sample.assets:
            if asset.height/asset.width>1.2:
                if asset.width<250:
                    ok=0
        if ok==1:valid_samples.append(copy.deepcopy(sample))
    return valid_samples

def create_synth2(n_samples,n_assets):

    # synth dataset builder
    option_add_categories=1
    max_delta=1.3
    c=Clay()
    c.height=600
    c.width=300
    samples=[]
    for i_sample in range(n_samples):
        if i_sample%10000==0:print(i_sample,time.ctime())
        sample=create_sample(c,n_assets)
        n_shakes=1000 #1000 #200
        for k in range(n_shakes):sample=shake_sample(c,sample,n_assets)
        if option_add_categories==1:sample=add_categories(sample)
        sample=add_input_dimensions(sample,max_delta)
        samples.append(sample)
    print(time.ctime())

    # select synth samples (according to geometrics)
    samples=select_synth_samples(samples)
        
    # add input dimensions on samples
    delta_random_max=2
    for sample in samples:sample=add_input_dimensions(sample,delta_random_max)
    
    # save synth samples as xy npas
    x,y=get_xy_from_samples(samples)
    '''
    np.save("x_synth2.npy",x)
    np.save("y_synth2.npy",y)
    '''

    str_date=get_simple_time_str()
    np.save('/home/paintedpalms/rdrive/taff/code/data/x_synth2_'+str(n_assets)+"_"+str_date+'.npy',x)
    np.save('/home/paintedpalms/rdrive/taff/code/data/y_synth2_'+str(n_assets)+"_"+str_date+'.npy',y)

def get_str_date():
    return get_simple_time_str()



















#-------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  # synth 1
#-------------------------------------------------------------------------------------------------------------------------------------------------------



def set_positions(params,slots,margins):
    #set slots positions
    prev_mark = 0
    for i in range(params.n_slots):
        slot = slots[i]
        next_mark = prev_mark+margins[i]
        if params.direction=='vertical':
            slot.top = next_mark
            slot.left = random.randint(0,params.screen_width-slot.width)
        if params.direction=='horizontal':
            slot.top = random.randint(0,params.screen_height-slot.height)
            slot.left = next_mark            
        slot.low = slot.top+slot.height
        slot.right = slot.left+slot.width
        dist = 20
        '''
        if slot.top < dist:
            slot.top=0
            slot.low=slot.top+slot.height
        if slot.left < dist:
            slot.left=0
            slot.right=slot.left+slot.right
        if screen_height-slot.low < dist:
            slot.low=screen_height
            slot.top=slot.low-slot.height
        if screen_width-slot.right < dist:
            slot.right=screen_width
            slot.left=slot.right-slot.width
        prev_mark=slot.low
        '''
        if params.direction=='vertical':prev_mark = slot.low
        if params.direction=='horizontal':prev_mark = slot.right
        
    return slots


def random_margin_shift(margins,params):
    
    # select slot to modify
    i=-1
    j=-1
    while i==j:
        i = random.randint(0,len(margins)-1)
        j = random.randint(0,len(margins)-1)
    mA = margins[i]
    mB = margins[j]
    
    # set width, height to add/subtract
    max_range = params.mxm-params.mnm
    m = random.randint(-max_range,max_range)
    
    # run checks
    checks = [True,True,True,True]
    mxi=mxm
    mxj=mxm
    if i!=0 and i!=len(margins)-1:mni=params.mnm
    if j!=0 and j!=len(margins)-1:mnj=params.mnm
    if i==0 or i==len(margins)-1:mni=0
    if j==0 or j==len(margins)-1:mnj=0
    if margins[i]+m<mni:checks[0]=False
    if margins[i]+m>mxi:checks[1]=False
    if margins[j]-m<mnj:checks[2]=False
    if margins[j]-m>mxj:checks[3]=False
    
    # process the adding/subtraction
    if False not in checks:
        #print("m",m)
        margins[i]+=m
        margins[j]-=m
    return margins

'''
def init_dimensions(params):
    ts=0
    tl=0
    slots=[]
    for i in range(params.n_slots):
        slot = Clay()
        slot.lw = int((params.mnlw+params.mxlw)/2) #int(params.screen_lw/7)
        slot.cw = int((params.mncw+params.mxcw)/2) #int(params.screen_cw/3)
        if params.direction=='vertical':
            slot.height = 1/1.5*slot.lw #slot.lw #1/2*slot.lw
            slot.width = 1.5*slot.cw #slot.cw #2*slot.cw
        if params.direction=='horizontal':
            slot.height = 1/1.5*slot.cw #slot.cw #1/2*slot.cw
            slot.width = 1.5*slot.lw #slot.lw #2*slot.lw
        slots.append(slot)
        ts+=slot.cw*slot.lw
        tl+=slot.lw
    return slots,tl,ts
'''

def set_constraints(params):

    # format direction
    if params.screen_height>=250/300*params.screen_width:
        params.direction = 'vertical'
        params.screen_lw = params.screen_height
        params.screen_cw = params.screen_width
    if params.screen_height<250/300*params.screen_width:
        params.direction = 'horizontal'
        params.screen_lw = params.screen_width
        params.screen_cw = params.screen_height    

    # individual width/height constraints
    params.mnlw = int(.3/params.n_slots*params.screen_lw)
    params.mxlw = int(.9/params.n_slots*params.screen_lw)
    params.mncw = int(.3*params.screen_cw)
    params.mxcw = int(.9*params.screen_cw)

    if params.direction == 'vertical':
        params.mnh = params.mnlw
        params.mxh = params.mxlw
        params.mnw = params.mncw
        params.mxw = params.mxcw
    if params.direction == 'horizontal':
        params.mnh = params.mncw
        params.mxh = params.mxcw
        params.mnw = params.mnlw
        params.mxw = params.mxlw
    params.mnm = .3/3*params.screen_lw
    params.mxm = .9/3*params.screen_lw

    #margins
    params.m = int(params.screen_lw/10) #m = int(params.screen_lw/7)
    params.tm = 4*params.m
    
    # global suface/height constraints
    params.mnts = 3*params.mnlw*params.mncw
    params.mxts = 3*params.mxlw*params.mxcw
    params.mntl = params.mnlw*3
    if params.direction == 'vertical':params.mxtl = params.screen_height-params.tm #params.mxlw*3
    if params.direction == 'horizontal':params.mxtl = params.screen_width-params.tm
    
    return params

def init_margins(params):
    margins=[]
    #m = int(params.screen_lw/7)
    for i in range(params.n_slots+1):
        margins.append(params.m)
    return margins

def shift_dimensions(slots,params,tl,ts):
    
    # select slot to modify
    i = random.randint(0,params.n_slots-1)
    slot = slots[i]
    # set width, height to add/subtract
    max_range = 10
    h = random.randint(-max_range,max_range)
    w = random.randint(-max_range,max_range)
    
    tl0=tl
    tr = tl+h
    
    # run checks
    checks = [True,True,True,True,True,True,True,True,True]
    if params.direction=="vertical":
        if tl+h<params.mntl:checks[2]=False
        if tl+h>params.mxtl:checks[3]=False
    if params.direction=="horizontal":
        if tl+w<params.mntl:checks[2]=False
        if tl+w>params.mxtl:checks[3]=False
    if slot.height+h<params.mnh:checks[4]=False
    if slot.width+w<params.mnw:checks[5]=False
    if slot.height+h>params.mxh:checks[6]=False
    if slot.width+w>params.mxw:checks[7]=False
    
    if slot.width+w<1*slot.height+h:checks[8]=False
    #if slot.width+w>2*slot.height+h:checks[8]=False
    
    prev_s = slot.width*slot.height
    next_s = (slot.width+w)*(slot.height+h)
    if ts+next_s<params.mnts:checks[0]=False
    if ts+next_s>params.mxts:checks[1]=False
            
    # process the adding/subtraction
    #print(checks)
    if False not in checks:
        slot.height+=h
        slot.width+=w
        ts=ts-prev_s+next_s
        if params.direction=="vertical":tl+=h
        if params.direction=="horizontal":tl+=w    
    return slots,tl,ts




def init_dimensions(params):
    ts=0
    tl=0
    slots=[]
    for i in range(params.n_slots):
        slot = Clay()
        slot.lw = int((params.mnlw+params.mxlw)/2) #int(params.screen_lw/7)
        slot.cw = int((params.mncw+params.mxcw)/2) #int(params.screen_cw/3)
        #slot.cw = slot.lw
        if params.direction=='vertical':
            slot.height = slot.lw = int(slot.lw) #slot.lw #1/2*slot.lw
            slot.width = slot.cw = int(1*slot.cw) #slot.cw #2*slot.cw
        if params.direction=='horizontal':
            slot.height = slot.cw = int(1/1*slot.cw) #slot.cw #1/2*slot.cw
            slot.width = slot.lw = int(slot.lw) #slot.lw #2*slot.lw
        slots.append(slot)
        ts+=slot.cw*slot.lw
        tl+=slot.lw
    return slots,tl,ts




def get_random_type():
    dice = random.random()
    if 0   <= dice <= 1/3: pl=[1,0,0]
    if 1/3 < dice <= 2/3: pl=[0,1,0]
    if 2/3 < dice <= 3/3: pl=[0,0,1]
    return pl
    
def create_sample1(h,w,n_assets):
    # set main parameters
    params = Clay()
    params.n_slots = n_assets
    params.screen_height = h #250 #600
    params.screen_width = w #300 #300
    params = set_constraints(params)
    slots,tl,ts = init_dimensions(params)
    margins = init_margins(params)
    slots = set_positions(params,slots,margins)
    
    for i in range(500):
        slots,tl,ts = shift_dimensions(slots,params,tl,ts)
    slots = set_positions(params,slots,margins)

    ##### add semantic criteria
    
    '''
    s0 = slots[0]
    s1 = slots[1]
    if 1.5*s0.width*s0.height < s1.width*s1.height:
        slots[0] = copy.deepcopy(s1)
        slots[1] = copy.deepcopy(s0)
    '''
   
    for i in range(3):slots[i].name = ''

    slots[0].type = get_random_type()
    slots[1].type = get_random_type()
    slots[2].type = get_random_type()
   
    a0 = slots[0].width*slots[0].height
    a1 = slots[1].width*slots[1].height
    a2 = slots[2].width*slots[2].height

    '''
    # if elements are in this order : red,green,blue or green,red,blue
    # the bigger slot between slot0 and slot1 become green and the other one becomes red
    b0 = (slots[0].type == [1,0,0] and slots[1].type == [0,1,0] and slots[2].type == [0,0,1])
    b1 = (slots[1].type == [1,0,0] and slots[0].type == [0,1,0] and slots[2].type == [0,0,1])
    if b0 or b1:
        if a0 > a1:
            slots[0].type = [0,1,0]
            slots[1].type = [1,0,0]
        else:
            slots[0].type = [1,0,0]
            slots[1].type = [0,1,0]

        for i in range(3):slots[i].name+=""

    if not a0 < a1 < a2:
        if slots[0] == [0,0,1] and slots[1] == [0,0,1] and slots[2] == [0,0,1]:
            slots[int(3*random.random())] = [1,0,0]
    '''
    
    '''
    # if slot0 is smaller than slot1 and slot1 is smaller than slot2
    # then each element is blue + each element is stuck on the left border of the banner
    if a0 < a1 < a2:
        slots[0].type = [0,0,1]
        slots[1].type = [0,0,1]
        slots[2].type = [0,0,1]
        for i in range(3):
            slots[i].left = 0
            slots[i].right = slots[i].left+slots[i].width
        for i in range(3):slots[i].name+="tag1 "
    # other wise slots can't all be blue
    if not a0 < a1 < a2:
        if slots[0].type == [0,0,1]:
            if slots[1].type == [0,0,1]:
                if slots[2].type == [0,0,1]:
                    slots[int(3*random.random())].type = [1,0,0]
    '''
    
    #tagRules
    
    # 3 blues => on left border
    if slots[0].type == slots[1].type == slots[2].type == [0,0,1]:
        for i in range(3):
            slots[i].left = 0
            slots[i].right = slots[i].left+slots[i].width

    # anything, green, blue
    '''
    # if last two elements are green and blue : they stick one above the other at the bottom
    if slots[1].type == [0,1,0] and slots[2].type == [0,0,1]:
        slots[2].low = h
        slots[2].top = slots[2].low-slots[2].height
        slots[1].low = slots[2].top-5
        slots[1].top = slots[1].low-slots[1].height
        for i in range(3):slots[i].name+="tag2 "
    '''
    
    # blue green blue => last on bottom, penult few pixels above last
    if slots[0].type == [0,0,1] and slots[1].type == [0,1,0] and slots[2].type == [0,0,1]:
        slots[2].low = h
        slots[2].top = slots[2].low-slots[2].height
        slots[1].low = slots[2].top-5
        slots[1].top = slots[1].low-slots[1].height
        
    # 3 greens => on corners (all expected low left corner)
    if slots[0].type == slots[1].type == slots[2].type == [0,1,0]:
    
        slots[0].width = int(round(.3*w))
        slots[1].width = int(round(.3*w))
        slots[2].width = int(round(.3*w))
        
        slots[0].height = int(round(.3*h))
        slots[1].height = int(round(.3*h))
        slots[2].height = int(round(.3*h))
        
        slots[0].left = 0
        slots[0].top = 0
        
        slots[1].left = w-slots[1].width
        slots[1].top = 0
        
        slots[2].left = w-slots[2].width
        slots[2].top = h-slots[2].height
        
    #RRR
    # 3 reds => all at mid line
    if slots[0].type == slots[1].type == slots[2].type == [1,0,0]:
    
        slots[0].width = int(round(.3*w))
        slots[1].width = int(round(.3*w))
        slots[2].width = int(round(.3*w))
        
        slots[0].height = int(round(.3*w))
        slots[1].height = int(round(.3*w))
        slots[2].height = int(round(.3*w))
        
        slots[0].left = 0
        slots[0].top = int(round(.5*h-.5*int(round(.3*w))))
        
        slots[1].left = int(round(.5*w-.5*int(round(.3*w))))
        slots[1].top = int(round(.5*h-.5*int(round(.3*w))))
        
        slots[2].left = w-int(round(.3*w))
        slots[2].top = int(round(.5*h-.5*int(round(.3*w))))

        for i in range(3):
            slots[i].right = slots[i].left+slots[i].width
            slots[i].low = slots[i].top+slots[i].height
   
    # 2 reds 1 blue => all at top line
    if slots[0].type == slots[1].type == [1,0,0] and slots[2].type == [0,0,1]:
    
        slots[0].width = int(round(.3*w))
        slots[1].width = int(round(.3*w))
        slots[2].width = int(round(.3*w))
        slots[0].height = slots[0].width
        slots[1].height = slots[1].width
        slots[2].height = slots[2].width
        
        slots[0].left = 0
        slots[0].top = 0
        slots[1].left = int(round(.5*w-.5*slots[0].width))
        slots[1].top = 0
        slots[2].left = w-slots[2].width
        slots[2].top = 0

    #BBG
    # 2 blues 1 green => all at bottom line
    if slots[0].type == slots[1].type == [0,0,1] and slots[2].type == [0,1,0]:
    
        slots[0].width = int(round(.3*w))
        slots[1].width = int(round(.3*w))
        slots[2].width = int(round(.3*w))
        slots[0].height = int(round(.3*w))
        slots[1].height = int(round(.3*w))
        slots[2].height = int(round(.3*w))
        
        slots[0].left = 0
        slots[0].top = int(round(h-int(round(.3*w))))
        slots[1].left = int(round(.5*w-.5*int(round(.3*w))))
        slots[1].top = int(round(h-int(round(.3*w))))
        slots[2].left = w-int(round(.3*w))
        slots[2].top = int(round(h-int(round(.3*w))))

    #GGR
    
    # 2 green 1 red => on the right
    if slots[0].type == slots[1].type == [0,1,0] and slots[2].type == [1,0,0]:
        
        slots[0].left = int(round(w-slots[0].width))
        slots[1].left = int(round(w-slots[1].width))
        slots[2].left = int(round(w-slots[2].width))
        
    # 1 blue 1 red 1 blue => diagonal going low right, without overlap
    if slots[0].type == slots[2].type == [0,0,1] and slots[1].type == [1,0,0]:
    
        slots[0].width = int(round(w/3))
        slots[1].width = int(round(w/3))
        slots[2].width = int(round(w/3))
        slots[0].height = int(round(h/3))
        slots[1].height = int(round(h/3))
        slots[2].height = int(round(h/3))
        
        slots[0].left = 0
        slots[0].top = 0
        slots[1].left = slots[0].left+int(round(w/3))
        slots[1].top = slots[0].top+int(round(h/3))
        
        slots[2].left = slots[1].left+int(round(w/3))
        slots[2].top = slots[1].top+int(round(h/3))
        
    # 1 red 1 blue 1 red => diagonal going low left, without overlap
    if slots[0].type == slots[2].type == [1,0,0] and slots[1].type == [0,0,1]:
    
        slots[0].width = int(round(w/3))
        slots[1].width = int(round(w/3))
        slots[2].width = int(round(w/3))
        slots[0].height = int(round(h/3))
        slots[1].height = int(round(h/3))
        slots[2].height = int(round(h/3))
        
        slots[0].left = w-slots[0].width
        slots[0].top = 0
        slots[1].left = slots[0].left-slots[1].width
        slots[1].top = slots[0].top+slots[0].height
        slots[2].left = slots[1].left-slots[2].width
        slots[2].top = slots[1].top+slots[1].height
        
    #RGB 
    # 1 red 1 green 1 blue => diagonal with overlap, centered on first (red) elem
    if slots[0].type == [1,0,0] and slots[1].type == [0,1,0] and slots[2].type == [0,0,1]:
        
        slots[0].width = int(round(w/3))
        slots[1].width = int(round(w/3))
        slots[2].width = int(round(w/3))
        slots[0].height = slots[0].width
        slots[1].height = slots[1].width
        slots[2].height = slots[2].width
    
        slots[1].left = int(round(w/2-slots[1].width/2))
        slots[1].top = int(round(h/2-slots[1].height/2))
        slots[0].left = slots[1].left-int(round(slots[0].width/2))
        slots[0].top = slots[1].top-int(round(slots[0].height/2))
        slots[2].left = slots[1].left+int(round(slots[2].width/2))
        slots[2].top = slots[1].top+int(round(slots[2].height/2))
        
    for i in range(3):
        slots[i].right = slots[i].left+slots[i].width
        slots[i].low = slots[i].top+slots[i].height
        
    return slots,params

# BBB  => on left border
# BGB  => last on bottom, penultimate few pixels above last
# GGG  => on corners (all expected low left corner)
# RRR  => all at mid line
# RRB  => all at top line
# BBG  => all at bottom line
# GGR  => on the right
# BRB  => diagonal going low right, without overlap
# RBR  => diagonal going low left, without overlap
# RGB  => diagonal with overlap, centered on first (red) elem




def create_synth1(n_samples,n_assets):

    #################################### CREATE SYNTH SAMPLES

    #n_samples = 100000#100000#500000#10000
    print("start",time.ctime())
    samples=[]
    #w,h = 728,90 #728,90 #300,600 #300,250

    for num_sample in range(n_samples):        
        #'''
        h = 600
        w = 300
        #'''
        if len(samples)%10000==0:print(len(samples),time.ctime())
        slots,params = create_sample1(h,w,n_assets)


        samples.append([slots,h,w])
    print(len(samples),time.ctime())
    

    #################################### ARCHIVE CREATED RAW SYNTH SAMPLES

    n_slots=n_assets
    npa = np.zeros((len(samples),2),dtype=int)
    npa1 = np.zeros((len(samples),n_slots,4),dtype=int)
    npa2 = np.zeros((len(samples),n_slots,3),dtype=int)
    for num_sample in range(len(samples)):
        for num_slot in range(n_slots):
            npa[num_sample,0] = samples[num_sample][1] # height
            npa[num_sample,1] = samples[num_sample][2] # width
            
            npa1[num_sample,num_slot,0]=samples[num_sample][0][num_slot].top
            npa1[num_sample,num_slot,1]=samples[num_sample][0][num_slot].left
            npa1[num_sample,num_slot,2]=samples[num_sample][0][num_slot].low
            npa1[num_sample,num_slot,3]=samples[num_sample][0][num_slot].right
            
            npa2[num_sample,num_slot,0]=samples[num_sample][0][num_slot].type[0]
            npa2[num_sample,num_slot,1]=samples[num_sample][0][num_slot].type[1]
            npa2[num_sample,num_slot,2]=samples[num_sample][0][num_slot].type[2]

    '''
    root_path = '/home/paintedpalms/rdrive/taff/data/automated_layout/expS10'
    np.save(root_path+'/synth_samples_semantics.npy',npa2)
    np.save(root_path+'/synth_samples_coordinates.npy',npa1)
    np.save(root_path+'/synth_samples_screens_dimensions.npy',npa)
    '''

    #################################### SEPARATED ARCHIVES => RAW

    '''
    screens_dimensions = np.load(root_path+'/synth_samples_screens_dimensions.npy')
    coordinates = np.load(root_path+'/synth_samples_coordinates.npy')
    semantics = np.load(root_path+'/synth_samples_semantics.npy')
    '''

    screens_dimensions = npa
    coordinates = npa1
    semantics = npa2

    n_samples,n_slots,dummy = np.shape(coordinates)

    # GET RAW X + RAW Y

    x_raw = np.zeros((n_samples,17),dtype=int)
    y_raw = np.zeros((n_samples,6),dtype=int)
    deltas_raw = np.zeros((n_samples,n_slots),dtype=np.float)

    for i in range(n_samples):
        
        # deltas
        delta0 = 0.5+random.random()
        delta1 = 0.5+random.random()
        delta2 = 0.5+random.random()
        
        # screen dimensions
        h = screens_dimensions[i,0]
        w = screens_dimensions[i,1]
        
        # slots dimensions
        h0 = (coordinates[i,0,2]-coordinates[i,0,0]) # slot0 original h
        h1 = (coordinates[i,1,2]-coordinates[i,1,0]) # slot1 original h
        h2 = (coordinates[i,2,2]-coordinates[i,2,0]) # slot2 original h
        w0 = (coordinates[i,0,3]-coordinates[i,0,1]) # slot0 original w
        w1 = (coordinates[i,1,3]-coordinates[i,1,1]) # slot1 original w
        w2 = (coordinates[i,2,3]-coordinates[i,2,1]) # slot2 original w
        
        # slots positions
        top0 = coordinates[i,0,0]
        top1 = coordinates[i,1,0]
        top2 = coordinates[i,2,0]
        left0 = coordinates[i,0,1]
        left1 = coordinates[i,1,1]
        left2 = coordinates[i,2,1]

        #tag1

        # slots categories
        type0 = semantics[i,0]
        type1 = semantics[i,1]
        type2 = semantics[i,2]
        
        # deltas
        deltas_raw[i,0] = delta0
        deltas_raw[i,1] = delta1
        deltas_raw[i,2] = delta2
        
        # screen
        x_raw[i,0] = h
        x_raw[i,1] = w
        
        # slot0
        x_raw[i,2] = int(round(h0*delta0)) # slot0 twisted h
        x_raw[i,3] = int(round(w0*delta0)) # slot0 twisted w
        x_raw[i,4] = type0[0] # slot0 semantic 0
        x_raw[i,5] = type0[1] # slot0 semantic 1
        x_raw[i,6] = type0[2] # slot0 semantic 2
        
        # slot1
        x_raw[i,7] = int(round(h1*delta1)) # slot1 twisted h
        x_raw[i,8] = int(round(w1*delta1)) # slot1 twisted w
        x_raw[i,9] = type1[0] # slot1 semantic 0
        x_raw[i,10] = type1[1] # slot1 semantic 1
        x_raw[i,11] = type1[2] # slot1 semantic 2

        # slot2
        x_raw[i,12] = int(round(h2*delta2)) # slot2 twisted h
        x_raw[i,13] = int(round(w2*delta2)) # slot2 twisted w
        x_raw[i,14] = type2[0] # slot2 semantic 0
        x_raw[i,15] = type2[1] # slot2 semantic 1
        x_raw[i,16] = type2[2] # slot2 semantic 2

        # slot0
        y_raw[i,0] = top0 # slot0 top
        y_raw[i,1] = left0 # slot0 left
        deltas_raw[i,0] = delta0 # slot0 delta

        # slot1
        y_raw[i,2] = top1 # slot1 top
        y_raw[i,3] = left1 # slot1 left
        deltas_raw[i,1] = delta1 # slot1 delta

        # slot2
        y_raw[i,4] = top2 # slot2 top
        y_raw[i,5] = left2 # slot2 left
        deltas_raw[i,2] = delta2 # slot2 delta
        
    '''
    np.save(root_path+'/x_raw.npy',x_raw)
    np.save(root_path+'/y_raw.npy',y_raw)
    np.save(root_path+'/deltas_raw.npy',deltas_raw)
    '''

    x_norm = np.zeros(np.shape(x_raw),dtype=float)
    y_norm = np.zeros((len(y_raw),9),dtype=float)

    n_samples = len(y_norm)
    n_slots = 3

    for i in range(n_samples):
        
        # screen dimensions
        x_norm[i,0] = x_raw[i,0]/1000
        x_norm[i,1] = x_raw[i,1]/1000
        
        # slot0
        x_norm[i,2] = x_raw[i,2]/1000 # slot0 twisted h
        x_norm[i,3] = x_raw[i,3]/1000 # slot0 twisted w
        x_norm[i,4] = x_raw[i,4]      # slot0 category score 0
        x_norm[i,5] = x_raw[i,5]      # slot0 category score 1
        x_norm[i,6] = x_raw[i,6]      # slot0 category score 2

        # slot1
        x_norm[i,7] = x_raw[i,7]/1000
        x_norm[i,8] = x_raw[i,8]/1000
        x_norm[i,9] = x_raw[i,9]
        x_norm[i,10] = x_raw[i,10]
        x_norm[i,11] = x_raw[i,11]

        # slot2
        x_norm[i,12] = x_raw[i,12]/1000
        x_norm[i,13] = x_raw[i,13]/1000
        x_norm[i,14] = x_raw[i,14]
        x_norm[i,15] = x_raw[i,15]
        x_norm[i,16] = x_raw[i,16]
        
        # slot0
        y_norm[i,0] = y_raw[i,0]/1000 # slot0 top
        y_norm[i,1] = y_raw[i,1]/1000 # slot0 left
        y_norm[i,2] = deltas_raw[i,0]/1.5 # slot0 delta

        # slot1
        y_norm[i,3] = y_raw[i,2]/1000
        y_norm[i,4] = y_raw[i,3]/1000
        y_norm[i,5] = deltas_raw[i,1]/1.5

        # slot2
        y_norm[i,6] = y_raw[i,4]/1000
        y_norm[i,7] = y_raw[i,5]/1000
        y_norm[i,8] = deltas_raw[i,2]/1.5

    str_date=get_simple_time_str()
    np.save('/home/paintedpalms/rdrive/taff/code/data/x_synth1_'+str_date+'.npy',x_norm)
    np.save('/home/paintedpalms/rdrive/taff/code/data/y_synth1_'+str_date+'.npy',y_norm)


def display_synth_samples_1(x_norm,y_norm,n,rule):

    #n_samples = len(x_norm)
    n_samples=1000*n
    n_slots = 3

    x_raw = np.zeros(np.shape(x_norm),dtype=int)
    y_raw = np.zeros((n_samples,6),dtype=int)
    deltas_raw = np.zeros((n_samples,n_slots),dtype=float)

    for i in range(n_samples):
        
        # screen dimensions
        x_raw[i,0] = int(np.round(x_norm[i,0]*1000))
        x_raw[i,1] = int(np.round(x_norm[i,1]*1000))
        
        # slot0
        x_raw[i,2] = int(np.round(x_norm[i,2]*1000)) # slot0 twisted h
        x_raw[i,3] = int(np.round(x_norm[i,3]*1000)) # slot0 twisted w
        x_raw[i,4] = int(np.round(x_norm[i,4]))      # slot0 category score 0
        x_raw[i,5] = int(np.round(x_norm[i,5]))      # slot0 category score 1
        x_raw[i,6] = int(np.round(x_norm[i,6]))      # slot0 category score 2

        # slot1
        x_raw[i,7] = int(np.round(x_norm[i,7]*1000))
        x_raw[i,8] = int(np.round(x_norm[i,8]*1000))
        x_raw[i,9] = int(np.round(x_norm[i,9]))
        x_raw[i,10] = int(np.round(x_norm[i,10]))
        x_raw[i,11] = int(np.round(x_norm[i,11]))

        # slot2
        x_raw[i,12] = int(np.round(x_norm[i,12]*1000))
        x_raw[i,13] = int(np.round(x_norm[i,13]*1000))
        x_raw[i,14] = int(np.round(x_norm[i,14]))
        x_raw[i,15] = int(np.round(x_norm[i,15]))
        x_raw[i,16] = int(np.round(x_norm[i,16]))

        # slot0
        y_raw[i,0] = int(np.round(y_norm[i,0]*1000)) # slot0 top
        y_raw[i,1] = int(np.round(y_norm[i,1]*1000)) # slot0 left
        deltas_raw[i,0] = y_norm[i,2]*1.5 # slot0 delta

        # slot1
        y_raw[i,2] = int(np.round(y_norm[i,3]*1000))
        y_raw[i,3] = int(np.round(y_norm[i,4]*1000))
        deltas_raw[i,1] = y_norm[i,5]*1.5

        # slot2
        y_raw[i,4] = int(np.round(y_norm[i,6]*1000))
        y_raw[i,5] = int(np.round(y_norm[i,7]*1000))
        deltas_raw[i,2] = y_norm[i,8]*1.5

    n_slots = 3
    new_samples = []
    for num_sample in range(n_samples):

        kx = 2
        ky = 0
        slots = []
        for num_slot in range(n_slots):

            slot = Clay()
            slot.top = int(y_raw[num_sample,ky+0])
            slot.left = int(y_raw[num_sample,ky+1])

            slot.h =  int(x_raw[num_sample,kx+0]/deltas_raw[num_sample,num_slot])
            slot.w =  int(x_raw[num_sample,kx+1]/deltas_raw[num_sample,num_slot])
            slot.low = int(slot.top+slot.h)
            slot.right = int(slot.left+slot.w)

            if slot.right > 300: print("tag2 : error", slot.right)

            type0 = int(x_raw[num_sample,kx+2])
            type1 = int(x_raw[num_sample,kx+3])
            type2 = int(x_raw[num_sample,kx+4])
            slot.type = np.asarray([type0,type1,type2])

            slot.type = list(slot.type)
            slots.append(slot)

            kx+=5
            ky+=2

        new_samples.append(slots)

    k=0
    for sample in new_samples:
        slots = sample#[0]

        '''
        s0=slots[0]
        s1=slots[1]
        s2=slots[2]
        print("right 0",s0.left+s0.w)
        print("right 1",s1.left+s1.w)
        print("right 2",s2.left+s2.w)
        '''

        if k<n:
            if sample_is_concerned_by_rule(slots,rule):
                show_screen5_ancien(slots,600,300)
                k+=1

# get type of a synth1 sample
def get_types_trigram(slots):
    tp=""
    for s in slots:
        if s.type == [1, 0, 0]: tp += "r"
        if s.type == [0, 1, 0]: tp += "g"
        if s.type == [0, 0, 1]: tp += "b"
    return tp

def sample_is_concerned_by_rule(slots,rule):
    tp=get_types_trigram(slots)
    spec_combinations=get_special_combinations_trigram()
    ok = False
    if rule=="general" and tp not in spec_combinations:ok=True
    if rule==tp:ok=True
    return ok

def add_shape_color5_ancien(npa,top,left,low,right,r,g,b):    
    for i in range(len(npa)):
        for j in range(len(npa[0])):
            if top<=i<=low and left<=j<=right:
                npa[i,j,0] = r
                npa[i,j,1] = g
                npa[i,j,2] = b
    return npa

def show_screen5_ancien(slots,screen_h,screen_w):
    npa = init_screen_ancien(screen_h,screen_w)
    for num_slot in range(len(slots)):
        slot = slots[num_slot]
        
        '''
        if num_slot == 0:(r,g,b) = (255,100,100)
        if num_slot == 1:(r,g,b) = (100,255,100)
        if num_slot == 2:(r,g,b) = (100,100,255)
        '''
        
        [r,g,b] = 155*np.asarray(slot.type)+100
        
        npa = add_shape_color5_ancien(npa,slot.top,slot.left,slot.low,slot.right,r,g,b)
    npa=resize_image(npa, 100)
    display(get_image_from_npa(npa))

def init_screen_ancien(h,w):    
    npa = np.zeros((h,w,4),dtype=np.uint8)
    for i in range(len(npa)):
        for j in range(len(npa[0])):
            v=100
            for k in [i,j]:
                if k%100==0:v=70
            npa[i,j,0] = v
            npa[i,j,1] = v
            npa[i,j,2] = v
            npa[i,j,3] = 255
    return npa
            

## eval



#------------------------------------------------------------------------------------------------------------------------------------
#                                                        imports
#------------------------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        basic plots
#------------------------------------------------------------------------------------------------------------------------------------

# display 2D npa as an image
def plot_map(npa):
    plt.imshow(npa)
    plt.axis('off')
    if 0==1:plt.title('npa')
    plt.show()

# plot 1D npa as a curve
def plot_curve(npa):    
    plt.plot(npa)
    plt.show()

# display histogram of a list
def plot_hist(npa):
    plt.hist(list(npa))
    plt.show()

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        color maps
#------------------------------------------------------------------------------------------------------------------------------------

# plot color maps of a 2D npa
def plot_examples():

    viridis = cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    pink = np.array([248/256, 24/256, 148/256, 1])
    newcolors[:25, :] = pink
    newcmp = ListedColormap(newcolors)
    cms=[viridis, newcmp]

    #np.random.seed(19680801)
    data = np.random.randn(30, 30)

    fig, axs = plt.subplots(1, 2, figsize=(6, 3), constrained_layout=True)
    for [ax, cmap] in zip(axs, cms):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        fig.colorbar(psm, ax=ax)
    plt.show()

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        quant
#------------------------------------------------------------------------------------------------------------------------------------

# root mean squared error (rmse)
def get_rmse(y_test, y_pred):
    n_samples=len(y_test)
    sq_errors=[]
    for i_sample in range(n_samples):
        sq_errors.append((y_pred[i_sample]-y_test[i_sample])**2)     # get squared errors
    mse = np.mean(sq_errors)                                         # get mean squared error
    rmse = sqrt(mse)                                                 # get root mean squared error
    return rmse

#------------------------------------------------------------------------------------------------------------------
#                                                        display quantiative results
#------------------------------------------------------------------------------------------------------------------

# show two arrays results, side by side
def collate(y_test,y_pred):
    n_samples=len(y_test)
    for i_sample in range(n_samples):
        print(np.round(y_test[i_sample],2),"\t",np.round(y_pred[i_sample],2))


#------------------------------------------------------------------------------------------------------------------
#                                     # plot
#------------------------------------------------------------------------------------------------------------------

# na

#------------------------------------------------------------------------------------------------------------------
#                                     # layout eval : overlap
#------------------------------------------------------------------------------------------------------------------

'''

#                                   /!\ MOVED IN LAYOUT_PROCESS

def get_intersection_area(ba,bb):
    # dw = min(rights) - max(lefts)
    # dh = min(lows) - max(tops)
    dw = min(ba.x2,bb.x2) - max(ba.x1,bb.x1)
    dh = min(ba.y2,bb.y2) - max(ba.y1,bb.y1)
    area = 0
    if dw > 0 and dh > 0 : 
        area = dw * dh
    return area

def get_exceeding_score(bbox_samples,w,h):
    # input : top,left,low,right
    area_samples=0
    for i_sample in range(len(bbox_samples)):
        bboxes=bbox_samples[i_sample]
        area_samples+=get_sample_exceeding_score(bboxes,w,h)
    return area_samples/len(bbox_samples)/w/h

def get_sample_exceeding_score(bboxes,w,h):
    area_sample=0
    bg=get_bbox_obj_from_npa1([0,0,h,w])
    for i in range(len(bboxes)):
        bb=get_bbox_obj_from_npa1(bboxes[i])
        area_bboxes = bb.w * bb.h - get_intersection_area(bb,bg)
        area_sample+=area_bboxes
    return area_sample

def get_overlap_score(bbox_samples,w,h):
    # input : top,left,low,right
    area_samples=0
    for i_sample in range(len(bbox_samples)):
        bboxes=bbox_samples[i_sample]
        area_samples+=get_sample_overlap_score(bboxes)
    return area_samples/len(bbox_samples)/w/h

def get_sample_overlap_score(bboxes):
    area_sample=0
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            if i<j:
                bb_i=get_bbox_obj_from_npa1(bboxes[i])
                bb_j=get_bbox_obj_from_npa1(bboxes[j])
                area_sample+=get_intersection_area(bb_i,bb_j)
    return area_sample
'''

## basics numpy array

if 1==0:

    # np range
    np.arange(0,10)

    # merge two np arrays
    npa1=np.arange(0,10)
    npa2=np.arange(20,30)
    npa=np.asarray([npa1,npa2])

    # concatenate two np arrays
    npa=np.concatenate((npa1,npa2),axis=0)

    # sort npa by second array
    sorted_npa = npa[numpy.argsort(npa[:, 1])]

import sys
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageDraw

#------------------------------------------------------------------------------------------------------------------
#                           # fid : apply frechet inception distance 
#------------------------------------------------------------------------------------------------------------------

# example of calculating the frechet inception distance in Keras
import numpy
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from numpy import asarray
from numpy.random import randint
from scipy.linalg import sqrtm
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.datasets.mnist import load_data
from skimage.transform import resize

# scale an array of images to a new size
def scale_images(images, new_shape):
    images_list = list()
    for image in images:
        # resize with nearest neighbor interpolation
        new_image = resize(image, new_shape, 0)
        # store
        images_list.append(new_image)
    return asarray(images_list)

# calculate frechet inception distance
def calculate_fid(model, images1, images2):
    '''
    images1 = real
    images2 = gen
    '''
    # calculate activations
    act1 = model.predict(images1)
    act2 = model.predict(images2)
    # calculate mean and covariance statistics
    mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
    mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)
    # calculate sum squared difference between means
    ssdiff = numpy.sum((mu1 - mu2)**2.0)
    # calculate sqrt of product between cov
    covmean = sqrtm(sigma1.dot(sigma2))
    # check and correct imaginary numbers from sqrt
    if iscomplexobj(covmean):
        covmean = covmean.real
    # calculate score
    fid = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
    return fid

def get_fid(images_real,images_gen,option_print):

    # prepare the inception v3 model
    model = InceptionV3(include_top=False, pooling='avg', input_shape=(299,299,3))

    if 1==0:

        # define two fake collections of images
        images1 = randint(0, 255, 10*32*32*3)
        images1 = images1.reshape((10,32,32,3))
        images2 = randint(0, 255, 10*32*32*3)
        images2 = images2.reshape((10,32,32,3))

    if 1==0:

        # images1 = rasterized real layouts
        # images2 = rasterized generated layouts

        images1=images_real
        images2=images_gen3b

    if 1==1:

        images1=images_real
        images2=images_gen

    if option_print==1:print('Prepared', images1.shape, images2.shape)
    # convert integer to floating point values
    images1 = images1.astype('float32')
    images2 = images2.astype('float32')


    # resize images
    images1 = scale_images(images1, (299,299,3))
    images2 = scale_images(images2, (299,299,3))
    if option_print==1:print('Scaled', images1.shape, images2.shape)
    # pre-process images
    images1 = preprocess_input(images1)
    images2 = preprocess_input(images2)

    

    '''
    if 1==0:
        # fid between images1 and images1
        fid = calculate_fid(model, images1, images1)
        if option_print==1:print('FID (same): %.3f' % fid)
    '''

    # fid between images1 and images2
    fid = calculate_fid(model, images1, images2)
    if option_print==1:print('FID (different): %.3f' % fid)
        
    

    return fid

## gan layout



#------------------------------------------------------------------------------------------------------------------------------------
#                                                        public imports
#------------------------------------------------------------------------------------------------------------------------------------

# imports : public (standard)
import numpy as np
from PIL import Image
import datetime

# imports : public (deep learning)
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Input, Dense, Conv2D, GlobalAveragePooling2D, Dropout,LeakyReLU, Conv2DTranspose, Reshape, Concatenate,BatchNormalization,UpSampling2D,Activation
from tensorflow.keras.optimizers import Adam, SGD
from keras.optimizers import Adam, RMSprop
from keras.layers.merge import concatenate


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        save / load weights
#------------------------------------------------------------------------------------------------------------------------------------

'''
if 0==1:
    sequential_model.save_weights("weights.h5")
    sequential_model.load_weights("weights.h5")
'''

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        train gan
#------------------------------------------------------------------------------------------------------------------------------------

# to test
def train_step_gen1(c,g_optimizer,gen,dsc,real_image, noise, experimental_relax_shapes=True):

    fake_image = gen(noise)
    pred_real, pred_fake = tf.split(dsc(tf.concat([real_image, fake_image], axis=0)), num_or_size_splits=2, axis=0)
    g_loss = tf.reduce_mean(-tf.math.log(pred_fake + 1e-8))
    g_gradients = tf.gradients(g_loss, gen.trainable_variables)
    g_optimizer.apply_gradients(zip(g_gradients, gen.trainable_variables))

    if 1==0:return g_loss
    if 1==1:return gen,dsc,g_loss

# to test
def train_step_dsc1(c,d_optimizer,gen,dsc,real_image, noise,experimental_relax_shapes=True):
    
    if "rasterize dsc input" not in c.options:fake_image = gen(noise)
    if "rasterize dsc input" in c.options:fake_image = rasterize_sample(gen(noise),c.w,c.h,2)

    pred_real, pred_fake = tf.split(dsc(tf.concat([real_image, fake_image], axis=0)), num_or_size_splits=2, axis=0)
    d_loss = tf.reduce_mean(-tf.math.log(pred_real + 1e-8)) + tf.reduce_mean(-tf.math.log(1 - pred_fake + 1e-8))
    d_gradients = tf.gradients(d_loss, dsc.trainable_variables)
    d_optimizer.apply_gradients(zip(d_gradients, dsc.trainable_variables))
    
    if 1==0:return d_loss
    if 1==1:return gen,dsc,d_loss

# to replace because tf framework too much constraint
def build_train_step_gen(c,gen,dsc):

    '''
    d_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    '''

    if 1==1:g_optimizer = Adam(lr=c.lr_gen, beta_1=0.0, beta_2=0.9) # adam (origin)
    if 1==0:g_optimizer = SGD(learning_rate=c.lr_gen) # sgd

    @tf.function
    def train_step_gen(real_image, noise, experimental_relax_shapes=True):

        fake_image = gen(noise)
        pred_real, pred_fake = tf.split(dsc(tf.concat([real_image, fake_image], axis=0)), num_or_size_splits=2, axis=0)
        g_loss = tf.reduce_mean(-tf.math.log(pred_fake + 1e-8))
        g_gradients = tf.gradients(g_loss, gen.trainable_variables)
        g_optimizer.apply_gradients(zip(g_gradients, gen.trainable_variables))

        if 1==0:return d_loss, g_loss
        if 1==1:return g_loss

    return train_step_gen

# to replace because tf framework too much constraint
def build_train_step_dsc(c,gen,dsc):

    '''
    d_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    '''
    d_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)

    @tf.function
    def train_step_dsc(real_image, noise,experimental_relax_shapes=True):
        
        if "rasterize dsc input" not in c.options:fake_image=gen(noise)
        if "rasterize dsc input" in c.options:
            
            #fake_image = rasterize_sample(gen(noise),c.w,c.h)

            '''
            if h==None:h=600
            if w==None:w=300
            npa_bg=get_npa_bg3(h,w)
            for i_asset in range(len(sample.assets)):
                asset=sample.assets[i_asset]
                r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
                npa_bg=add_shape2(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
            npa_bg=resize_image(npa_bg,100)
            '''

        pred_real, pred_fake = tf.split(dsc(tf.concat([real_image, fake_image], axis=0)), num_or_size_splits=2, axis=0)
        d_loss = tf.reduce_mean(-tf.math.log(pred_real + 1e-8)) + tf.reduce_mean(-tf.math.log(1 - pred_fake + 1e-8))
        g_loss = tf.reduce_mean(-tf.math.log(pred_fake + 1e-8))
        d_gradients = tf.gradients(d_loss, dsc.trainable_variables)
        d_optimizer.apply_gradients(zip(d_gradients, dsc.trainable_variables))
        
        if 1==0:return d_loss, g_loss
        if 1==1:return d_loss

    return train_step_dsc

def build_train_step(c,gen, dsc):

    '''
    d_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=0.0001, beta_1=0.0, beta_2=0.9)
    '''

    d_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)

    @tf.function
    def train_step(real_image, noise,experimental_relax_shapes=True):

        fake_image = gen(noise)
        pred_real, pred_fake = tf.split(dsc(tf.concat([real_image, fake_image], axis=0)), num_or_size_splits=2, axis=0)
        d_loss = tf.reduce_mean(-tf.math.log(pred_real + 1e-8)) + tf.reduce_mean(-tf.math.log(1 - pred_fake + 1e-8))
        g_loss = tf.reduce_mean(-tf.math.log(pred_fake + 1e-8))
        d_gradients = tf.gradients(d_loss, dsc.trainable_variables)
        g_gradients = tf.gradients(g_loss, gen.trainable_variables)

        #print("gradient",g_gradients)#[0][0][0].numpy())

        # original
        d_optimizer.apply_gradients(zip(d_gradients, dsc.trainable_variables))
        g_optimizer.apply_gradients(zip(g_gradients, gen.trainable_variables))

        return d_loss, g_loss
    return train_step

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        use gan
#------------------------------------------------------------------------------------------------------------------------------------

# generate gan synth layouts from noise with trained gan
def generate_synth_layouts(c,generator,n_samples):
    stop=False
    #y_gen=generator.predict(np.random.normal(size=(1000,)+c.noise_size))
    y_gen=generator.predict(np.random.normal(size=(n_samples,)+c.noise_size))
    y_gen=y_gen[:,:,:,0]
    for i in range(y_gen.shape[0]):
        for j in range(y_gen.shape[1]):
            for k in range(y_gen.shape[2]):
                if np.isnan(y_gen[i,j,k]):stop=True
    samples_gan=[]
    if stop==False:
        '''
        if c.option_dataset==1:n_tp=3
        if c.option_dataset>1:n_tp=4
        '''
        if c.option_norm=="tanh":y_gen=denormalize_y_gan(y_gen,c.w,c.h,c.n_tp)
        if c.option_norm=="sigm":y_gen=denormalize2_y_gan(y_gen,c.w,c.h,c.n_tp)
    return y_gen,stop


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        build residual gan
#------------------------------------------------------------------------------------------------------------------------------------

'''
read = Input(shape=input_shape,name='read')

dense0 = Dense(n_input_units)(read)
activ0 = Activation('relu')(dense0)
drop0 = Dropout(drop_rate)(activ0)

dense1 = Dense(n_input_units)(drop0)
activ1 = Activation('relu')(dense1)
drop1 = Dropout(drop_rate)(activ1)

conc1 = concatenate([read,drop1],axis = 1)
'''

'''
def build_generator_residual(c):

    a1=c.noise_size[0]
    a2=c.noise_size[1]
    a3=c.noise_size[2]
    
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((a1,a2,a3))
    y = Reshape((a1*a2*a3,))(x)

    for i_block in range(c.n_residual_blocks):
        
        y0=y
        #y=Dense(c.numbers_neurons[0])(y)
        y=Dense(c.numbers_neurons[i_block])(y)
        y=Activation('relu')(y)
        y=Dropout(c.drop_out)(y)
        y=concatenate([y0,y])
        
    y = Dense(b1*b2*b3, activation="tanh")(y)
    y = Reshape((b1,b2,b3))(y)

    return Model(x, y)+
'''




def build_generator_residual(c):

    a1=c.noise_size[0]
    a2=c.noise_size[1]
    a3=c.noise_size[2]
    
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((a1,a2,a3))
    y = Reshape((a1*a2*a3,))(x)

    for i_block in range(c.n_residual_blocks):
        y0=y
        for i_rank in range(c.n_layers_per_residual_block):
            y=Dense(c.numbers_neurons[i_block])(y)
            y=Activation('relu')(y)
            y=Dropout(c.drop_out)(y)
        y=concatenate([y0,y])
        
    if c.option_norm=="tanh":y = Dense(b1*b2*b3, activation="tanh")(y)
    if c.option_norm=="sigm":y = Dense(b1*b2*b3, activation="sigmoid")(y)
    
    y = Reshape((b1,b2,b3))(y)

    return Model(x, y)

def build_discriminator_residual(c):

    x = Input(c.image_size)
    
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((b1,b2,b3))
    y = Reshape((b1*b2*b3,))(x)

    for i_block in range(c.n_residual_blocks):
        y0=y
        y=Dense(c.numbers_neurons[0])(y)
        y=Activation('relu')(y)
        y=Dropout(c.drop_out)(y)
        y=concatenate([y0,y])

    #y = LeakyReLU(0.2)(y)
    y = Dense(1, activation="sigmoid")(y)
    
    return Model(x, y)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        build simple gan
#------------------------------------------------------------------------------------------------------------------------------------

  
def build_generator_simple(c):

    a1=c.noise_size[0]
    a2=c.noise_size[1]
    a3=c.noise_size[2]
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((a1,a2,a3))
    y = Reshape((a1*a2*a3,))(x)

    i_layer=0
    while i_layer<len(c.numbers_neurons) and c.numbers_neurons[i_layer]>0:
        y = Dense(c.numbers_neurons[i_layer])(y)
        y = LeakyReLU(0.2)(y)
        y = Dropout(c.drop_out)(y)
        i_layer+=1
        
    y = Dense(b1*b2*b3, activation="tanh")(y)
    y = Reshape((b1,b2,b3))(y)

    return Model(x, y)

def build_discriminator_simple(c):

    x = Input(c.image_size)
    
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((b1,b2,b3))
    y = Reshape((b1*b2*b3,))(x)

    i_layer=len(c.numbers_neurons)-1
    while i_layer>0:
        y = Dense(c.numbers_neurons[i_layer])(y)
        y = LeakyReLU(0.2)(y)
        y = Dropout(c.drop_out)(y)
        i_layer-=1
        
    #y = LeakyReLU(0.2)(y)
    y = Dense(1, activation="sigmoid")(y)
    
    return Model(x, y)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        build gan 1
#------------------------------------------------------------------------------------------------------------------------------------

  
def build_generator1(c):

    a1=c.noise_size[0]
    a2=c.noise_size[1]
    a3=c.noise_size[2]
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((a1,a2,a3))
    y = Reshape((a1*a2*a3,))(x)

    i_layer=0
    while i_layer<len(c.numbers_neurons) and c.numbers_neurons[i_layer]>0:
        y = Dense(c.numbers_neurons[i_layer])(y)
        y = LeakyReLU(0.2)(y)
        i_layer+=1
        
    y = Dense(b1*b2*b3, activation="tanh")(y)
    y = Reshape((b1,b2,b3))(y)

    return Model(x, y)

def build_discriminator1(c):

    x = Input(c.image_size)
    
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((b1,b2,b3))
    y = Reshape((b1*b2*b3,))(x)

    i_layer=len(c.numbers_neurons)-1
    while i_layer>0:
        y = Dense(c.numbers_neurons[i_layer])(y)
        y = LeakyReLU(0.2)(y)
        i_layer-=1
        
    y = LeakyReLU(0.2)(y)
    y = Dense(1, activation="sigmoid")(y)
    
    return Model(x, y)


def build_discriminator_conv(c):

    x = Input(c.image_size)
    
    b1 = c.image_size[0]
    b2 = c.image_size[1]
    b3 = c.image_size[2]

    x = Input((b1,b2,b3))

    #y = Conv2D(64, 5, 5,subsample=(2,2),border_mode='same')(x)
    y = Conv2D(64, (5, 5))(x)
    
    y = LeakyReLU(0.2)(y)
    y = Dropout(c.drop_out)(y)

    y = Conv2D(128, 5, 5,subsample=(2,2),border_mode='same')(x)
    y = LeakyReLU(0.2)(y)
    y = Dropout(c.drop_out)(y)

    y = Flatten()(y)
    y = Dense(1, activation='sigmoid')(y)

    '''
    Convolution2D(64, 5, 5,subsample=(2,2),input_shape=(b1,b2,b3),border_mode='same', activation=LeakyReLU(0.2))
    Convolution2D(128, 5, 5, subsample=(2,2), border_mode='same', activation=LeakyReLU(0.2))
    '''
    return Model(x, y)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        à trier
#------------------------------------------------------------------------------------------------------------------------------------

'''
def build_discriminator(c):

    x = Input(c.image_size)
    y = Reshape((15,))(x)
    y = Dense(int(15/3))(y)
    y = LeakyReLU(0.2)(y)
    y = Dense(1, activation="sigmoid")(y)
    
    return Model(x, y)
'''

'''
def build_generator(c):

    x = Input(c.noise_size)
    y = Reshape((20,))(x)
    y = Dense(int(15/3))(y)
    y = LeakyReLU(0.2)(y)
    y = Dense(15, activation="tanh")(y)
    y = Reshape((3,5,1))(y)

    return Model(x, y)
  
def build_discriminator(c):

    x = Input(c.image_size)
    y = Reshape((15,))(x)
    y = Dense(int(15/3))(y)
    y = LeakyReLU(0.2)(y)
    y = Dense(1, activation="sigmoid")(y)
    
    return Model(x, y)
'''

'''
def build_generator(c):

    c.gen_betas=[]
    for i_layer in range(c.n_layers):betas.append(1)

    
    a1=c.noise_size[0]
    a2=c.noise_size[1]
    a3=c.noise_size[2]
    b1=c.image_size[0]
    b2=c.image_size[1]
    b3=c.image_size[2]
    
    x = Input((a1,a2,a3))
    y = Reshape((a1*a2*a3,))(x)

    for i_layer in range(c.n_layers):
    
        alpha=(i_layer+1)/(c.n_layers+2)
        beta=c.betas[i_layer]
        n=int(alpha*beta*b1*b2*b3)
        print("tr",alpha,n)
        n=max(n,1)
        c.gen_numbers.append(n)
        
        y = Dense(n)(y)
        y = LeakyReLU(0.2)(y)

        
    y = Dense(b1*b2*b3, activation="tanh")(y)
    y = Reshape((b1,b2,b3))(y)

    return Model(x, y)
'''

    

## exp



#------------------------------------------------------------------------------------------------------------------
#                                         public imports
#------------------------------------------------------------------------------------------------------------------

import os
import matplotlib.pyplot as plt
import shutil
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn import datasets
import time


#------------------------------------------------------------------------------------------------------------------
#                                         #     data
#------------------------------------------------------------------------------------------------------------------

def load_data_default(x,y):
    return x,y

def load_data_iris_romain():
    iris = load_iris()
    x = iris.data[:, :2]
    y = (iris.target != 0) * 1
    return x,y

#------------------------------------------------------------------------------------------------------------------
#                                         # pre-processing
#------------------------------------------------------------------------------------------------------------------

def add_intercept(x):
    intercept = np.ones((x.shape[0], 1))
    return np.concatenate((intercept, x), axis=1)

def preprocess_default(x,y):    
    return x,y

def preprocess_logistic(x,y):    
    x = add_intercept(x)
    return x,y

#------------------------------------------------------------------------------------------------------------------
#                                         # maths
#------------------------------------------------------------------------------------------------------------------

def tr(x):
    return x.T

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

#------------------------------------------------------------------------------------------------------------------
#                                         # models
#------------------------------------------------------------------------------------------------------------------

# linear regression
def model_linear(x,weights):
    h=np.dot(x, weights)
    return h

# logistic regression
def model_logistic(x,weights):
    h=model_linear(x,weights)
    h=sigmoid(h)
    return h

#------------------------------------------------------------------------------------------------------------------
#                                         optim
#------------------------------------------------------------------------------------------------------------------


def init_weights_zeros(c,x,y):
    weights = np.zeros(c.n_features+1)
    return weights

def loss_logistic(h, y):
    return (-y*np.log(h)-(1-y)*np.log(1-h)).mean()

# gradient = vector of n_features values
# each value = derivative of loss according the weight assigned to one feature 

def gradient_logistic(x,y,h):
    # linear regression : error : E = ... 
    # linear regression : gradient : dE/dx = x.(h-y)
    n_samples=x.shape[0]
    gradient=np.dot(tr(x),(h-y))/n_samples 
    return gradient
        
def gradient_linear(x,y,h):
    # linear regression : error : E = (y-ax)^2
    # linear regression : gradient : dE/dx = 2*(y-ax)*(-x)
    n_samples=x.shape[0]
    gradient=np.dot(tr(x),(h-y))/n_samples 
    return gradient

'''
def gradient_descent(c,x,y):
    for i_epoch in range(c.n_epochs):
        h = c.model_train(x,c.weights)         # predict train output
        gradient = c.gradient(x,y,h)           # compute gradient according to output
        c.weights -= c.lr * gradient           # update weights according to gradient
        display_results_train(c,x,y,i_epoch)
'''        

def gradient_descent(c,x,y):
    for i_epoch in range(c.n_epochs):
        for i_batch in range(c.n_batches):
            
            #x_batch,y_batch=sub_batch(x,y,c.batch_size,c.indexes)
            #x_batch,y_batch=random_batch(x,y,c.batch_size)
            x_batch,y_batch=get_batch(c,x,y,i_batch)
            
            h_batch = c.model_train(x_batch,c.weights)               # predict train output
            gradient = c.gradient(x_batch,y_batch,h_batch)           # compute gradient according to output
            c.weights -= c.lr * gradient                             # update weights according to gradient
        display_results_train(c,x,y,i_epoch)

def get_batch(c,x,y,i_batch):
    if c.option_bgd=="regular":
        x_batch=x[i_batch*c.batch_size:(i_batch+1)*c.batch_size]
        y_batch=y[i_batch*c.batch_size:(i_batch+1)*c.batch_size]
    if c.option_bgd=="stochastic":
        x_batch,y_batch=sub_batch(x,y,c.batch_size,c.indexes)
    if c.option_bgd=="stochastic rebate":
        x_batch,y_batch=random_batch(x,y,20)

    return x_batch,y_batch

#------------------------------------------------------------------------------------------------------------------
#                                         eval + prod
#------------------------------------------------------------------------------------------------------------------

def display_results_train(c,x,y,i_epoch):
    if i_epoch % int(.1*c.n_epochs) == 0:
        h=c.model_train(x,c.weights)
        print(i_epoch,"loss",c.loss(h, y),time.ctime())

def display_results_test(c,x,y):
    h=c.model_prod(c, x, c.weights)
    acc=(h==y).mean()
    print("")
    print("weights",c.weights)
    print("")
    print("accuracy",acc)
    print("")
        
def output_bin(c,x, weights):
    h=c.model_train(x,weights)
    h_bin=h>= 0.5
    return h_bin







#------------------------------------------------------------------------------------------------------------------------------------
#                                         ## draft
#------------------------------------------------------------------------------------------------------------------------------------

def get_valid_exps_results(p_exps_folder,start,end):

    '''
    # for each parameters file in folder results temp
    if exp_folder=="":p_results="/home/paintedpalms/rdrive/taff/code/results/results_temp"
    if exp_folder!="":p_results="/home/paintedpalms/rdrive/taff/code/results"+"/"+exp_folder
    '''

    result_dicts=[]
    valid_exp_names=[]
    exp_names=os.listdir(p_exps_folder)

    exp_names.sort()
    for exp_name in exp_names[start:end]:
        # check folder is valid
        p_exp=p_exps_folder+"/"+exp_name
        file_names=os.listdir(p_exp)
        if len(file_names)>1:

            # check parameters file is valid
            p_text_file=p_exp+"/parameters.txt"
            if os.path.exists(p_text_file):

                # get values from parameters file
                valid_exp_names.append(exp_name)
                d=get_exp_results(p_text_file)

                '''
                s=read_text_file(p_text_file)
                valid_exp_names.append(exp_name)
                result_dicts.append(get_dict_from_text(s,"\t"))
                '''

    return valid_exp_names,result_dicts

def get_exp_results2(exps_folder_name,exp_name):
    
    p_text_file=p_code+"/"+"results"+"/"+exps_folder_name+"/"+exp_name+"/parameters.txt"
    return get_exp_results(p_text_file)

def get_exp_results(p_text_file):
    s=read_text_file(p_text_file)
    d=get_dict_from_text(s,"\t")
    return d

def get_dicts_value(dicts,key):
    values=[]
    for d in dicts:values.append(d[key])
    return values

# print weights
def print_weights(model):
    w=model.get_weights()[0][1][20:25]
    pl=[]
    for v in w:
        v=(v-np.round(v,5))*10000000
        if np.isnan(v)==False:v=int(v)
        pl.append(v)
    return str(pl)

def get_y_gan(c):

    y_gan=np.load(c.p_data)
    y_gan=y_gan[:c.n_samples_max_train]

    c.n_samples=len(y_gan)

    c.n_steps=c.n_samples//c.batch_size

    if c.option_norm=="tanh":y_gan=normalize_y_gan(y_gan,c.w,c.h,c.n_tp)
    if c.option_norm=="sigm":y_gan=normalize2_y_gan(y_gan,c.w,c.h,c.n_tp)
    
    y_gan=np.expand_dims(y_gan, axis=3)
    y_gan=y_gan.astype("float32")

    return y_gan

def print_summary(c,generator,discriminator):
    if c.summary_option==1:
        print("")
        print("")
        print("summary : generator")
        print("")
        print(generator.summary())
        print("")
        print("")
        print("summary : discriminator")
        print("")
        print(generator.summary())
        print("")
        print("")

## fw_tensorflow

# main
def train_gan(c):

    if c.get_y_gan=="":y_gan = get_y_gan(c)
    if c.get_y_gan!="":y_gan = c.get_y_gan(c)

    # build generator
    if "gen simple" in c.options:generator = build_generator_simple(c)
    if "gen residual" in c.options:generator = build_generator_residual(c)

    # build discriminator
    if "dsc simple" in c.options:discriminator = build_discriminator_simple(c)
    if "dsc residual" in c.options:discriminator = build_discriminator_residual(c)
    if "dsc conv" in c.options:discriminator = build_discriminator_conv(c)
    
    # display model
    print_summary(c,generator,discriminator)

    # build train step
    if 1==0:train_step=build_train_step(c,generator, discriminator)
    if 1==1:train_step_gen=build_train_step_gen(c,generator, discriminator)
    if 1==1:train_step_dsc=build_train_step_dsc(c,generator, discriminator)
    if 1==0:train_step_gen=train_step_gen1
    if 1==0:train_step_dsc=train_step_dsc1

    # load initial weights
    if c.weights_path!="":
        generator.load_weights(c.weights_path+"/gen_weights_prev"+".h5")
        discriminator.load_weights(c.weights_path+"/dsc_weights_prev"+".h5")
        print("generator weights have been initialized with previous weights",print_weights(generator))

    # load initial real sample batch (standard)
    y_real = y_gan[np.random.permutation(c.n_samples)[:c.batch_size]]

    # load initial real sample batch (rasterized)
    if "rasterize dsc input" in c.options:y_real_rast=rasterize_sample(y_real,c.w,c.h,2)

    # create random noise
    noise = np.random.normal(0.0, 1.0, (c.batch_size,) + c.noise_size)

    # optimizers
    d_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)
    g_optimizer = Adam(lr=c.lr_dsc, beta_1=0.0, beta_2=0.9)

    # first training step : gen
    if 1==0:d_loss, ok = train_step_dsc(y_real, noise) # (origin)
    if 1==1:d_loss = train_step_dsc(y_real, noise) # (corrected) # ok
    if 1==0:d_loss = train_step_dsc(c,g_optimizer,generator,discriminator,y_real, noise)
    if 1==0:d_loss = train_step_dsc(y_real_rast, noise) # (rasterized)

    # first training step : dsc
    if 1==0:ok, g_loss = train_step_gen(y_real, noise) # (origin)
    if 1==1:g_loss = train_step_gen(y_real, noise) # (corrected) # ok
    if 1==0:g_loss = train_step_gen(c,g_optimizer,generator,discriminator,y_real,noise)
    if 1==0:g_loss = train_step_gen(y_real, noise) # (rasterized)

    # train model
    stop=False
    switch=0
    mn_overlap=1
    mx_div=0
    for i_epoch in range(c.n_epochs):
        for i_step in range(c.n_steps-1):

            # get real layouts
            if 1==1:y_real = y_gan[np.random.permutation(c.n_samples)[:c.batch_size]]
            if 1==0:y_real = y_gan[i_step*c.batch_size:(i_step+1)*c.batch_size]

            # prints
            if 1==0:print("d_loss",np.round(d_loss.numpy(),2),"g_loss",np.round(g_loss.numpy(),2))
            if 1==0:print("train gen")
            
            # train generator
            noise = np.random.normal(0.0, 1.0, (c.batch_size,) + c.noise_size)
            if 1==0:d_loss, g_loss = train_step_gen(y_real, noise)
            if 1==1:g_loss = train_step_gen(y_real, noise)

            # check gen loss // dsc loss
            #if g_loss.numpy()<2/3*d_loss.numpy():
            if 1==1:

                # prints
                if 1==0:print("train dsc")

                # train discriminator
                if 1==0:d_loss, g_loss = train_step_dsc(y_real, noise)
                if 1==1:d_loss = train_step_dsc(y_real, noise)
                if 1==0:d_loss = train_step_dsc(y_real_rast, noise)

            if 1==0:print("")

        # print weights
        if 1==0:print("\t epoch",i_epoch,"weights",print_weights(generator))
                
        # interm process
        if i_epoch % c.n_every_save==0:
            
            # get interm y_gen
            y_gen,stop=generate_synth_layouts(c,generator,c.n_eval_quant)

            # get interm bboxes_gen
            bboxes_gen=get_bboxes_from_y_gan(y_gen,"y_gan") # output bbox : top,left,low,right

            # apply quant eval on inter y_gen
            if 1==1:score_align=get_layouts_alignment_score_a16(bboxes_gen,c.w)
            if 1==0:score_exceed=get_layouts_exceeding_score(bboxes_gen,c.w,c.h)
            if 1==0:score_overlap=get_layouts_overlap_score(bboxes_gen,c.w,c.h,"nested == overlap")
            if 1==1:score_overlap=get_layouts_overlap_score(bboxes_gen,c.w,c.h,"nested != overlap")
            '''
            if 1==1:score_div=get_layouts_diversity_score(bboxes_gen,c.w,c.h,c.n_assets)
            '''
            score_div = 0

            # check : init
            ok=0

            # check : nan errors
            if not np.isnan(score_overlap):
                if not np.isnan(score_div):
                    if not np.isnan(g_loss.numpy()):
                        if not np.isnan(d_loss.numpy()):
                            ok=1

            # check : diversity
            if 1==0:
                if score_div<0.15: # 0.25:
                    if i_epoch>20:
                        ok=0

            if ok==1:

                # get interm gen results
                if 1==0:c.errors.append(score_overlap)
                if 1==1:c.errors.append(score_align)
                c.diversities.append(score_div)
                c.losses_gen.append(g_loss.numpy())
                c.losses_dsc.append(d_loss.numpy())
                s_dloss=np.round(d_loss.numpy(),2)
                s_gloss=np.round(g_loss.numpy(),2)
                if 1==0:s_error=np.round(score_overlap,5)
                if 1==1:s_error=np.round(score_align,5)
                s_div=score_div
                
                # display gen samples
                if i_epoch % c.n_every_display==0:
                    samples_gen=get_samples_from_y_gan(y_gen,[],1)
                    npas=get_npas_show(samples_gen,c.w,c.h,0,5)
                    npa_all=align_images(npas)
                    img=get_image_from_npa(npa_all)
                    display(img)

                # save weights (alternately)
                if switch==0:
                    generator.save_weights(c.results_folder+"/gen_weights_a"+".h5")
                    discriminator.save_weights(c.results_folder+"/dsc_weights_a"+".h5")
                    print("OK, switch 0, saving weights gen a",print_weights(generator))
                if switch==1:
                    generator.save_weights(c.results_folder+"/gen_weights_b"+".h5")
                    discriminator.save_weights(c.results_folder+"/dsc_weights_b"+".h5")
                    print("OK, switch 1, saving weights gen b",print_weights(generator))
                switch=abs(1-switch)                

                # print results
                print("save epoch",i_epoch,"\t",s_div,"\t",s_dloss,"\t",s_gloss,"\t",s_error,"\t",time.ctime())
                print("")

                # save results
                np.save(c.results_folder+"/y_gen.npy",y_gen)
                s=get_exp_summary(c)
                s+=get_str_with_tabs("overlap",score_overlap,5)
                s+=get_str_with_tabs("diversity",score_div,5)
                save_text(c.results_folder+"/parameters.txt",s)

                # save best results
                if score_overlap < mn_overlap and score_div > .20:
                    np.save(c.results_folder+"/y_gen_best_overlap.npy",y_gen)
                    mn_overlap=score_overlap
                if score_div > mx_div and score_overlap < .01:
                    np.save(c.results_folder+"/y_gen_best_div.npy",y_gen)
                    mx_div=score_div

            # if problem
            if ok==0:

                # rebuild model
                generator = build_generator_residual(c) #build_generator(c)
                if 1==1:discriminator = build_discriminator_residual(c) #build_discriminator(c)
                if 1==0:discriminator = build_discriminator_conv(c) #build_discriminator(c)
                train_step = build_train_step(c,generator, discriminator)

                # load previous weights
                print("nan error at epoch",i_epoch,"get back to previous checkpoint weights")

                if switch==0:
                    print("KO, switch",switch)
                    if os.path.exists(c.results_folder+"/gen_weights_a.h5"):
                        generator.load_weights(c.results_folder+"/gen_weights_a"+".h5")
                        discriminator.load_weights(c.results_folder+"/dsc_weights_a"+".h5")
                        print("generator load weights a",print_weights(generator))
                    else:
                        if os.path.exists(c.weights_path+"/gen_weights_prev"+".h5"):
                            generator.load_weights(c.weights_path+"/gen_weights_prev"+".h5")
                            discriminator.load_weights(c.weights_path+"/dsc_weights_prev"+".h5")
                            print("generator load weights prev",print_weights(generator))
                        
                if switch==1:
                    if os.path.exists(c.results_folder+"/gen_weights_b.h5"):
                        generator.load_weights(c.results_folder+"/gen_weights_b"+".h5")
                        discriminator.load_weights(c.results_folder+"/dsc_weights_b"+".h5")
                        print("generator load weights b",print_weights(generator))
                    else:
                        if os.path.exists(c.weights_path+"/gen_weights_prev"+".h5"):
                            generator.load_weights(c.weights_path+"/gen_weights_prev"+".h5")
                            discriminator.load_weights(c.weights_path+"/dsc_weights_prev"+".h5")
                            print("generator load weights prev",print_weights(generator))
                print("")

    '''

    #show_gan_synth_layouts(c,samples_gen[:c.n_eval_visual],i_epoch,1)
    
    # generate + save final results
    samples_gen,stop=generate_synth_layouts(c,generator,c.n_eval_quant)

    #####################
    if stop==False:show_gan_synth_layouts(c,samples_gen[:c.n_eval_visual],i_epoch,1)
    #####################

    # save str params
    s=get_exp_summary(c)

    # save str error (assets in overlaps + assets exceeding screen limits)
    samples_quant_eval=select_general_samples(samples_gen,1)
    v,error=quant_eval(samples_quant_eval,1)
    s+=v
    #c.errors.append(error)

    # get str diversity
    v=diversity_eval(samples_quant_eval)
    s+=get_str_with_tabs("diversity",v,3)
    #c.diversities.append(v)
    


    

    #print("n general generated samples",len(samples_quant_eval))
    

    #stats=get_stats(c,samples_gen)
    #save_stats_str(c,stats)
    #save_text(c.results_folder+"/stats.txt",s)
    #print(s)
    
    '''

    return samples_gen


## layout process

import numpy as np
import random 

class BBox():
    def __init__(self):
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.w=0
        self.h=0

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        get overlap + exceeding
#------------------------------------------------------------------------------------------------------------------------------------

# layout process
def rasterize_sample(sample,w,h,option_color):
    if h==None:h=600
    if w==None:w=300
    npa_bg=get_npa_bg3(h,w,option_color)
    n=len(sample.assets)
    for i_asset in range(n):
        asset=sample.assets[i_asset]
        if option_color==1:r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
        if option_color==2:r=g=b=int(255/(n-i_asset))
        npa_bg=add_shape2(npa_bg,asset.top,asset.left,asset.low,asset.right,r,g,b)
    npa_bg=resize_image(npa_bg,100)
    return npa_bg

def get_npas_show(samples_gen,w,h,start,end):
    npas=[]
    for i_sample in range(start,end): #[0] #range(5):
        npa=show_synth_sample2(samples_gen[i_sample],"npa",h,w)
        npas.append(npa)
    return npas

## eval layouts overlap

def get_layouts_overlap_scores(bbox_samples,w,h,option):
    # bbox : top,left,low,right
    scores=[]
    for i_sample in range(len(bbox_samples)):
        bboxes=bbox_samples[i_sample]
        scores.append(get_layout_overlap_score(bboxes,w,h))
    return scores

def get_layouts_overlap_score(bbox_samples,w,h,option):
    # bbox : top,left,low,right
    area_samples=0
    for i_sample in range(len(bbox_samples)):
        bboxes=bbox_samples[i_sample]
        if option=="" or option=="nested == overlap":area_samples+=get_layout_overlap_score(bboxes,w,h)
        if option=="nested != overlap":area_samples+=get_layout_overlap_score_except_nested(bboxes,w,h)
    return area_samples/len(bbox_samples)

def get_layout_overlap_score(bboxes,w,h):
    area_sample=0
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            if i<j:
                bb_i=get_bbox_obj_from_npa1(bboxes[i])
                bb_j=get_bbox_obj_from_npa1(bboxes[j])
                area_sample+=get_intersection_area(bb_i,bb_j)
    return area_sample/w/h

def get_layout_overlap_score_except_nested(bboxes,w,h):
    area_sample=0
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            if i<j:
                bb_i=get_bbox_obj_from_npa1(bboxes[i])
                bb_j=get_bbox_obj_from_npa1(bboxes[j])
                intersection_area=get_intersection_area(bb_i,bb_j)
                area_i=get_bbox_area(bboxes[i],w,h)
                area_j=get_bbox_area(bboxes[j],w,h)
                if 0 < intersection_area/w/h < min(area_i,area_j):
                    area_sample+=intersection_area
    return area_sample/w/h

def get_intersection_area(ba,bb):
    # dw = min(rights) - max(lefts)
    # dh = min(lows) - max(tops)
    dw = min(ba.x2,bb.x2) - max(ba.x1,bb.x1)
    dh = min(ba.y2,bb.y2) - max(ba.y1,bb.y1)
    area = 0
    if dw > 0 and dh > 0 : 
        area = dw * dh
    return area

def get_layouts_exceeding_score(bbox_samples,w,h):
    # input : top,left,low,right
    area_samples=0
    for i_sample in range(len(bbox_samples)):
        bboxes=bbox_samples[i_sample]
        area_samples+=get_layout_exceeding_score(bboxes,w,h)
    return area_samples/len(bbox_samples)

def get_layout_exceeding_score(bboxes,w,h):
    area_sample=0
    bg=get_bbox_obj_from_npa1([0,0,h,w])
    for i in range(len(bboxes)):
        bb=get_bbox_obj_from_npa1(bboxes[i])
        area_bboxes = bb.w * bb.h - get_intersection_area(bb,bg)
        area_sample+=area_bboxes
    return area_sample/w/h

def get_bbox_area(bbox,w,h):
    # bbox : top,left,low,right
    [top,left,low,right]=bbox
    return (low-top)*(right-left)/h/w

## eval layouts diversity

def get_layouts_diversity_score_for_all_elements_numbers2(bbox_layouts,w,h,n_min,n_max):
    # n_min : minimum number of elements per layouts
    # n_max : maximum number of elements per layouts
    scores=[]
    for n in range(n_min,n_max+1):
        bbox_layouts_temp=[]
        for bboxes in bbox_layouts:
            if len(bboxes)==n:
                bbox_layouts_temp.append(bboxes)
        score=get_layouts_diversity_score(bbox_layouts,w,h,n)
        scores.append(score)
    return min(scores)

def get_layouts_diversity_score_for_all_elements_numbers(bboxes_gen,bboxes_real,w,h,n_min,n_max):
    # n_min : minimum number of elements per layouts
    # n_max : maximum number of elements per layouts
    scores=[]
    for n in range(n_min,n_max+1):
        bboxes_gen_ok=[]
        bboxes_real_ok=[]
        for bboxes in bboxes_gen:
            if len(bboxes)==n:
                bboxes_gen_ok.append(bboxes)
        for bboxes in bboxes_real:
            if len(bboxes)==n:
                bboxes_real_ok.append(bboxes)
        mn=min(len(bboxes_gen_ok),len(bboxes_real_ok))
        if mn>0:
            score=get_layouts_diversity_ratio(bboxes_gen_ok,bboxes_real_ok,w,h,n)
            scores.append(score)
    return max(scores)

def get_layouts_diversity_ratio(bboxes_gen,bboxes_real,w,h,n_bboxes):
    std_dev_gen=get_layouts_diversity_features(bboxes_gen,w,h,n_bboxes)
    std_dev_real=get_layouts_diversity_features(bboxes_real,w,h,n_bboxes)
    n_features=4
    ratios=[]
    for i_bbox in range(n_bboxes):
        for i_feature in range(n_features):
            ratio=get_score_ratio(std_dev_gen[i_bbox][i_feature],std_dev_real[i_bbox][i_feature])
            ratios.append(ratio)
    return np.max(np.asarray(ratios))

def get_layouts_diversity_ratio2(bboxes_real,bboxes_gen,w,h,nareal,nagen):
    std_dev_real=get_layouts_diversity_features(bboxes_real,w,h,nareal)
    std_dev_gen=get_layouts_diversity_features(bboxes_gen,w,h,nagen)

    option="min"
    if option=="min":
        score_real=np.min(std_dev_real)
        score_gen=np.min(std_dev_gen)

    if option=="max":
        print("ok")
        score_real=np.max(std_dev_real)
        score_gen=np.max(std_dev_gen)
    if option=="mean":
        score_real=np.average(std_dev_real)
        score_gen=np.average(std_dev_gen)
        #print("ok",std_dev_real,score_real)


    score_comp=get_score_ratio(score_real,score_gen)

    '''
    n_features=4
    ratios=[]
    for i_bbox in range(n_bboxes):
        for i_feature in range(n_features):
            ratio=get_score_ratio(std_dev_gen[i_bbox][i_feature],std_dev_real[i_bbox][i_feature])
            ratios.append(ratio)
    return np.max(std_dev_real),np.max(std_dev_gen),np.max(np.asarray(ratios))
    '''

    return score_real,score_gen,score_comp



## eval layouts alignment

def get_layouts_with_extreme_scores(scores,bbox_samples,w_ref,start,end):
    #indexes=get_indexes(scores,indexes,)

    print("n sub",end-start)
    print("n samples",len(bbox_samples))
    print("n scores",len(scores))
    npa=np.zeros((len(bbox_samples),2))
    npa[:,0]=np.arange(0,len(bbox_samples))
    npa[:,1]=np.asarray(scores)
    sorted_npa = npa[numpy.argsort(npa[:, 1])]
    sorted_npa = sorted_npa[start:end]
    indexes=sorted_npa.astype(int)[:,0]
    scores=sorted_npa.astype(float)[:,1]
    samples_new=[]
    for i in indexes:
        samples_new.append(bbox_samples[i])
    return samples_new,indexes,scores

def get_scores_alignment_a16(bbox_samples,w_ref):
    # input bboxes : top,left,low,right
    k=0
    scores=[]
    for bbox_sample in bbox_samples:
        bboxes=bbox_sample
        k+=1
        score=get_layout_alignment_score_a16(bboxes,w_ref)#,mn,mx)
        if score != None:
            scores.append(score)
    return scores

def get_layouts_alignment_score_a16(bbox_samples,w_ref):#,mn,mx):
    scores=get_scores_alignment_a16(bbox_samples,w_ref)
    score=1/len(bbox_samples)*sum(scores)
    return score

def get_layout_alignment_score_a16(bboxes,w_ref):#,mn,mx):
    factor = w_ref
    n=len(bboxes)
    mns_layout=[]
    for i in range(n):
        leftA=bboxes[i][1]
        rightA=bboxes[i][3]
        centerA=(leftA-rightA)/2
        mns_elem=[]
        for j in range(n):
            if i!=j:
                leftB=bboxes[j][1]
                rightB=bboxes[j][3]
                centerB=(leftB-rightB)/2
                left=abs(leftA-leftB)
                right=abs(rightA-rightB)
                center=abs(leftA-centerB)
                mns_elem.append(min(left,right,center))
        if len(mns_elem)>0:
            v=min(mns_elem)
            v=v/factor
            mns_layout.append(v)
    option=1
    score=None
    if option==0:
        if len(mns_layout)>0:
            score=min(mns_layout)
    if option==1:
        score=sum(mns_layout)#/len(bboxes)
    return score

def get_comparative_score(score_gen,score_real):
    v=(score_gen+1e-10)/(score_real+1e-10)
    v=abs(np.log(v))
    #v=abs(v)
    return v

def get_score_ratio2(score_gen,score_real,option):
    option = 1
    if option==0:
        v=(score_gen+1e-10)/(score_real+1e-10)
        v=abs(np.log(v))
    if option==0:
        v=(score_gen+1e-10)/(score_real+1e-10)
        v=abs(np.log2(v))
    if option==0:
        v=(score_gen+1e-10)/(score_real+1e-10)
        v=abs(np.log10(v))
    if option==0:
        mx=max(score_gen,score_real)    
        if mx==0:v=0
        if mx!=0:v=abs(score_gen-score_real)/mx#np.power(mx,2)
    if option==0:
        v=np.exp(score_gen)/np.exp(score_real)
    if option==0:
        if score_gen==score_real:return 0
        if score!=score_real:
            if score_real==0:return np.exp(score_gen)-1
            if score_real!=0:return score_gen/score_real
    if option==0:
        v=np.exp(score_gen)/np.power(mx,factor)
    return v

def get_layouts_diversity_features(bbox_layouts,w,h,n_bboxes):
    npa=np.asarray(bbox_layouts)
    std_devs=[]
    for i_bbox in range(n_bboxes):
        tops=npa[:,i_bbox,0]
        lefts=npa[:,i_bbox,1]
        heights=npa[:,i_bbox,2]-npa[:,i_bbox,0]
        widths=npa[:,i_bbox,3]-npa[:,i_bbox,1]
        std_tops=np.std(tops/h)
        std_lefts=np.std(tops/w)
        std_heights=np.std(tops/h)
        std_widths=np.std(tops/w)
        std_devs.append([std_tops,std_lefts,std_heights,std_widths])
    return std_devs
    
#'''
def get_layouts_diversity_score(bbox_layouts,w,h,n_bboxes):
    std_dev=get_layouts_diversity_features(bbox_layouts,w,h,n_bboxes)
    #return np.average(np.asarray(std_devs))
    #return np.min(np.asarray(std_devs))
    print("ok")
    return np.average(np.asarray(std_devs))
#'''

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        object samples <=> model inputs
#------------------------------------------------------------------------------------------------------------------------------------

def vectorize_sample(sample):
    n_features=5
    n_assets=3
    npa=np.zeros(n_assets*n_features)
    i=0
    for asset in sample.assets:
        npa[i+0]=get_num_cat(asset.type)
        npa[i+1]=asset.width
        npa[i+2]=asset.height
        npa[i+3]=asset.left
        npa[i+4]=asset.top
        i+=5
    return npa

def preprocess(x,y,max_delta):
    #x=x.reshape((len(x),6))
    x,y=normalize_xy(x,y,max_delta)
    x=x.reshape((len(x),9))
    y=y.reshape((len(y),9))
    return x,y

def normalize_xy(x,y,max_delta):
    max_cat=3
    x_norm=np.zeros(np.shape(x),dtype=float)
    y_norm=np.zeros(np.shape(y),dtype=float)
    w_screen,h_screen=300,600
    n_samples=len(x)
    n_assets=len(x[0])
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            prev=x[i_sample,i_asset,0]
            
            x_norm[i_sample,i_asset,0]=x[i_sample,i_asset,0]/w_screen/max_delta     # input width
            x_norm[i_sample,i_asset,1]=x[i_sample,i_asset,1]/h_screen/max_delta     # input height
            x_norm[i_sample,i_asset,2]=x[i_sample,i_asset,2]/max_cat                # input cat
            
            y_norm[i_sample,i_asset,0]=y[i_sample,i_asset,0]/w_screen               # output width
            y_norm[i_sample,i_asset,1]=y[i_sample,i_asset,1]/w_screen               # output left
            y_norm[i_sample,i_asset,2]=y[i_sample,i_asset,2]/h_screen               # output top
    return x_norm,y_norm

def get_num_cat(tp_str):
    tp=None
    if tp_str=="red":tp=0
    if tp_str=="green":tp=1
    if tp_str=="blue":tp=2
    if tp_str=="text":tp= 0
    if tp_str=="image":tp= 1
    if tp_str=="logo":tp= 2
    if tp_str=="cta":tp= 3

    if tp==None:print("tag3",tp_str,tp)

    return tp

# real samples => xy
def get_xy_from_samples(samples):
    n_samples=len(samples)
    n_assets=len(samples[0].assets)
    x=np.zeros((n_samples,n_assets,3),dtype=int)
    y=np.zeros((n_samples,n_assets,3),dtype=int)
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            asset=samples[i_sample].assets[i_asset]
            x[i_sample,i_asset,0]=asset.input_width
            x[i_sample,i_asset,1]=asset.input_height
            x[i_sample,i_asset,2]=get_num_cat(asset.type)
            y[i_sample,i_asset,0]=asset.width
            y[i_sample,i_asset,1]=asset.left
            y[i_sample,i_asset,2]=asset.top
    return x,y

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        model outputs <=> object samples
#------------------------------------------------------------------------------------------------------------------------------------

def devectorize_sample(npa):
    n_features=5
    n_assets=3
    n=len(npa)
    i=0
    sample=Clay()
    sample.assets=[]
    for i_assets in range(n_assets):
        asset=Clay()
        asset.type=get_str_cat(int(np.round(npa[i+0])),option_dataset)
        asset.width=npa[i+1]
        asset.height=npa[i+2]
        asset.left=npa[i+3]
        asset.top=npa[i+4]
        asset.right=asset.left+asset.width
        asset.low=asset.top+asset.height
        sample.assets.append(asset)
        i+=5
    return sample

def postprocess(x,y,max_delta):
    #x=x.reshape((len(x_test),3,2))
    x=x.reshape((len(x_test),3,3))
    y=y.reshape((len(y_test),3,3))
    x,y=denormalize_xy(x,y,max_delta)
    return x,y

def denormalize_xy(x,y,max_delta):
    max_cat=3
    x_denorm=np.zeros(np.shape(x),dtype=int)
    y_denorm=np.zeros(np.shape(y),dtype=int)
    w_screen,h_screen=300,600
    n_samples=len(x)
    n_assets=len(x[0])
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            x_denorm[i_sample,i_asset,0]=x[i_sample,i_asset,0]*w_screen*max_delta     # input width
            x_denorm[i_sample,i_asset,1]=x[i_sample,i_asset,1]*h_screen*max_delta     # input height
            x_denorm[i_sample,i_asset,2]=x[i_sample,i_asset,2]*max_cat                # input cat
            y_denorm[i_sample,i_asset,0]=y[i_sample,i_asset,0]*w_screen               # output width
            y_denorm[i_sample,i_asset,1]=y[i_sample,i_asset,1]*w_screen               # output left
            y_denorm[i_sample,i_asset,2]=y[i_sample,i_asset,2]*h_screen               # output top
    return x_denorm,y_denorm

def get_str_cat(tp,option_dataset):

    tp_str=None
    if option_dataset==1:
        if tp==0:tp_str= "red"
        if tp==1:tp_str= "green"
        if tp==2:tp_str= "blue"

    if option_dataset>1:
        if tp==0:tp_str= "text"
        if tp==1:tp_str= "image"
        if tp==2:tp_str= "logo"
        if tp==3:tp_str= "cta"



    return tp_str

# xy => samples
def get_samples_from_xy(x,y,names,option_dataset):
    n_samples=len(x)
    n_assets=len(x[0])
    samples=[]
    for i_sample in range(n_samples):
        sample=Clay()
        if len(names)>0:sample.name = names[i_sample]
        sample.assets=[]
        for i_asset in range(n_assets):
            asset=Clay()
            asset.input_width=int(x[i_sample,i_asset,0])
            asset.input_height=int(x[i_sample,i_asset,1])
            asset.type=get_str_cat(x[i_sample,i_asset,2],option_dataset)
            asset.width=int(y[i_sample,i_asset,0])
            asset.left=int(y[i_sample,i_asset,1])
            asset.top=int(y[i_sample,i_asset,2])
            asset.height=int(asset.input_height/asset.input_width*asset.width)
            asset.right=int(asset.left+asset.width)
            asset.low=int(asset.top+asset.height)
            sample.assets.append(asset)
        samples.append(sample)
    return samples

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        archived samples <=> object samples
#------------------------------------------------------------------------------------------------------------------------------------

# coordinates => samples
def get_samples_from_coordinates(coordinates,option_dataset):
    samples=[]
    n_samples=np.shape(coordinates)[0]
    n_assets=np.shape(coordinates)[1]
    for i_sample in range(n_samples):
        sample = Clay()
        sample.assets=[]
        for i_asset in range(n_assets):
            asset=Clay()
            asset.input_width=coordinates[i_sample,i_asset,0]
            asset.input_height=coordinates[i_sample,i_asset,1]
            asset.width=coordinates[i_sample,i_asset,2]
            asset.height=coordinates[i_sample,i_asset,3]
            asset.left=coordinates[i_sample,i_asset,4]
            asset.top=coordinates[i_sample,i_asset,5]
            asset.type=get_str_cat(coordinates[i_sample,i_asset,6],option_dataset)
            asset.right=asset.left+asset.width
            asset.low=asset.top+asset.height
            sample.assets.append(asset)
        samples.append(sample)
    return samples

# samples => coordinates
def get_coordinates_from_samples(samples):
    n_samples=len(samples)
    n_assets=len(samples[0].assets)
    n_features=7
    coordinates = np.zeros((n_samples,n_assets,n_features),dtype=np.int64)
    for i_sample in range(n_samples):
        sample = samples[i_sample]
        for i_asset in range(n_assets):
            asset=sample.assets[i_asset]
            coordinates[i_sample,i_asset,0]=asset.input_width
            coordinates[i_sample,i_asset,1]=asset.input_height
            coordinates[i_sample,i_asset,2]=asset.width
            coordinates[i_sample,i_asset,3]=asset.height
            coordinates[i_sample,i_asset,4]=asset.left
            coordinates[i_sample,i_asset,5]=asset.top
            coordinates[i_sample,i_asset,6]=get_num_cat(asset.type)
            #coordinates[i_sample,i_asset,6]=get_num_cat(asset.type)
    return coordinates

def get_samples_from_text_file(option_exclude_mentions):
    file_path='/home/paintedpalms/rdrive/taff/data/automated_layout_real/pubs_madmix/segm3/segm.txt'
    file = open(file_path,"r")
    text = file.read()
    file.close()    
    lines = text.split('\n')
    names=[]
    samples=[]
    for line in lines:
        line = line[:-1]
        line_chunks=line.split(" ")
        sample = Clay()
        sample.name=line_chunks[0]
        sample.assets=[]
        i=1
        while i < len(line_chunks):        
            assets_chunks=line_chunks[i:i+5]
            asset=Clay()
            asset.type=assets_chunks[0]
            if option_exclude_mentions==0 or asset.type!="mentions":
                asset.left=int(assets_chunks[1])
                asset.top=int(assets_chunks[2])
                asset.right=int(assets_chunks[3])
                asset.low=int(assets_chunks[4])
                asset.width=asset.right-asset.left
                asset.height=asset.low-asset.top
                sample.assets.append(asset)
            i+=5
        samples.append(sample)
    return samples

def write_pl(file_path,pl):
    text=""
    for v in pl:text+=str(v)+'\n'
    fs = open(file_path,"w")
    fs.write(text)
    fs.close()

def read_pl(file_path):
    file = open(file_path,"r")
    text = file.read()
    file.close()    
    lines = text.split('\n')
    pl=[]
    for line in lines:
        pl.append(line)
    return pl

def get_names():
    names_path="/home/paintedpalms/rdrive/taff/data/automated_layout_real/pubs_madmix/segm3/names.txt"
    names=read_pl(names_path)
    return names
    
def save_names(samples):
    names=[]
    for sample in samples:names.append(sample.name)
    write_pl("names.txt",names)

#------------------------------------------------------------------------------------------------------------------------------------
#                                              modify object samples
#------------------------------------------------------------------------------------------------------------------------------------

def select_real_samples(samples):
    n_assets_valid=3
    valid_samples=[]
    for sample in samples:
        sample_is_valid=True
        if len(sample.assets)!=n_assets_valid:sample_is_valid=False
        for asset in sample.assets:
            if asset.type=='mentions':
                sample_is_valid=False
        if sample_is_valid:
            valid_samples.append(sample)
    return valid_samples

def add_input_dimensions(sample,delta_random_max):
    delta_random_min=1/delta_random_max
    for asset in sample.assets:
        delta=delta_random_min+(delta_random_max-delta_random_min)*random.random()
        asset.input_width=int(asset.width*delta)
        asset.input_height=int(asset.height*delta)
    return sample


# bbox obj # bbox npa
def get_bbox_obj_from_npa1(npa):
    # input npa : top,left,low,right
    bb=BBox()
    bb.y1=npa[0]
    bb.x1=npa[1]
    bb.y2=npa[2]
    bb.x2=npa[3]
    bb.h=bb.y2-bb.y1
    bb.w=bb.x2-bb.x1
    return bb

def get_bbox_npa_from_obj(bb):
    npa=np.zeros(4,dtype=int)
    bb.y1=npa[0]=bb.y1
    bb.x1=npa[1]=bb.x1
    bb.y2=npa[2]=bb.y2
    bb.x2=npa[3]=bb.x2
    return npa

#---------------------------------------------------------------------------------------------------------------------------
#                                              y_gan <=> bboxes
#---------------------------------------------------------------------------------------------------------------------------

'''def get_bbox_samples_for_alignment_a16(npa,option):'''

def get_nb_of_assets(preal):
    npa=np.load(preal)
    return len(npa[0])

def get_bboxes_from_y_gan2(npa,option):

    # input bbox : w,h,left,top(,tp)
    # output bbox : top,left,low,right
    bbox_samples=[]
    if option=="y_gan":
        y_gan=npa
        n_samples=len(y_gan)
        n_assets=len(y_gan[0])
        #n_assets=3
        for i_sample in range(n_samples):
            bboxes=[]
            for i_asset in range(n_assets):
                w=y_gan[i_sample,i_asset,0]
                h=y_gan[i_sample,i_asset,1]
                left=y_gan[i_sample,i_asset,2]
                top=y_gan[i_sample,i_asset,3]
                low=top+h
                right=left+w
                bboxes.append([top,left,low,right])
            bbox_samples.append(bboxes)
    return bbox_samples

def get_bboxes_from_y_gan(npa,option):
    # input bbox : w,h,left,top(,tp)
    # output bbox : top,left,low,right
    bbox_samples=[]
    if option=="y_gan":
        y_gan=npa
        n_samples=len(y_gan)
        n_assets=3
        for i_sample in range(n_samples):
            bboxes=[]
            for i_asset in range(n_assets):
                w=y_gan[i_sample,i_asset,0]
                h=y_gan[i_sample,i_asset,1]
                left=y_gan[i_sample,i_asset,2]
                top=y_gan[i_sample,i_asset,3]
                low=top+h
                right=left+w
                bboxes.append([top,left,low,right])
            bbox_samples.append(bboxes)
    return bbox_samples

def get_y_gan_from_bboxes(bbox_samples,option):
    n_samples = len(bbox_samples)
    n_assets=3
    npa=np.zeros((n_samples,n_assets,5))
    if option=="y_gan":
        y_gan=npa
        n_samples=len(y_gan)
        for i_sample in range(n_samples):
            bboxes=bbox_samples[i_sample]
            if len(bboxes)==n_assets or 1==1:
                for i_asset in range(len(bboxes)):
                    top=bboxes[i_asset][0]
                    left=bboxes[i_asset][1]
                    low=bboxes[i_asset][2]
                    right=bboxes[i_asset][3]
                    h=low-top
                    w=right-left
                    y_gan[i_sample,i_asset,0]=w
                    y_gan[i_sample,i_asset,1]=h
                    y_gan[i_sample,i_asset,2]=left
                    y_gan[i_sample,i_asset,3]=top
    return npa

def get_y_gan_from_bboxes2(bbox_samples,option,n_assets):
    n_samples = len(bbox_samples)
    npa=np.zeros((n_samples,n_assets,5))
    if option=="y_gan":
        y_gan=npa
        n_samples=len(y_gan)
        for i_sample in range(n_samples):
            bboxes=bbox_samples[i_sample]
            if len(bboxes)<=n_assets:
                for i_asset in range(len(bboxes)):
                    top=bboxes[i_asset][0]
                    left=bboxes[i_asset][1]
                    low=bboxes[i_asset][2]
                    right=bboxes[i_asset][3]
                    h=low-top
                    w=right-left
                    y_gan[i_sample,i_asset,0]=w
                    y_gan[i_sample,i_asset,1]=h
                    y_gan[i_sample,i_asset,2]=left
                    y_gan[i_sample,i_asset,3]=top
    return npa

def sort_assets_by_size(samples):
    samples_new=[]
    for s in samples:
        s_new=copy.deepcopy(s)
        assets=copy.deepcopy(s.assets)
        ok=0
        while ok==0:
            ok=1
            for i in range(len(assets)-1):
                a1=assets[i]
                a2=assets[i+1]
                if a1.width*a1.height<a2.width*a2.height:
                    ok=0
                    assets[i]=a2
                    assets[i+1]=a1
        s_new.assets=assets
        samples_new.append(s_new)
    return samples_new

## pending

def get_images_from_layouts(samples,w,h,n,option_color):
    return get_images_from_layout_samples(samples,w,h,n,option_color)

def get_images_from_layout_samples(samples,w,h,n,option_color):
    # n=10 : nb of samples to turn into images
    # rico : w,h=1440,2560 : width, height
    # synth : w,h=300,600 : width, height

    samples=sort_assets_by_size(samples)
    n=min(len(samples),n)
    new_w=100
    new_h=int(h/w*new_w)
    images=np.zeros((n,new_h,new_w,3),dtype=np.uint8)
    for i in range(n):
        npa=rasterize_sample(samples[i],w,h,option_color)
        images[i]=npa[:,:,:3]
    return images

'''
def get_images_from_layouts(samples,w,h,n,option_color):
    # n=10 : nb of samples to turn into images
    # w,h=1440,2560 : width, height
    # w,h=300,600 : width, height
    n=min(len(samples),n)
    new_w=100
    new_h=int(h/w*new_w)
    images=np.zeros((n,new_h,new_w,3),dtype=np.uint8)
    for i in range(n):
        npa=rasterize_sample(samples[i],w,h,option_color)
        images[i]=npa[:,:,:3]
    return images
'''

def filter_n_assets(bbox_samples,n):
    new_samples=[]
    for bboxes in bbox_samples:
        if len(bboxes)==3:new_samples.append(bboxes)
    return new_samples

def get_max_wh(boxes):
    # boxes : top,left,low,right,tp
    mxw,mxh=0,0
    for box in boxes:
        h=box[2]-box[0]
        w=box[3]-box[1]
        mxw=max(mxw,w)
        mxh=max(mxh,h)
    return mxw,mxh

def get_rico_stats(bbox_samples):
    w,h=1440,2560
    values=np.zeros((len(bbox_samples),4))
    i=-1
    for bboxes in bbox_samples:
        i+=1
        score_overlap=get_layout_overlap_score(bboxes)
        score_exceed=get_layout_exceeding_score(bboxes,w,h)
        mxw,mxh=get_max_wh(bboxes)
        values[i,0]=score_overlap
        values[i,1]=score_exceed
        values[i,2]=mxw
        values[i,3]=mxh
    return values

# remove samples : overlap
def clean_rico_overlap(bbox_samples):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        score_overlap=get_layout_overlap_score(bboxes)
        if score_overlap==0:
            new_samples.append(bboxes)
    return new_samples

# remove elems : overlap
def clean_rico_overlap_elems(bbox_samples):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        n=len(bboxes)
        n_new=-1
        while n_new!=n:
            n=len(bboxes)
            bboxes=remove_bbox_with_biggest_overlaps(bboxes)
            n_new=len(bboxes)
        new_samples.append(bboxes)
    return new_samples

def remove_bbox_with_biggest_overlaps(bboxes):
    mx=0
    i_mx=-1
    for i in range(len(bboxes)):
        area_elem=0
        for j in range(len(bboxes)):
            if i!=j:
                bb_i=get_bbox_obj_from_npa1(bboxes[i])
                bb_j=get_bbox_obj_from_npa1(bboxes[j])
                area_elem+=get_intersection_area(bb_i,bb_j)
        if area_elem>mx:
            i_mx=i
            mx=area_elem
    new_bboxes=[]
    for i in range(len(bboxes)):
        if i!=i_mx:
            new_bboxes.append(bboxes[i])
    return new_bboxes


def clean_rico_area_min_elems(bbox_samples,alpha):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        new_bboxes=[]
        for bbox in bboxes:
            h_bbox=bbox[2]-bbox[0]
            w_bbox=bbox[3]-bbox[1]
            if h_bbox*w_bbox>=alpha*h*w:
                new_bboxes.append(bbox)
        new_samples.append(new_bboxes)
    return new_samples


def clean_rico_area_max_elems(bbox_samples,alpha):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        new_bboxes=[]
        for bbox in bboxes:
            h_bbox=bbox[2]-bbox[0]
            w_bbox=bbox[3]-bbox[1]
            if h_bbox*w_bbox<=alpha*h*w:
                new_bboxes.append(bbox)
        new_samples.append(new_bboxes)
    return new_samples

def clean_rico_exceed(bbox_samples):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        score_exceed=get_sample_exceeding_score(bboxes,w,h)
        if score_exceed==0:
            new_samples.append(bboxes)
    return new_samples

# remove layouts with less than n elems
def clean_rico_n_min(bbox_samples,n_min):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        if len(bboxes)>=n_min:
            new_samples.append(bboxes)
    return new_samples

# remove layouts with more than n elems
def clean_rico_n_max(bbox_samples,n_max):
    w,h=1440,2560
    new_samples=[]
    for bboxes in bbox_samples:
        if len(bboxes)<=n_max:
            new_samples.append(bboxes)
    return new_samples

#------------------------------------------------------------------------------------------------------------------------------------
#                                              # xy synth <=> y_gan
#------------------------------------------------------------------------------------------------------------------------------------

## data
## process

# get y_gan from xy (synth 2)
def get_y_gan_from_xy(x,y):
    n_samples=len(x)
    n_assets=len(x[0])
    y_gan=np.zeros((n_samples,n_assets,5))
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            
            input_width=int(x[i_sample,i_asset,0])
            input_height=int(x[i_sample,i_asset,1])
            tp=x[i_sample,i_asset,2]
            width=int(y[i_sample,i_asset,0])
            left=int(y[i_sample,i_asset,1])
            top=int(y[i_sample,i_asset,2])
            height=int(input_height/input_width*width)
                             
            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            y_gan[i_sample,i_asset,4]=tp
            
    return y_gan

# get y_gan from xy (synth 1)
def get_y_gan_from_xy1(x,y,deltas):
    n_samples=len(x)
    n_assets=3
    y_gan=np.zeros((n_samples,n_assets,5))
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):

            # input width + input height
            input_width=int(np.round(x[i_sample,3+5*i_asset]))
            input_height=int(np.round(x[i_sample,2+5*i_asset]))

            # type
            if x[i_sample,4+5*i_asset]==1:tp=0
            if x[i_sample,5+5*i_asset]==1:tp=1
            if x[i_sample,6+5*i_asset]==1:tp=2

            # width + height
            delta=deltas[i_sample,i_asset]
            width=int(np.round(input_width/delta))
            height=int(np.round(input_height/delta))

            # left + top
            left=int(np.round(y[i_sample,1+2*i_asset]))
            top=int(np.round(y[i_sample,0+2*i_asset]))
                                
            # y gan
            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            y_gan[i_sample,i_asset,4]=tp
            
    return y_gan

# get sample from y_gan
def get_samples_from_y_gan(y,names,option_dataset):
    n_samples=len(y)
    n_assets=len(y[0])
    samples=[]
    for i_sample in range(n_samples):
        sample=Clay()
        if len(names)>0:sample.name = names[i_sample]
        sample.assets=[]
        for i_asset in range(n_assets):
            asset=Clay()
            asset.width=int(np.round(y[i_sample,i_asset,0]))
            asset.height=int(np.round(y[i_sample,i_asset,1]))
            asset.left=int(np.round(y[i_sample,i_asset,2]))
            asset.top=int(np.round(y[i_sample,i_asset,3]))
            v=int(np.round((y[i_sample,i_asset,4])))
            asset.type=get_str_cat(v,option_dataset)
            asset.right=int(asset.left+asset.width)
            asset.low=int(asset.top+asset.height)
            sample.assets.append(asset)
        samples.append(sample)
    return samples

# get y_gan from samples
def get_y_gan_from_samples(samples):
    n_samples=len(samples)
    n_assets=3
    y_gan=np.zeros((n_samples,n_assets,5))
    for i_sample in range(n_samples):
        sample=samples[i_sample]
        for i_asset in range(n_assets):
            asset=sample.assets[i_asset]
            y_gan[i_sample,i_asset,0]=asset.width
            y_gan[i_sample,i_asset,1]=asset.height
            y_gan[i_sample,i_asset,2]=asset.left
            y_gan[i_sample,i_asset,3]=asset.top
            y_gan[i_sample,i_asset,4]=get_num_cat(asset.type)
    return y_gan

# get y_gan from samples
def get_y_gan_from_samples2(samples,n_assets):
    n_samples=len(samples)
    y_gan=np.zeros((n_samples,n_assets,5))
    for i_sample in range(n_samples):
        sample=samples[i_sample]
        for i_asset in range(n_assets):
            asset=sample.assets[i_asset]
            y_gan[i_sample,i_asset,0]=asset.width
            y_gan[i_sample,i_asset,1]=asset.height
            y_gan[i_sample,i_asset,2]=asset.left
            y_gan[i_sample,i_asset,3]=asset.top
            y_gan[i_sample,i_asset,4]=0
    return y_gan

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        y_gan normalisation
#------------------------------------------------------------------------------------------------------------------------------------

# normalize (-1,1)
def normalize_y_gan(y_gan,mxw,mxh,n_tp):
    y_gan=copy.deepcopy(y_gan)
    n_samples=y_gan.shape[0]
    n_assets=y_gan.shape[1]
    n_features=y_gan.shape[2]
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
    
            width=y_gan[i_sample,i_asset,0]
            height=y_gan[i_sample,i_asset,1]
            left=y_gan[i_sample,i_asset,2]
            top=y_gan[i_sample,i_asset,3]
            if n_features>=5:tp=y_gan[i_sample,i_asset,4]

            width=width/mxw*2-1
            height=height/mxh*2-1
            top=top/mxh*2-1
            left=left/mxw*2-1
            if n_features>=5:tp=tp/(n_tp-1)*2-1

            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            if n_features>=5:y_gan[i_sample,i_asset,4]=tp

    return y_gan
        
# normalize (0,1)
def normalize2_y_gan(y_gan,mxw,mxh,n_tp):

    n_samples=y_gan.shape[0]
    n_assets=y_gan.shape[1]
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
    
            width=y_gan[i_sample,i_asset,0]
            height=y_gan[i_sample,i_asset,1]
            left=y_gan[i_sample,i_asset,2]
            top=y_gan[i_sample,i_asset,3]
            tp=y_gan[i_sample,i_asset,4]

            width=width/mxw
            height=height/mxh
            top=top/mxh
            left=left/mxw
            tp=tp/(n_tp-1)

            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            y_gan[i_sample,i_asset,4]=tp

    return y_gan

# denormalize (0,1)
def denormalize2_y_gan(y_gan,mxw,mxh,n_tp):
    
    n_samples=y_gan.shape[0]
    n_assets=y_gan.shape[1]
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            
            width=y_gan[i_sample,i_asset,0]
            height=y_gan[i_sample,i_asset,1]
            left=y_gan[i_sample,i_asset,2]
            top=y_gan[i_sample,i_asset,3]
            tp=y_gan[i_sample,i_asset,4]

            width=int(np.round(width*mxw))
            left=int(np.round(left*mxw))
            height=int(np.round(height*mxh))
            top=int(np.round(top*mxh))
            tp=int(np.round(tp*(n_tp-1)))

            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            y_gan[i_sample,i_asset,4]=tp

    return y_gan


# denormalize (-1,1)
def denormalize_y_gan(y_gan,mxw,mxh,n_tp):
    
    n_samples=y_gan.shape[0]
    n_assets=y_gan.shape[1]
    for i_sample in range(n_samples):
        for i_asset in range(n_assets):
            
            width=y_gan[i_sample,i_asset,0]
            height=y_gan[i_sample,i_asset,1]
            left=y_gan[i_sample,i_asset,2]
            top=y_gan[i_sample,i_asset,3]
            tp=y_gan[i_sample,i_asset,4]

            width=int(np.round((width+1)/2*mxw))
            left=int(np.round((left+1)/2*mxw))
            height=int(np.round((height+1)/2*mxh))
            top=int(np.round((top+1)/2*mxh))
            tp=int(np.round((tp+1)/2*(n_tp-1)))

            y_gan[i_sample,i_asset,0]=width
            y_gan[i_sample,i_asset,1]=height
            y_gan[i_sample,i_asset,2]=left
            y_gan[i_sample,i_asset,3]=top
            y_gan[i_sample,i_asset,4]=tp

    return y_gan



if 0==1:
    p="/home/paintedpalms/rdrive/taff/jpnb/layout_gan_fall_2020/y_gan.npy"
    y_gan=np.load(p)
    y_gan=normalize_y_gan(y_gan,300,600,4)
    
    print(np.max(y_gan))
    print(np.min(y_gan))
    print("")
    
    y_gan=denormalize_y_gan(y_gan,300,600,4)
    
    print(np.max(y_gan))
    print(np.min(y_gan))
    print("")


## data

def one_hot(npa,mx):
    n=len(npa)
    npa_new=np.zeros((n,mx+1),dtype=str(npa.dtype))
    for i_sample in range(n):
        v=npa[i_sample,0]
        npa_new[i_sample,v]=1
    return npa_new

def reverse_one_hot(npa):
    n=len(npa)
    n_values=len(npa[0])
    npa_new=np.zeros((n,1),dtype=str(npa.dtype))
    for i_sample in range(n):
        for i_value in range(n_values):
            if npa[i_sample,i_value]==1:
                npa_new[i_sample]=i_value
    return npa_new

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        # imports
#------------------------------------------------------------------------------------------------------------------------------------

from tensorflow.keras.datasets import cifar10, mnist
import torch
from torchvision import transforms
import torch.nn.functional as F
import pickle
from scipy.spatial.distance import cdist
import numpy as np
from PIL import Image

if 1==0:
    
    train_loader = load_data_gt8(dataset) # origin


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        # rico dataset
#------------------------------------------------------------------------------------------------------------------------------------

# private imports

import sys
from importlib import reload
p_git1="/home/paintedpalms/rdrive/taff/code/git/gcn-cnn"
sys.path.insert(0,p_git1)

import init_paths
from dataloaders.dataloader_test import *
from dataloaders.dataloader_test import RICO_ComponentDataset

import models
import opts_dml
import os 

from BoundingBox import BoundingBox
from BoundingBoxes import BoundingBoxes

from utils import mkdir_if_missing, load_checkpoint
from eval_metrics.get_overall_Classwise_IOU import get_overall_Classwise_IOU
from eval_metrics.get_overall_pix_acc import get_overall_pix_acc

import sys
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageDraw

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        magazine dataset
#------------------------------------------------------------------------------------------------------------------------------------

# create bbox visual representation
def get_npa_mag(p):
    # p = path to xml file
    tree = ET.parse(p)
    root = tree.getroot()
    #h_screen,w_screen=300,225
    h_screen=int(root.findall('size')[0].findall('height')[0].text)
    w_screen=int(root.findall('size')[0].findall('width')[0].text)
    npa=create_grey_bg(h_screen,w_screen)
    for layout in root.findall('layout'):
        for element in layout.findall('element'):
            label = element.get('label')
            px = [int(i) for i in element.get('polygon_x').split(" ")]
            py = [int(i) for i in element.get('polygon_y').split(" ")]
            top,left,low,right=py[0],px[0],py[2],px[2]
            npa=add_shape(npa,top,left,low,right,100,255,100)
    return npa

def get_bboxes_mag(p):
    # p = path to xml file
    tree = ET.parse(p)
    root = tree.getroot()
    bboxes=[]
    #h_screen,w_screen=300,225
    h_screen=int(root.findall('size')[0].findall('height')[0].text)
    w_screen=int(root.findall('size')[0].findall('width')[0].text)
    
    '''
    if h_screen!=300:print("h_screen",h_screen)
    if w_screen!=225:print("w_screen",w_screen)
    '''
    
    ok=1
    c=clay()
    c.labels=[]
    for layout in root.findall('layout'):
        for element in layout.findall('element'):
            label = element.get('label')
            if label not in c.labels:c.labels.append(label)
            
            px,py=[],[]
            for v in element.get('polygon_x').split(" "):
                if "NaN" in v:ok=0    
                if ok==1:
                    v=int(ast.literal_eval(v))
                    px.append(v)
                    
            for v in element.get('polygon_y').split(" "):
                if "NaN" in v:ok=0
                if ok==1:
                    v=int(ast.literal_eval(v))
                    py.append(v)
            
            if ok==1:
                top,left,low,right=py[0],px[0],py[2],px[2]
                bboxes.append([top,left,low,right]) #tag2
                
    return h_screen,w_screen,bboxes,ok

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        rico dataset
#------------------------------------------------------------------------------------------------------------------------------------

if 1==0:

    '''

    ########### RICO DATASET #####################

    imageName: String representing the image name.

    classId: String value representing class id.

    x: Float value representing the X upper-left coordinate of the bounding box.
    y: Float value representing the Y upper-left coordinate of the bounding box.
    w: Float value representing the width bounding box.
    h: Float value representing the height bounding box.

    typeCoordinates: (optional) Enum (Relative or Absolute) represents if the bounding box
    coordinates (x,y,w,h) are absolute or relative to size of the image. Default:'Absolute'.

    imgSize: (optional) 2D vector (width, height)=>(int, int) represents the size of the
    image of the bounding box. If typeCoordinates is 'Relative', imgSize is required.

    bbType: (optional) Enum (Groundtruth or Detection) identifies if the bounding box
    represents a ground truth or a detection. If it is a detection, the classConfidence has
    to be informed.

    classConfidence: (optional) Float value representing the confidence of the detected
    class. If detectionType is Detection, classConfidence needs to be informed.

    format: (optional) Enum (BBFormat.XYWH or BBFormat.XYX2Y2) indicating the format of the
    coordinates of the bounding boxes. BBFormat.XYWH: <left> <top> <width> <height>
    BBFormat.XYX2Y2: <left> <top> <right> <bottom>.

    '''

def show_at(o,name):
    if hasattr(o,name):print(name,getattr(o, name))

def show_ats(o,names):
    for name in names:show_at(o,name)

def getBoundingBoxes_from_info(info_file = p_git1+"/"+'data/rico_box_info.pkl'):
    allBoundingBoxes = BoundingBoxes()
    info = pickle.load(open(info_file, 'rb'))
    #files = glob.glob(data_dir+ "*.json")
    for imageName in info.keys():
        count = info[imageName]['nComponent']
        for i in range(count):
            box = info[imageName]['xywh'][i]
            bb = BoundingBox(
                imageName,
                info[imageName]['componentLabel'][i],
                box[0],
                box[1],
                box[2],
                box[3],
                iconClass=info[imageName]['iconClass'],
                textButtonClass=info[imageName]['textButtonClass'])
            allBoundingBoxes.addBoundingBox(bb)
    #print('Collected {} bounding boxes from {} images'. format(allBoundingBoxes.count(), len(info) ))
    # testBoundingBoxes(allBoundingBoxes)
    return allBoundingBoxes

# modify : get_image_rico
def get_rico_image(layout_name):
    p="/media/paintedpalms/backupRomain/data/rico/unique_uis/combined/"+layout_name+".jpg"
    img=Image.open(p)
    img=resize_image(img,150)
    return img
    
# modify : get_bbox_npa_rico
def get_bbox_npa(bbox_obj):
    option=1
    if option==1:
        tp=bbox_obj.classId
    if option==2:
        tp="text"
        if bbox_obj.classId=="Icon":tp="cta"
        if bbox_obj.classId=="Button":tp="cta"
        if bbox_obj.classId=="Toolbar":tp="cta"
        if bbox_obj.classId=="Image":tp="image"
        if bbox_obj.classId=="Text":tp="text"
    raw_box=[bbox_obj.x,bbox_obj.y,bbox_obj.w,bbox_obj.h,tp]
    return raw_box

if 1==0:
    
    bboxes = getBoundingBoxes_from_info().boundingBoxes



def show_images_rico(layouts):
    layout_names=list(layouts.keys())
    n_max=len(layout_names) 
    for layout_name in layout_names[:n_max]:        
        # show screenshot
        img=get_rico_image(layout_name)
        display(img)

def show_bboxes_rico(samples):
    for sample in samples:
        show_synth_sample(sample,"",2560,1440)

def get_layouts_rico():
    # get layouts
    bboxes = getBoundingBoxes_from_info().boundingBoxes
    n=len(bboxes)
    start=0
    layouts={}
    for i_box in range(start,start+n):
        bx=bboxes[i_box]
        image_name=bx.getImageName()   
        if image_name not in layouts.keys():
            layouts[image_name]=[]
        layouts[image_name].append(bx)
    return layouts

def get_samples_rico(layouts):
    samples=[]
    layout_names=list(layouts.keys())
    n_max=len(layout_names) 
    names=[]
    for layout_name in layout_names[:n_max]:
        # get raw bboxes (with types)
        valid_types=["text","image"]
        valid_types=["Toolbar", "Image", "Text", "Icon", "Button", "Input", "List Item", "Advertisement", "Pager Indicator", "Web View", "Background Image", "Drawer", "Modal"]
        raw_boxes=[]
        k=0
        for bx in layouts[layout_name]:
            if k<10 or 1==0:
                raw_box = get_bbox_npa(bx)
                if raw_box[-1] in valid_types:
                    raw_boxes.append(raw_box)
            k+=1
        if k<10 and len(raw_boxes)>0:
            sample=create_sample_from_boxes2(raw_boxes)
            samples.append(sample)
            names.append(layout_name)
    return samples,names

def get_samples_raw_rico(samples):
    # bbox output : top,left,low,right
    # get bboxes : preproces rico layouts to measure alignment score on it
    samples_raw=[]
    for sample in samples:
        bboxes_raw=[]
        for a in sample.assets:
            bboxes_raw.append([a.top,a.left,a.low,a.right,a.type]) #tag1
        samples_raw.append(bboxes_raw)
        
    return samples_raw

if 1==0:

    layouts=get_layouts_rico()
    samples=get_samples_rico(layouts)
    samples_raw=get_samples_raw_rico(samples)
    
    show_images_rico(layouts)
    show_bboxes_rico(samples)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        image datasets
#------------------------------------------------------------------------------------------------------------------------------------

if 1==0:
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

def get_xy_cifar_32():
    
    image_size = (32, 32, 3)
    noise_size = (2, 2, 32)
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x_train = x_train.astype("float32")
    x_train = (x_train / 255) * 2 - 1
    y_train = tf.keras.utils.to_categorical(y_train, 10)
    return image_size,noise_size,x_train,y_train

def get_xy_mnist_32():
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    image_size = (32, 32, 3)
    noise_size = (2, 2, 32)
    n=np.shape(x_train)[0]
    w=np.shape(x_train)[1]
    h=np.shape(x_train)[2]
    new_npa=np.zeros((n,32,32,3),dtype=np.uint8)
    for i in range(n):
        npa=resize_image(x_train[i],32)
        new_npa[i,:,:,:]=npa
    x_train=new_npa    
    x_train = x_train.astype("float32")
    x_train = (x_train / 255) * 2 - 1
    y_train = tf.keras.utils.to_categorical(y_train, 10)
    return image_size,noise_size,x_train,y_train
    
def get_xy_mnist_28():
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    image_size = (28, 28, 1)
    noise_size = (2, 2, 32)
    x_train = np.expand_dims(x_train, axis=3)
    x_train = x_train.astype("float32")
    x_train = (x_train / 255) * 2 - 1
    y_train = tf.keras.utils.to_categorical(y_train, 10)
    return image_size,noise_size,x_train,y_train

## basics files

if 1==0:

    if os.path.exists(pim)==False:os.makedirs(pim)

def is_value(x):
    c0=0
    if isinstance(x,int):c0=1
    if isinstance(x,float):c0=1
    if isinstance(x,str):c0=1
    return c0

'''
def get_now(x):
    v=None
    if is_value(x)==1:v=x
    if is_value(x)==0:
        if hasattr(x,"tensor"):v=x.tensor.item()
    return v
'''

## exp inst

def init_seeds1(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    
    
# close exp
def close_exp1(c):
    if 1==0:writer.close()

# inst gan
def inst_exp1(c):
    
    # inst results management
    if 1==0: #20210422n1308
        if not os.path.exists('default-mnist'):os.makedirs('default-mnist')
        if not os.path.exists('default-mnist'+'/tensorboard_logs'):os.makedirs('default-mnist'+'/tensorboard_logs')
        c.writer = tensorboard.SummaryWriter(log_dir='default-mnist'+'/tensorboard_logs')
    
    # inst model
    c.generator = Generator2(c.sample_shape) # inst gen model
    if c.cuda:c.generator.cuda() # inst gen device
    c.discriminator = Discriminator2(c.sample_shape) # inst dsc model
    if c.cuda:c.discriminator.cuda() # inst dsc device
    
    # inst losses + optimizers
    c.criterion = torch.nn.BCELoss() # inst loss function
    if c.cuda:c.criterion.cuda() # inst loss device
    c.goptim = torch.optim.Adam(c.generator.parameters(), lr=c.lr_gen, betas=(c.beta1,c.beta2)) # inst goptim
    c.doptim = torch.optim.Adam(c.discriminator.parameters(), lr=c.lr_dsc, betas=(c.beta1,c.beta2)) # inst doptim
    
# inst classifier
def inst_exp2(c):

    # inst model
    c.model = Classifier1(c.sample_shape,c.n_classes) # inst model
    if c.cuda:c.model.cuda() # inst model device

    # inst losses + optimizers
    if 1==0:c.criterion = torch.nn.BCELoss() # inst loss function
    if 1==1:c.criterion = torch.nn.CrossEntropyLoss(weight=c.class_weights.to(c.device))
    if 1==0:c.criterion = torch.nn.NLLLoss()
    if c.cuda:c.criterion.cuda() # inst loss device
    if 1==1:c.optim = torch.optim.Adam(c.model.parameters(), lr=c.lr_dsc, betas=(c.beta1,c.beta2)) # inst optim
    if 1==0:c.optim = optim.SGD(c.model.parameters(), lr=0.1)

## exp run

def prepare_batch_gan(c):
    # format batch real samples to cpu/gpu device
    c.real_batch_samples = c.real_batch_samples.to(c.device)
    # set y_fake and y_real (same size as batch)
    c.y_real_tensor = Variable(torch.Tensor(c.real_batch_samples.size(0),1).fill_(c.y_real_value), requires_grad=False).to(c.device)
    c.y_fake_tensor = Variable(torch.Tensor(c.real_batch_samples.size(0),1).fill_(c.y_fake_value), requires_grad=False).to(c.device)
    # set batch noise
    c.batch_noise = get_torch_batch_noise(c.real_batch_samples.size(0),c.noise_dim,c.device)

def prepare_batch(c):
    # format batch real samples to cpu/gpu device
    c.x_batch = c.x_batch.to(c.device)
    c.y_batch = c.y_batch.long()
    c.y_batch = c.y_batch.to(c.device)
    
# train classifier pytorch
def run_exp2(c):

    inst_exp2(c)
    for c.i_epoch in range(c.n_epochs): # for each epoch
        for c.i_batch, (c.x_batch, c.y_batch) in enumerate(c.train_loader): # for each batch
            prepare_batch(c)

            # train dsc : maximize log(D(x)) + log(1 - D(G(z)))
            c.optim.zero_grad() # reset dsc gradient to zero
            update_loss(c) # update model loss
            c.loss.tensor.backward() # update model gradient
            c.optim.step() # update model weights

            update_optim_tracks(c)
        print_results(c)
        process_epoch_results(c)
    close_exp1(c)

# train gan pytorch
def run_exp1(c):
    
    '''
    article : https://papers.nips.cc/paper/5423-generative-adversarial-nets.pdf)
    github : https://github.com/h3lio5/gan-pytorch
    '''
    
    inst_exp1(c)
    for c.i_epoch in range(c.n_epochs): # for each epoch
        for c.i_batch, (c.real_batch_samples, _) in enumerate(c.train_loader): # for each batch
            prepare_batch_gan(c)
            if check_dsc_can_be_trained(c)==1:
                
                # train dsc : maximize log(D(x)) + log(1 - D(G(z)))
                c.doptim.zero_grad() # reset dsc gradient to zero
                update_dloss(c) # update dsc loss
                c.dloss.tensor.backward() # update dsc gradient
                c.doptim.step() # update dsc weights
            
            if check_gen_can_be_trained(c)==1:

                # train gen : maximize log(D(G(z)))
                c.goptim.zero_grad() # reset gen gradient to zero
                update_gloss(c) # update gen loss
                c.gloss.tensor.backward() # update gen gradient
                c.goptim.step() # update gen weights

            update_optim_tracks_gan(c)
        print_results_gan(c)
        process_epoch_results_gan(c)
    close_exp1(c)

## exp train

def update_loss(c):

    # update model loss
    c.output=c.model(c.x_batch)
    if 1==0:c.output = torch.squeeze(c.output)
    if 1==1:c.y_batch = torch.squeeze(c.y_batch)

    '''
    print(np.shape(c.output))
    print(np.shape(c.y_batch))
    print(type(c.output))
    print(type(c.y_batch))
    '''
    '''
    output = Variable(torch.randn(10, 120).float())
    target = Variable(torch.FloatTensor(10).uniform_(0, 120).long())
    print("------------")
    print(np.shape(output))
    print(np.shape(target))
    print(type(output))
    print(type(target))
    #c.loss.tensor = c.criterion(output, target)
    '''

    c.loss.tensor = c.criterion(c.output, c.y_batch)
    
def update_dloss(c):

    # update dsc loss on real samples
    c.dsc_real_output=c.discriminator(c.real_batch_samples)
    c.real_loss = c.criterion(c.dsc_real_output, c.y_real_tensor)

    # update dsc loss on fake samples
    c.gen_samples = c.generator(c.batch_noise)
    c.dsc_fakes_output=c.discriminator(c.gen_samples.detach())
    c.fake_loss = c.criterion(c.dsc_fakes_output, c.y_fake_tensor)

    # update dsc loss
    c.dloss.tensor = c.real_loss + c.fake_loss

def update_gloss(c):

    c.gen_samples = c.generator(c.batch_noise) # get gen samples
    c.dsc_output = c.discriminator(c.gen_samples) # get updated dsc output
    c.gloss.tensor = c.criterion(c.dsc_output, c.y_real_tensor) # get gen loss
    
## exp data

def load_data_gan_synth(p,batch_size,w,h,start,end):
    '''
    p='/home/paintedpalms/rdrive/taff/code/data/y_gan_synth2_20210406_193136.npy'
    '''
    x_npa=np.load(p)[start:end]
    #x_npa=normalize_y_gan(x_npa,300,600,4)
    x_npa=normalize_y_gan(x_npa,w,h,4)
    y_npa=np.full(len(x_npa),1,dtype=np.uint8)
    dataloader=npa_to_dataloader(x_npa,y_npa,batch_size)
    return dataloader

## exp results optim

def display_optim_results(c,str_date,n_ma):
    c.ploss=c.presults+"/"+str_date+"_loss_track.npy"
    c.pacc=c.presults+"/"+str_date+"_acc_track.npy"
    c.loss.track=np.load(c.ploss)
    c.acc.track=np.load(c.pacc)
    loss_ma=ma_track(c.loss.track,n_ma)
    acc_ma=ma_track(c.acc.track,n_ma)
    plt.plot(loss_ma)
    plt.show()
    plt.plot(acc_ma)
    plt.show()

def get_optim_results_gan(c,str_date):
    n_ma=1000
    c.pdloss=c.presults+"/"+str_date+"_dloss_track.npy"
    c.pgloss=c.presults+"/"+str_date+"_gloss_track.npy"
    c.pdacc=c.presults+"/"+str_date+"_dacc_track.npy"
    c.dloss.track=np.load(c.pdloss)
    c.gloss.track=np.load(c.pgloss)
    c.dacc.track=np.load(c.pdacc)
    dloss_ma=ma_track(c.dloss.track,n_ma)
    gloss_ma=ma_track(c.gloss.track,n_ma)
    dacc_ma=ma_track(c.dacc.track,n_ma)
    return dloss_ma,gloss_ma,dacc_ma

def display_optim_results_gan(c,str_date):
    dloss_ma,gloss_ma,dacc_ma=get_optim_results_gan(c,str_date)
    plt.plot(dloss_ma)
    plt.plot(gloss_ma)
    plt.show()
    plt.plot(dacc_ma)
    plt.show()

def update_optim_tracks(c):
    with torch.no_grad():

        update_loss(c) # update loss tensor
        c.loss.now=c.loss.tensor.item() # update loss value
        update_track(c.loss,[c.n_ma]) # update loss track

        # get output
        c.output=c.model(c.x_batch) # get dsc output on fakes samples

        # update acc
        if 1==0:
            c.acc.now=torch.sum(c.output == c.y_batch).item() # update dacc value
        if 1==1:
            y_one_hot = torch.nn.functional.one_hot(c.y_batch)
            c.acc.now=torch.sum(c.output == y_one_hot).item()/c.batch_size/c.n_classes # update dacc value (one hot)

            '''
            print("y_one_hot",y_one_hot.detach().numpy()[0])
            print("c.output",c.output.detach().numpy()[0])
            print("c.acc.now",c.acc.now)
            '''

        update_track(c.acc, [c.n_ma]) # update dacc track

def update_optim_tracks_gan(c):
    with torch.no_grad():

        # update dloss
        update_dloss(c) # update tensor
        c.dloss.now=c.dloss.tensor.item() # update value
        update_track(c.dloss,[c.n_ma]) # update track

        # update gloss 
        update_gloss(c) # update tensor
        c.gloss.now=c.gloss.tensor.item() # update value
        update_track(c.gloss,[c.n_ma]) # update track

        # update dacc
        c.gen_samples = c.generator(c.batch_noise) # generate fakes samples
        c.dsc_fakes_output = c.discriminator(c.gen_samples) # get dsc output on fakes samples
        c.dacc.now=1-c.dsc_fakes_output.mean().item() # update dacc value
        update_track(c.dacc, [c.n_ma]) # update dacc track

def print_results_gan(c):
    if c.freq_print!=-1:
        if c.i_epoch%c.freq_print==0:
            print(c.i_epoch,"dloss ma",c.dloss.ma[c.n_ma],"gloss ma",c.gloss.ma[c.n_ma],"dsc acc ma",c.dacc.ma[c.n_ma])

def print_results(c):
    if c.freq_print!=-1:
        if c.i_epoch%c.freq_print==0:
            print(c.i_epoch,"loss ma",c.loss.ma[c.n_ma],"acc ma",c.acc.ma[c.n_ma])

## exp results generated samples

def display_layouts_from_gen_output(c,gen_output,n,option_color):
    npa=get_npa_from_gen_output(gen_output)
    npa=denormalize_y_gan(npa,c.w_screen,c.h_screen,4)
    npa=get_images_from_layout_npa(npa,c.w_screen,c.h_screen,option_color)
    images=get_images_from_npa(npa[:n])
    display_images(images)

def process_epoch_results(c):
    # save weights + track
    if c.freq_save!=-1:
        if (c.i_epoch+1)%c.freq_save==0:

            # save weights
            torch.save(c.model.state_dict(), c.pmodel)

            # save track
            np.save(c.ploss,c.loss.track)
            np.save(c.pacc,c.acc.track)

def process_epoch_results_gan(c):

    # display stats
    '''
    print("------------------------------------",time.ctime())
    print('[%d/%d][%d/%d]\tLoss_D: %.4f\tLoss_G: %.4f\tD(x): %.4f\t'
            % (c.i_epoch+1, c.n_epochs, c.i_batch+1, len(c.train_loader),c.dloss.tensor.item(), c.gloss.tensor.item(), c.dacc.ma[c.n_ma]))
    '''

    if c.freq_display!=-1:
        if (c.i_epoch+1)%c.freq_display == 0:

            with torch.no_grad():
                
                # get npa samples from gen(z) samples
                gen_output=c.generator(c.fixed_noise)
                npa=get_npa_from_gen_output(gen_output)
                
            # denormalize generated samples
            if c.samples_type=="images":npa=denormalize_dataset_tanh_color(npa)
            if c.samples_type=="layouts":npa=denormalize_y_gan(npa,c.w_screen,c.h_screen,4)
                
            # save generated samples
            np.save(c.presults+"/"+c.str_date+"_gen"+".npy",npa)
            
            # display generated samples
            if c.samples_type=="layouts":
                npa=get_images_from_layout_npa(npa,c.w_screen,c.h_screen,5,c.option_color) 
            for i in range(5):
                img=get_image_from_npa(npa[i])
                display(img)

    # save weights + track
    if c.freq_save!=-1:
        if (c.i_epoch+1)%c.freq_save==0:

            # save weights
            torch.save(c.generator.state_dict(), c.pgen)
            torch.save(c.discriminator.state_dict(), c.pdsc)

            # save track
            np.save(c.pdloss,c.dloss.track)
            np.save(c.pgloss,c.gloss.track)
            np.save(c.pdacc,c.dacc.track)

## pytorch
## basics

if 1==0:

    torch.save(c.generator.state_dict(), c.pgen)
    torch.save(c.discriminator.state_dict(), c.pdsc)

    c.generator.load_state_dict(torch.load(pgen))
    c.discriminator.load_state_dict(torch.load(pdsc))

def get_class_distribution(obj):
    count_dict = {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
    }
    
    for i in obj:
        if i == 0: 
            count_dict['0'] += 1
        elif i == 1: 
            count_dict['1'] += 1
        elif i == 2: 
            count_dict['2'] += 1
        elif i == 3: 
            count_dict['3'] += 1
        elif i == 4: 
            count_dict['4'] += 1  
        elif i == 5: 
            count_dict['5'] += 1
        elif i == 6: 
            count_dict['6'] += 1
        elif i == 7: 
            count_dict['7'] += 1
        elif i == 8: 
            count_dict['8'] += 1
        elif i == 9: 
            count_dict['9'] += 1
        else:
            print(i,"Check classes.")
            
    return count_dict

## exp checks

def check_dsc_can_be_trained(c):

    c0=0
    
    if c.dcheck=="na":c0=1
    
    if c.dcheck=="dloss_over_gloss":
        if c.gloss.ma==None or c.dloss.ma==None:c0=1
        if c.gloss.ma!=None and c.dloss.ma!=None:
            if c.gloss.ma<c.gloss_over_dloss_max*c.dloss.ma:c0=1

    if c.dcheck=="dsc_acc":
        if c.dacc.ma[c.n_ma]==None:c0=1
        if c.dacc.ma[c.n_ma]!=None:
            if c.dacc.ma[c.n_ma]<c.dacc_max:c0=1
    return c0

def check_gen_can_be_trained(c):
    
    c0=0
    
    if c.gcheck=="na":c0=1
    
    if c.gcheck=="gloss_over_dloss":
        if c.gloss.ma[c.n_ma]==None or c.dloss.ma==None:c0=1
        if c.gloss.ma[c.n_ma]!=None and c.dloss.ma!=None:
            if c.dloss.ma<c.dloss_over_gloss_max*c.gloss.ma:c0=1

    if c.gcheck=="dsc_acc":
        if c.dacc.ma[c.n_ma]==None:c0=1
        if c.dacc.ma[c.n_ma]!=None:
            if c.dacc_min<c.dacc.ma[c.n_ma]:#.45:
                c0=1
                
    if c.gcheck=="k_dsc_over_gen":
        if c.i_epoch%c.k_dsc_over_gen==0:

            c0=1
    #print("tag1",c0)
                
    return c0

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        public imports
#------------------------------------------------------------------------------------------------------------------------------------

import os
import csv
import xlsxwriter
import datetime
import numpy as np
import ast
import random
import copy

import torch
import torchvision
from model import *
import torch.nn as nn
from torch.utils import tensorboard
from torch.autograd import Variable
from torchvision.utils import save_image,make_grid

class Clay():
    def __init__(self):
        return None

class clay():
    def __init__(self):
        return None


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        ## numpy arrays
#------------------------------------------------------------------------------------------------------------------------------------

def shuffle_sub(npa,n):
    seed=2000
    npa=copy.deepcopy(npa)
    np.random.seed(seed)
    np.random.shuffle(npa)
    npa=npa[:n]
    return npa

if 0==1:
    
    # create npa
    n0,n1,n2,v=150,100,1,150
    npa=np.zeros((n0,n1,n2))
    npa=np.full((n0,n1,n2),v,dtype=np.uint8)
    npa=np.random.rand(3,2) # random numpy array
    m=npa.mean(axis=0)
    s=npa.sum(axis=0)

    # 
    npa1=copy.deepcopy(npa)
    n0,n1,n2,n3=np.shape(npa1)
    npa2=np.zeros((n0,n2,n3,n1),dtype=type(npa[0,0,0,0]))
    for i in range(n0):
        for j in range(n1):
            for k in range(n2):
                for l in range(n3):
                    npa2[i,l,k,j]=npa1[i,j,k,l]


def get_dum_vector(h,option):
    m=np.zeros(h)
    for i in range(h):
        if option==1:m[i]=i
    return m

def get_dum_matrix(h,w,option):
    m=np.zeros((h,w))
    for i in range(h):
        for j in range(w):
            if option==1:m[i,j]=i
            if option==2:m[i,j]=j
            if option==3:m[i,j]=10*i+j
    return m

def random_sample(x,k):
    return np.asarray(random.sample(list(x),k))

def sub_batch(x,y,batch_size,indexes):
    x_batch=np.zeros((batch_size,x.shape[1]))
    y_batch=np.zeros(batch_size)
    k=0
    for i_random in indexes[:batch_size]:
        x_batch[k]=x[i_random]
        y_batch[k]=y[i_random]
        k+=1
    return x_batch,y_batch   

def random_batch(x,y,batch_size):
    x_batch=np.zeros((batch_size,x.shape[1]))
    y_batch=np.zeros(batch_size)
    n=len(x)
    indexes=np.arange(n)
    random.shuffle(indexes)
    k=0
    for i_random in indexes[:batch_size]:
        x_batch[k]=x[i_random]
        y_batch[k]=y[i_random]
        k+=1
    return x_batch,y_batch

def get_random_indexes(n):
    indexes=np.arange(n)
    random.shuffle(indexes)
    return indexes

def get_n_best_average(values,n):
    cp=copy.deepcopy(values)
    cp.sort()
    return np.average(cp[:n])

def get_min_curve(values):
    mins=[]
    mn=values[0]
    for v in values:
        if v<mn:
            mn=v
        mins.append(mn)
    return mins

def get_average_deriv(values,start,end):
    deltas=[]
    for i in range(start,end):
        delta=values[i]/max(0.0000001,values[i-1])
        #print(i-1,i,delta)
        deltas.append(delta)
    score=1
    if len(deltas)>0:score=np.average(deltas)
    return score

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        variables 
#------------------------------------------------------------------------------------------------------------------------------------

if 0==1:

    # call variable by its name as a string
    eval("a")

    # check instance of a variable
    if isinstance(pl, list):
        print("this is a list")

    # convert string content into correspondant type
    pl=ast.literal_eval("[2,3,5]")
    tu=ast.literal_eval("(2,3,5)")
    nt=ast.literal_eval("2")
    fl=ast.literal_eval("2.0")

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        class + object 
#------------------------------------------------------------------------------------------------------------------------------------

def is_value(x):
    c0=0
    if isinstance(x,int):c0=1
    if isinstance(x,float):c0=1
    if isinstance(x,str):c0=1
    return c0

if 0==1:

    # read + write global variable from variable name
    globals()['a']=3

    # read object variable from variable name
    getattr(obj, obj_attribute_name)


# get name + value of each attribute of an object
def get_names_and_values_from_object(o):
    '''
    names,values=get_names_and_values(c.pm)
    '''
    names=[]
    values=[]
    for name in dir(o):
        if name[0]!="_":
            names.append(name)
            values.append(getattr(o, name))
    return names,values

def show_attr(o,name):
    if hasattr(o,name):print(name,getattr(o, name))

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        # prints
#------------------------------------------------------------------------------------------------------------------------------------

def get_random_id():
    s=""
    for i in range(5):s+=str(random.randint(0,9))
    return s

def get_trigram_count(k):
    s=""
    if k<100:s+="0"
    if k<10:s+="0"
    s+=str(k)
    return s

def pr(k):
    print("-----------",k)
    print("")

def prs(v,k):
    print(k)
    print("")
    print(v)
    print("")
    
def prss(v):
    print(v)
    print("")

'''
# print step
def prs(s,i_step):
    if i_step!=-1:
        s+="------------------------------------------- "
        s+="step"+str(i_step)
        s+=" -------------------------------------------\n\n"
    if i_step==-1:s+="\n"
    return s

# print sub step
def prss(s,v):
    return s+"\n"+str(v)+"\n"
'''

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        text process
#------------------------------------------------------------------------------------------------------------------------------------

if 0==1:

    # get lines from a text
    lines=s.splitlines()

    # get substring before first occurence of a character
    i=line.index('\t')
    key_str=line[:i]
    print("key",key_str)

    # get substring after last occurence of a character
    i=line.rindex('\t')
    value_str=line[i+1:]
    value=float(value_str)
    print("value",value)

    # get dict, list, int, float, booleans from a string
    v=ast.literal_eval(s)

def get_dict_from_text(s,sep):
    lines=s.splitlines()
    d={}
    for line in lines :
        if sep in line:
            name=line[:line.index(sep)]
            v=line[line.rindex(sep)+1:]
            
            if "/" not in v:
                if "inf" not in v:
                    #if len(v)>0:
                    '''
                    if "red" not in v:
                        if "green" not in v:
                            if "blue" not in v:
                    '''
                    '''
                    print("")
                    print(v)
                    print("check","nan" in v)
                    print("")
                    '''
                    if v!="" and "tanh" not in v and "sigm" not in v:v=ast.literal_eval(str(v))
                    #print("tag1",name,v)
                    d[name]=v
    return d

def get_names_and_values_from_text(s,sep):
    names=[]
    values=[]
    lines=s.splitlines()
    for line in lines :
        if sep in line:
            names.append(line[:line.index(sep)])
            v=line[line.rindex(sep)+1:]
            if "/" in v:values.append(v)
            if "/" not in v:values.append(ast.literal_eval(v))
    return names,values

def show_basic_stats(values,n_dec):
    avg=np.round(np.average(values),n_dec)
    std=np.round(np.std(values),n_dec)
    mn=np.round(np.min(values),n_dec)
    mx=np.round(np.max(values),n_dec)
    n=len(values)
    print(avg,std,mn,mx,n)

def get_str_with_tabs(name,value,n_tabs_max):
    n_tabs=n_tabs_max-len(name)//8
    tabs=""
    for i in range(n_tabs):
        tabs+="\t"
    s=name+tabs+str(value)+"\n"
    return s

def get_stats_line_ancien(name,values):
    s=""
    if isinstance(values, list):
        s=str(len(values))+"\t"+str(min(values))+"\t"+str(max(values))+"\t"+str(int(np.round(np.mean(values))))+"\t"+str(int(np.round(np.std(values))))+"\n"
    return s

# ancien, utilisé seulement dans train_gan (gan_layout)
def get_exp_summary(c):

    # prepare sum up
    s=""
    s+="\n"
    s+="parameters \n"
    s+="\n"
    names,values=get_names_and_values_from_object(c)
    for i in range(len(names)):
        s+=get_str_with_tabs(names[i],values[i],3)
    return s

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        date and time
#------------------------------------------------------------------------------------------------------------------------------------

if 1==0:
    prev=tm(None)
    prev=tm(prev)

def tm(t_prev):
    t=time.time()
    if t_prev==None:t_prev=t
    else:print(t-t_prev)
    return t

## basics
## str date

def get_bookmark_date():
    str_date=get_simple_time_str()
    str1=str_date[:8]
    str2=str_date[9:-2]
    h=datetime.datetime.now().hour
    if 0<=h<12:ch="a"
    if 12<=h<18:ch="n"
    if 18<=h<24:ch="s"
    str_date="tm"+str1+ch+str2    
    return str_date

def get_simple_time_str():
    '''
    name=get_simple_time_str()
    '''
    y=str(datetime.datetime.now().year)
    m=str(datetime.datetime.now().month)
    d=str(datetime.datetime.now().day)
    h=str(datetime.datetime.now().hour)
    mn=str(datetime.datetime.now().minute)
    s=str(datetime.datetime.now().second)
    if len(m)==1:m="0"+m
    if len(d)==1:d="0"+d
    if len(h)==1:h="0"+h
    if len(mn)==1:mn="0"+mn
    if len(s)==1:s="0"+s
    name=y+m+d+"_"+h+mn+s
    return name


## results 

def init_track(maturities):
    x=clay()
    x.track=[]
    x.ma={}
    for m in maturities:
        x.ma[m]=None
    return x

def update_track(x,maturities):
    x.track.append(x.now)
    for m in maturities:
        if len(x.track)>=m:
            x.ma[m]=np.average(x.track[-m:])

## private imports

'''
import sys
from importlib import reload
p_code="/home/paintedpalms/rdrive/taff/code"
sys.path.insert(0,p_code)
import omega
reload (omega)
from omega import *
'''

# files

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        folder and files
#------------------------------------------------------------------------------------------------------------------------------------


if 0==1:

    # get names of all files in a folder
    p_folder="/home/paintedpalms/rdrive/taff/code"
    file_names=os.listdir(p_folder)

    # set path to imports folder
    sys.path.insert(0,"/home/paintedpalms/rdrive/taff/code")
    

if 1==0:

    # copy file
    from shutil import copyfile
    p_src="/home/paintedpalms/rdrive/taff/code/results/results_temp/20201229_230217/y_gen.npy"
    p_new="y_gen_synth.npy"
    copyfile(p_src,p_new)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        text files
#------------------------------------------------------------------------------------------------------------------------------------

# read text file
def read_text_file(p):
    file=open(p,"r")
    s=file.read()
    file.close() 
    return s

# write text in file
def write_text_file(p,s):
    file=open(p,"w")
    file.write(s)
    file.close()

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        excel files
#------------------------------------------------------------------------------------------------------------------------------------

import csv

def read_csv(file_path):
    rows=[]
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            rows.append(row)
    return rows

# read + write .xls
#def read_xls():
def write_xls(p,lines):
    #root_path='/home/paintedpalms/rdrive/taff/data/automated_layout_real/pubs_madmix/segm3'
    #workbook = xlsxwriter.Workbook(root_path+'/results.xlsx')
    workbook = xlsxwriter.Workbook(p)
    worksheet = workbook.add_worksheet()
    for i_line in range(len(lines)):
        for i_column in range(len(lines[i_line])):
            worksheet.write(i_line, i_column,lines[i_line][i_column])
    workbook.close()

'''
def get_rows_from_csv(filename):
    reader = csv.DictReader(filename)
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        samples_rows=[]
        for row in csv_reader:
            if not row:
                continue
            samples_rows.append(row)
    return samples_rows

def get_npa_from_rows(samples_rows,tp):
    n_samples=len(samples_rows)
    n_features=len(samples_rows[0])
    samples_npa=np.zeros((n_samples,n_features),dtype=tp)
    for i_sample in range(n_samples):
        for i_feature in range(n_features):
            samples_npa[i_sample,i_feature]=samples_rows[i_sample][i_feature]
    return samples_npa
'''
 
#------------------------------------------------------------------------------------------------------------------------------------
#                                                        à trier
#------------------------------------------------------------------------------------------------------------------------------------

if 0==1:

    file_name = input("file path: ")
    
'''
if type(values)!=list:s+=name+after_name+"\t"+str(values)+"\n"
if type(values)==list:
    if 0<len(values)<20:s+=name+after_name+"\t"+str(len(values))+"\t"+str(min(values))+"\t"+str(max(values))+"\t"+str(int(np.round(np.mean(values))))+"\t"+str(int(np.round(np.std(values))))+"\n"
    if len(values)==0:s+=name+after_name+"\t"+"no values"+"\n"
'''

'''
# present names + values with adapted tabs
def get_str_with_tabs(names,values,n_tabs_max):
    names=make_list(names)
    values=make_list(values)

    print("tr")
    s=""
    for i_value in range(len(names)):
        n_chars_batches=len(names[i_value])//8
        n_tabs=n_tabs_max-n_chars_batches
        tabs=""
        for i in range(n_tabs):
            tabs+="\t"
        s+=names[i_value]+tabs+str(values[i_value])+"\n"
    return s
'''

## sample process


# assign given type to each value of 3D npa
def format_3d(npa,tp):    
    (n0,n1,n2)=np.shape(npa)
    npa_new=np.zeros((n0,n1,n2),dtype=tp)
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                npa_new[i0,i1,i2]=tp(npa[i0,i1,i2])
    return npa_new

def split_samples(samples,split_ratio):
    #random.shuffle(samples)    
    n_train=int(round(len(samples)*split_ratio))
    train_samples=samples[:n_train]
    test_samples=samples[n_train:]
    return train_samples,test_samples

def get_xy(samples_npa):
    n_samples=len(samples_npa)
    n_features=len(samples_npa[0])
    x=samples_npa[:,:n_features-1]
    y=samples_npa[:,n_features-1]
    #if len(np.shape(x))==1:x=np.expand_dims(x,1)
    #if len(np.shape(y))==1:y=np.expand_dims(y,1)
    return x,y




#------------------------------------------------------------------------------------------------------------------------------------
#                                                        normalisation (code A)
#------------------------------------------------------------------------------------------------------------------------------------

def minmax_1D(npa):
    #closes=closes/1.5
    npa_scaled=copy.deepcopy(npa)
    mn=np.min(npa)
    mx=np.max(npa)
    for i in range(len(npa)):
        npa_scaled[i]=(npa[i]-mn)/(mx-mn)
        npa_scaled[i]=max(npa_scaled[i],0.000001)
    return npa_scaled

def minmax_2D(npa):
    #closes=closes/1.5
    npa_scaled=copy.deepcopy(npa)
    mn=9999999999
    mx=0
    for i in range(len(npa)):
        mn=min(mn,min(npa[i]))
        mx=max(mx,max(npa[i]))
    for i in range(len(npa)):
        for j in range(len(npa[0])):
            npa_scaled[i,j]=(npa[i,j]-mn)/(mx-mn)
            npa_scaled[i,j]=max(npa_scaled[i,j],0.000001)
    return npa_scaled

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        normalisation (code B)
#------------------------------------------------------------------------------------------------------------------------------------

# normalize minmax 2D npa
def normalize_minmax(npa,minmax):
    n_samples=np.shape(npa)[0]
    n_features=np.shape(npa)[1]
    npa_norm=np.zeros((n_samples,n_features))
    for i_sample in range(n_samples):
        for i_feature in range(n_features):
            a=npa[i_sample,i_feature]
            b=minmax[i_feature,0]
            c=minmax[i_feature,1]
            npa_norm[i_sample,i_feature]=(a-b)/(c-b)
    return npa_norm

def denormalize_minmax_2D(npa,minmax):
    n_samples=np.shape(npa)[0]
    n_features=np.shape(npa)[1]
    npa_norm=np.zeros((n_samples,n_features))
    for i_sample in range(n_samples):
        for i_feature in range(n_features):
            a=npa[i_sample,i_feature]
            b=minmax[i_feature,0]
            c=minmax[i_feature,1]
            npa_norm[i_sample,i_feature]=a*(c-b)+b
            #x=(a-b)/(c-b)
            #x*(c-b)=a-b
            #x*(c-b)+b=a
    return npa_norm

def denormalize_minmax_1D(npa,minmax):
    n_samples=np.shape(npa)[0]
    npa_norm=np.zeros(n_samples)
    for i_sample in range(n_samples):
        a=npa[i_sample]
        b=minmax[-1,0]
        c=minmax[-1,1]
        npa_norm[i_sample]=a*(c-b)+b
        #x=(a-b)/(c-b)
        #x*(c-b)=a-b
        #x*(c-b)+b=a
    return npa_norm

def get_minmax(x):
    n_features=len(x[0])
    minmax=np.zeros((n_features,2),type(x))
    for i_feature in range(n_features): 
        minmax[i_feature,0]=np.min(x[:,i_feature])
        minmax[i_feature,1]=np.max(x[:,i_feature])
    return minmax

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        reshape
#------------------------------------------------------------------------------------------------------------------------------------

def reshape_samples(npa,new_w):
    n_samples=np.shape(x)[0]
    w=np.shape(x)[1]
    h=np.shape(x)[2]
    new_h=h/w*new_w
    if len(sh)==3:
        new_npa=np.zeros((n,new_w,new_h),dtype=np.uint8)
        for i in range(n_samples):
            npa=resize_image(x[i],32)
            new_npa[i,:,:]=npa
    if len(sh)==4:
        d=sh[3]   
        new_npa=np.zeros((n,new_w,new_h,d),dtype=np.uint8)
        for i in range(n_samples):
            npa=resize_image(x[i],32)
            new_npa[i,:,:,:]=npa
    return new_npa


## image process

def get_images_from_npa(npa):
    images=[]
    for i in range(len(npa)):
        images.append(get_image_from_npa(npa[i]))
    return images

def display_images(images):
    k=0
    for img in images:
        k+=1
        display(img)



#------------------------------------------------------------------------------------------------------------------------------------
#                                                        imports
#------------------------------------------------------------------------------------------------------------------------------------

'''
## pytorch imports

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from torch.autograd import Variable
from torchvision.utils import save_image
import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
import tensorflow as tf

'''



import numpy as np
import PIL
from PIL import Image
import copy 
import requests
from io import BytesIO

if 1==0:

    p="images/flower.jpg"
    img=Image.open(p)

def align_images(npas):
    n=len(npas)
    right=0
    space=20
    w,h=len(npas[0][0]),len(npas[0])
    w_all,h_all=w*n+space*(n-1),h
    npa_all=np.zeros((h_all,w_all,4),dtype=np.uint8)
    for i_sample in range(n): #[0] #range(5):
        left=right
        if i_sample>0:left+=space
        right=left+100
        npa_all[:,left:right,:]=npas[i_sample]
    return npa_all

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        format + resize
#------------------------------------------------------------------------------------------------------------------------------------

# (w,h) npa => (w,h,1) npa
def go3D(npa):
    shape=np.shape(npa)
    if len(shape)==2:(n0,n1)=shape
    if len(shape)==3:(n0,n1,_)=shape
    new_npa=np.zeros((n0,n1,3),dtype=np.uint8)
    for i in range(3):
        if len(shape)==2:new_npa[:,:,i]=npa
        if len(shape)>2:new_npa[:,:,i]=npa[:,:,0]
    return new_npa
    
def go3D_dataset(npa,option_tp):
    if option_tp==1:tp=type(npa[0,0,0,0])
    if option_tp==2:tp=np.uint8
    n_samples,_,n0,n1=np.shape(npa)
    new_npa=np.zeros((n_samples,3,n0,n1),dtype=tp)
    for i_sample in range(n_samples):
        for i in range(3):
            new_npa[i_sample,i,:,:]=npa[i_sample,0,:,:]
    return new_npa

# 2D npa => 3D image
def get_image_from_npa(npa):
    shape=np.shape(npa)
    if len(shape)==2:
        npa=go3D(npa)
        image=Image.fromarray(npa, 'RGB')
    if len(shape)>2:
        if shape[2]==1:image = Image.fromarray(go3D(npa), 'RGB')
        if shape[2]==3:image = Image.fromarray(npa, 'RGB')
        if shape[2]==4:image = Image.fromarray(npa, 'RGBA')
    return image

## process_data


def normalize_value_tanh_color_0_255(x):return x/255*2-1
def normalize_value_tanh_color_0_600(x):return x/600*2-1
def normalize_dataset_tanh_color(npa):return np.vectorize(normalize_value_tanh_color_0_255)(npa)
def normalize_dataset_tanh_color1(npa):return np.vectorize(normalize_value_tanh_color_0_600)(npa)

def normalize_dataset_tanh_color0(npa):
    '''
    npa shape = (n_samples,n1,n2)
    '''
    n0,n1,n2=np.shape(npa)
    npa_new=np.zeros((n0,n1,n2),dtype=np.float32)
    for i0 in range(n0):
        if i0%1000==0:print(i0)
        for i1 in range(n1):
            for i2 in range(n2):
                '''
                v=npa[i0,i1,i2]
                v=v/255
                v=v*2-1
                v=np.round(v)
                v=np.uint8(v)
                '''
                npa_new[i0,i1,i2]=npa[i0,i1,i2]/255*2-1
    return npa_new

def denormalize_dataset_tanh_color(npa):
    '''
    npa shape = (n_samples,n1,n2)
    '''
    n0,n1,n2=np.shape(npa)
    npa_new=np.zeros((n0,n1,n2),dtype=np.uint8)
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                v=npa[i0,i1,i2]
                v=(v+1)/2
                v=v*255
                v=np.round(v)
                v=np.uint8(v)
                npa_new[i0,i1,i2]=v
    return npa_new

def denormalize_dataset_tanh_color1(npa,mx):
    '''
    npa shape = (n_samples,n1,n2)
    '''
    n0,n1,n2=np.shape(npa)
    npa_new=np.zeros((n0,n1,n2),dtype=np.uint8)
    for i0 in range(n0):
        for i1 in range(n1):
            for i2 in range(n2):
                v=npa[i0,i1,i2]
                v=(v+1)/2
                v=v*mx
                v=np.round(v)
                v=np.uint8(v)
                npa_new[i0,i1,i2]=v
    return npa_new

def denormalize_dataset_tanh_color2(npa,mx):
    '''
    npa shape = (n_samples,n1,n2)
    '''
    n0,n1,n2=np.shape(npa)
    npa_new=np.zeros((n0,n1,n2),dtype=np.uint8)
    for i0 in range(n0): # i_sample
        for i1 in range(n1): # i_asset
            for i2 in range(n2): # i_feat
                v=npa[i0,i1,i2]
                v=(v+1)/2
                v=v*mx
                v=np.round(v)
                v=np.uint8(v)
                npa_new[i0,i1,i2]=v
    return npa_new

def denormalize_dataset_tanh_color3(npa,mx):
    '''
    npa shape = (n_samples,n1,n2)
    '''
    n0,_,n1,n2=np.shape(npa)
    npa_new=np.zeros((n0,1,n1,n2),dtype=np.uint8)
    for i0 in range(n0): # i_sample
        for i1 in range(n1): # i_asset
            for i2 in range(n2): # i_feat
                v=npa[i0,0,i1,i2]
                v=(v+1)/2
                v=v*mx
                v=np.round(v)
                v=np.uint8(v)
                npa_new[i0,0,i1,i2]=v
    return npa_new


# resize 2D npa / 3D image
def resize_image(npa,new_width):
    if type(npa)==np.ndarray:img=get_image_from_npa(npa)
    if type(npa)!=np.ndarray:img=npa
    wpercent = (new_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((new_width,hsize), Image.ANTIALIAS)
    if type(npa)==np.ndarray:npa=np.asanyarray(img)
    if type(npa)!=np.ndarray:npa=img
    return npa

def get_npa_from_image(img):
    return np.asarray(copy.copy(img))

def save_npa_as_image(npa,p):
    get_image_from_npa(npa).save(p)

'''
def get_image_from_npa(npa):
    if np.shape(npa)[2] == 3: image = Image.fromarray(npa, 'RGB')
    if np.shape(npa)[2] == 4: image = Image.fromarray(npa, 'RGBA')
    return image
'''

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        display
#------------------------------------------------------------------------------------------------------------------------------------

## data
## display

def display_npa_layouts(npa,w,h,n,option_color):
    npa=shuffle_sub(npa,n)
    images_npa=get_images_from_layout_npa(npa,w,h,n,option_color)
    for i in range(n):
        display(get_image_from_npa(images_npa[i]))

## now

def display_layouts(y_gan,option_color):
    bboxes_gan=get_bboxes_from_y_gan(y_gan,"y_gan")
    samples_gan=get_samples_from_y_gan(y_gan,[],1)
    images_gan=get_images_from_layouts(samples_gan,300,600,5,option_color) ## tag0
    n=5
    for i_sample in range(min(len(images_gan),n)):
        img=get_image_from_npa(images_gan[i_sample])
        display(img)

def get_images_from_layout_npa(y_gan,w_screen,h_screen,n,option_color):
    '''
    npa layouts (denormalized) => images
    '''
    bboxes_gan=get_bboxes_from_y_gan(y_gan,"y_gan")
    samples_gan=get_samples_from_y_gan(y_gan,[],1)
    samples_gan=sort_assets_by_size(samples_gan)
    images_gan=get_images_from_layout_samples(samples_gan,w_screen,h_screen,n,option_color)
    return images_gan


def get_image_from_url(url):

    imageData = requests.get(url).content
    image = PIL.Image.open(BytesIO(imageData))
    rgba = image.convert('RGBA')

    return rgba

## data
## image process

def create_grey_bg(h,w):
    r,g,b=100,100,100
    npa_bg=np.zeros((h,w,4),dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            npa_bg[i,j,0]=r
            npa_bg[i,j,1]=g
            npa_bg[i,j,2]=b
            npa_bg[i,j,3]=255
    return npa_bg

def add_shape(npa,top,left,low,right,r,g,b):
    for i in range(len(npa)):
        for j in range(len(npa[0])):
            if top<=i<=low and left<=j<=right:
                npa[i,j,0] = r
                npa[i,j,1] = g
                npa[i,j,2] = b
    return npa

def add_shape2(npa,top,left,low,right,r,g,b):
    #npa=copy.deepcopy(npa)
    #npa=copy.copy(npa)
    npa[int(top):int(low),int(left):int(right),0]=r
    npa[int(top):int(low),int(left):int(right),1]=g
    npa[int(top):int(low),int(left):int(right),2]=b 
    return npa

def draw_box(top,left,low,right,npa,r,g,b,a):
    t = copy.copy(npa)
    for num_line in range(len(t)):
        for num_column in range(len(t[0])):
            margin = 2
            check = False
            if top-margin < num_line < top+margin and left-margin < num_column < right+margin:check = True
            if low-margin < num_line < low+margin and left-margin < num_column < right+margin:check = True
            if left-margin < num_column < left+margin and top-margin < num_line < low+margin:check = True
            if right-margin < num_column < right+margin and top-margin < num_line < low+margin:check = True
            if check == True:
                pixel = t[num_line,num_column]
                pixel[0] = r
                pixel[1] = g
                pixel[2] = b
                pixel[3] = a
    return t

def draw_line(num_line,p_t,r,g,b,a):
    t = copy.copy(p_t)
    for num_column in range(len(t[0])):
        pixel = t[num_line,num_column]
        pixel[0] = r
        pixel[1] = g
        pixel[2] = b
        pixel[3] = a
    return t

def draw_column(num_column,p_t,r,g,b,a):
    t = copy.copy(p_t)
    for num_line in range(len(t)):
        pixel = t[num_line,num_column]
        pixel[0] = r
        pixel[1] = g
        pixel[2] = b
        pixel[3] = a
    return t

def add_point(npa,i_line,i_column):
    npa_draw=draw_column(i_column,npa,0,255,0,255)
    npa_draw=draw_line(i_line,npa_draw,0,255,0,255)
    img=get_image_from_npa(npa_draw)
    return img

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        à trier
#------------------------------------------------------------------------------------------------------------------------------------

# post-process mnist + cifar
def post_process_generated_image_1(c,image):
    image = np.reshape(image, (10, 10, 32, 32, 3))
    image = np.transpose(image, (0, 2, 1, 3, 4))
    image = np.reshape(image, (10 * 32, 10 * 32, 3))
    image = 255 * (image + 1) / 2
    image = image.astype("uint8")
    return image

def post_process_generated_image_2(c,image):
    n=10 #1
    #image = generator.predict(np.random.normal(size=(n * n,) + noise_size))
    image = np.reshape(image, (n, n, 28, 28, 1))
    image = np.transpose(image, (0, 2, 1, 3, 4))
    image = np.reshape(image, (n * 28, n * 28, 1))
    image = 255 * (image + 1) / 2
    image = image.astype("uint8")
    image=get_image_from_npa(image)
    return image

# ip
def post_process_generated_image_3(c,image):
    n=10 #1
    image = np.reshape(image, (n, n, 3, 5, 1))
    image = np.transpose(image, (0, 2, 1, 3, 4))
    image = np.reshape(image, (n * 3, n * 5, 1))
    image = 600 * (image + 1) / 2
    image = image.astype("uint8")
    #image=get_image_from_npa(image)
    return image


## maths


#------------------------------------------------------------------------------------------------------------------------------------
#                                                        imports
#------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import random

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        stats
#------------------------------------------------------------------------------------------------------------------------------------

if 0==1:

    # covariance    
    covariance=np.cov(matrice_m)

#------------------------------------------------------------------------------------------------------------------------------------
#                                                        linear algebra
#------------------------------------------------------------------------------------------------------------------------------------

# mobile average
def ma_track(npa,timespan):
    npa_ma=np.zeros(len(npa)-timespan)
    for i in range(timespan,len(npa)):
        npa_ma[i-timespan]=np.average(npa[i-timespan:i])
    return npa_ma

def is_pos_def(x): 
    return np.all(np.linalg.eigvals(x) > 0)

def multivariate_normal(x, d, mean, covariance):
    """pdf of the multivariate normal distribution."""
    x_m = x - mean
    return (1. / (np.sqrt((2 * np.pi)**d * np.linalg.det(covariance))) *
            np.exp(-(np.linalg.solve(covariance, x_m).T.dot(x_m)) / 2))



## tp_nn

import torch.nn as nn
import torch.nn.functional as fnc
import torch

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 200) # premier fully connected layer
        self.fc2 = nn.Linear(200, 200) # deuxième fully connected layer
        self.fc3 = nn.Linear(200, 10) # troisième fully connected layer
        
def forward(self, x):
    x = fnc.relu(self.fc1(x))
    x = fnc.relu(self.fc2(x))
    x = fnc.log_softmax(self.fc3(x))
    return x

if 1==0:

    net = Net()
    print(net)

def simple_gradient():
    # print the gradient of 2x^2 + 5x
    x = Variable(torch.ones(2, 2) * 2, requires_grad=True)
    z = 2 * (x * x) + 5 * x
    # run the backpropagation
    z.backward(torch.ones(2, 2))
    print(x.grad)

def create_nn(batch_size=200, learning_rate=0.01, epochs=10,
              log_interval=10):

    # load data
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=batch_size, shuffle=True)

    # build model
    class Net(nn.Module):
        
        
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(28 * 28, 200) 
            self.fc2 = nn.Linear(200, 200) 
            self.fc3 = nn.Linear(200, 10) 

        def forward(self, x):
            x = F.relu(self.fc1(x))        # layer 1 : fully connected + relu activation
            x = F.relu(self.fc2(x))        # layer 2 : fully connected + relu activation
            x = F.log_softmax(self.fc3(x)) # layer 3 : fully connected + relu activation
            return x
        
    net = Net()
    print(net)

    # optimizer : stochastic gradient descent
    optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9)
    
    # loss function : negative log-likelihood
    criterion = nn.NLLLoss()

    # train
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = Variable(data), Variable(target)
            
            # resize data from (batch_size, 1, 28, 28) to (batch_size, 28*28)
            data = data.view(-1, 28*28)
            optimizer.zero_grad()
            net_out = net(data)
            loss = criterion(net_out, target)
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                           100. * batch_idx / len(train_loader), loss.data)) #loss.data[0]))

    # test
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        
        # NB
        # inputs       : data
        # outputs pred : net_out
        # outputs test : target
        
        # pre-process inputs + outputs test
        data, target = Variable(data, volatile=True), Variable(target)
        data = data.view(-1, 28 * 28)
        
        # predict
        net_out = net(data) # output brut, sous forme d'un vecteur avec des valeurs comprises entre 0 et 1
        
        # get loss
        test_loss += criterion(net_out, target).data#[0]
        
        # output post-processé : on récupère l'index de la valeur la plus élevée dans le vecteur output
        pred = net_out.data.max(1)[1]  # (chaque valeur est une log-probabilité)
        
        # nombre de réponses correctes
        correct += pred.eq(target.data).sum()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

#if __name__ == "__main__":
if 1==0:

    run_opt = 2
    if run_opt == 1:
        simple_gradient()
    elif run_opt == 2:
        create_nn()


## tensors pytorch

def get_npa_from_gen_output(gen_output):
    fake_samples = gen_output
    npa=fake_samples[:,0,:,:]
    npa=npa.cpu().detach().numpy() # if several channels : [:,0,:,:] => [:,:,:,:]
    return npa




#------------------------------------------------------------------------------------------------------------------
#                                       pytorch : basics
#------------------------------------------------------------------------------------------------------------------

import numpy as np
import torch
from torch.autograd import Variable

if 0 == 1:
    
    print(torch.__version__)
    print("")

    # set tensors 
    x = torch.Tensor(2, 3)   # rand [-inf,inf]
    x = torch.zeros(2,3)     # zeros
    x = torch.rand(2, 3)     # rand [0,1]
    x = torch.ones(2,3)      # ones
    y = torch.ones(2,3) * 2  # 
    y[:,1] = y[:,1] + 1      # 
    z = x + y                # 
    
    # matrix basic operations
    z = x * x
    z = np.dot(x,x)
    
    # assign values by hand to a tensor
    x = torch.empty(2, 2)
    x[0,0]=1
    x[0,1]=2
    x[1,0]=3
    x[1,1]=4
    
    print(x)
    print(y)
    print(z)
    print("")

# z = 2x² + 5x + 10y³   : x = [[2,2],[2,2]] , y = [[2,2],[2,2]] => z = [[98,98],[98,98]]
# dz/dx = 4x + 5        : x = [[2,2],[2,2]] => z = [[13,13],[13,13]]
# dz/dy = 30y²          : y = [[2,2],[2,2]] => z = [[120,120],[120,120]]

def demo(option):

    pr("init inputs")

    x = Variable(torch.ones(2, 2) * 2, requires_grad=True)
    y = Variable(torch.ones(2, 2) * 2, requires_grad=True)
    prs(x,"x")
    prs(y,"y")

    pr("compute outputs")

    if option in [0,2]:
        
        z1 = 2 * (x * x) + 5 * x + 10*y*y*y
        prs(z1,"z1 = 2x² + 5x + 10y³")

    if option in [1,2]:

        z2 = 2 * x + y
        prs(z2,"z2 = 2x + y")

    pr("retro propagation")

    if option in [0,2]:
        z1.backward(torch.ones(2, 2))
        prss("backward through z1")
        
    if option in [1,2]:
        z2.backward(torch.ones(2, 2))
        prss("backward through z2")
   
    pr("compute gradients")
    
    dzdx = x.grad
    dzdy = y.grad

    # z1 = z1 = 2x² + 5x + 10y³
    # dz/dx = 4x + 5
    # dz/dy = 30y²
    if option==0:
        
        prs(dzdx,"dz1/dx = 4x + 5")
        prs(dzdy,"dz1/dy = 30y²")
        
    # z2 = 2x + y
    # dz/dx = 2
    # dz/dy = 1
    if option==1:
        
        prs(dzdx,"dz2/dx = 2")
        prs(dzdy,"dz2/dy = 1")
        
    # z1 = z1 = 2x² + 5x + 10y³
    # z2 = 2x + y
    # dz1/dx + dz2/dx = 4x + 5 + 2 = 4x + 7
    # dz1/dy + dz2/y = 30y² + 1
    if option==2:
        
        prs(dzdx,"dz1/dx + dz2/dx = 4x + 5 + 2 = 4x + 7")
        prs(dzdy,"dz1/dy + dz2/y = 30y² + 1")
        
if 1==0:

    demo(0)
    demo(1)
    demo(2)

## display

import os
import sys
from importlib import reload
import matplotlib.pyplot as plt

def show_vectors(vectors):
    for vec in vectors:
        timespan=int(np.round(.05*len(vec))) 
        vec=ma_track(vec,timespan) # apply mobile average
        plt.plot(vec/np.max(vec))
    plt.show()

def show_vector(vec):
    timespan=int(np.round(.05*len(vec)))
    vec=ma_track(vec,timespan) # apply mobile average
    plt.plot(vec)
    plt.show()
    
def show_min_max_values(values):
    cp=copy.deepcopy(values)
    cp.sort()
    n=5
    for v in cp[:n]:print(v)
    print("")
    for v in cp[-n:]:print(v)

def show_results(exps_folder_name,exp_name,n,option):
    #exps_folder_name="results_temp"
    #exp_name="20210108_165524"
    p_code="/home/paintedpalms/rdrive/taff/code"
    p_text_file=p_code+"/"+"results"+"/"+exps_folder_name+"/"+exp_name+"/parameters.txt"
    d=get_exp_results(p_text_file)
    show_min_max_values(d["errors"])
    if option==1:
        show_vector(d["errors"][:n])
        show_vector(d["diversities"][:n])
    if option==2:
        show_vector(d["errors"][n:])
        show_vector(d["diversities"][n:])

def show_results2(exps_folder_name,exp_name,n,option):
    #exps_folder_name="results_temp"
    #exp_name="20210108_165524"
    p_code="/home/paintedpalms/rdrive/taff/code"
    p_text_file=p_code+"/"+"results"+"/"+exps_folder_name+"/"+exp_name+"/parameters.txt"
    d=get_exp_results(p_text_file)
    show_min_max_values(d["errors"])
    if option==1:show_vectors([d["losses_gen"][:n],d["losses_dsc"][:n]])
    if option==2:show_vector([d["losses_gen"][n:],d["losses_dsc"][n:]])
     

def print_basic_scores(folder_name,file_name):
    # n best overlap : average
    d=get_exp_results2(folder_name,file_name)
    score=get_n_best_average(d["errors"],5)
    print(np.round(score,7))
    # min overlap curves : deltas average
    if 0==1:
        d=get_exp_results2(folder_name,file_name)
        mins=get_min_curve(d["errors"])
        score=get_average_deriv(mins,100,300)
        print(np.round(score,7))

## equality : main
def init_users(c,user_names):
    c.users={}
    for name in user_names:
        user=clay()
        user.decision=clay()
        user.validation=clay()
        user.decision.credit=0
        user.decision.pending=[]
        user.decision.done=[]
        user.validation.credit=0
        user.validation.pending=[]
        user.validation.done=[]
        c.users[name]=user

def add_prop(c,id_prop,author,users,dates,strr):
    prop=clay()
    prop.dates=clay()
    prop.validation={}
    prop.id=id_prop
    prop.author=author
    prop.users=users
    prop.dates.start=dates[0]
    prop.dates.end=dates[1]
    prop.dates.validation=prop.dates.end+datetime.timedelta(days=1)
    prop.str=strr
    prop.decision={}
    prop.state="pending"
    for user in users:
        prop.decision[user]=clay()
        prop.decision[user].value=0
        prop.decision[user].state="pending"
        prop.validation[user]=-1
        c.users[user].decision.pending.append(id_prop)
    c.props[id_prop]=prop

## equality : sub
def check_decision_consensus(c,id_prop):
    all_positive=1
    all_negative=1
    for user in c.props[id_prop].users:
        if c.props[id_prop].decision[user].value<0:all_positive=0
        if c.props[id_prop].decision[user].value>0:all_negative=0
    check=0
    if all_positive==1 or all_negative== 1:check=1
    return check

def check_validation_consensus(c,id_prop):
    k_neg=0
    k_pos=0
    for user in c.props[id_prop].users:
        if c.props[id_prop].validation[user]<0:k_neg+=1
        if c.props[id_prop].validation[user]>0:k_pos+=1
    check=1
    if k_neg!=0 and k_pos!=0:check=0
    return check

def check_decision_completion(c,id_prop):
    check=1
    for user in c.props[id_prop].users:
        if c.props[id_prop].decision[user].state!="closed":check=0
    return check

def valid_prop(c,id_prop,user,value):
    # checks
    c1=c.props[id_prop].state=="locked" # prop decision is locked
    c2=check_decision_consensus(c,id_prop) # there is consensus on this prop decision
    c3=check_validation_consensus(c,id_prop) # there is consensus on this prop validation
    c4=c.props[id_prop].dates.end<=datetime.datetime.now()<=c.props[id_prop].dates.validation # end date < now < validation date
    if c1==1:
        # if decision completion ok
        if c2==0 and c3==1:
            # if decision ko + validation ok
            for user in c.props[id_prop].users: # record decision credits for the prop
                c.users[user].decision.credit-=c.props[id_prop].auction[user]
        if c2==0 and c3==0:
            # if decision ko + validation ko
            for user in c.props[id_prop].users: # record validation credits for the prop
                v=c.props[id_prop].auction[user]
                c.users[user].validation.credit-=v
            
def update_bid(c,id_prop,user,value):
    prev_value=c.props[id_prop].decision[user].value
    # checks
    c0=value*prev_value>=0 # new bid is in the same way than previous bid
    c1=abs(value)>abs(prev_value) # new bid is stronger than previous bid
    c2=datetime.datetime.now()<=c.props[id_prop].dates.start #  now < start date
    c3=c.props[id_prop].state!="locked" # prop decision is not locked yet
    if 0 not in [c0,c1,c2,c3]:
        # if checks ok
        c.props[id_prop].decision[user].value=value # update value
        for user in c.props[id_prop].users:c.props[id_prop].decision[user].state="pending" # reset users decision state to pending

def lock_bid(c,id_prop,user):
    # checks
    c1=datetime.datetime.now()<=c.props[id_prop].dates.start #  now < start date
    if 0 not in [c1]:
        # if checks ok
        c.props[id_prop].decision[user].state="locked" # update user decision state
        
        # update prop state to : locked / prev state
        prev_state=c.props[id_prop].state
        c.props[id_prop].state="locked"
        for user in c.props[id_prop].users:
            if c.props[id_prop].decision[user].state!="locked":c.props[id_prop].state=prev_state
     
        # update prop state to : accepted / declined
        if  c.props[id_prop].state=="locked":
            c.props[id_prop].state=get_decision(c,id_prop)
        
        print("prop",id_prop,"is",c.props[id_prop].state)

def get_decision(c,id_prop):
    s=0
    for user in c.props[id_prop].users:
        s+=c.props[id_prop].decision[user].value
    if s>=0:return "accepted"
    if s<0:return "declined"

def switch_channel_dim(npa,option):
    if option==1:
        n,n0,n1,n2=np.shape(npa)
        npa1=copy.deepcopy(npa)
        npa2=np.zeros((n,n1,n2,n0),dtype=np.uint8)#dtype=type(npa[0,0,0,0]))
        #for i_sample in range(n):
        for i_sample in range(1):
            for i in range(n0):
                for j in range(n1):
                    for k in range(n2):
                        v=npa1[i_sample,i,j,k]
                        v=(v+1)/2
                        v=v*255
                        v=np.round(v)
                        v=np.uint8(v)
                        npa2[i_sample,j,k,i]=v
    if option==2:
        n,n0,n1,n2=np.shape(npa)
        npa1=copy.deepcopy(npa)
        npa2=np.zeros((n,n1,n2,n0),dtype=np.uint8)#dtype=type(npa[0,0,0,0]))
        #for i_sample in range(n):
        for i_sample in range(1):
            for i in range(n0):
                for j in range(n1):
                    for k in range(n2):
                        v=npa1[i_sample,i,j,k]
                        '''
                        v=(v+1)/2
                        v=v*255
                        v=np.round(v)
                        v=np.uint8(v)
                        '''
                        npa2[i_sample,j,k,i]=v
    return npa2


## data
## pytorch

def get_images_from_dataloader1(dataloader,option):
    '''
    (n_samples, 1, w, h)
    '''
    npa=dataloader_to_npa(dataloader)

    npa=denormalize_dataset_tanh_color3(npa,255)

    images=get_images_from_npa(npa[:5,0,:,:])
    #display_images(images)
    return images

def show_images_dataloader(dataloader,option):
    for i in range(5):
        dataiter = iter(dataloader)
        images, labels = dataiter.next()
        npa=images.numpy()#[3]
        print(np.shape(npa))
        npa=switch_channel_dim(npa,option)
        print(np.shape(npa))
        #display(get_image_from_npa(npa[0,:,:,0]))
        display(get_image_from_npa(npa[0]))
        
def resize_dataset_x(x,n,option):

    if option=="dim first":
        
        n_samples=len(x)
        x_new=np.zeros((n_samples,n,n,3),dtype=np.uint8)
        for i_sample in range(n_samples):
            v=resize_image(go3D(x[i_sample]),n)
            x_new[i_sample]=v
    
    if option=="no chan":
        
        n_samples=len(x)
        x_new=np.zeros((n_samples,n,n),dtype=np.uint8)
        for i_sample in range(n_samples):
            v=resize_image(x[i_sample],n)
            x_new[i_sample]=v
        return x_new
    
    if option=="chan first":
    
        n_samples=len(x)
        n_channels=3
        x_new=np.zeros((n_samples,n_channels,n,n),dtype=np.uint8)

        for i_sample in range(n_samples):
            for i_chan in range(n_channels):
                v=resize_image(x[i_sample,i_chan],n)
                x_new[i_sample,i_chan]=v
    
    return x_new

def get_inputs_shape_from_dataloader(dataloader):
    ok=1
    for i, data in enumerate(dataloader, 0):
        if ok:
            # get the inputs
            inputs, labels = data
            ok=0
    sh=np.shape(inputs[0].numpy())
    return (1,sh[0],sh[1])

if 1==0:

    dataiter = iter(train_loader)
    images, labels = dataiter.next()
    npa=images.numpy()[3]
    print(np.shape(npa))
    display(get_image_from_npa(npa[0]))

import torch
import torch.nn as nn
import torch.functional as F
import numpy as np

## model : vgan0
## pytorch

#'''
class Generator(nn.Module):

    def __init__(self,model_type,z_dim=100):
        super(Generator, self).__init__()

        self.model_type = model_type
        self.image_shape = {'mnist':(1,28,28),
                            'cifar10':(3,32,32)
                        }
        self.models = nn.ModuleDict({
            'mnist': nn.Sequential(
                        nn.Linear(z_dim,128,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(128,256,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(256,512,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(512,1024,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(1024,int(np.prod(self.image_shape[model_type]))),
                        nn.Tanh()
                    ),
            'cifar10':nn.Sequential(
                        nn.Linear(z_dim,128,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(128,256,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(256,512,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(512,1024,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(1024,2048,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(2048,int(np.prod(self.image_shape[model_type]))),
                        nn.Tanh()
                    )
                })

    def forward(self, z):
        img = self.models[self.model_type](z)
        img = img.view(img.size(0), *self.image_shape[self.model_type])
        return img

class Discriminator(nn.Module):

    def __init__(self,model_type):
        super(Discriminator, self).__init__()

        self.model_type = model_type
        self.image_shape = {'mnist':(1,28,28),
                            'cifar10':(3,32,32)
                        }
        self.models = nn.ModuleDict({
                'mnist':nn.Sequential(
                            nn.Linear(int(np.prod(self.image_shape[model_type])), 512),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(512, 256),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(256, 1),
                            nn.Sigmoid(),
                    ),
                'cifar10':nn.Sequential(
                            nn.Linear(int(np.prod(self.image_shape[model_type])), 1024),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(1024,512),
                            nn.LeakyReLU(0.2,inplace=True),
                            nn.Linear(512, 256),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(256, 1),
                            nn.Sigmoid(),
                    )
                })

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        output = self.models[self.model_type](img_flat)
        return output
#'''

## basics
## pytorch

def get_torch_batch_noise(batch_size,noise_dim,device):
    noise=Variable(torch.Tensor(np.random.normal(0, 1, (batch_size, noise_dim)))).to(device)
    if device!=None:noise=noise.to(device)
    return noise

def get_torch_vector(n_values,value,device):
    vector=Variable(torch.Tensor(n_values,1).fill_(value), requires_grad=False).to(device)
    return vector


if 1==0:

    v=x.item() # get value from a pytorch tensor x containing a single value
    npa=x.numpy() # get numpy array from a pytorch tensor x

## model_vgan2
## fw_pytorch

class Generator2(nn.Module):
    def __init__(self,sample_shape,z_dim=100):
        super(Generator2, self).__init__()
        self.sample_shape=sample_shape

        '''
        sample_shape=1,7,3
        '''

        
        self.models = nn.ModuleDict({
            'gen2': nn.Sequential(
                        nn.Linear(z_dim,128,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(128,256,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(256,512,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(512,1024,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.Linear(1024,int(np.prod(self.sample_shape))),
                        nn.Tanh()
                    ),
                })
        '''

        self.models = nn.ModuleDict({
            'gen2': nn.Sequential(
                        nn.Linear(z_dim,128,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.BatchNorm2d(100)
                        nn.Linear(128,256,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.BatchNorm2d(100)
                        nn.Linear(256,512,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.BatchNorm2d(100)
                        nn.Linear(512,1024,bias=True),
                        nn.LeakyReLU(0.2,inplace=True),
                        nn.BatchNorm2d(100)
                        nn.Linear(1024,int(np.prod(self.sample_shape))),
                        nn.Tanh()
                    ),
                })
        '''
        

    def forward(self, z):
        img = self.models['gen2'](z)
        img = img.view(img.size(0), *self.sample_shape)
        return img


class Classifier1(nn.Module):
    def __init__(self,sample_shape,n_classes):
        super(Classifier1, self).__init__()
        self.sample_shape=sample_shape
        
        '''
        sample_shape=1,7,3
        '''

        self.models = nn.ModuleDict({
                'dsc2':nn.Sequential(
                            nn.Linear(int(np.prod(self.sample_shape)), 512),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(512, 256),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(256, n_classes),
                            nn.Sigmoid(),
                    )
                })

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        output = self.models['dsc2'](img_flat)
        return output

class Discriminator2(nn.Module):
    def __init__(self,sample_shape):
        super(Discriminator2, self).__init__()
        self.sample_shape=sample_shape
        '''
        sample_shape=1,7,3
        '''

        self.models = nn.ModuleDict({
                'dsc2':nn.Sequential(
                            nn.Linear(int(np.prod(self.sample_shape)), 512),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(512, 256),
                            nn.LeakyReLU(0.2, inplace=True),
                            nn.Linear(256, 1),
                            nn.Sigmoid(),
                    )
                })

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        output = self.models['dsc2'](img_flat)
        return output


## process_data
## fw_pytorch

from torchvision.datasets import  mnist,cifar
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

class DataLoad_gt8():

    def __init__(self):
        pass


    def load_data_mnist_gt8(self,batch_size=128):
        '''
        Returns a nested structure of tensors based on MNIST database.
        Will be divided into (60000/batch_size) batches of (batch_size) each.
        '''
        mnist_data = mnist.MNIST(root='./data/mnist',train=True,download=True,transform=transforms.Compose(
                                                 [transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]))
        mnist_loader = DataLoader(mnist_data,batch_size=batch_size,shuffle=True)
        return mnist_loader

    def load_data_cifar10_gt8(self,batch_size=128):
        '''
        Returns a nested structure of tensors based on CIFAR10 database.
        Will be divided into (60000/batch_size) batches of (batch_size) each.
        '''
        cifar_data = cifar.CIFAR10(root='./data/cifar10',train=True,download=True,transform=transforms.Compose(
                                                 [transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]))
        cifar_loader = DataLoader(cifar_data,batch_size=batch_size,shuffle=True)
        return cifar_loader

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.utils.data import TensorDataset, DataLoader

def dataloader_to_npa(dataloader):
    dataiter = iter(dataloader)
    images, labels = dataiter.next()
    npa=images.numpy()#[3]
    return npa

def tvd_to_dataloader(x_npa,batch_size): # tvd : torchvision dataset
    p="/home/paintedpalms/rdrive/taff/code/data/celeba"
    x_dataset = dset.ImageFolder(root=dataroot,
                            transform=transforms.Compose([
                                transforms.Resize(image_size),
                                transforms.CenterCrop(image_size),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                            ]))
    x_loader = torch.utils.data.DataLoader(dataset=x_dataset, batch_size=batch_size, shuffle=True)
    return x_loader

def npa_to_dataloader(x_npa,y_npa,batch_size):
    x_tensor = torch.Tensor(x_npa) # transform to torch tensor
    y_tensor = torch.Tensor(y_npa)
    dataset = TensorDataset(x_tensor,y_tensor) # create your dataset
    loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)
    return loader

def preprocess_mnist1(x,y,sample_size,option):
    ''' # mnist keras
    (x_train_keras, y_train_keras), (x_test_keras, y_test_keras) = tf.keras.datasets.mnist.load_data()
    '''
    if option=="mnist keras":
        x=resize_dataset_x(x,sample_size,"dim first")
        x=np.expand_dims(x[:,:,:,0], axis=1)
        x=go3D_dataset(x,1)
        y=np.expand_dims(y, axis=1)
    return x,y
            
'''
def load_data_priv(option):

    if option == 1:

        dataroot="/home/paintedpalms/rdrive/taff/code/data/celeba"
        dataset = dset.ImageFolder(root=dataroot,
                                   transform=transforms.Compose([
                                       transforms.Resize(image_size),
                                       transforms.CenterCrop(image_size),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                   ]))

        print("type of dataset",type(dataset))
        
        # Create the dataloader
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                                 shuffle=True, num_workers=workers)


    if option==2:

        #bs=150
        #ns=100
        bs=batch_size

        (x_train_keras, y_train_keras), (x_test_keras, y_test_keras) = tf.keras.datasets.mnist.load_data()
        x_train_keras=resize_dataset_x(x_train_keras,image_size,"dim first")
        x_test_keras=resize_dataset_x(x_test_keras,image_size,"dim first")
        x_train_keras=np.expand_dims(x_train_keras[:,:,:,0], axis=1)
        y_train_keras=np.expand_dims(y_train_keras, axis=1)
        x_test_keras=np.expand_dims(x_test_keras[:,:,:,0], axis=1)
        y_test_keras=np.expand_dims(y_test_keras, axis=1)
        x_train_keras=go3D_dataset(x_train_keras,1)
        x_test_keras=go3D_dataset(x_test_keras,1)
        if 1==0:
            npa=x_train_keras[0]
            print(np.shape(npa))
            img=get_image_from_npa(npa)
            display(img)
        x_tensor_train = torch.Tensor(x_train_keras) # transform to torch tensor
        y_tensor_train = torch.Tensor(y_train_keras)
        x_tensor_test = torch.Tensor(x_test_keras) # transform to torch tensor
        y_tensor_test = torch.Tensor(y_test_keras)

        dataset_train = TensorDataset(x_tensor_train,y_tensor_train ) # create your dataset
        
        dataset_test = TensorDataset(x_tensor_test,y_tensor_test ) # create your dataset
        
        # gt7 data loader
        if 1==0:my_dataloader = DataLoader(my_dataset) # create your dataloader

        # Data Loader (Input Pipeline)
        train_loader = torch.utils.data.DataLoader(dataset=dataset_train, batch_size=bs, shuffle=True)
        test_loader = torch.utils.data.DataLoader(dataset=dataset_test, batch_size=bs, shuffle=False)

        dataloader=train_loader

    return dataloader
'''


## random
## seed


import numpy as np

import torch
    
if 1==0:

    seed=0

    # standard
    torch.manual_seed(seed)
    torch.manual_seed_all(seed)

    # cuda
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)










## deprec
def get_score_ratio(score_gen,score_real):
    return get_comparative_score(score_gen,score_real)
