from urllib.request import urlopen
from bs4 import BeautifulSoup

import sys #argvの取得

#from queue import Queue
#import re

def parse(url_in):
    #URLを読み込み
    html = urlopen(url_in)
    soup = BeautifulSoup(html, "html.parser")

    '''
    h3タグを抜き出して、"入力"の部分を見つける。
    見つかったものがh3_indexに保存される。
    '''
    h3_index = -1
    h3 = soup.find_all("h3")

    inputformat=["入力","Input","Input Format"]
    for i in range(len(h3)):
        h3_str=h3[i].get_text()
        if(h3_str in inputformat):
            h3_index=i
            break
    #print("h3_index =",h3_index)

    '''
    この見つけたh3タグを頼りに、その次にあるpreタグを見つけることで
    入力の形式を取り出す。
    '''
    in_style=h3[h3_index].find_next_sibling("pre")
    #print(h3[h3_index])
    print(in_style.get_text())

    #見つからなかったのでダイレクトにpreタグを探しにいく
    if(in_style==None):
        print("<pre> not found")
        in_style = soup.find("pre")


    #check print
    #print(" --- raw ---")
    #print(in_style.get_text())


    #入力形式を行ごとのリストに分ける
    in_str=in_style.get_text().split("\r\n")
    #先頭と末尾はpreタグの分、空白なので除く
    del in_str[0]
    del in_str[-1]

    #print(in_str)

    '''
    変数表の作成
    行ごとに見ていく。
    _(アンダーバー)を見つけたら、その変数は配列型。
    '''
    #変数名と数・1次元配列・2次元配列の対応を記述
    var_dict = {}
    #横の"..."要素を集めた
    yoko = ["...","..","…","‥"]

    #print(" --- for each rows ---")

    #行ごとに見ていく
    for row in in_str:
        row_list=row.split(" ")
        print(row_list)

        if(row_list[0]==":" or row_list[0]=="："):
            continue
        else:
            for var in row_list:
                #横の...要素がないかチェック
                if(var in yoko):
                    continue
                if("_" in var):
                    content = var.split("_")
                    #print(content)
                    content_index = content[1]

                    ct=0
                    for i in content_index:
                        if(('a'<=i<='z')or('A'<=i<='Z')or('0'<=i<='9')):
                            ct+=1
                    #print("ct = ",ct)

                    if(ct==1):
                        var_dict[content[0]]="v"
                    elif(ct==2):
                        var_dict[content[0]]="v2"
                else:
                    var_dict[var] = "c"

    #完成した変数と数・1次元配列・2次元配列の対応表
    #print(" --- make dict --- (c:定数, v:1次元配列, v2:2次元配列)")
    #print(var_dict)


    '''
    "..."を見つけたら、その行内にベクトルがある。
    ":"を見つけたら、その前後は同じベクトルになる。
    '''

    #実際の形式を行ごとに入れていく
    cpp_input = []
    #v_q=queue.Queue()

    #行ごとに見ていく
    i=0
    while(i<len(in_str)):
        row_list=in_str[i].split(" ")

        for var in row_list:
            if("_" in var): #配列型を検知
                continue

            elif(var in yoko): #横にベクトルが伸びる
                end_line = row_list[-1]
                end_line = end_line.split("_")

                if(len(end_line)==2):
                    cpp_input.append("for(int i=0; i<"+end_line[1]+"; ++i) cin >>"+end_line[0]+"[i];")

            elif(row_list[0]==':' or row_list[0]=="："): #縦にベクトルが伸びる
                i+=1
                r_tmp_list=in_str[i].split(" ")

                rr=[]
                for j in r_tmp_list:
                    a=j.split("_")
                    rr.append(a[0])

                a=r_tmp_list[0].split("_")
                aa=a[-1]

                a=""
                for j in aa:
                    if(('a'<=j<='z')or('A'<=j<='Z')or('0'<=j<='9')):
                        a+=j

                cpp_input.append("for(int i=0; i<"+a+"; ++i) cin")
                for p in rr:
                    cpp_input[-1]+=" >>"+p+"[i]"
                cpp_input[-1]+=";"

            else:
                cpp_input.append("cin >>%s;" %var)

        i+=1


    #print(" --- cpp input ---")
    #for r in cpp_input:
    #    print(r)

    #制約文(型を決める時に多分必要)
    in_cond=h3[h3_index].find_next_sibling("ul")
    #print(in_cond)


    """
    tag_preについて
    <pre>タグが付いているものをすべて取り出す
    このt1はリスト構造になっており、0番目に入力形式が入っているのでそれを利用する。
    また1~2m番目には(i,i+1)番目をペアとして入出力例がm個入っている。
    自動テストを作る時に使えそう?
    """

    return cpp_input

if __name__ == "__main__":
    print("input URL > ", end="") #改行を無効
    url_in=input()
    ret=parse(url_in)

    for r in ret:
        print(r)
