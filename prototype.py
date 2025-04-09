import heapq
import math
import random
import matplotlib.pyplot as plt

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

# Handles route optimization using Nearest Neighbor
class RouteOptimizer:
    def __init__(self, warehouse=(0, 0)):
        self.warehouse = warehouse
    
    # Calculate distance between two points
    def calc_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    # Find optimal route using greedy nearest neighbor
    def find_best_route(self, package_ids, packages_dict):
        if not package_ids:
            return []
        
        # Start from warehouse
        current_pos = self.warehouse
        packages_to_visit = list(package_ids)  # make a copy
        route = []
        
        # Keep finding closest unvisited package
        while packages_to_visit:
            # Find closest package
            min_dist = float('inf')
            closest_idx = -1
            
            for i, pkg_id in enumerate(packages_to_visit):
                package = packages_dict[pkg_id]
                dist = self.calc_distance(current_pos, package.coordinates)
                
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = i
            
            # Add closest to route
            next_pkg_id = packages_to_visit.pop(closest_idx)
            route.append(next_pkg_id)
            
            # Update position
            current_pos = packages_dict[next_pkg_id].coordinates
        
        return route
    
    # Visualize delivery route
    def make_route_map(self, truck, packages_dict):
        plt.figure(figsize=(10, 8))
        
        # Plot warehouse
        plt.plot(self.warehouse[0], self.warehouse[1], 'ks', markersize=10, label='Warehouse')
        
        # Create route coordinates
        x_coords = [self.warehouse[0]]
        y_coords = [self.warehouse[1]]
        
        # Plot all packages on route
        stop_num = {}
        for i, pkg_id in enumerate(truck.route, 1):
            stop_num[pkg_id] = i
            package = packages_dict[pkg_id]
            x, y = package.coordinates
            x_coords.append(x)
            y_coords.append(y)
            
            # Different markers for priority
            if package.priority == 'High':
                plt.plot(x, y, 'ro', markersize=8)
            else:
                plt.plot(x, y, 'bo', markersize=8)
            
            # Label with package ID and stop number
            plt.text(x+0.2, y+0.2, f"P{pkg_id}(#{i})", fontsize=9)
        
        # Complete the route back to warehouse
        x_coords.append(self.warehouse[0])
        y_coords.append(self.warehouse[1])
        
        # Connect the dots
        plt.plot(x_coords, y_coords, 'k--', alpha=0.6)
        
        # Add title and legend
        plt.title(f"Delivery Route - Truck {truck.id}")
        
        # Create custom legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='r', label='High Priority', markersize=8, linestyle=''),
            Line2D([0], [0], marker='o', color='b', label='Normal Priority', markersize=8, linestyle=''),
            Line2D([0], [0], marker='s', color='k', label='Warehouse', markersize=8, linestyle='')
        ]
        plt.legend(handles=legend_elements)
        
        # Set grid
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xlim(-1, 11)
        plt.ylim(-1, 11)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        
        # Save the figure
        plt.savefig(f"truck_{truck.id}_route.png")
        plt.close()

# Scheduler using priority queue with aging
class Scheduler:
    def __init__(self):
        self.queue = []  # our priority queue
        self.package_ids_in_queue = set()
        self.aging_count = 0
    
    def add(self, package):
        # Add to priority queue (negative for max-heap)
        priority = -package.get_effective_priority()  # negative to make it a max heap
        heapq.heappush(self.queue, (priority, package.id, package))
        self.package_ids_in_queue.add(package.id)
    
    def get_next(self):
        if not self.queue:
            return None
        
        # Get highest priority package
        _, pkg_id, package = heapq.heappop(self.queue)
        self.package_ids_in_queue.remove(pkg_id)
        return package
    
    # Implement aging to avoid starvation
    def apply_aging(self):
        # Need to rebuild queue with updated priorities
        temp_queue = []
        
        # Process all packages
        while self.queue:
            _, pkg_id, package = heapq.heappop(self.queue)
            package.increase_age()
            # Re-add with new priority
            new_priority = -package.get_effective_priority()
            heapq.heappush(temp_queue, (new_priority, pkg_id, package))
        
        # Update queue and count
        self.queue = temp_queue
        self.aging_count += 1
    
    def is_empty(self):
        return len(self.queue) == 0

# Handles assigning packages to trucks
class Loader:
    def __init__(self, high_priority_truck, regular_truck, route_optimizer):
        self.truck1 = high_priority_truck
        self.truck2 = regular_truck
        self.optimizer = route_optimizer
    
    # Assign packages to trucks based on priority and capacity
    def assign_packages(self, scheduler, packages_dict):
        cycles = 0
        
        # Keep going until no packages left or we can't assign any more
        while not scheduler.is_empty():
            assigned_something = False
            cycles += 1
            
            # Try to assign as many as possible in this round
            remaining_queue_size = len(scheduler.queue)
            for _ in range(remaining_queue_size):
                package = scheduler.get_next()
                if not package:
                    break
                
                # Try to assign based on priority and capacity
                if package.priority == 'High' and self.truck1.has_capacity_for(package):
                    # High priority package goes to truck 1 if possible
                    self.truck1.add_package(package)
                    assigned_something = True
                elif self.truck2.has_capacity_for(package):
                    # Otherwise try truck 2
                    self.truck2.add_package(package)
                    assigned_something = True
                else:
                    # Put back in queue if it can't be assigned now
                    scheduler.add(package)
            
            # If we couldn't assign anything but still have packages, age them
            if not assigned_something and not scheduler.is_empty():
                print(f"Applying aging in cycle {cycles} to prevent starvation")
                scheduler.apply_aging()
                
                # Emergency break if we keep aging without progress
                if scheduler.aging_count > 10:
                    print("WARNING: Some packages couldn't be assigned after multiple aging cycles")
                    # Could be too heavy for any truck
                    break
        
        # Optimize routes for both trucks
        print("Optimizing delivery routes...")
        self.truck1.route = self.optimizer.find_best_route(self.truck1.route, packages_dict)
        self.truck2.route = self.optimizer.find_best_route(self.truck2.route, packages_dict)
        
        # Calculate distances
        self.truck1.calculate_route_length(packages_dict)
        self.truck2.calculate_route_length(packages_dict)
        
        # Create loading order (LIFO)
        self.truck1.create_loading_order(packages_dict)
        self.truck2.create_loading_order(packages_dict)
        
        print(f"Assignment completed in {cycles} cycles with {scheduler.aging_count} aging operations")
    
    # Create route visualizations
    def visualize_routes(self, packages_dict):
        self.optimizer.make_route_map(self.truck1, packages_dict)
        self.optimizer.make_route_map(self.truck2, packages_dict)
    
    # Print summary statistics
    def print_summary(self):
        truck1_stats = self.truck1.get_stats()
        truck2_stats = self.truck2.get_stats()
        
        total_packages = (truck1_stats["high"] + truck1_stats["normal"] + 
                          truck2_stats["high"] + truck2_stats["normal"])
        
        print("\n===== DELIVERY SUMMARY =====")
        print(f"Total packages: {total_packages}")
        
        print(f"\nTruck 1 ({self.truck1.role}):")
        print(f"  High priority packages: {truck1_stats['high']}")
        print(f"  Normal priority packages: {truck1_stats['normal']}")
        print(f"  Total weight: {truck1_stats['weight']}/{self.truck1.max_capacity} units")
        print(f"  Capacity usage: {truck1_stats['usage']:.1f}%")
        print(f"  Route distance: {self.truck1.route_distance:.2f} units")
        
        print(f"\nTruck 2 ({self.truck2.role}):")
        print(f"  High priority packages: {truck2_stats['high']}")
        print(f"  Normal priority packages: {truck2_stats['normal']}")
        print(f"  Total weight: {truck2_stats['weight']}/{self.truck2.max_capacity} units")
        print(f"  Capacity usage: {truck2_stats['usage']:.1f}%")
        print(f"  Route distance: {self.truck2.route_distance:.2f} units")

# Main function to test the system
def main():
    # Set random seed for consistent results
    random.seed(42)
    
    # Define where trucks start/end
    warehouse = (5, 5)
    
    # Create packages (simulating real-world data)
    packages = {}
    
    # Generate some random test packages
    # In real system would load from database/file
    print("Generating random test packages...")
    for i in range(20):
        # Random location on 10x10 grid
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        
        # Random package properties
        size = random.randint(1, 5)  # arbitrary units
        weight = random.randint(1, 10)  # weight units
        
        # 30% high priority, 70% normal
        priority = 'High' if random.random() < 0.3 else 'Normal'
        
        # Create and store package
        packages[i] = Package(i, x, y, size, weight, priority)
    
    # Print out all generated packages
    print("\n--- Package Information ---")
    high_count = sum(1 for p in packages.values() if p.priority == 'High')
    normal_count = len(packages) - high_count
    print(f"Generated {len(packages)} packages: {high_count} high priority, {normal_count} normal priority")
    
    # Show package details
    for p in packages.values():
        print(f"  {p} (Weight: {p.weight})")
    
    # Create our delivery trucks
    # Truck 1 has less capacity but handles high priority
    # Truck 2 has more capacity for regular deliveries
    truck1 = Truck(1, 50, "High-priority", warehouse)
    truck2 = Truck(2, 100, "Normal", warehouse)
    
    # Initialize scheduler and add all packages
    scheduler = Scheduler()
    for package in packages.values():
        scheduler.add(package)
    
    # Create route optimizer
    optimizer = RouteOptimizer(warehouse)
    
    # Create package loader
    loader = Loader(truck1, truck2, optimizer)
    
    print("\nStarting package assignment and route optimization...")
    
    # Run the assignment algorithm
    loader.assign_packages(scheduler, packages)
    
    # Print routes and loading order
    truck1.show_route(packages)
    truck1.show_loading_order()
    
    truck2.show_route(packages)
    truck2.show_loading_order()
    
    # Print summary statistics
    loader.print_summary()
    
    # Create visualizations
    print("\nGenerating route visualizations...")
    loader.visualize_routes(packages)
    print("Route visualizations saved as 'truck_1_route.png' and 'truck_2_route.png'")
    
    print("\nLogistics system simulation complete!")

# Run program if executed directly
if __name__ == "__main__":
    # Could add command line arguments here in future versions
    main()
