import os
import csv
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta, date

l=[]
m=[]
n=[]
p=[]
p2=[]
p3=[]
p4=[]
p5=[]
l1=[]
l2=[]
l3=[]
l4=[]
l5=[]
l6=[]
l7=[]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def dash_view(request):
    global l,m,n
    l=[]
    m=[]
    n=[]
    error = False
    file = os.path.join(os.path.join(BASE_DIR, "graph"),'Top_lanes.csv')
    file1 = os.path.join(os.path.join(BASE_DIR, "graph"),'FMC_data_1.csv')
    csv_file = open(file, 'r')
    csv_file1 = open(file1, 'r')
    x = csv.reader(csv_file, delimiter=',')
    x1 = csv.reader(csv_file1, delimiter=',')
    d=str(request.GET.get("d"))
    d1 = str(request.GET.get("d1"))
    f = str(request.GET.get("start")).upper()
    t = str(request.GET.get("end")).upper()
    if not d or not f or not t:
        error = True
    if not d1:
        d1 = d
    if not error:
        c = f + "->" + t
        xd = d.split('-')
        try:
            d = date(int(xd[0]),int(xd[1]),int(xd[2]))
            xd1=d1.split('-')
            d1 = date(int(xd1[0]),int(xd1[1]),int(xd1[2]))
            ro = daterange(d,d1)
            ro1=[r.strftime("%Y-%m-%d") for r in ro]
        except:
            ro1=[]

        filtered = [row for row in x if row[1] in ro1 and row[0] == c]
        filtered1 = [row for row in x1 if row[3] in ro1 and row[2] == c]
        for i in filtered:
            o = i[2].split(" ")
            if d != d1:
                l.append(o[0]+' '+i[1])
            else:
                l.append(o[0])
            m.append(float(i[3]))
            n.append(float(i[4]))
         #   p2.append(float(i[5]))
          #  p3.append(float(i[6]))
           # p4.append(float(i[7]))
            #p5.append(float(i[8]))
        n1=[]
        n2 = []
        row = False
        for i in filtered1:
            if i[5] != '':
                n1.append(float(i[5]))
        for i in filtered1:
            if i[5]=='':
                i[5]='Canceled'
            if i[4]==i[8] and i[9]=='AM':
                i[8]='----'
                i[9]='----'
            n2.append([i[0],i[1],i[4],i[5],i[7],i[8],i[9]])
        svl=[i for i in filtered if i[2]=='01:00 PDT']
        if n2:
            for i in n2:
                if i[1]=='FindWork':
                    i[1]='Adhoc booked'
                    row = True
                else:
                    i[1]=''

        try:
            sv=float(svl[0][4])
        except:
            sv=0
        sum1=sum(n1)#+sum(n)
        fv = sv - sum1
        if n2:
            xuv=n2[0][2]
        else:
            xuv=0
        for i in n2:
            x = i[-2].split(':')
            if n2[-1]=='PM':
                if int(x[1]):
                    x[0]=int(x[0])+1
                x1 = int(x[0])+12
                x[0]=x1
            x.pop()
            i[-2] = ':'.join(x)
            if i[-3]==d:
                p.append(i[-2])
        context={'c':c,'d':d,'d1':d1,'cpt':n2,'sum':sum1,'fv':fv,'sv':sv,'cpt1':xuv,'row':row}
        return render(request,"dash.html",context)
    else:
        return render(request, "dash.html", {'error':error})

def percentile(request):
    global l1,l2,l3,l4,l5,l6,l7
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    l7 = []
    file = os.path.join(os.path.join(BASE_DIR, "graph"), 'Top_15_coordinates.csv')
    csv_file = open(file, 'r')
    x = csv.reader(csv_file, delimiter=',')
    #d = str(request.GET.get("d"))
    f = str(request.GET.get("start")).upper()
    t = str(request.GET.get("end")).upper()
    c = f + "->" + t
    c1=0
    filtered = [row for row in x if row[2] == c]
    print(filtered)
    for i in filtered:
        l1.append(i[4])
        l2.append(float(i[5]))
        l3.append(float(i[6]))
        l4.append(float(i[11]))
        l5.append(float(i[12]))
        l6.append(float(i[17]))
        l7.append(float(i[18]))
        c1 =i[3]
    context={"c":c,"cpt1":c1}
    return render(request,'dash1.html',context)
# Create your views here.
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        usernames =(l,m,n,p)
        return Response(usernames)
class ChartData1(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        usernames1 =(l1,l2,l3,l4,l5,l6,l7)
        return Response(usernames1)
