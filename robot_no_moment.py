
from math import log

in_file=open("robot_no_momemtum.data",'r')
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
#print len(train_data)
#print train_data

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
    return (float(count)+1)/(count_a+2)


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
    return (float(count)+1)/(count_a+2)

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

#print observe_prob[0]
#print travers_prob[0]

#buil HMMM

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
def main_viterbi(observe,states):

    l=[]
    prev_states=[]
    for i in state:
        prob=0
        prev_state=[]
        max_v=0
        for j in states:
            p1=0
            for m in travers_prob:
                if m[0:2]==[j[1],i]:
                    p1=m[2]*j[0]
            if max_v<p1:
                max_v=p1
                prev_state=j[1]

        for j in observe_prob:
            if [i,observe]==j[0:2]:
                prob=j[2]*max_v
        l.append([prob,i])
        prev_states.append([i,prev_state])
    l1=[l,prev_states]
    return l1


out_put=[]

def rev(list1):
    l=[]
    i=len(list1)
    i-=1
    while(i>=0):
        l.append(list1[i])
        i-=1
    return l




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
