import math

# Package class for representing delivery items
class Package:
    def __init__(self, package_id, x, y, size, weight, priority):
        self.id = package_id  # unique identifier
        self.coordinates = (x, y)  # location for delivery
        self.size = size  
        self.weight = weight
        self.priority = priority  # High or Normal
        self.age = 0  # for aging mechanism
    
    def __str__(self):
        return f"Package {self.id}: ({self.priority} priority) at {self.coordinates}"
    
    # Age increases waiting time importance
    def increase_age(self):
        self.age += 1
        return self.age
    
    def get_effective_priority(self):
        # High priority packages start with higher base value
        if self.priority == 'High':
            base = 100
        else:
            base = 10
        return base + self.age  # age adds to priority


# Class for delivery trucks
class Truck:
    def __init__(self, id, capacity, role, warehouse=(0, 0)):
        self.id = id
        self.max_capacity = capacity
        self.role = role  # High-priority or Normal
        self.current_weight = 0
        self.route = []  # delivery sequence
        self.packages_to_load = []  # loading stack (LIFO)
        self.starting_point = warehouse
        self.route_distance = 0
    
    def __str__(self):
        return f"Truck {self.id} ({self.role}): {self.current_weight}/{self.max_capacity} capacity used"
    
    # Check if we can add more weight
    def has_capacity_for(self, package):
        return self.current_weight + package.weight <= self.max_capacity
    
    # Add package to delivery route
    def add_package(self, package):
        self.route.append(package.id)
        self.current_weight += package.weight
    
    # Build loading stack (reverse of delivery order)
    def create_loading_order(self, packages_dict):
        # Clear the loading stack first
        self.packages_to_load = []
        
        # Remember: last delivery = first loaded!
        for package_id in reversed(self.route):
            self.packages_to_load.append(packages_dict[package_id])
    
    # Calculate total route distance
    def calculate_route_length(self, packages_dict):
        if not self.route:
            return 0
        
        total = 0
        current = self.starting_point
        
        # Calculate distance between each stop
        for pkg_id in self.route:
            package = packages_dict[pkg_id]
            next_stop = package.coordinates
            
            # Use Euclidean distance
            distance = math.sqrt((current[0] - next_stop[0])**2 + 
                                (current[1] - next_stop[1])**2)
            total += distance
            current = next_stop
        
        # Add return trip to warehouse
        return_dist = math.sqrt((current[0] - self.starting_point[0])**2 + 
                               (current[1] - self.starting_point[1])**2)
        total += return_dist
        
        self.route_distance = total
        return total
    
    # Print the delivery route for this truck
    def show_route(self, packages_dict):
        print(f"\nDelivery Route for Truck {self.id}:")
        print(f"Starting at Warehouse {self.starting_point}")
        
        for i, pkg_id in enumerate(self.route, 1):
            package = packages_dict[pkg_id]
            print(f"  Stop {i}: {package}")
        
        print(f"Return to Warehouse {self.starting_point}")
        print(f"Total distance: {self.route_distance:.2f} units")
    
    # Print loading order
    def show_loading_order(self):
        print(f"\nLoading Order for Truck {self.id} (LIFO):")
        for i, package in enumerate(self.packages_to_load, 1):
            print(f"  {i}. Load Package {package.id} ({package.priority} priority)")
    
    # Calculate statistics about packages
    def get_stats(self):
        if not self.packages_to_load:
            return {"high": 0, "normal": 0, "weight": 0, "usage": 0}
        
        high_count = 0
        normal_count = 0
        total_weight = 0
        
        for p in self.packages_to_load:
            if p.priority == 'High':
                high_count += 1
            else:
                normal_count += 1
            total_weight += p.weight
        
        return {
            "high": high_count,
            "normal": normal_count,
            "weight": total_weight,
            "usage": (total_weight / self.max_capacity) * 100
        }