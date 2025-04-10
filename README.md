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
The suggested logistics system will take the input of two types of information. One is delivery packages are described as sets of three components: delivery location (as coordinate pairs or node numbers of delivery graph), physical dimensions (size and/or weight), and priority class (e.g., high or usual). The other being two delivery vehicles described as sets of two components: car capacity and delivery function. Truck 1 is specialized to high-priority packages to deliver as soon as possible, and Truck 2 deals with overflows and lower priorities.
The system outputs the route of delivery per truck and its corresponding order of loading. The paths are formed through an efficient greedy plan when they are created, and the order of loading from delivery order reversal–i.e., the earliest package required to the last one to be loaded.
These outputs are created by having the system execute the following  series of operations. It first allocates packages to the vehicles according to their priority and capacity. Then it calculates the delivery route of each vehicle according to the Nearest Neighbor heuristic. Having determined the delivery route, it generates the loading order according to the strategy of adding a stack data structure to reverse the delivery order. In the interest of fairness, an aging mechanism is implemented to give increasing priority to lower-priority packages aging beyond a certain threshold.
The system is subject to several key constraints. Trucks cannot be overfilled to their rated capacity. Priority packages must be shipped before lower-priority packages. And most critically, regular-priority packages cannot be starved; fairness must be implemented using aging or batch handling. This part most readily satisfies the systems engineering aspect of the problem by defining the logistics workflow as an orthodox data processing pipe.

## **3. Algorithm and Data Structure Justification (30%)**
The system makes use of various graph and algorithmic approaches outlined in the COMP20230 course notes. In delivery routing, delivery locations are graph vertices and delivery distances are weighted edges. For figuring out the delivery order, the greedy Nearest Neighbor algorithm is applied. Although this does not provide the best possible route for the TSP, it significantly reduces computational complexity and is good enough to give reasonable approximations for this situation. Using these simplified approaches, as discussed in Lecture 16, strikes a balance between performance and simplicity.
For scheduling, the priority queue implemented as a binary heap allows the removal of highest packages effectively. This allows high-priority deliveries to be allocated first, and the system may allow insertions and removals as often as logarithmic time. For ensuring fairness, the system incorporates an aging mechanism whereby the active priority of pending packages is raised periodically. This does not let lower-priority deliveries get constantly deferred and reflects how scheduling solutions are implemented within operating systems for processes.
The truck loading makes use of a stack to apply Last-In-First-Out (LIFO). The packages are pushed onto the stack in the opposite delivery order, i.e., the packages of the first stop are packed last. This straightforward yet efficient implementation takes inspiration from Lecture 6's discussion of the LIFO principle. Hash maps implemented using Python dictionaries are made use of to support quick lookup of package metadata, destination, size, and priority, etc., with O(1) average-case access to help achieve an efficient overall system.
Both the data structure and the algorithm were selected for their respective simplicity of implementation, scalability, and time efficiency. Avoiding using brute-force TSP or bin-packing was done intentionally in the interests of simplification for faster execution and easier interpretation, as this situation is an abstracted version of what would be encountered in a much more complex real world situation. While these simplifications undeniably leave out some of the detail that would exist in real logistics systems, it allows for the demonstration of these algorithms in a manner that is simple enough to be implemented by us but still demonstrates the algorithms solving a real world problem albeit abstracted.

## **4. Modelling and Implementation Considerations (20%)**
This system models delivery geography as simple 2D gridding or as graph mapping where delivery point-to-point distance is modeled as weight. Abstraction makes it possible to simulate cities realistically. Delivery locations are modeled as vertices or as coordinates, and vertices are joined by edges having Euclidean or road-based weights.
Object-oriented design is leveraged to encapsulate all different entities. Package class encapsulates all package information including package size, target location, and adjusted aging due to priority. Truck class keeps its capacity, loaded stack, and route and consists of package adding, deleting, and visualization operations. RouteOptimizer class carries on routing scheduling using the Nearest Neighbor routing and can include 2-opt routing optimization to achieve maximum efficiency. A class named Scheduler deals with priority queue and aging to achieve fairness without resulting in system overload.
Test and simulation use surrogate package sets of varying size and priority blend. For example, some use all high-priority packages, and they use sets of low-priority packages that require the aging mechanism so that delivery is assured. Overflows also exercise the truck assignment mechanism and verify Truck 2 is filled when Truck 1 is full.
Challenges are maintaining the route and stacking consistent, forcing the aging mechanism to alter priorities appropriately over time without costing much computation, and maintaining creation of the route as efficient and punctual as possible. There also needs to be testing to incorporate system behavior in corner cases, i.e., when all packages are equidistant from the router and when various packages are of the same priority.
Design considerations prefer simplicity and robustness over final accuracy and completeness. Rather than solving NP-hard spatial bin-packing problems to optimize loading, the system makes the simplifying assumptions of applying weight or size constraints linearly and having purely stack-based spatial analysis. These are pedagogic and practical trade-offs and are nonetheless evincing the usefulness of classical algorithms and data structures.
