import sys
filename = sys.argv[1]
file = open(filename,"r")
t = file.readline()
T = int(t)
a = []
c = []
if T < 1 or T > 1000 :
    print("Invalid value of T")
else :
    for i in range(T):
        y = file.readline()
        y = y.split()
        '''print(y)'''
        H = int(y[0])
        M = int(y[1])
        S = int(y[2])
        a = int(y[3])
        b = int(y[4])
        c = int(y[5])
        '''print(H,M,S,a,b,c)'''
        hr = (360/(H*M*S))*(a*M*S + b*S + c)
        '''(360/(S*M))*(b*S + c)'''
        mins = (360/(M*S))*(b*S + c)
        '''while hr > 180:
            hr -= 180'''
        theta_hr = hr
        '''while mins > 180:
            mins -= 180'''
        theta_min = mins
        '''print("Hour_hand_angle=" + str(theta_hr))
        print("Minute_hand_angle=" + str(theta_min))'''
        angle1 = abs(theta_hr - theta_min)
        if angle1 > 180:
            angle1 = angle1 - 180
        angle = round(angle1,2)
        print(angle)
         
