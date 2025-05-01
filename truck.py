import math

class Truck:
    """
    Class representing a delivery truck
    """
    def __init__(self, id, capacity, role, warehouse=(0, 0)):
        
        self.id = id
        self.max_capacity = capacity # maximum weight capacity
        self.role = role  # High-priority or Normal
        self.starting_point = warehouse # coordinates of the warehouse
        
        self.current_weight = 0
        self.route = []         # delivery sequence :  #ist of package IDs in delivery order
        self.packages_to_load = []  # list of Package objects, in LIFO loading order
        self.route_distance = 0   # total length of the completed route
    
    
    def __str__(self):
        return f"Truck {self.id} ({self.role}): {self.current_weight}/{self.max_capacity} capacity used"
    
    
    def has_capacity_for(self, package):
        """
        Method to check if the truck has enough capacity for a new package (based on weight)
        """
        return self.current_weight + package.weight <= self.max_capacity
    

    def add_package(self, package):
        """
        Method to add a package to the delivery route
        """
        self.route.append(package.id)
        self.current_weight += package.weight
    
    
    def create_loading_order(self, packages_dict):
        """
        Build a loading stack --> LIFO (Last In First Out)
        The last package to be delivered is the first one to be loaded
        """
        
        # Clear the loading stack first
        self.packages_to_load = []
        
        # Load packages in reverse order of delivery
        for package_id in reversed(self.route):
            # packages_dict has this structure: {package_id: Package object}
            # route has the package IDs in delivery order
            self.packages_to_load.append(packages_dict[package_id])
    
    

    def calculate_route_length(self, packages_dict):
        """
        Calculate the total distance of the delivery route
        """
        
        if not self.route:
            return 0
        
        total_distance = 0
        current = self.starting_point # starting point is the warehouse
        
        # Calculate distance between each stop
        for pkg_id in self.route:
            package = packages_dict[pkg_id]
            next_stop = package.coordinates
            
            # Use Euclidean distance
            distance = math.sqrt((current[0] - next_stop[0])**2 + 
                                (current[1] - next_stop[1])**2)
            
            total_distance += distance
            current = next_stop
        
        # Add return trip to warehouse
        return_dist = math.sqrt((current[0] - self.starting_point[0])**2 + 
                               (current[1] - self.starting_point[1])**2)
        
        total_distance += return_dist
        
        self.route_distance = total_distance
        return total_distance
    
    
    def show_route(self, packages_dict):
        """
        Print the delivery route for the truck
        """
        print(f"\nDelivery Route for Truck {self.id}:")
        print(f"Starting at Warehouse {self.starting_point}")
        
        for i, pkg_id in enumerate(self.route, 1):
            package = packages_dict[pkg_id]
            print(f"  Stop {i}: {package}")
        
        print(f"Return to Warehouse {self.starting_point}")
        print(f"Total distance: {self.route_distance:.2f} units")
    
    
    def show_loading_order(self):
        """
        Print the loading order for the truck
        """
        print(f"\nLoading Order for Truck {self.id} (LIFO):")
        for i, package in enumerate(self.packages_to_load, 1):
            print(f"  {i}. Load Package {package}")
    
    
    
    def get_stats(self):
        """
        Calculate statistics about the packages loaded in the truck
        """
        
        if not self.packages_to_load:
            stats_dict = {"high": 0, "normal": 0, "weight": 0, "usage": 0}
        
        high_count = 0
        normal_count = 0
        total_weight = 0
        
        for package in self.packages_to_load:
            if package.priority_label == 'High':
                high_count += 1
            else:
                normal_count += 1
            total_weight += package.weight
        
        stats_dict = {
            "high": high_count,
            "normal": normal_count,
            "weight": total_weight,
            "usage": (total_weight / self.max_capacity) * 100
        }
        
        self.stats = stats_dict