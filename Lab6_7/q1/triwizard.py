import numpy as np

# ---- Task (a) -------
# Do as directed in function:
# 'my_list': a list of 25 integers

def avada_kedavra(my_list):
	# Create an array 'a0' from this list 'my_list'
	#reshape, argmax, amax, copy, matmul and astype.
	a0 = np.array(my_list)
	# print a0
	print("a0 at beginning:\n{}".format(a0))

	# reshape a0 to create a 5X5 matrix a1
	a1 = a0.reshape((5,5))
	# print a1
	print("a1 at the beginning:\n{}".format(a1))

	# now, change the central element of a1 to 0
	a1[2,2] = 0
	# print a1
	print("a1 after change:\n{}".format(a1))
	# print a0
	print("a0 after changing a1:\n{}".format(a0))
	print("reshaping doesn't create a copy of array. It just returns another view. So, changing one changed the other")

	# make a copy of a1 and flatten it (call it a1cpy)
	a1cpy = np.copy(a1)
	a1cpy = a1cpy.flatten()
	# multiply each element of a1cpy by 0.7:
	a1cpy = np.round_(a1cpy*(0.7) , decimals =2)
	# print a1cpy:
	print("a1cpy\n{}".format(a1cpy))

	# print a1:
	print("a1 after changing its copy:\n{}".format(a1))


# ---- Task (b) -------
# Do as directed in function:
# 'my_integer': an even integer

def incendio(my_integer):
	# create an array 'arng0' of shape (3,2) containing consecutive even numbers starting from 'my_integer', arranged along rows
        arng0 = np.arange(my_integer, 7*my_integer,2)
        arng0 = arng0.reshape(3,2)
	# print arng0
        print("arng0\n{}".format(arng0))

	# create another array 'arng1' of shape ((4,3)) containing consecutive numbers starting from 'my_integer' arranged along columns:
        arng1 = np.arange(my_integer, 12+my_integer)
        arng1 = np.reshape(arng1 , (4,3), order='F')
	# print arng1
        print("arng1\n{}".format(arng1))

	# multiply transpose of arng0 with transpose of arng1 to get mult0:
        mult0 = np.dot(np.transpose(arng0), np.transpose(arng1))

	# print mult0:
        print("mult0\n{}".format(mult0))

	# take min of mult0 along its rows and store it in v0:
        v0 = mult0.min(axis = 1)
	# print v0's shape:
        print("shape of v0: \n{}".format(v0.shape))
        
	# reshape v0 to make it a column vector:
        v0 = v0.reshape(v0.shape[0],1)
        
	# subtract v0 from each column of mult0 and store it in base0:
        base0 = np.subtract(mult0, v0)
	# print base0
        print("base0\n{}".format(base0))
        
	# square all the elements present in base0
        base0 = np.square(base0)
	# store the sum of all elements of base0 in ans
        ans = np.sum(base0)
	# print ans
        print("ans : {}".format(ans))


# ---- Task (c) -------
# 'n': integer
# 'm': integer that divides n
# return type: int numpy Ndarray; dim: nxn
def alohomora(n, m):
        fin_arr = np.ones((n,n))
        k=0
        for i in range(0,n,m):
                key = 1 if k%2 == 0 else 0
                for j in range(0,n,m):
                        if key==1:
                                key = 0
                        else:
                                fin_arr[i:i+m,j:j+m]= np.zeros((m,m))
                                key = 1
                k+=1
        fin_arr = fin_arr.astype('int')
        return (fin_arr)
                        


# ---- Task (d) -------
# 'arr': float Ndarray; dim: Nx3, 
# 'theta': float; 0≤theta<360 (in degrees)
# 'axis': str; axis ∈ {'X','Y','Z'}
# return type: float Ndarray; dim: Nx3
def expelliarmus(arr, theta, axis):
        arr = arr.astype('float')
        angle = np.radians(theta)
        cosine = np.cos(angle)
        #print(cosine)
        sine = np.sin(angle)
        #print(sine)
        if axis == 'X':
                angle_matrix = np.array([[1,0,0],[0,cosine,-sine],[0,sine,cosine]])
                arr = np.dot(angle_matrix, np.transpose(arr))
                arr = np.round_(np.transpose(arr), decimals = 2)
                
        if axis == 'Y':
                angle_matrix = np.array([[cosine,0,sine],[0,1,0],[-sine,0,cosine]])
                arr = np.dot(angle_matrix, np.transpose(arr))
                arr = np.round_(np.transpose(arr), decimals = 2)
                #arr = np.round_(np.dot(arr,angle_matrix), decimals = 2)
        if axis == 'Z':
                angle_matrix = np.array([[cosine,-sine,0],[sine,cosine,0],[0,0,1]])
                arr = np.dot(angle_matrix, np.transpose(arr))
                arr = np.round_(np.transpose(arr), decimals = 2)
                
        return arr


# ---- Task (e) -------
# 'arr': float Ndarray; dim: MxN
# return type: float Ndarray; dim: MxN
def crucio(arr):
        mean = np.mean(arr, axis=0)
        std = np.std(arr, axis=0)
        arr = np.subtract(arr, mean)
        arr = np.divide(arr, std)
        return(np.round_(arr, decimals = 2))


# ---- Task (f) -------
# 'arr': int 1-D array; dim: (n,)
# k: integer
# return type: int 1-D array; dim: (n+k-1,)
def leviosa(arr, k):
        #arr = np.pad(arr,(k-1,k-1) )
        x = np.ones(k).astype('int')
        return np.convolve(x,arr)

        


# ---- Task (g) -------
# 'mat': int n-D array; dim: (m,n)
# k: integer
# return type: n-D integer array; dim: (m,k)
def accio(mat, k):
        return np.argsort(mat)[:,-k:][:,::-1]
	

