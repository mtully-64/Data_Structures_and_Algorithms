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

## **1. Problem Statement (15%)**
In today’s competitive e-commerce landscape, logistics plays a crucial role in maintaining customer satisfaction and operational efficiency. Large-scale logistic services such as Amazon Prime, require seamless integration between route planning and package handling to ensure timely, prioritized deliveries. This project identifies and proposes a solution for two interconnected challenges in last-mile logistics. Firstly, delivery routes must be optimized to minimize both travel time and fuel consumption. Secondly, packages need to be loaded into delivery trucks in a manner that supports the delivery sequence. Packages intended for earlier delivery must be more accessible, meaning they should be loaded last.
This system design proposal will model a logistics system that incorporates these considerations, by making algorithmic decisions based on package priority, truck capacity, and delivery route structure. Additionally, it considers the problem of starvation, where low-priority packages could be delayed indefinitely, and offers a solution through “aging”, a mechanism that gradually increases a package’s effective priority over time. By addressing both efficiency and fairness, this system provides a realistic, scalable approach to the demands of real-world delivery networks.


## **2. System Design and Functionality (15%)**
The system takes two types of input: details about delivery packages and information about delivery vehicles. Each package is described by its delivery location (graph coordinates), physical size or weight, and priority level ('high' or 'low'). Each vehicle is assigned certain types of packages based on their priority and delivery needs. For example, Truck 1 focuses on the delivery of high-priority packages and assuring its arrival as soon as possible. Truck 2 deals with overflows and lower priority parcel shipping.
Therefore utilising the previous information referenced, the logistics system will output each truck’s route of delivery and its corresponding loading order. The delivery routes are formed using an efficient algorithm, known as the “greedy algorithm” (Cormen, Leiserson, Rivest, & Stein, 2009). The order of loading is determined by the reverse of the delivery order: the earliest package to be delivered will be loaded in the end.
These outputs are created by having the system execute the following series of operations. It first allocates packages to the vehicles according to their priority and capacity. Then it calculates the delivery route of each vehicle according to the Nearest Neighbor heuristic (Stopka, 2020). 
Having determined the delivery route, it generates the loading order according to the reverse delivery order. In the interest of fairness, an aging mechanism is implemented to give increasing priority to lower-priority packages aging beyond a certain threshold. The system is subject to several key constraints. Trucks cannot be overfilled to their rated capacity. Priority packages must be shipped before lower-priority packages. Additionally, regular-priority packages cannot be starved and fairness must be implemented using aging.


## **3. Algorithm and Data Structure Justification (30%)**
For planning out the order of delivery to the various nodes the system uses the Greedy Nearest Neighbour (GNN) algorithm, which always moves to the nearest unvisited location and has a standard time complexity of O(n²). Although this doesn’t guarantee the shortest possible path for the Travelling Salesman Problem (TSP) it significantly reduces computational complexity compared to exact solutions like the Held-Karp algorithm which has a time complexity of O(n²·2ⁿ) while being simpler to implement compared to more optimal algorithms. This careful balance between efficiency, optimality and simplicity makes the GNN a practical choice for our simplified logistics problem (Johnson & McGeoch, 1997).
For scheduling deliveries, the system uses a priority queue implemented using a heap-based structure via Python’s heapq library, to efficiently manage package priorities with the design. Thus, ensuring that high priority packages are handled first, with insertions and removals operating in logarithmic time (O(log n)), allowing for the system to efficiently scale up as package numbers increase. 
To maintain fairness the system incorporates an ageing mechanism that gradually increases the priority of lower priority packages over time, hence preventing them from being postponed indefinitely. This draws inspiration from process scheduling techniques in operating systems (Silberschatz, Galvin, and Gagne, 2005).
For truck loading, a Last-in-First-Out (LIFO) approach is utilised through a stack with packages being loaded onto the truck in the reverse order of delivery. For example, the first package to be delivered will be loaded onto the truck last so it can be easily accessed at the first delivery stop, making LIFO a great fit for this system. Additionally the use of hashmaps implemented through Python dictionaries are used to enable fast constant time (O(1)) lookups of package information such as; destination, size, and priority, supporting fast access during both scheduling and loading operations.
By choosing simple heuristics and efficient data structures our delivery system remains fast, scalable, easy to implement and understandable. Although we avoid the use of exact TSP solutions like the Held-Karp algorithm, as well as more complex alternatives suggested by (Johnson & McGeoch, 1997), in favour of our GNN approach for its scalability and ease of implementation. 
These simplifications in our design were deliberate, as the system is supposed to model an abstracted version of real world delivery logistics problems. While this abstraction inevitably excludes some of the complexities that exist in real world logistical operations, it captures the primary challenges of this industry such as routing, loading and prioritizing in a manner that is feasible to be implemented within our project scope. However, while still also demonstrating how algorithmic solutions can be effectively applied in practice to solve real world problems.


## **4. Modelling and Implementation Considerations (20%)**
The delivery network is modelled using a graph data structure, where the delivery locations are the ‘vertices’ and ‘Euclidean distances’ are the weighted edges , providing a simple but realistic simulation of the city grid without the use of external mapping data. Distance calculations are performed within the calc_distance() method of the RouteOptimizer class.
The system utilises an object oriented design to encapsulate all of its major entities. The Package class caches all delivery coordinates, parcel sizes, parcel weights and parcel priority (“High” or “Normal”), including methods for parcel aging (increase_age()) and calculating the effective priority of a parcel (get_effective_priority()) to manage prevention of parcel starvation (Silberschatz et al., 2005). Truck objects represent the delivery vehicles, maintaining their maximum weight capacity and delivery route, using the create_loading_order() method to arrange the packages in a Last-In-First-Out (LIFO) order for efficient parcel unloading. 
Route planning is then performed by the RouteOptimizer class, as it implements the Greedy Nearest Neighbor (GNN) heuristic through its innate find_best_route() method  (Johnson and McGeoch, 1997). Albeit the GNN algorithm does not guarantee the most optimal delivery path, it provides an efficient and scalable solution that suits the needs of real-time logistic constraints (Stopka, 2020). The make_route_map() method within the RouteOptimizer is utilised to visualise the resulting delivery routes via Matplotlib.
The package scheduling is managed by the Scheduler class, where it maintains a heap based priority queue (using Python’s heapq library) to enable O(log n) insertion and removal of parcels from the queue (Python Software Foundation, 2024). This class also uses the add(), get_next() and apply_aging() methods to manage the package prioritisation and prevent package starvation from occurring by periodically boosting lower priority packages.
The Loader class integrates all of these components together. It assigns each package to the appropriate truck based on its priority and the truck’s available capacity (assign_packages()). The class then applies the route optimisation to the truck (find_best_route() from RouteOptimizer), generates its loading order (create_loading_order() from Truck), and summarises final delivery statistics (print_summary()). 
Key challenges to this system include: the maintenance of consistency between the planned delivery route and the LIFO based loading order, ensuring fairness through aging without the incurring significant computational overhead, and designing the overall system for scalability. While the system focuses on modelling the core concepts/challenges of routing, scheduling and loading, it deliberately abstracts away more complex real world factors, such as dynamic traffic conditions, real time order updates and maintaining the balance between realism and practical implementability.

