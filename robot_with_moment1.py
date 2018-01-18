

from math import log
import numpy as  np
#get from file
in_file=open("robot_with_momemtum.data",'r')
train_data=[]
test_data=[]
temp=in_file.readline()
sequenc=[]
step=[]
count=0
while(temp != '..\n'):
    s=[]
    if temp=='.\n':
        train_data.append(sequenc)
        sequenc=[]
    else:
        s1=temp.split()
        s.append(int(s1[0][0]))
        s.append(int(s1[0][2]))
        s.append(s1[1])
        sequenc.append(s)
    temp=in_file.readline()
train_data.append(sequenc)
sequenc=[]

temp=in_file.readline()
while(temp):
    s=[]
    if temp=='.\n':
        test_data.append(sequenc)
        sequenc=[]
    else:
        s1=temp.split()
        s.append(int(s1[0][0]))
        s.append(int(s1[0][2]))
        s.append(s1[1])
        sequenc.append(s)
    temp=in_file.readline()

state=[[1,2],[1,3],[2,1],[2,3],[2,4],[3,1],[3,2],[3,3],[3,4],[4,1],[4,2],[4,4]]
color=['r','b','y','g']

travers_prob=[]
observe_prob=[]

def prob_observe(state,color):
    count_a=0
    count=0
    for i in train_data:
        for j in i :
            if j==[state[0],state[1],color]:
                count+=1
    for i in train_data:
        for j in i :
            if j[0:2]==state:
                count_a+=1
    return float(count)/count_a


def prob_travers(state1,state2):
    count=0
    count_a=0
    for i in train_data:
        for j in range(0,199):
            if i[j][0:2]==state1 and i[j+1][0:2]==state2:
                count+=1
    for i in train_data:
        for j in range(0,199):
            if i[j][0:2]==state1:
                count_a+=1
    return float(count)/count_a

for i in state:
    for j in color:
        observe_prob.append([i,j,prob_observe(i,j)])

for i in state:
    for j in state:
        travers_prob.append([i,j,prob_travers(i,j)])


observation=[]
for i in test_data:
    l=[]
    for j in i :
        l.append(j[2])
    observation.append(l)
predect_list=[]

#buil HMM
def max_prob(li):
    max=[]
    l=0
    for i in li :
        if i[0] > l:
            l=i[0]
            max=i[1]
    return max





def start_viterbi(observe):
    l=[]

    for i  in  state:
        prob=0
        for j in observe_prob:
            if [i,observe]==j[0:2]:
                prob=j[2]
        l.append([prob,i])
    l1=[l,[]]
    return l1

direction=' '


def get_direction(state1,state2):


    if state1[0]==(state2[0]+1) and state1[1]==state2[1]:
        return 'r'
    elif state1[0]==(state2[0]-1) and state1[1]==state2[1]:
        return 'l'
    elif state1[0]==state2[0] and state1[1]==(state2[1]+1):
        return 'u'
    elif state1[0]==state2[0] and state1[1]==(state2[1]-1):
        return 'd'
    else:
        return ' '


def main_viterbi(observe,states):
    global direction

    k1=max_prob(states)
    l=[]

    prev_states=[]

    if  direction== 'r' and ([k1[0]+1,k1[1]] in state):
        for i in state:
            prob=0
            p=[]
            p1=0
            max_v=0
            prev_state=[]
            for j in states:
                
                if [k1[0]+1,k1[1]]==j[1]:
		    print "right"	
                    p1=j[0]*0.85
                else:
		    print "no right"
                    p1=j[0]*0.15
                if max_v<p1:
                    max_v=p1
                    prev_state=j[1]

            for j in observe_prob:
                if [i,observe]==j[0:2]:
                    prob=(j[2]*max_v)
            l.append([prob,i])
            prev_states.append([i,prev_state])
    elif  direction== 'l' and ([k1[0]-1,k1[1]] in state):
        for i in state:
            prob=0
            p=[]
            p1=0
            max_v=0
            prev_state=[]
            for j in states:
         
                if [k1[0]-1,k1[1]]==j[1]:
		    print "left"
                    p1=j[0]*0.85
                else:
                    p1=j[0]*0.15
                if max_v<p1:
                    max_v=p1
                    prev_state=j[1]
            for j in observe_prob:
                if [i,observe]==j[0:2]:
                    prob=(j[2]*max_v)
            l.append([prob,i])
            l.append([prob,i])
            prev_states.append([i,prev_state])
    elif  direction== 'u' and ([k1[0],k1[1]+1] in state):
        for i in state:
            prob=0
            p=[]
            p1=0
            prev_state=[]
            max_v=0
            for j in states:
               
                if [k1[0],k1[1]+1]==j[1]:
		    print "up"
                    p1=j[0]*0.85
                else:
		    
                    p1=j[0]*0.15
                if max_v<p1:
                    max_v=p1
                    prev_state=j[1]


            for j in observe_prob:
                if [i,observe]==j[0:2]:
                    prob=(j[2]*max_v)
            l.append([prob,i])
            prev_states.append([i,prev_state])
    elif  direction== 'd' and ([k1[0],k1[1]-1] in state):
        for i in state:
            prob=0
            p=[]
            p1=0
            prev_state=[]
            max_v=0
            for j in states:
                
                if [k1[0],k1[1]-1]==j[1]:
		    print "down"
                    p1=j[0]*0.85
                else:
                    p1=j[0]*0.15
                if max_v<p1:
                    max_v=p1
                    prev_state=j[1]

            for j in observe_prob:
                if [i,observe]==j[0:2]:
                    prob=(j[2]*max_v)
            l.append([prob,i])
            prev_states.append([i,prev_state])

    else:

        for i in state:
            prob=0
            p=[]
            p1=0
            max_v=0
            prev_state=[]
            for j in states:
                for m in travers_prob:
                    if m[0:2]==[j[1],i]:
                        m1=np.log(m[2])
                        m2=np.log(j[0])
                        m3=np.logaddexp(m1,m2)
                        p1=m[2]*j[0]
                if max_v<p1:
                    max_v=p1
                    prev_state=j[1]
            for j in observe_prob:
                if [i,observe]==j[0:2]:
                    prob=(j[2]*max_v)
            l.append([prob,i])
            prev_states.append([i,prev_state])
    k2=max_prob(l)
    direction=get_direction(k1,k2)
    l1=[l,prev_states]
    return l1







def rev(list1):
    l=[]
    i=len(list1)
    i-=1
    while(i>=0):
        l.append(list1[i])
        i-=1
    return l


out_put=[]

for i in range(len(observation)):
    out_put1=[]
    k=start_viterbi(observation[i][0])
    #print  "acssssssssssssssssssssssssssss"
    k1=max_prob(k[0])
    sequenc_out_put=[]
    for j in range(1,len(observation[i])):
        k=main_viterbi(observation[i][j],k[0])
        sequenc_out_put.append(k[1])
    i1=198
    s1=max_prob(k[0])


    while(i1>=0):
        count=0
        k=s1
        for t in sequenc_out_put[i1]:
            if t[0]==k:
                out_put1.append(s1)
                s1=t[1]
                count+=1


        i1-=1
    out_put1.append(s1)
    #print out_put1.reverse()
    out_put.append(rev(out_put1))


true_count=0
all_count=0
for i in range(0,200):
    for j in range(0,200):
        if out_put[i][j]==test_data[i][j][0:2]:
            true_count+=1
        all_count+=1
print "acuracy:"
print float(true_count)/all_count
