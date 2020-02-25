import numpy as np

from proj1_3.code.graph_search import graph_search

class WorldTraj(object):
    max_Velocity = 0.5
    max_Acceleration = 3
    """

    """
    def __init__(self, world, start, goal):
        """
        This is the constructor for the trajectory object. A fresh trajectory
        object will be constructed before each mission. For a world trajectory,
        the input arguments are start and end positions and a world object. You
        are free to choose the path taken in any way you like.

        You should initialize parameters and pre-compute values such as
        polynomial coefficients here.

        Parameters:
            world, World object representing the environment obstacles
            start, xyz position in meters, shape=(3,)
            goal,  xyz position in meters, shape=(3,)

        """

        # You must choose resolution and margin parameters to use for path
        # planning. In the previous project these were provided to you; now you
        # must chose them for yourself. Your may try these default values, but
        # you should experiment with them!
        self.resolution = np.array([0.25, 0.25, 0.25])
        self.margin = 0.5

        # You must store the dense path returned from your Dijkstra or AStar
        # graph search algorithm as an object member. You will need it for
        # debugging, it will be used when plotting results.
        self.path = graph_search(world, self.resolution, self.margin, start, goal, astar=True)

        # You must generate a sparse set of waypoints to fly between. Your
        # original Dijkstra or AStar path probably has too many points that are
        # too close together. Store these waypoints as a class member; you will
        # need it for debugging and it will be used when plotting results.
        self.points = np.zeros((1,3)) # shape=(n_pts,3)
        last_direction = np.zeros(3)
        for i in range(len(self.path)-1): 
            direction = self.path[i+1] - self.path[i]
            if not (direction == last_direction).all():
                self.points = np.append(self.points,[self.path[i]],axis=0)
            last_direction = direction
        self.points = np.append(self.points,[self.path[-1]],axis=0)
        self.points = self.points[1:,:]
        print(self.points)
        self.point_List = []
        self.trajectory_List = []
        self.direction_List = []
        self.time_List = [0]
        self.real_time_List = [0]
        self.hover_interval = 0
        
        for i in range(self.points.shape[0]):
            self.point_List.append(self.points[i,:])
        for i in range(len(self.point_List)-1):
            self.trajectory_List.append(self.point_List[i+1]-self.point_List[i])
            self.direction_List.append(self.trajectory_List[i]/np.linalg.norm(self.trajectory_List[i]))
            self.real_time_List.append(self.time_List[i]+2*np.sqrt(np.linalg.norm(self.trajectory_List[i])/self.max_Acceleration))
            self.time_List.append(self.real_time_List[i+1]+self.hover_interval)
            
                
                


        # Finally, you must compute a trajectory through the waypoints similar
        # to your task in the first project. One possibility is to use the
        # WaypointTraj object you already wrote in the first project. However,
        # you probably need to improve it using techniques we have learned this
        # semester.

        # STUDENT CODE HERE

    def update(self, t):
        """
        Given the present time, return the desired flat output and derivatives.

        Inputs
            t, time, s
        Outputs
            flat_output, a dict describing the present desired flat outputs with keys
                x,        position, m
                x_dot,    velocity, m/s
                x_ddot,   acceleration, m/s**2
                x_dddot,  jerk, m/s**3
                x_ddddot, snap, m/s**4
                yaw,      yaw angle, rad
                yaw_dot,  yaw rate, rad/s
        """
        x        = np.zeros((3,))
        x_dot    = np.zeros((3,))
        x_ddot   = np.zeros((3,))
        x_dddot  = np.zeros((3,))
        x_ddddot = np.zeros((3,))
        yaw = 0
        yaw_dot = 0
        
        if t > self.time_List[-1]:
            x = self.point_List[-1]
            x_dot = np.zeros((3,))
            x_ddot = np.zeros((3,))
            yaw = 0
        elif t <= self.time_List[-1]:
            for i in range(len(self.time_List)-1):
                if t>=self.time_List[i] and t<self.time_List[i+1]:
                    if t > self.time_List[i+1]-self.hover_interval and t < self.time_List[i+1]:
                        x = self.point_List[i+1]
                        x_ddot = np.zeros((3,))
                    elif t-self.time_List[i] <= self.time_List[i+1]-self.hover_interval-t:
                        x_ddot = self.direction_List[i] * self.max_Acceleration
                        x_dot = x_ddot * (t-self.time_List[i])
                        x = self.point_List[i] + 1/2* x_ddot*(t-self.time_List[i])**2
                    elif t-self.time_List[i] > self.time_List[i+1]-t-self.hover_interval:
                        x_ddot = -self.direction_List[i] * self.max_Acceleration
                        x_dot = -x_ddot*(self.time_List[i+1]-self.hover_interval-t)
                        x = self.point_List[i+1] + 1/2* x_ddot*(self.time_List[i+1]-self.hover_interval-t)**2
        # STUDENT CODE HERE

        flat_output = { 'x':x, 'x_dot':x_dot, 'x_ddot':x_ddot, 'x_dddot':x_dddot, 'x_ddddot':x_ddddot,
                        'yaw':yaw, 'yaw_dot':yaw_dot}
        return flat_output
