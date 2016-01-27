'''
arcとabcの各問題に関してparser2.pyを試すスクリプト
'''

import parser2
import os

def doExp():
    abc_lim=32
    arc_lim=47

    if(not os.path.exists("./abc")):
        os.mkdir("./abc")
    if(not os.path.exists("./arc")):
        os.mkdir("./arc")

    '''
    abcは19以前はは数字、20以降はアルファベット
    '''
    os.chdir("./abc")
    for i in range(1,abc_lim+1):
        num="0"
        if(i<10):
            num+="0"
        num+=str(i)

        print("abc"+num)

        url="http://abc"+num+".contest.atcoder.jp/tasks/abc"+num+"_"

        if(i<=19):
            problem_list=["1","2","3","4"]
        else:
            problem_list=["a","b","c","d"]

        for pr in problem_list:
            url_in=url+pr
            ret=parser2.parse(url_in)

            f=open("abc"+num+pr,"w")
            for row in ret:
                f.write(row+"\n")
            f.close()

    #作業ディレクトリに戻る
    os.chdir("..")

    '''
    arcは34以前はは数字、35以降はアルファベット
    '''
    os.chdir("./arc")
    for i in range(1,arc_lim+1):
        num="0"
        if(i<10):
            num+="0"
        num+=str(i)

        print("arc"+num)

        url="http://arc"+num+".contest.atcoder.jp/tasks/arc"+num+"_"

        if(i<=34):
            problem_list=["1","2","3","4"]
        else:
            problem_list=["a","b","c","d"]

        for pr in problem_list:
            url_in=url+pr
            ret=parser2.parse(url_in)

            f=open("arc"+num+pr,"w")
            for row in ret:
                f.write(row+"\n")
            f.close()

    #作業ディレクトリに戻る
    os.chdir("..")


if __name__ == "__main__":
    print("start")
    doExp()
