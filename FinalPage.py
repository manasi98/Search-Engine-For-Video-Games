#!/usr/bin/env python
# coding: utf-8


import json
from typing import OrderedDict
from whoosh.index import create_in
from whoosh.fields import *
import streamlit as st
import streamlit.components.v1 as components
from whoosh.qparser import QueryParser
from googleapiclient.discovery import build
from operator import itemgetter
from whoosh import index
import json
import os,os.path
from whoosh.fields import Schema, ID, TEXT,STORED
from whoosh.qparser import QueryParser
import whoosh.index as index
from Association_Cluster import association_main
from Metric_Clusters import metric_cluster_main
from Scalar_Clustering import scalar_main





#ix = index.open_dir('indexdir')
def parse_whoosh_results(whoosh_results):
    if len(whoosh_results.top_n) == 0:
        return ("query out of scope")
    else:
        api_resp = list()
        rank = 0
        for result in whoosh_results:
            rank += 1
            title = ""
            url = ""
            description = ""
            if 'title' in result:
                title = result['title']
            if 'url' in result:
                url = result['url']
            if 'description' in result:
                description = result['description']
            link_json = {
                "title": title,
                "url": url,
                "description":description,
                "rank": rank
            }
            api_resp.append(link_json)
    return api_resp



#authority_file = open("authority_scores_full.txt","r")
pagerank_file = open("pagerank_full.txt","r")


#authority_line = authority_file.readline()
pagerank_line = pagerank_file.readline()



#authority_scores = json.loads(authority_line)
pagerank = json.loads(pagerank_line)






schema = Schema(url=ID(stored=True, unique=True), title=TEXT(stored=True), developer=TEXT, description=TEXT(stored=True),  doc=STORED)
#if not os.path.exists("indexdir"):
    #os.mkdir("indexdir")
#crawl = open("games.json","r")

ix = index.open_dir('indexdir')
#ix = create_in("indexdir", schema)
#writer = ix.writer()
#line = crawl.readline()
#while line:
    #line_dict = json.loads(line)
    #print(line_dict)
    #if 'developer' not in line_dict.keys():
        #line_dict['developer'] = ''

    #if 'description' in line_dict.keys():
        #if 'title' not in line_dict.keys():
            #line_dict['title'] = line_dict['app_name']
        #writer.add_document(url=line_dict['url'],title=line_dict['title'],developer=line_dict['developer'],description=line_dict['description'])
    #elif 'title' in line_dict.keys():
        #writer.add_document(url=line_dict['url'],title=line_dict['title'],developer=line_dict['developer'],description=line_dict['title'])
    
    #line = crawl.readline()

#writer.commit() 


st.title("Search Engine for video games")
 
searchterm = st.text_input('SearchQuery', 'Video Game')

urllist = []
titlelist = []
desclist = []
with ix.searcher() as searcher:
  doclist = []
  query = QueryParser("description", ix.schema).parse(searchterm)
  doclist = list(query.docs(searcher))
  results = searcher.search(query,limit=20)
  st.write(results)
  results_mod = []
  #change len(doclist to 0,20 later)
  
  for i in range(len(results.top_n)):
    results_mod.append({})
  for i in range(len(results.top_n)):
    results_mod[i]['url'] = results[i]['url']
    #urllist[i] = results[i]['url']
    results_mod[i]['title'] = results[i]['title']
    #titlelist[i] = results[i]['title']
    results_mod[i]['description'] = results[i]['description']
    #desclist[i]= results[i]['description']
  
  relevance = st.checkbox("Relevance Model")
  st.write("Link Analysis")
  pagerankcb = st.checkbox("PageRank")
  hitscb = st.checkbox("HITS")
  st.write("Clustering")
  fclustering = st.checkbox("Flat Clustering")
  aggclustering = st.checkbox("Agglomorative Clustering")
  st.write("Query Expansion")
  association = st.checkbox("Association")
  metric = st.checkbox("Metric")
  scalar = st.checkbox("Scalar")
  st.write("Search Engine")
  google = st.checkbox("Google")
  bing = st.checkbox("Bing")
  #relevance = st.radio("Link Analysis :",('Relevance Model','PageRank', 'HITS','Flat Clustering','Agglomorative Clustering','Association','Metric','Scalar','Google','Bing'))



  

  if relevance==True and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
      st.write('You selected Relevance Model.')
      for i in range(len(results_mod)):
        #st.write(results_mod[i])
        st.write(i+1)
        st.subheader(results_mod[i]['title'])
        st.write("URL :",results_mod[i]['url'])
        st.write(results_mod[i]['description'][0:200])
        st.write(" ")

  elif relevance==True and pagerankcb==True and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    #doclist2=[]


    pagerank_file = open("pagerank_full.txt","r")
    pagerank_line = pagerank_file.readline()
    pagerank = json.loads(pagerank_line)

    st.write("You selected PageRank.")
    pagerank = {x.replace(' ', ''): v 
    for x, v in pagerank.items()}
    
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      results_mod = []
      # for i in range(20):
      #   results_mod.append({})
      for i in range(len(results.top_n)):
        result_dict = {}
        #results_mod[i]['url'] = results[i]['url']
        result_dict['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        result_dict['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        result_dict['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if result_dict['url'] in pagerank.keys():
          result_dict['score'] = pagerank[results[i]['url']]
        else:
          result_dict['score'] = 0.001*i
        results_mod.append(result_dict)
      count = 1
      for value in sorted(results_mod, key=itemgetter('score'), reverse=True):
        st.write(count)
        count+=1
        st.subheader(value['title'])
        st.write("URL :",value['url'])
        st.write(value['description'][0:200])
        st.write("SCORE : ",value['score'])
        #st.write(" ")

  elif relevance==True and pagerankcb==False and hitscb==True and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    #doclist2=[]
    authority_file = open("authority_scores_full.txt","r")
    authority_line = authority_file.readline()
    authority_scores = json.loads(authority_line)
    st.write("HITS was selected")


    authority_scores = {x.replace(' ', ''): v 
    for x, v in authority_scores.items()}
    # max_key = max(authority_scores, key=authority_scores.get)
    # st.write(max_key)
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      results_mod = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in authority_scores.keys():
          results_mod[i]['score'] = authority_scores[results[i]['url']]
        else:
          results_mod[i]['score'] = 0.001*i
    count = 0
    for value in sorted(results_mod, key=itemgetter('score'), reverse=True):
      st.write(count+1)
      count+=1
      st.subheader(value['title'])
      st.write("URL : ",value['url'])
      st.write(value['description'][0:200])
      #st.write("SCORE : ",value['score'])
      #st.write(" ")

  elif relevance==True and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==True and association==False and metric==False and scalar==False and google==False and bing==False:
    #st.write("under construction")
    #doclist2=[]
    hcluster_file = open("hclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Agglomorative clustering with vector relevance model")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue
    #hcluster_scores = {x.replace(' ', ''): v 
    #for x, v in hcluster_scores.items()}
    
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      
      hresults = []
      cset = []
      final_result = []
      results_mod = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
      count = 0
      for value in final_result:
        st.write(count+1)
        count+=1
        st.subheader(value['title'])
        st.write("URL : ",value['url'])
        st.write(value['description'][0:200])
        #st.write(value['cluster'])
      #st.write("SCORE : ",value['score'])
      #st.write(" ")

    
    
    
    # cset = []

    # for c in hcluster_scores.values():
    #   if c not in cset:
    #     cset.append(c)
    # #print(cset)
    # result = []
    # for i in cset:
    #   for key,values in dict1.items():
    #     if values == i:
    #       result.append(key)
    #   print(result)

  elif relevance==True and pagerankcb==False and hitscb==False and fclustering==True and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    #st.write("under construction")
    #doclist2=[]
    hcluster_file = open("fclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Flat clustering with vector relevance model")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue
    #hcluster_scores = {x.replace(' ', ''): v 
    #for x, v in hcluster_scores.items()}
    
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      
      hresults = []
      cset = []
      final_result = []
      results_mod = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
      count = 0
      for value in final_result:
        st.write(count+1)
        count+=1
        st.subheader(value['title'])
        st.write("URL : ",value['url'])
        st.write(value['description'][0:200])
        #st.write(value['cluster'])

  elif relevance==True and pagerankcb==False and hitscb==True and fclustering==True and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    authority_file = open("authority_scores_full.txt","r")
    authority_line = authority_file.readline()
    authority_scores = json.loads(authority_line)
    hcluster_file = open("fclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Flat clustering with HITS")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue


    authority_scores = {x.replace(' ', ''): v 
    for x, v in authority_scores.items()}
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      
      #st.write(searchterm)
      results_mod = []
      hresults = []
      cset = []
      final_result = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in authority_scores.keys():
          results_mod[i]['score'] = authority_scores[results[i]['url']]
        else:
          results_mod[i]['score'] = 0.001*i
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
    count = 0
    temp_result=[]
    k=0
    for value in sorted(results_mod, key=itemgetter('score'),reverse=True):
      temp_result.append(value)
      k+=1
    for j in cset:
      for result_dict in results_mod:
        if result_dict['cluster'] == j:
          final_result.append(result_dict)

    for value in final_result:
      st.write(count+1)
      count+=1
      st.subheader(value['title'])
      st.write("URL : ",value['url'])
      st.write(value['description'][0:200])

  elif relevance==True and pagerankcb==True and hitscb==False and fclustering==True and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    authority_file = open("pagerank_full.txt","r")
    authority_line = authority_file.readline()
    authority_scores = json.loads(authority_line)
    hcluster_file = open("fclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Flat clustering with PageRank")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue


    authority_scores = {x.replace(' ', ''): v 
    for x, v in authority_scores.items()}
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      results_mod = []
      hresults = []
      cset = []
      final_result = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in authority_scores.keys():
          results_mod[i]['score'] = authority_scores[results[i]['url']]
        else:
          results_mod[i]['score'] = 0.001*i
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
    count = 0
    temp_result=[]
    k=0
    for value in sorted(results_mod, key=itemgetter('score'),reverse=True):
      temp_result.append(value)
      k+=1
    for j in cset:
      for result_dict in results_mod:
        if result_dict['cluster'] == j:
          final_result.append(result_dict)

    for value in final_result:
      st.write(count+1)
      count+=1
      st.subheader(value['title'])
      st.write("URL : ",value['url'])
      st.write(value['description'][0:200])
  
  elif relevance==True and pagerankcb==True and hitscb==False and fclustering==False and aggclustering==True and association==False and metric==False and scalar==False and google==False and bing==False:
    authority_file = open("pagerank_full.txt","r")
    authority_line = authority_file.readline()
    authority_scores = json.loads(authority_line)
    hcluster_file = open("hclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Agglomorative clustering with PageRank")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue


    authority_scores = {x.replace(' ', ''): v 
    for x, v in authority_scores.items()}
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      results_mod = []
      hresults = []
      cset = []
      final_result = []
      for i in range(len(results.top_n)):
        results_mod.append({})
      for i in range(len(results.top_n)):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in authority_scores.keys():
          results_mod[i]['score'] = authority_scores[results[i]['url']]
        else:
          results_mod[i]['score'] = 0.001*i
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
    count = 0
    temp_result=[]
    k=0
    for value in sorted(results_mod, key=itemgetter('score'),reverse=True):
      temp_result.append(value)
      k+=1
    for j in cset:
      for result_dict in results_mod:
        if result_dict['cluster'] == j:
          final_result.append(result_dict)

    for value in final_result:
      st.write(count+1)
      count+=1
      st.subheader(value['title'])
      st.write("URL : ",value['url'])
      st.write(value['description'][0:200])

  elif relevance==True and pagerankcb==False and hitscb==True and fclustering==False and aggclustering==True and association==False and metric==False and scalar==False and google==False and bing==False:
    authority_file = open("pagerank_full.txt","r")
    authority_line = authority_file.readline()
    authority_scores = json.loads(authority_line)
    hcluster_file = open("hclusters.txt","r")
    hcluster_line = hcluster_file.readlines()
    st.write("Agglomorative clustering with HITS")
    #hcluster_scores = json.loads(hcluster_line)
    hcluster_scores = {}
    for i in hcluster_line:
      hc_split = i.split(',')
      #st.write(hc_split)
      try:
        hcluster_scores[hc_split[0]] = hc_split[1]
      except:
        continue


    authority_scores = {x.replace(' ', ''): v 
    for x, v in authority_scores.items()}
    with ix.searcher() as searcher:
      #doclist2 = list(query.docs(searcher))
      query = QueryParser("description", ix.schema).parse(searchterm)
      results = searcher.search(query,limit=20)
      #st.write(searchterm)
      results_mod = []
      hresults = []
      cset = []
      final_result = []
      for i in range(10):
        results_mod.append({})
      for i in range(10):
        results_mod[i]['url'] = results[i]['url']
        #urllist[i] = results[i]['url']
        results_mod[i]['title'] = results[i]['title']
        #titlelist[i] = results[i]['title']
        results_mod[i]['description'] = results[i]['description']
        #desclist[i]= results[i]['description']
        if results[i]['url'] in authority_scores.keys():
          results_mod[i]['score'] = authority_scores[results[i]['url']]
        else:
          results_mod[i]['score'] = 0.001*i
        if results[i]['url'] in hcluster_scores.keys():
          results_mod[i]['cluster'] = hcluster_scores[results[i]['url']]
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
        else:
          results_mod[i]['cluster'] = 99
          if results_mod[i]['cluster'] not in cset:
            cset.append(results_mod[i]['cluster'])
      for j in cset:
        for result_dict in results_mod:

          if result_dict['cluster'] == j:
            final_result.append(result_dict)
    count = 0
    temp_result=[]
    k=0
    for value in sorted(results_mod, key=itemgetter('score'),reverse=True):
      temp_result.append(value)
      k+=1
    for j in cset:
      for result_dict in results_mod:
        if result_dict['cluster'] == j:
          final_result.append(result_dict)

    for value in final_result:
      st.write(count+1)
      count+=1
      st.subheader(value['title'])
      st.write("URL : ",value['url'])
      st.write(value['description'][0:200])
  
  elif relevance==True and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==True and metric==False and scalar==False and google==False and bing==False:
    #st.write("under construction....")
    query = QueryParser("description", ix.schema).parse(searchterm)
    results = searcher.search(query,limit=20)

    expanded_query = association_main(searchterm, results)
    st.write("Association Cluster")
            
    query = QueryParser("description", ix.schema).parse(expanded_query)
    results_qe = searcher.search(query,limit=20)
    results = parse_whoosh_results(results_qe)
    st.write("----------")
    st.write("**Expanded Query: "+expanded_query+"**")
    st.write("----------")
    if(results_qe.top_n!=0):
      for i in results_qe:
        #st.write(i)
        #st.write(i)
        st.subheader(i['title'])
        st.write("URL : ",i['url'])
        st.write(i['description'][0:200])
    else:
      st.write("no results found")

  elif relevance==True and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==True and scalar==False and google==False and bing==False:
    #st.write("under construction....")
    st.write("Metric Cluster")
    query = QueryParser("description", ix.schema).parse(searchterm)
    results = searcher.search(query,limit=20)

    expanded_query = metric_cluster_main(searchterm, results)
            
    query = QueryParser("description", ix.schema).parse(expanded_query)
    results_qe = searcher.search(query,limit=20)
    results = parse_whoosh_results(results_qe)
    st.write("----------")
    st.write("**Expanded Query: "+expanded_query+"**")
    st.write("----------")
    for i in results:
      #st.write(i)
      st.subheader(i['title'])
      st.write("URL : ",i['url'])
      st.write(i['description'][0:200])

  elif relevance==True and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==True and google==False and bing==False:
    #st.write("under construction....")
    st.write("Scalar Cluster")
    query = QueryParser("description", ix.schema).parse(searchterm)
    results = searcher.search(query,limit=20)

    expanded_query = association_main(searchterm, results)
            
    query = QueryParser("description", ix.schema).parse(expanded_query)
    results_qe = searcher.search(query,limit=20)
    results = parse_whoosh_results(results_qe)
    st.write("----------")
    st.write("**Expanded Query: "+expanded_query+"**")
    st.write("----------")
    for i in results:
      st.subheader(i['title'])
      st.write("URL : ",i['url'])
      st.write(i['description'][0:200])

  # elif relevance==True and pagerankcb==True and hitscb==False and fclustering==False and aggclustering==False and association==True and metric==False and scalar==False and google==False and bing==False:
  #   #st.write("under construction....")
  #   query = QueryParser("description", ix.schema).parse(searchterm)
  #   results = searcher.search(query,limit=None)

  #   expanded_query = association_main(searchterm, results)
            
  #   query = QueryParser("description", ix.schema).parse(expanded_query)
  #   results_qe = searcher.search(query,limit=None)
  #   results = parse_whoosh_results(results_qe)
  #   st.write("----------")
  #   st.write("**Expanded Query: "+expanded_query+"**")
  #   st.write("----------")
  #   if results[i]['url'] in authority_scores.keys():
  #     results_mod[i]['score'] = authority_scores[results[i]['url']]
  #   else:
  #     results_mod[i]['score'] = 0.001*i
  #   for i in results:
  #     st.subheader(i['title'])
  #     st.write("URL : ",i['url'])
  #     st.write(i['description'][0:200])





  


  elif relevance==False and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==True and bing==False:

    #my_api_key = "AIzaSyBVWC68JcCxqDkwXog9TImX_Ht8Y1AXbGU"
    st.write("Google Search Results")
    #my_cse_id = "6943d84dd9b124a58"
    #service = build("customsearch", "v1", developerKey=my_api_key)
    #res = service.cse().list(
        #q=searchterm,
        #cx=my_cse_id,
      #).execute()
    #st.write(res['url'])
    components.iframe("https://www.google.com/search?q="+searchterm+"&igu=1", height=500, scrolling=True)

  

  elif relevance==False and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==True:
 
    # embed streamlit docs in a streamlit app
    components.iframe("https://www.bing.com/search?q="+searchterm, height=500, scrolling=True)
    st.write("Bing Search Results")
  
  elif relevance==False and pagerankcb==False and hitscb==False and fclustering==False and aggclustering==False and association==False and metric==False and scalar==False and google==False and bing==False:
    st.write("choose a combination")

  else: 
    st.subheader("Invalid Combination")
    st.write("An example of a valid combination: Relevance model, PageRank, Flat Clustering")




# else:
#   authority_scores = {x.replace(' ', ''): v 
#      for x, v in authority_scores.items()}
#   pagerank = {x.replace(' ', ''): v 
#      for x, v in pagerank.items()}
#   with ix.searcher() as searcher:
#     doclist = list(query.docs(searcher))
#     query = QueryParser("description", ix.schema).parse(searchterm)
#     results = searcher.search(query,limit=20)
#     st.write(searchterm)
#     results_mod = []

#     for i in range(len(doclist)):
#         results_mod.append({})

#     for i in range(len(doclist)):
#         results_mod[i]['url'] = results[i]['url']
#         results_mod[i]['title'] = results[i]['title']
#         results_mod[i]['description'] = results[i]['description']

#         if(genre == 'HITS'):
#             if results[i]['url'] in authority_scores.keys():
            
#                 results_mod[i]['score'] = authority_scores[results[i]['url']]
#             else:
#                 results_mod[i]['score'] = 0.001*i
#             for i in range(len(doclist)):
#               st.write(i+1)
#               st.write("TITLE : ",results_mod[i]['title'])
#               st.write("URL : ",results_mod[i]['url'])
#               st.write(results_mod[i]['description'][0:200])
#               st.write("SCORE : ",results_mod[i]['score'])
#               st.write(" ")

#         elif(genre == 'PageRank'):
#             if results[i]['url'] in pagerank.keys():
            
#                 results_mod[i]['score'] = pagerank[results[i]['url']]
#             else:
#                 results_mod[i]['score'] = 0.001*i
#             OrderedDict
#             for i in range(len(doclist)):
#               st.write(i+1)
#               st.write("TITLE : ",results_mod[i]['title'])
#               st.write("URL :",results_mod[i]['url'])
#               st.write(results_mod[i]['description'][0:200])
#               st.write("SCORE : ",results_mod[i]['score'])
#               st.write(" ")
#st.write('The current movie title is', title)

#components.iframe("https://docs.streamlit.io/en/latest")
#components.iframe("https://www.randomservices.org/")
#call of duty
#assassin's creed
#pubg
#angry birds
   



