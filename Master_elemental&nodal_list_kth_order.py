import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import copy

print("Please enter the number of hexagons in the row (Gives idea on number of columns) : ")
n = int(input()) # number of hexagons in a row
print("Please enter the number of hexagons in the column (Gives idea on number of rows): ")
m = int(input()) # number of hexagons in a colum
print("Please enter the order of the hexagonal lattice")
k = int(input())
print("Please enter the side length (you can give 1 for convenience)")
a = float(input())
x1= []
x2= []
y1= []
y2= []

def x_arrays(x): #x is the length of the array we want
    c = a/2
    d = 0
    for i in range(2*x):
        x1.append(c)
        x2.append(d)
        if(i%2 == 0):
            c = c + a
            d = d + 2*a
        else:
            c = c + 2*a
            d = d + a
    return [x1, x2]

def y_arrays(y): #x is the length of the array we want
    c = 0
    d = (a*(3**0.5))/2
    for i in range(y +1):
        y1.append(c)
        if(i!=y):
            y2.append(d)
        c = c + a*(3**0.5)
        d = d + a*(3**0.5)
    return [y1, y2]

x1,x2 = x_arrays(n)
y1,y2 = y_arrays(m)

rows, cols = (2*m+1,2*n)
zeroth_order_nodal_list = [] #nodal list of 0th order (Base 2D List)

for i in range(m+1): #Making a 0th order nodal array
    p = [] #empty row that gets appended into the nodal array corresponding to x1
    q = [] #empty row that gets appended into the nodal array corresponding to x2
    if(i!= m):
        for j in range(cols):
            p.append([x1[j],y1[i]])
            q.append([x2[j],y2[i]])
        zeroth_order_nodal_list.append(p)
        zeroth_order_nodal_list.append(q)
    else:
        for j in range(cols):
            p.append([x1[j],y1[i]])
        zeroth_order_nodal_list.append(p)

def nodes_list(n_a, k): #n_a is the nodal array, u is alpha, k is order
    complete_nodes_list = [] #includes all the points of connectivity 2 & 3 (helps in making horizontal and vertical elements)
    if(k!= 0):
        print("Please enter the value of ratio between the side lengths of higher orders (or) alpha (It should be less than 1/3 ! you can give 0.25 for convenience) :")
        alpha = float(input())
        for j in range(len(n_a)):
            row = n_a[j]
            splitted_points_row = [] # for elements
            for i in range(len(row)):
                p = row[i]
                sum = i+j
                def generate_hexagonal_points(p, a, k, sum, alpha=0.1):
                    px, py = p  # coordinates of the center point

                    # Calculate six points around p at specified angles
                    angles = [-120, -60, 0, 60, 120, 180]
                    points = [
                        [px + a * math.cos(math.radians(angle)), py + a * math.sin(math.radians(angle))]
                        for angle in angles
                    ]

                    if k == 1:
                        return points  # Base case: return six points around p for k=1
                    
                    # Determine which indices to subdivide based on sum of indices rule
                    subdivide_indices = [0, 2, 4] if (sum % 2 == 0) else [1, 3, 5]

                    # Recursive case: for k > 1, create nested lists of points
                    def recursive_division(p, a, k, sum=0):
                        if k == 0:
                            return p

                        # Generate the hexagonal points around p
                        px, py = p
                        surrounding_points = [
                            [px + a * math.cos(math.radians(angle)), py + a * math.sin(math.radians(angle))]
                            for angle in angles
                        ]

                        # Recursive subdivision of points at the selected indices
                        for i in subdivide_indices:
                            surrounding_points[i] = recursive_division(
                                surrounding_points[i], a*alpha, k - 1, sum)

                        return surrounding_points

                    return recursive_division(p, a, k, sum)
                
                if(((i!=0 or j%2 ==0) and (i!= cols-1 or j%2 ==0)) and (j!=0 and j!=rows-1)): #condition to validate connectivity is 3
                    kth_order_points_set = generate_hexagonal_points(p, a*alpha, k, sum, alpha)
                    splitted_points_row.append(kth_order_points_set)
                else:
                    splitted_points_row.append(p)
            
            complete_nodes_list.append(splitted_points_row)
            
            
            
            
        return(complete_nodes_list)
    else:
        return(n_a)
    
kth_order_nodal_list = nodes_list(zeroth_order_nodal_list, k)

def store_plot_points(points):
    # Helper function to flatten the nested list of points
    def flatten_points(nested_points, flat_points=[]):
        
        for item in nested_points:
            if isinstance(item[0], list):  # If the item is a list of points, go deeper
                flatten_points(item, flat_points)
            else:
                flat_points.append(item.copy())  # Append the x, y point
            
        return flat_points
    
    # Flatten all points into a list of (x, y) tuples
    flattened_points = flatten_points(points)
    

    # Extract x and y coordinates for plotting
    x_coords = [p[0] for p in flattened_points]
    y_coords = [p[1] for p in flattened_points]

    
    
    # Plot the points
    
    plt.scatter(x_coords, y_coords, color="red")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Hexagonal kth order Nodal Points with 0th order Elements Plot")
    plt.grid(True)

    return flattened_points


"""print(kth_order_nodal_list)""" # if you want to print the list

#making and plotting function of zeroth order elemental array 
"""def zeroth_order_elemental_list(n_a):
    element_arr = [[],[]] # one list for horizontal elements and one list for slant elements
    for i in range(len(n_a)):
        p = n_a[i]
        q1 = [] #horizontal elements of a row
        if(i%2 == 0):
            for j in range(len(p)):
                if(j%2==0):
                    q1.append([p[j],p[j+1]])
                if (i!= len(n_a)-1):
                    q = n_a[i+1]
                    element_arr[1].append([p[j],q[j]])
        else:
            for j in range(len(p)):
                if(j%2==1 and j!=len(p)-1):
                    q1.append([p[j],p[j+1]])
                if (i!= len(n_a)-1):
                    q = n_a[i+1]
                    element_arr[1].append([p[j],q[j]])
        if(q1 != []):
            element_arr[0].append(q1)

    

    
    return(element_arr)

zeroth_elemental_list = zeroth_order_elemental_list(zeroth_order_nodal_list)
     
for q in zeroth_elemental_list[0]: # plot for 0nly 0th order elements
    for p in q:
        plt.plot([p[0][0],p[1][0]],[p[0][1],p[1][1]], 'k-')

for p in zeroth_elemental_list[1]:
    plt.plot([p[0][0],p[1][0]],[p[0][1],p[1][1]], 'k-')"""

def get_point(p,i): # we want last point of order k at the ith index in p. Assumes length greater than 2
    if(len(p)==2):
        return p
    elif(len(p[i])==2):
        return(p[i])
    elif(len(p[i])>=6):
        return get_point(p[i],i)

#Gives back element array for a splitted point       
def element_array(p,sum, e_a=[]):
    
    def lastset(p): # works for a tuple as well
        c = 0
        for i in p:
            if(len(i)>2):
                c = c+1
        if(c>0):
            return False
        elif(c==0):
            return True
        
        
    def connect_hex(p,arr): #accepts a tuple input as well
        for i in range(len(p)):
            if(len(p[i]) == 2 and i!=len(p)-1):
                arr.append([p[i],p[i+1]])
            elif(len(p[i]) == 2 and i== len(p)-1):
                arr.append([p[i],p[0]])
            else:
                return(print("Can't Build a Hexagon"))
    
    def connecting_points(p,i): # connecting points of the point p[i]
        #h, i, j are indices of previous, current and next point when taken in CCW sense
        if(i == 0):
            h = 5
            j = i+1
        elif(i == 5):
            h = i-1
            j = 0
        else:
            h = i-1
            j = i+1
        
        if(len(p[h])<=2 or len(p[j])<=2):
            print('Same level point')
        else:
            c1 = get_point(p[h],j)
            c2 = get_point(p[j],h)
            return(c1,c2)

 #Actual code starts from here
    if(len(p)<=2):
        return(print("Not a useful point for forming elements"))
    else:
        if(lastset(p)):
            connect_hex(p,e_a)
        else:
            for i in range(6):
                if ((sum%2 ==0 and i in [0,2,4]) or (sum%2 ==1 and i in [1,3,5])):
                    element_array(p[i],sum, e_a)
                else:
                    c1, c2 = connecting_points(p,i)
                    e_a.append([p[i],c1])
                    e_a.append([p[i],c2])
        return e_a



written_rows = set()  # Use a set to track unique rows

def plot_lines_for_splitted_points(lines):
    """
    Plots a list of lines on a 2D plot. Each line is represented by a list of two points,
    where each point is a list of [x, y] coordinates.
    
    Parameters:
        lines (list): A list of lines, where each line is a list of two points, and each point is [x, y].
    """
    for line in lines:
        # Extract the two points of the line
        (x1, y1), (x2, y2) = line
        
        # Plot the line
        plt.plot([x1, x2], [y1, y2], color='b')
        
        # Find indices of the points
        n1 = search_index([x1, y1], flattend_points)
        n2 = search_index([x2, y2], flattend_points)
        
        # Prepare the row for CSV
        csv_row = (n1, n2)  # Use a tuple for set compatibility
        
        # Write to CSV only if the row is new
        if csv_row not in written_rows:
            writer.writerow(csv_row)
            written_rows.add(csv_row)  # Add to the set to track uniqueness

    

"""
for j in range(rows):
    for i in range(cols):
        if(((i!=0 or j%2 ==0) and (i!= cols-1 or j%2 ==0)) and (j!=0 and j!=rows-1)): #condition to validate connectivity is 3
            p = kth_order_nodal_list[j][i]
            elements_connected_point = element_array(p, i+j)
            plot_lines(elements_connected_point)
"""



elements_list = [[],[],[]] # first list for storing horizontal elements, second list for vertical elements and third for splitted points

def full_elements_array(elements_list = [[],[],[]]): 
    for i in range(rows):
        h_e = [] #one row of horizontal elements
        v_e = [] #one row of vertical elements
        p_e = [] #one row of splitted point elements
        row = kth_order_nodal_list[i]
        for j in range(cols):
            p = row[j] #the point / place where we are at
            sum = i+j
            if(j!= cols-1):
                s = row[j+1] #side point
            if(i!= rows-1):
                u = kth_order_nodal_list[i+1][j] #upper point
            
            #((i!=0 or j%2 ==0) and (i!= cols-1 or j%2 ==0)) and (j!=0 and j!=rows-1) notice the interchange of i and j in previous and current conditional
            
            if(((j!=0 or i%2 ==0) and (j!= cols-1 or i%2 ==0) and (i!=0 and i!= rows-1))): #If a point is of connectivity 3 store its splitted elements
                p_e.append(element_array(p,sum))

            if(sum%2 == 0): # if a point is even store its horizontal element and only if its not a point on top row store its vertical element
                
                h1 = get_point(p,2)
                h2 = get_point(s,5)
                h_e.append([h1,h2])

                if(i!=rows-1):
                    v1 = get_point(p,4)
                    v2 = get_point(u,1)
                    v_e.append([v1,v2])

            elif((sum%2 == 1) and (i != rows-1)):
                v1 = get_point(p,3)
                v2 = get_point(u,0)
                v_e.append([v1,v2])
        
        if(h_e != []):
            elements_list[0].append(h_e)
        if(v_e != []):
            elements_list[1].append(v_e)
        if(p_e != []):
            elements_list[2].append(p_e)
    return elements_list

elements_list = full_elements_array()

nodes = "nodes.csv"

# Open the file manually
file = open(nodes, mode="w", newline="")

# Create a CSV writer object
writer = csv.writer(file)

# Writing the header
writer.writerow(["n","x", "y"])

flattend_points = store_plot_points(kth_order_nodal_list)

c= 0
for points in flattend_points:
    c= c+1
    points.insert(0,c)

writer.writerows(flattend_points)
file.close()



print(f"Data has been written to {nodes}")


print(f"Current Working Directory: {os.getcwd()}")


def search_index(p,arr):

    for point in arr:
        if(p[0]==point[1] and p[1]==point[2]):
            return point[0]



"""

print(elements_list[0])
print('\n',elements_list[1])
print('\n',elements_list[2])
"""


master_elements = "master_elements.csv"

# Open the file manually
file = open(master_elements, mode="w", newline="")

# Create a CSV writer object
writer = csv.writer(file)

# Writing the header
writer.writerow(["n1","n2"])


for row in elements_list[0]:
    for line in row:
        # Extract the two points of the line
        (x1, y1), (x2, y2) = line
        # Plot the line
        plt.plot([x1, x2], [y1, y2], color='b')
        
        n1 = search_index([x1,y1],flattend_points)
        n2 = search_index([x2,y2],flattend_points)
        csv_row = [n1,n2]
        writer.writerow(csv_row)
    # Set equal scaling for x and y axes for better representation



for row in elements_list[1]:
    for line in row:
        # Extract the two points of the line
        (x1, y1), (x2, y2) = line
        # Plot the line
        plt.plot([x1, x2], [y1, y2], color='b')
        n1 = search_index([x1,y1],flattend_points)
        n2 = search_index([x2,y2],flattend_points)
        csv_row = [n1,n2]
        writer.writerow(csv_row)




for row in elements_list[2]:
    for splitted_point in row:
        plot_lines_for_splitted_points(splitted_point)

file.close()

print(f"Data has been written to {master_elements}")


print(f"Current Working Directory: {os.getcwd()}")

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Plot of Lines")
plt.grid(True)
plt.axis("equal")

plt.show()