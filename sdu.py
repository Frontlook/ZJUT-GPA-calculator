# coding=gbk
import urllib
import urllib2
import cookielib
import string
from bs4 import BeautifulSoup
import re
import sys
syscode=sys.getfilesystemencoding()

class SDU:
    def __init__(self,studentid,password):
        self.loginUrl = 'http://yjs.zjut.edu.cn/yjssql_xxjhpt/NewLoginCheck.asp'
        self.gradeUrl = 'http://yjs.zjut.edu.cn/yjssql_xxjhpt/index.asp?serviceType=lookForGrade-disp'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'typeid': '2',
            'user': studentid,
            'pass': password
        })
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                     'Referer': 'http://yjs.zjut.edu.cn/yjssql_xxjhpt/index.asp?serviceType=degreeQualification-Edit',
                     'Host':'yjs.zjut.edu.cn'
        }
        # 课程名
        self.one = []
        # 课程类型
        self.two= []
        self.two_1=[]
        # 学分
        self.three=[]
        self.three_1=[]
        # 成绩
        self.four=[]
        # 成绩2
        self.five=[]
        # 成绩转为绩点
        self.five_1=[]
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def getPage(self):
        request = urllib2.Request(
            url=self.loginUrl,
            data=self.postdata,
            headers=self.head
        )
        result = self.opener.open(request)
        result = self.opener.open(self.gradeUrl)
        # result.encoding = 'utf-8'
        # soup=BeautifulSoup(result, 'lxml',from_encoding="gbk").find('div',id='main-right').find_all('table')[2].find_all('tr')
        # self.jidian(soup)
        return result.read().decode('gbk')

    def jidian(self, soup):
        kechengming=[]
        gerenkecheng=[]
        for soup_a in soup:
            i=0
            for soup_b in soup_a.find_all('td'):
                if soup_a==soup[0]:
                    kechengming.append(soup_b.get_text())
                else:
                    gerenkecheng.append((kechengming[i],soup_b.get_text()))
                    i+=1

    def getGrades(self):
        # 获得本学期成绩页面
        page = self.getPage()
        output=[]
        # 正则匹配
        page2=re.findall('<table.*?>(.*?)</table>',page, re.S)
        myItems = re.findall('<tr.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<td.*?>(.*?)</td>.*?<td.*?<td.*?<td.*?<td.*?>(.*?)</td>.*?<td.*?</tr>', page2[1], re.S)
        for item in myItems:
            # print item[0]+item[1]+item[2]+item[3]
            self.one.append(item[0])
            self.two.append(item[1])
            self.three.append(item[2])
            self.four.append(item[3])
            six=re.findall('<strong.*?>(.*?)</strong>',item[3],re.S)
            for i in six:
                self.five.append(i)
            output.append(item)
            # output+=item[0]+'\r\n'+item[1]+'\r\n'+item[2]+'\r\n'+item[3]+'\r\n'
        return output
        # self.getGrade()

    def getGrade(self):
        # 计算总绩点
        sum = 0.0
        member=0.0#分子
        denominator = 0.0#分母

        length=len(self.five)
        for i in range(0,length):
            if self.two[i+1]==u'学位课':
                self.two_1.append(0.6)
            elif self.two[i+1]==u'选修课':
                self.two_1.append(0.25)
            else:
                self.two_1.append(0.15)

        for i in range(0,length):
            self.three_1.append(float(self.three[i+1]))

        for i in range(0,length):
            if self.five[i]==u'优' or self.five[i]==u'优秀':
                self.five_1.append(4.5)
            elif self.five[i]==u'良' or self.five[i]==u'良好':
                self.five_1.append(3.5)
            elif self.five[i]==u'中' or self.five[i]==u'中等':
                self.five_1.append(2.5)
            elif self.five[i]==u'及' or self.five[i]==u'及格':
                self.five_1.append(1.5)
            else:
                a=int(self.five[i])#2017-2-19 12:15:52
                if a<60:
                    self.five_1.append(0)
                else:
                    b=(a-50)/10.0
                    self.five_1.append(b)

        for i in range(length):
            member+=self.two_1[i]*self.five_1[i]*self.three_1[i]
            denominator+=self.two_1[i]*self.three_1[i]
        sum=member/denominator
        return sum


if __name__ == "__main__":
    sdu = SDU(studentid,password)
    sdu.getGrades()
    print sdu.getGrade()
