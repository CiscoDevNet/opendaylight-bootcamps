'''
Created on May 12, 2016

@author: Yongsheng Liu
'''
#first step, create all paths from s to d; second step, find two paths without same points
g=[[0, 1, 0, 0, 1, 0, 0, 0], \
[1, 0, 1, 0, 0, 1, 0, 0], \
[0, 1, 0, 1, 0, 1, 0, 0], \
[0, 0, 1, 0, 0, 1, 1, 1], \
[1, 0, 0, 0, 0, 1, 0, 0], \
[0, 1, 1, 1, 1, 0, 1, 0], \
[0, 0, 0, 1, 0, 1, 0, 1], \
[0, 0, 0, 1, 0, 0, 1, 0]]


def compute_all_path():
    p=[[-1 for col in range(0,10)] for row in range(0,50)] #used to store paths, p[0]=[1,2,6,7,8] denotes the first path; 20 may be enough
    ass_p=[2 for col in range(0,10)]   #all nodes test start from node 1, the source node    
    cur_node=1;
    path_index=0;
    path_count=0;
    p[0][0]=1
    while True:
        add_node=False
        next_node=ass_p[path_index]
        while next_node<=8:
            #find the next possible node
            if g[cur_node-1][next_node-1]!=0:
                #lookup the p[path_count]
                contained=False
                for j in range(0, path_index+1):
                    if p[path_count][j] == next_node:
                        contained=True
                        break
                if contained==False:
                    add_node=True 
                    break       
            next_node=next_node+1
            
        if add_node==True:
            ass_p[path_index]=next_node+1
            path_index=path_index+1
            p[path_count][path_index]=next_node
            cur_node=next_node
            if cur_node==8:
                if path_index-2>=0 :
                    #finish one route,    
                    path_count=path_count+1
                    #copy the old path from source to back_pos
                    for a in range(0, path_index-1):
                        p[path_count][a]=p[path_count-1][a]
                    ass_p[path_index]=2
                    ass_p[path_index-1]=2
                    path_index=path_index-2
                    cur_node=p[path_count][path_index]
                else:
                    return p
        else:
            if cur_node ==1:
                #quit
                p[path_count]=[-1 for col in range(0,20)]
                return p
            else:
                ass_p[path_index]=2
                p[path_count][path_index]=-1
                path_index=path_index-1
                cur_node=p[path_count][path_index]                

def select_two_path(paths):
    for i in range(0,51):
        if paths[i][0]<0:
            break
    
    for j_row in range(0,i):
        for k_row in range(j_row+1, i):
            equal=False
            for j_col in range(1,9):
                for k_col in range(1,9):
                    comp1=paths[j_row][j_col]
                    comp2=paths[k_row][k_col]
                    if comp1==comp2 and comp1!=-1 and comp1!=8 and comp1!=1:
                        equal=True
                        break
                if equal==True:
                    break
            if equal==False:
                route1=[]
                route2=[]
                for t1 in paths[j_row]:
                    if t1>0:
                        route1.append(t1)
                for t2 in paths[k_row]:
                    if t2>0:
                        route2.append(t2)
                return [route1, route2]
                
                        
def main():
    p=compute_all_path()  
    two_route=select_two_path(p)     
    print(two_route[0])
    print(two_route[1])

if __name__ == '__main__':
    main()