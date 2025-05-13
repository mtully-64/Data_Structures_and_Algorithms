# **Instructions**

## **Objective:**
The objective of this assignment is to apply the principles of algorithms and data structures to solve real-world problems by designing a system that addresses a specific need or solve a particular problem. Students will demonstrate their understanding of fundamental algorithms and data structures, their ability to analyze trade-offs, and their capacity to justify their design choices.

## **Tasks:**

- Select a Real-World Problem: 
    - Choose a real-world problem that can be solved using computer algorithms and data structures. This could be anything from optimizing a transportation network to managing a social media platform's feed.

- System Design Proposal: 
    - Propose a high-level system design that addresses the chosen problem. Outline the functionalities of the system, including input/output requirements, key operations, and any constraints.

- Algorithm and Data Structure Selection: 
    - Identify and justify the algorithms and data structures that will be used in your system design. Consider factors such as efficiency, scalability, and complexity. Explain how these choices align with the requirements and constraints of the problem.

- Modelling and Implementation: 
    - Describe how you would model the problem using the chosen algorithms and data structures. Discuss any challenges or considerations in implementing your design. Implement a basic version (a prototype, demo) of your system, including sample data, data structures and algorithms. 


## **Grading Rubric:**

- Problem Selection (15 points)
    - Clear articulation of the chosen real-world problem.
    - Relevance and significance of the problem in real-world contexts.
- System Design Proposal (15 points)
    - Comprehensive description of system functionalities.
    - Identification of key operations and constraints.
- Algorithm and Data Structure Justification (30 points)
    - Well-justified selection of algorithms and data structures.
    - Consideration of efficiency, scalability, and complexity.
Awareness of trade-offs and alternatives.
- Modelling and Implementation (20 points)
    - Thoughtful discussion of how the problem is modeled using chosen algorithms and data structures.
    - Identification of potential challenges and considerations in implementation.
- Clarity and Presentation (20 points)
    - Organization and clarity of writing.
    - Proper use of technical terminology.
    - Overall coherence and professionalism.
    - System Design Proposal: Optimizing Package Loading and Delivery Routing for an Amazon-Style Logistics System

---

# **Answers**

## The Optimisation of Package Loading and Delivery Routing for an Amazon-Style Logistics System 

### 1. Problem Statement 
In today’s competitive e-commerce landscape, logistics plays a crucial role in maintaining customer satisfaction and 
operational efficiency. Large-scale logistic services such as Amazon Prime, require seamless integration between 
route planning and package handling to ensure timely, prioritized deliveries. This project identifies and proposes a 
solution for two interconnected challenges in last-mile logistics. Firstly, delivery routes must be optimized to 
minimize both travel time and fuel consumption. Secondly, packages need to be loaded into delivery trucks in a 
manner that supports the delivery sequence. Packages intended for earlier delivery must be more accessible, 
meaning they should be loaded last. 

This system design proposal will model a logistics system that incorporates these considerations, by making 
algorithmic decisions based on package priority, truck capacity, and delivery route structure. Additionally, it 
considers the problem of starvation, where low-priority packages could be delayed indefinitely, and offers a solution 
through “aging”, a mechanism that gradually increases a package’s effective priority over time. By addressing both 
efficiency and fairness, this system provides a realistic, scalable approach to the demands of real-world delivery 
networks. 

### 2. System Design and Functionality 
The system takes two types of input: details about delivery packages and information about delivery vehicles. Each 
package is described by its delivery location (graph coordinates), physical size and weight, and priority level ('high' 
or 'low'). Each vehicle is assigned certain types of packages based on their priority and delivery needs. For 
example, Truck 1 focuses on the delivery of high-priority packages and assuring its arrival as soon as possible. 
Truck 2 deals with overflows and lower priority parcel shipping. 

Therefore utilising the previous information referenced, the logistics system will output each truck’s route of delivery 
and its corresponding loading order. The delivery routes are formed using an efficient algorithm, known as the 
“greedy algorithm” (Cormen, Leiserson, Rivest, & Stein, 2009). The order of loading is determined by the reverse of 
the delivery order: the earliest package to be delivered will be loaded in the end. 
These outputs are created by having the system execute the following series of operations. It first allocates 
packages to the vehicles according to their priority and capacity. Then it calculates the delivery route of each vehicle 
according to the Nearest Neighbor heuristic (Stopka, 2020).  

Having determined the delivery route, it generates the loading order according to the reverse delivery order. In the 
interest of fairness, an aging mechanism is implemented to give increasing priority to lower-priority packages aging 
beyond a certain threshold. The system is subject to several key constraints. Trucks cannot be overfilled to their 
rated capacity. Priority packages must be shipped before lower-priority packages. Additionally, regular-priority 
packages cannot be starved and fairness must be implemented using aging. 

### 3. Algorithm and Data Structure Justification 
For planning out the order of delivery to the various nodes the system uses the Greedy Nearest Neighbour (GNN) 
algorithm, which always moves to the nearest unvisited location and has a standard time complexity of O(n²). 
Although this doesn’t guarantee the shortest possible path for the Travelling Salesman Problem (TSP) it significantly 
reduces computational complexity compared to exact solutions like the Held-Karp algorithm which has a time 
complexity of O(n²·2ⁿ) while being simpler to implement compared to more optimal algorithms. This careful balance 
between efficiency, optimality and simplicity makes the GNN a practical choice for our simplified logistics problem 
(Johnson & McGeoch, 1997). 

For scheduling deliveries, the system uses a priority queue implemented using a heap-based structure via Python’s 
heapq library, to efficiently manage package priorities with the design. Thus, ensuring that high priority packages 
are handled first, with insertions and removals operating in logarithmic time (O(log n)), allowing for the system to 
efficiently scale up as package numbers increase. 

To maintain fairness the system incorporates an ageing mechanism that gradually increases the priority of lower 
priority packages over time, hence preventing them from being postponed indefinitely. This draws inspiration from 
process scheduling techniques in operating systems (Silberschatz, Galvin, and Gagne, 2005). 

For truck loading, a Last-in-First-Out (LIFO) approach is utilised through a stack with packages being loaded onto 
the truck in the reverse order of delivery. For example, the first package to be delivered will be loaded onto the truck 
last so it can be easily accessed at the first delivery stop, making LIFO a great fit for this system. Additionally the 
use of hashmaps implemented through Python dictionaries are used to enable fast constant time (O(1)) lookups of 
package information such as; destination, size, and priority, supporting fast access during both scheduling and 
loading operations. 

By choosing simple heuristics and efficient data structures our delivery system remains fast, scalable, easy to 
implement and understandable. Although we avoid the use of exact TSP solutions like the Held-Karp algorithm, as 
well as more complex alternatives suggested by (Johnson & McGeoch, 1997), in favour of our GNN approach for its 
scalability and ease of implementation.  

These simplifications in our design were deliberate, as the system is supposed to model an abstracted version of 
real world delivery logistics problems. While this abstraction inevitably excludes some of the complexities that exist 
in real world logistical operations, it captures the primary challenges of this industry such as routing, loading and 
prioritizing in a manner that is feasible to be implemented within our project scope. However, while still also 
demonstrating how algorithmic solutions can be effectively applied in practice to solve real world problems. 

### 4. Modelling and Implementation Considerations 
The problem was modelled using the data structure of a graph, where each individual delivery location is treated as 
a vertex and the Euclidean distance between each pair of points will act as a weight edge. This allows for a more 
simplified but effective representation of a city’s delivery grid without the need of real-world mapping APIs. All the 
distance calculations are carried out on demand using the calc_distance() method of the RouteOptimizer class, 
this ensures that there is efficiency and we avoid the overhead of storing an entire adjacency matrix. The route 
planning is executed using the Greedy Nearest Neighbour (GNN) algorithm that is calculated in the 
find_best_route() method. Albeit the GNN does not guarantee the most optimal path, it is computationally efficient 
and suitable for the scale of logistics problems that are considered in this project (Johnson and McGeoch, 1997; 
Stopka, 2020). 

Our system follows OOP principles, where each of the main components of the system are organised into their own 
distinct classes. The Package class stores the essential delivery information of each package, such as its 
coordinates, size, weight and priority, alongside functions for the aging and computation of a parcel’s effective 
priority. This aging mechanism is essential for us to prevent the starvation of lower-priority packages, by the gradual 
increase of a parcel’s importance over time (Silberschatz et al., 2005). The trucks are characterised by the Truck 
class, which keeps track of each truck’s maximum parcel capacity, delivery route and Last-In-First-Out (LIFO) stack 
that models the loading order of packages with the create_loading_order() method. Ensuring that the first package 
intended to be delivered is the last one that is loaded into the truck, enabling a quick and efficient unload at each 
stop. 

The package scheduling is managed using the Scheduler class, this class implements a heap-based priority queue 
using Python’s heapq module. This data structure implementation provides an efficient O(log n) insertion and 
removal operations, supporting the use of methods such as add(), get_next() and apply_aging() to manage the 
order in which the packages are delivered (Python Software Foundation, 2024). The entire coordination of the 
system is handled by the Loader class, as it assigns the packages to a truck based on capacity and priority, applies 
the route optimisation, generates the correct truck loading order and produces the final delivery statistics via the 
print_summary() method. 

Several challenges arose while implementing this system. One challenge was maintaining the consistency between 
the delivery route and the LIFO based loading order; this point was addressed by deferring loading until after the 
routing is completed. Another challenge was applying the aging of a parcel in a fair manner without significantly 
slowing down the system, which was managed by only selectively triggering the aging function when a scheduling 
cycle fails to assign any packages. Finally, the scalability of this system is a key concern; whilst the current 
implementation handles a small to moderate workload effectively, it also deliberately strays from real-world 
complexities such as live traffic or real time order changes in favour of a more manageable/demonstrable system 
prototype. By balancing practical implementation with conceptual modelling, this system has the potential to provide 
a strong foundation for future extensions. 

### 5. References 

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (2009). Introduction to 
Algorithms (3rd Edition). MIT Press. Pg 414-430. URL: https://go.exlibris.link/8hGW2CJG   
2. Ondrej Stopka (2020). “Modeling the Delivery Routes Carried out by Automated Guided Vehicles when Using 
the Specific Mathematical Optimization Method.” Open Engineering 10(1): 166–174. URL: 
https://go.exlibris.link/3J1tKjwr  
3. David S. Johnson and Lyle A. McGeoch (1997). The Traveling Salesman Problem: A Case Study in Local 
Optimization. In: Dorit S. Hochbaum (ed.) Approximation Algorithms for NP-Hard Problems, PWS Publishing, 
Boston, 215–310. Available at: 
https://www.cs.ubc.ca/~hutter/previous-earg/EmpAlgReadingGroup/TSP-JohMcg97.pdf   
4. Silberschatz, A., Galvin, P.B., and Gagne, G. (2005). Operating System Principles, 7th Edition, John Wiley & 
Sons, p.159-167. Available at 
https://web.uettaxila.edu.pk/CMS/AUT2011/seAOSbs/notes/Text%20-%20Silberschatz.Galvin%20-%20Operat
 ing.System.Concepts.7th.pdf   
5. Johnson, D.S. and McGeoch, L.A. (1997). ‘The Traveling Salesman Problem: A Case Study in Local 
Optimization’, in Hochbaum, D.S. (ed.) Approximation Algorithms for NP-Hard Problems. PWS Publishing, 
Boston, pp. 215–310. Available at: 
https://www.cs.ubc.ca/~hutter/previous-earg/EmpAlgReadingGroup/TSP-JohMcg97.pdf  
6. Python Software Foundation (2024). heapq - Heap queue algorithm. Available at: 
https://docs.python.org/3/library/heapq.html

#### Youtube Videos 
1. The Traveling Salesman Problem: When Good Enough Beats Perfect 
2. Heaps & Priority Queues - Heapify, Heap Sort, Heapq Library - DSA Course in Python Lecture 9 
3. Construction Heuristic For Traveling Salesman Problem (TSP) in Python

