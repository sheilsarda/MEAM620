elifimport heapq
from heapq import heappush, heappop  # Recommended.
import numpy as np

from flightsim.world import World
from occupancy_map import OccupancyMap # Recommended.

def graph_search(world, resolution, margin, start, goal, astar):
    """
    Parameters:
        world,      World object representing the environment obstacles
        resolution, xyz resolution in meters for an occupancy map, shape=(3,)
        margin,     minimum allowed distance in meters from path to obstacles.
        start,      xyz position in meters, shape=(3,)
        goal,       xyz position in meters, shape=(3,)
        astar,      if True use A*, else use Dijkstra
    Output:
        path,       xyz position coordinates along the path in meters with
                    shape=(N,3). These are typically the centers of visited
                    voxels of an occupancy map. The first point must be the
                    start and the last point must be the goal. If no path
                    exists, return None.
    """


    always_added  = np.zeros((27,3,26),dtype = int)
    forced_to_check = np.zeros((27,3,12),dtype = int)
    forced_to_add = np.zeros((27,3,12),dtype = int)
    current_situation = np.array([[26,0],[1,8],[3,12],[7,12]])

    # While not required, we have provided an occupancy map you may use or modify.
    occ_map = OccupancyMap(world, resolution, margin)
    # Retrieve the index in the occupancy grid matrix corresponding to a position in space.
    start_index = tuple(occ_map.metric_to_index(start))
    goal_index = tuple(occ_map.metric_to_index(goal))

    occ_map.create_map_from_world

    Q = []

    cost_to_come = np.full((occ_map.map.shape[0],occ_map.map.shape[1],occ_map.map.shape[2]),np.inf)
    heuristic = np.zeros((occ_map.map.shape[0],occ_map.map.shape[1],occ_map.map.shape[2]))

    parent = np.zeros((occ_map.map.shape[0],occ_map.map.shape[1],occ_map.map.shape[2],3),dtype = int)





    if astar == False:

        for i in range(occ_map.map.shape[0]):
            for j in range(occ_map.map.shape[1]):
                for k in range(occ_map.map.shape[2]):
                    if  occ_map.map[i,j,k] == False:
                        heapq.heappush(Q,(cost_to_come[i,j,k],[i,j,k]))

        Q.remove((cost_to_come[start_index[0],start_index[1],start_index[2]],[start_index[0],start_index[1],start_index[2]]))
        cost_to_come[start_index[0],start_index[1],start_index[2]] = 0

        heapq.heappush(Q,(cost_to_come[start_index[0],start_index[1],start_index[2]],[start_index[0],start_index[1],start_index[2]]))
        heapq.heappush(Q,(cost_to_come[goal_index[0],goal_index[1],goal_index[2]],[goal_index[0],goal_index[1],goal_index[2]]))



        # heapq.heapreplace(Q, (cost_to_come[start_index[0],start_index[1]],[start_index[0],start_index[1]]))
        #Done with initialization
        #Following is the searching process

        while (cost_to_come[goal_index[0],goal_index[1],goal_index[2]],[goal_index[0],goal_index[1],goal_index[2]]) in Q and cost_to_come.min() < np.inf:
            u_indicies = heapq.heappop(Q)[1]
            u_x = u_indicies[0]
            u_y = u_indicies[1]
            u_z = u_indicies[2]

            # heapq.heappop(Q)

            for i in range(-1,2):
                for j in range(-1,2):
                    for k in range(-1,2):
                        if i==0 and j==0 and k==0:
                            pass
                        elif not occ_map.is_valid_index([u_x+i,u_y+j,u_z+k]) or occ_map.is_occupied_index([u_x+i,u_y+j,u_z+k]) or cost_to_come[u_x+i,u_y+j,u_z+k] != np.inf:
                            pass
                        else:

                            d = cost_to_come[u_x,u_y,u_z]+np.sqrt(i**2 + j**2 +k**2)
                            if d < cost_to_come[u_x+i,u_y+j,u_z+k]:
                                # start_time = time.time()
                                # Q.remove((cost_to_come[u_x+i,u_y+j,u_z+k],[u_x+i,u_y+j,u_z+k]))
                                cost_to_come[u_x+i,u_y+j,u_z+k] = d
                                heapq.heappush(Q,(cost_to_come[u_x+i,u_y+j,u_z+k],[u_x+i,u_y+j,u_z+k]))


                                # Q.append((d,[u_x+i,u_y+j,u_z+k]))


                                # heapq.heapify(Q)
                                # print(time.time()-start_time)
                                parent[u_x+i,u_y+j,u_z+k,:] = [u_x,u_y,u_z]

                # print([u_x,u_y,u_z])

    elif astar == True:

                    # if  occ_map.map[i,j,k] == False:

                        # heapq.heappush(Q,(cost_to_come[i,j,k],[i,j,k]))
                        # heuristic[i,j,k] = np.sqrt((goal_index[0]-i)**2+(goal_index[1]-j)**2 + (goal_index[2]-k)**2)

        cost_to_come[start_index[0],start_index[1],start_index[2]] = 0
        f = cost_to_come + heuristic
        heapq.heappush(Q,(f[start_index[0],start_index[1],start_index[2]],[start_index[0],start_index[1],start_index[2]]))
        heapq.heappush(Q,(f[goal_index[0],goal_index[1],goal_index[2]],[goal_index[0],goal_index[1],goal_index[2]]))


        # heapq.heapreplace(Q, (cost_to_come[start_index[0],start_index[1]],[start_index[0],start_index[1]]))
        #Done with initialization
        #Following is the searching process
        while (f[goal_index[0],goal_index[1],goal_index[2]],[goal_index[0],goal_index[1],goal_index[2]]) in Q and min(Q)[0] < np.inf:
            u_indicies = heapq.heappop(Q)[1]
            u_x = u_indicies[0]
            u_y = u_indicies[1]
            u_z = u_indicies[2]
            p_x,p_y,p_z= parent[int(u_x),int(u_y),int(u_z)]
            norm1 = abs(np.array([p_x,p_y,p_z])-u_indicies).sum()
            num_neib = current_situation[norm1][0]
            num_fneib = current_situation[norm1][1]
            for i in range(-1,2):
                for j in range(-1,2):
                    for k in range(-1,2):
                        for runs in range(num_neib):
                            
                            
                            
                        # if i==0 and j==0 and k==0:
                        #     pass
                        else:
                            always_added[i,j,k] =

                        #     pass
                        # elif not occ_map.is_valid_index([u_x+i,u_y+j,u_z+k]) or occ_map.is_occupied_index([u_x+i,u_y+j,u_z+k]):
                        #     pass
                        # else:
                        #     d = cost_to_come[u_x,u_y,u_z]+np.sqrt(i**2 + j**2 +k**2)
                        #     if d < cost_to_come[u_x+i,u_y+j,u_z+k]:
                        #         cost_to_come[u_x+i,u_y+j,u_z+k] = d
                        #         f = cost_to_come + heuristic
                        #         heapq.heappush(Q,(f[u_x+i,u_y+j,u_z+k],[u_x+i,u_y+j,u_z+k]))
                        #         parent[u_x+i,u_y+j,u_z+k,:] = [u_x,u_y,u_z]
                # print([u_x,u_y,u_z])
    current_X = goal_index[0]
    current_Y = goal_index[1]
    current_Z = goal_index[2]



    path = []
    if parent[goal_index[0],goal_index[1],goal_index[2],:].any() == 0:
        return None


    while [current_X,current_Y,current_Z] != [start_index[0],start_index[1],start_index[2]]:
        path.insert(0,occ_map.index_to_metric_center([current_X,current_Y,current_Z]))
        [current_X,current_Y,current_Z] = parent[int(current_X),int(current_Y),int(current_Z)]
    path.insert(0,occ_map.index_to_metric_center(start_index))
    path.insert(0,start)
    path.append(goal)

    return np.asarray(path)











    # if astar == False:
    #     pass




    return None

def getNeighbors(dx,dy,dz, runs ):
    norm = abs(np.array([dx,dy,dz])).sum()
    if norm == 0:
        if runs == 0:tx,ty,tz = 1,0,0
        elif runs == 1: tx=-1; ty=0; tz=0
        elif runs == 2: tx=0; ty=1; tz=0
        elif runs == 3: tx=1; ty=1; tz=0
        elif runs == 4: tx=-1; ty=1; tz=0
        elif runs == 5: tx=0; ty=-1; tz=0
        elif runs == 6: tx=1; ty=-1; tz=0
        elif runs == 7: tx=-1; ty=-1; tz=0
        elif runs == 8: tx=0; ty=0; tz=1
        elif runs == 9: tx=1; ty=0; tz=1
        elif runs == 10: tx=-1; ty=0; tz=1
        elif runs == 11: tx=0; ty=1; tz=1
        elif runs == 12: tx=1; ty=1; tz=1
        elif runs == 13: tx=-1; ty=1; tz=1
        elif runs == 14: tx=0; ty=-1; tz=1
        elif runs == 15: tx=1; ty=-1; tz=1
        elif runs == 16: tx=-1; ty=-1; tz=1
        elif runs == 17: tx=0; ty=0; tz=-1
        elif runs == 18: tx=1; ty=0; tz=-1
        elif runs == 19: tx=-1; ty=0; tz=-1
        elif runs == 20: tx=0; ty=1; tz=-1
        elif runs == 21: tx=1; ty=1; tz=-1
        elif runs == 22: tx=-1; ty=1; tz=-1
        elif runs == 23: tx=0; ty=-1; tz=-1
        elif runs == 24: tx=1; ty=-1; tz=-1
        elif runs == 25: tx=-1; ty=-1; tz=-1
    elif norm == 1:
        tx = dx; ty =dy; tz = dz
    elif norm == 2:
        if runs == 0:
            if dz == 0 :
                tx,ty,tz = 0,dy,0
            else:
                tx,ty,tz = 0,0,dz
        elif runs ==1:
            if dx == 0:
                tx,ty,tz = 0,dy,0
            else:
                tx,ty,tz = dx,0,0
        elif runs == 2:
            tx,ty,tz = dx,dy,dz
    elif norm == 3:
        if runs == 0: tx = dx; ty =  0; tz =  0
        elif runs == 1: tx =  0; ty = dy; tz =  0
        elif runs == 2: tx =  0; ty =  0; tz = dz
        elif runs == 3: tx = dx; ty = dy; tz =  0
        elif runs == 4: tx = dx; ty =  0; tz = dz
        elif runs == 5: tx =  0; ty = dy; tz = dz
        elif runs == 6: tx = dx; ty = dy; tz = dz
    return [tx,ty,tz]


def getForcedN(dx,dy,dz, runs):

    norm = abs(np.array([dx,dy,dz])).sum()
    if norm == 1:
        if runs == 0: fx= 0; fy= 1; fz = 0
        elif runs == 1: fx= 0; fy=-1; fz = 0
        elif runs == 2: fx= 1; fy= 0; fz = 0
        elif runs == 3: fx= 1; fy= 1; fz = 0
        elif runs == 4: fx= 1; fy=-1; fz = 0
        elif runs == 5: fx=-1; fy= 0; fz = 0
        elif runs == 6: fx=-1; fy= 1; fz = 0
        elif runs == 7: fx=-1; fy=-1; fz = 0
        nx,ny,nz = fx,fy,fz
        if(dx != 0):
            fz = fx; fx = 0;
            nz = fz; nx = dx
        if(dy != 0):
            fz = fy; fy = 0;
            nz = fz; ny = dy
    elif norm == 2:
        if dx == 0:
          if runs == 0:
            fx = 0; fy = 0; fz = -dz;
            nx = 0; ny = dy; nz = -dz;

          elif runs == 1:
            fx = 0; fy = -dy; fz = 0;
            nx = 0; ny = -dy; nz = dz;

          elif runs == 2:
            fx = 1; fy = 0; fz = 0;
            nx = 1; ny = dy; nz = dz;

          elif runs == 3:
            fx = -1; fy = 0; fz = 0;
            nx = -1; ny = dy; nz = dz;

          elif runs == 4:
            fx = 1; fy = 0; fz = -dz;
            nx = 1; ny = dy; nz = -dz;

          elif runs == 5:
            fx = 1; fy = -dy; fz = 0;
            nx = 1; ny = -dy; nz = dz;

          elif runs == 6:
            fx = -1; fy = 0; fz = -dz;
            nx = -1; ny = dy; nz = -dz;

          elif runs == 7:
            fx = -1; fy = -dy; fz = 0;
            nx = -1; ny = -dy; nz = dz;


          elif runs == 8:
            fx = 1; fy = 0; fz = 0;
            nx = 1; ny = dy; nz = 0;

          elif runs == 9:
            fx = 1; fy = 0; fz = 0;
            nx = 1; ny = 0; nz = dz;

          elif runs == 10:
            fx = -1; fy = 0; fz = 0;
            nx = -1; ny = dy; nz = 0;

          elif runs == 11:
            fx = -1; fy = 0; fz = 0;
            nx = -1; ny = 0; nz = dz;

        elif dy ==0:
          if runs == 0:
            fx = 0; fy = 0; fz = -dz;
            nx = dx; ny = 0; nz = -dz;

          elif runs == 1:
            fx = -dx; fy = 0; fz = 0;
            nx = -dx; ny = 0; nz = dz;

          elif runs == 2:
            fx = 0; fy = 1; fz = 0;
            nx = dx; ny = 1; nz = dz;

          elif runs == 3:
            fx = 0; fy = -1; fz = 0;
            nx = dx; ny = -1;nz = dz;

          elif runs == 4:
            fx = 0; fy = 1; fz = -dz;
            nx = dx; ny = 1; nz = -dz;

          elif runs == 5:
            fx = -dx; fy = 1; fz = 0;
            nx = -dx; ny = 1; nz = dz;

          elif runs == 6:
            fx = 0; fy = -1; fz = -dz;
            nx = dx; ny = -1; nz = -dz;

          elif runs == 7:
            fx = -dx; fy = -1; fz = 0;
            nx = -dx; ny = -1; nz = dz;

          # // Extras
          elif runs == 8:
            fx = 0; fy = 1; fz = 0;
            nx = dx; ny = 1; nz = 0;

          elif runs == 9:
            fx = 0; fy = 1; fz = 0;
            nx = 0; ny = 1; nz = dz;

          elif runs == 10:
            fx = 0; fy = -1; fz = 0;
            nx = dx; ny = -1; nz = 0;

          elif runs == 11:
            fx = 0; fy = -1; fz = 0;
            nx = 0; ny = -1; nz = dz;
        else:
          if runs == 0:
            fx = 0; fy = -dy; fz = 0;
            nx = dx; ny = -dy; nz = 0;

          elif runs == 1:
            fx = -dx; fy = 0; fz = 0;
            nx = -dx; ny = dy; nz = 0;

          elif runs == 2:
            fx =  0; fy = 0; fz = 1;
            nx = dx; ny = dy; nz = 1;

          elif runs == 3:
            fx =  0; fy = 0; fz = -1;
            nx = dx; ny = dy; nz = -1;

          elif runs == 4:
            fx = 0; fy = -dy; fz = 1;
            nx = dx; ny = -dy; nz = 1;

          elif runs == 5:
            fx = -dx; fy = 0; fz = 1;
            nx = -dx; ny = dy; nz = 1;

          elif runs == 6:
            fx = 0; fy = -dy; fz = -1;
            nx = dx; ny = -dy; nz = -1;

          elif runs == 7:
            fx = -dx; fy = 0; fz = -1;
            nx = -dx; ny = dy; nz = -1;


          elif runs == 8:
            fx =  0; fy = 0; fz = 1;
            nx = dx; ny = 0; nz = 1;

          elif runs == 9:
            fx = 0; fy = 0; fz = 1;
            nx = 0; ny = dy; nz = 1;

          elif runs == 10:
            fx =  0; fy = 0; fz = -1;
            nx = dx; ny = 0; nz = -1;

          elif runs == 11:
            fx = 0; fy = 0; fz = -1;
            nx = 0; ny = dy; nz = -1;
    elif norm ==3:
        if runs == 0:
          fx = -dx; fy = 0; fz = 0;
          nx = -dx; ny = dy; nz = dz;

        elif runs == 1:
          fx = 0; fy = -dy; fz = 0;
          nx = dx; ny = -dy; nz = dz;

        elif runs == 2:
          fx = 0; fy = 0; fz = -dz;
          nx = dx; ny = dy; nz = -dz;

        # // Need to check up to here for forced!
        elif runs == 3:
          fx = 0; fy = -dy; fz = -dz;
          nx = dx; ny = -dy; nz = -dz;

        elif runs == 4:
          fx = -dx; fy = 0; fz = -dz;
          nx = -dx; ny = dy; nz = -dz;

        elif runs == 5:
          fx = -dx; fy = -dy; fz = 0;
          nx = -dx; ny = -dy; nz = dz;

        # // Extras
        elif runs == 6:
          fx = -dx; fy = 0; fz = 0;
          nx = -dx; ny = 0; nz = dz;

        elif runs == 7:
          fx = -dx; fy = 0; fz = 0;
          nx = -dx; ny = dy; nz = 0;

        elif runs == 8:
          fx = 0; fy = -dy; fz = 0;
          nx = 0; ny = -dy; nz = dz;

        elif runs == 9:
          fx = 0; fy = -dy; fz = 0;
          nx = dx; ny = -dy; nz = 0;

        elif runs == 10:
          fx = 0; fy = 0; fz = -dz;
          nx = 0; ny = dy; nz = -dz;

        elif runs == 11:
          fx = 0; fy = 0; fz = -dz;
          nx = dx; ny = 0; nz = -dz;
    return [fx,fy,fz,nx,ny,nz]



def getNeibArray():
    always_added  = np.zeros((27,3,26),dtype = int)
    forced_to_check = np.zeros((27,3,12),dtype = int)
    forced_to_add = np.zeros((27,3,12),dtype = int)
    current_situation = np.array([[26,0],[1,8],[3,12],[7,12]])
    ID = 0
    for dz in range(-1,2):
        for dy in range(-1,2):
            for dx in range (-1,2):
                norm1 = abs(np.array([dx,dy,dz])).sum()
                    for runs in range(current_situation[norm1][0]):
                        always_added[ID][0][runs],always_added[ID][1][runs],always_added[ID][2][runs] = getNeighbors(dx, dy, dz, runs)
                    for runs in range(current_situation[norm1][1]):
                        forced_to_check[ID][0][runs],forced_to_check[ID][1][runs],forced_to_check[ID][2][runs],forced_to_add[ID][0][runs],forced_to_add[ID][1][runs],forced_to_add[ID][2][runs]=getForcedN(dx, dy, dz, runs)
                        
                        




    # if (norm == 0):
    #     for i in range(-1,2):
    #         for j in range(-1,2):
    #             for k in range(-1,2):
    #                 if i==0,j==0,k==0:
    #                     pass
    #                 always_added[i,j,k,:] = [index[0]+i,index[1]+j,index[2]+k]

    # if (norm == 1):
    #     always_added[0,0,0,:] = index + dif
    # if (norm == 2):
    #     if dz ==0:
    #         always_added[0,1,0,:] = index + np.array([0,1,0])
    #     else:
    #         always_added[0,0,1,:] = index + np.array([0,0,1])
    #     if dx ==0:
    #         always_added[0,1,0,:] = index + np.array([0,1,0])
    #     else:
    #         always_added[1,0,0,:] = index + np.array([1,0,0])
    #     al
