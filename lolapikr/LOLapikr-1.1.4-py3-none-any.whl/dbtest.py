# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 02:35:59 2020

@author: dhk13
"""
import cx_Oracle

#한글 지원 방법
import os
from functions import GetChampiondict, GameDataParser
os.putenv('NLS_LANG', '.UTF8')

#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)


connection = cx_Oracle.connect('admin','','lolgg.culykwl5fmgv.ap-northeast-2.rds.amazonaws.com:1521/ORCL')

cursor = connection.cursor()



def GameDataParser_(path):
    #Output으로 받은 txt파일을 파싱하는 함수 
    #각 줄의 형식
    #게임 id | 100,aa,bb,cc|200,aa,bb,cc|win, loss
    f=open(path, 'r')
    line=f.readline()
    while (line):
        row1=[int(line.split('|')[0]),1,line.split('|')[3].split(',')[0][0]]
        row2=[int(line.split('|')[0]),2,line.split('|')[3].split(',')[1][0]]

        cursor.execute("""
                       INSERT INTO MATCHDATA (GameId, Team, Result_) VALUES(:1, :2, :3)
                       """, row1
                       )
        connection.commit()
        cursor.execute("""
                       INSERT INTO MATCHDATA (GameId, Team, Result_) VALUES(:1, :2, :3)
                       """,row2
                       )
        
        connection.commit()
        print(row1)
        print(row2)
        line=f.readline()
    return




GameDataParser("C:/Users/dhk13/Documents/GitHub/League_of_Legend_4U/lolapi/gamedata0609.txt")

cursor.close()
connection.close()