#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import copy
import sys



### 파일 읽어오기
try:
    readfilename = sys.argv[1]
except:
    readfilename = 'students.txt'
    
f = open(readfilename,'r') ## Jupyter 환경에서는 파일명을 직접 입력했음

### 사용자 정의 함수 생성 - Grade 산출 함수
def cal_grade(score):
    if score >= 90:
        return "A"
    elif 80 <= score < 90:
        return "B"
    elif 70 <= score < 80:
        return "C"
    elif 60 <= score < 70:
        return "D"
    else:
        return "F"

### 전체 데이터를 관리할 리스트 생성
datalst = []
### 한줄씩 읽으면서 해당 데이터를 추가
for line in f:
    newdata = line.split()
    ### 중간고사 점수와 기말고사 점수를 int형으로 변환
    newdata[-2], newdata[-1] = int(newdata[-2]), int(newdata[-1])
    ### 성과 이름을 합치기
    newdata[1] += " "
    newdata[1] += newdata[2]
    del(newdata[2])
    newdata.append(round(np.mean(newdata[-2:]),1))
    newdata.append(cal_grade(newdata[-1]))
    ### 전체 데이터 리스트 추가
    datalst.append(newdata)
f.close()

### 전체 데이터 출력 함수 생성
def showall(datalst):
    print("Student number\tName\t\tMidterm\tFinal\tAverage\tGrade\n")
    print("---------------------------------------------------------------")
    ### 평균 점수 내림차순 정렬
    datalst.sort(key=lambda x: x[-2], reverse=True)
    for student_data in datalst:
        print('\t'.join(list(map(str,student_data))))

showall(datalst)

orderlst = ['show', 'search','changescore','searchgrade','add','remove','quit']
while True:
    order = input("# ")
    order = order.lower()
    if order in orderlst:
        if order == 'show':  # show 기능 구현
            showall(datalst)
        elif order == 'search': # search 기능 구현
            student_num = input("Student ID: ")
            student_numlst = [x[0] for x in datalst]
            if student_num in student_numlst:
                order_result = datalst[student_numlst.index(student_num)]
                showall([order_result])
            else:
                print("NO SUCH PERSON")
        elif order == 'changescore': # changescore 기능 구현
            student_num = input("Student ID: ")
            student_numlst = [x[0] for x in datalst]
            if student_num not in student_numlst:
                print("NO SUCH PERSON")
            else:
                score_type = input("Mid/Final? ")
                score_type = score_type.lower()
                if score_type == 'mid':
                    newscore = int(input("Input new score: "))
                    if newscore not in range(0, 101):
                        pass
                    else:
                        changeindex = student_numlst.index(student_num)
                        beforedata = copy.deepcopy(datalst[changeindex])
                        datalst[changeindex][2] = newscore
                        datalst[changeindex][4] = round(np.mean(datalst[changeindex][2:4]),1)
                        datalst[changeindex][-1] = cal_grade(datalst[changeindex][4])
                        showall([beforedata])
                        print('Score changed')
                        print('\t'.join(list(map(str, datalst[changeindex]))))
                elif score_type == 'final':
                    newscore = int(input("Input new score: "))
                    if newscore not in range(0, 101):
                        pass
                    else:
                        changeindex = student_numlst.index(student_num)
                        beforedata = copy.deepcopy(datalst[changeindex])
                        datalst[changeindex][3] = newscore
                        datalst[changeindex][4] = round(np.mean(datalst[changeindex][2:4]),1)
                        datalst[changeindex][-1] = cal_grade(datalst[changeindex][4])
                        showall([beforedata])
                        print('Score changed')
                        print('\t'.join(list(map(str, datalst[changeindex]))))
                else:
                    pass
        
        elif order == 'add':  # add 구현
            student_num = input("Student ID: ")
            student_numlst = [x[0] for x in datalst]
            if student_num in student_numlst:
                print("ALREADY EXISTS")
            else:
                newname = input("Name: ")
                newmid = int(input("Midterm Score: "))
                newfinal = int(input("Final Score: "))
                newavg = round(np.mean([newmid, newfinal]),1)
                newgrade = cal_grade(newavg)
                datalst.append([student_num, newname, newmid, newfinal, newavg, newgrade])
                print('Student added')
        
        elif order == 'searchgrade': # searchgrade 구현
            gradeinput = input("Grade to search: ")
            if gradeinput not in ['A','B','C','D','F']:
                pass
            else:
                gradelst = [x[-1] for x in datalst]
                if gradeinput not in gradelst:
                    print('NO RESULTS')
                else:
                    searchresult = [studata for studata in datalst if studata[-1] == gradeinput]
                    showall(searchresult)
        
        elif order == 'remove': # remove 구현
            if len(datalst) == 0:
                print("List is empty")
            else:
                student_num = input("Student ID: ")
                student_numlst = [x[0] for x in datalst]
                if student_num not in student_numlst:
                    print("NO SUCH PERSON")
                else:
                    changeindex = student_numlst.index(student_num)
                    datalst.remove(datalst[changeindex])
#                     del(datalst[changeindex])
                    print("Student removed")
    
        elif order == 'quit': # quit 기능 구현
            savedata = input("Save data?[yes/no] ")
            if savedata == 'yes':
                filename = input("File name: ")
                newf = open(filename, 'w')
                datalst.sort(key=lambda x: x[-2], reverse=True)
                for studata in datalst:
                    dataline = '\t'.join(list(map(str,studata[:-2]))) +'\n'
                    newf.write(dataline)
                newf.close()
            break

