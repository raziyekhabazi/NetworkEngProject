from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pws
from googlesearch import search


# ba47ec4286393d52f9b79db089d7573e8067384f6b23a6c9f80890d59355cb17 #maryam

class SearchAPIView(APIView):
    # lists = [['linka', 'linkc'], ['linkb', 'linkd', 'linka'], ['linkb', 'linka', 'linkc', 'linkd']]
    # ['linkb', 'linka', 'linkc', 'linkd']
    def borda_sort(self, lists):
        scores = {}
        for l in lists:
            for idx, elem in enumerate(reversed(l)):
                if not elem[0] in scores:
                    scores[elem] = 0
                scores[elem] += idx
        return sorted(scores.keys(), key=lambda elem: scores[elem], reverse=True)

    def get(self, request, format=None):
        # try:
        query = request.GET['query']
        # page = request.GET['page']
        l1 = []
        l2 = []
        l3 = []
        lists = []

        from serpapi import GoogleSearch

        # yahoo
        params = {
            "engine": "yahoo",
            "p": query,
            # "b": "101",
            "pz": "2",
            "vm": "p",
            "vs": ".com,.org,.cn",
            "yahoo_domain": "de",
            "api_key": "ba47ec4286393d52f9b79db089d7573e8067384f6b23a6c9f80890d59355cb17"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results['organic_results']
        for i in organic_results:
            if 'snippet' in i.keys():
                ltemp_yahoo = (i['link'], i['title'], i['displayed_link'], i['snippet'])
            l1.append(ltemp_yahoo)
        lists.append(l1)

        # google
        params = {
            "engine": "google",
            "q": query,
            "location": "Seattle-Tacoma, WA, Washington, United States",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "num": "2",
            # "start": "10",
            "safe": "active",
            "api_key": "ba47ec4286393d52f9b79db089d7573e8067384f6b23a6c9f80890d59355cb17"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results['organic_results']
        for i in organic_results:
            ltemp_google = (i['link'], i['title'], i['displayed_link'], i['snippet'])
            l2.append(ltemp_google)
        lists.append(l2)

        # bing
        params = {
            "engine": "bing",
            "q": query,
            "safeSearch": "strict",
            # "first": "10",
            "count": "2",
            "api_key": "ba47ec4286393d52f9b79db089d7573e8067384f6b23a6c9f80890d59355cb17"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results['organic_results']
        for i in range(len(organic_results)):
            ltemp_bing = (organic_results[i]['link'], organic_results[i]['title'], organic_results[i]['displayed_link'], organic_results[i]['snippet'])
            l3.append(ltemp_bing)
        lists.append(l3)

        answer = self.borda_sort(lists)
        answer_list = []
        for a in answer:
            d = {'link': a[0], 'title': a[1], 'displayed_link': a[2], 'snippet': a[3]}
            answer_list.append(d)
        dc = {'count_of_result': len(answer_list)}
        print(dc)

        return Response({'data': answer_list}, status=status.HTTP_200_OK)

    # except:
    #     return Response({'status': "Internal Server Error, We'll Check It Later"},
    #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
