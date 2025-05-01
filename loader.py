# Imports only necessay for type hinting
from truck import Truck
from route_optimizer import RouteOptimizer
from scheduler import Scheduler
from package import Package


class Loader:
    
    """
    Class responsible for loading packages into trucks and optimizing their routes
    
    It keeps track of:
        - The trucks used for delivery (one for high-priority and one for regular packages)
        - The route optimizer used to find the best delivery routes
        - The scheduler that manages the package queue
        - The packages assigned to each truck
    """
    
    def __init__(self, high_priority_truck : Truck, regular_truck : Truck, route_optimizer : RouteOptimizer):
        
        self.truck1 : Truck = high_priority_truck
        self.truck2 : Truck = regular_truck
        self.optimizer : RouteOptimizer = route_optimizer



    def assign_packages(self, scheduler : Scheduler, packages_dict: dict[Package]):
        
        """
        Assign packages to trucks based on their priority and available capacity
        High-priority packages are assigned to truck 1, while normal packages are assigned to truck 2
        The method also optimizes the delivery routes for both trucks
        """
        
        
        print("\nStarting package assignment and route optimization...")
        
        cycles : int = 0
        
        # Loop until all packages the scheduler is empty (all packages are assigned) 
                # or the scheduler has been through 10 aging cycles
        while not scheduler.is_empty():
            
            assigned_something : bool = False
            cycles += 1
            remaining_queue_size : int = len(scheduler.queue)
            low_priority_queu : list = []
            
            for _ in range(remaining_queue_size):
                
                # Get the next package from the scheduler, stop if the queue is empty
                package = scheduler.get_next()
                if not package:
                    break
                
                # first try to assign only high priority packages to truck 1, 
                        # if they fail make sure they at least get assigned to truck 2
                if package.priority >= 5:

                    if self.truck1.has_capacity_for(package):
                        self.truck1.add_package(package)
                        assigned_something = True
                    
                    elif self.truck2.has_capacity_for(package):
                        self.truck2.add_package(package)
                        assigned_something = True
                    
                    else:
                        # If it doesn't fit, add it to the sheduler again
                        scheduler.add(package)
                
                else:
                    low_priority_queu.append(package)
            
            
            # Now, once all high priority packages have been assigned (or not if they didn't fit)
                # we can assign the low priority packages to truck 2
            for package in low_priority_queu:
                
                if self.truck2.has_capacity_for(package):
                    self.truck2.add_package(package)
                    assigned_something = True
                
                else:
                    # If it doesn't fit, add it to the sheduler again
                    scheduler.add(package)
                
                    
            # If nothing was assigned in this cycle, we need to apply aging to the packages
            if not assigned_something and not scheduler.is_empty():
                print(f"Applying aging in cycle {cycles} to prevent starvation")
                scheduler.apply_aging()
                
                # stop againg if we have been through 10 cycles
                if scheduler.aging_count >= 10:
                    print("WARNING: Some packages couldn't be assigned after multiple aging cycles")
                    break


        print("Optimizing delivery routes...")
        self.truck1.route = self.optimizer.find_best_route(self.truck1.route, packages_dict) # This is a list of package IDs in delivery order
        self.truck2.route = self.optimizer.find_best_route(self.truck2.route, packages_dict)

        self.truck1.calculate_route_length(packages_dict) 
        self.truck2.calculate_route_length(packages_dict)

        self.truck1.create_loading_order(packages_dict)
        self.truck2.create_loading_order(packages_dict)
        print(f"Assignment completed in {cycles} cycles with {scheduler.aging_count} aging operations")



    def visualize_routes(self, packages_dict):
        self.optimizer.make_route_map(self.truck1, packages_dict)
        self.optimizer.make_route_map(self.truck2, packages_dict)
        

    def print_summary(self):
        self.truck1.get_stats()
        self.truck2.get_stats()
        total_packages = (self.truck1.stats["high"] + self.truck1.stats["normal"] +
                          self.truck2.stats["high"] + self.truck2.stats["normal"])
        
        print("\n===== DELIVERY SUMMARY =====")
        print(f"Total packages: {total_packages}")
        
        for truck in [self.truck1, self.truck2]:
            print(f"\nTruck {truck.id} ({truck.role}):")
            print(f"  Packages loaded: {len(truck.packages_to_load)}")
            print(f"  Route distance: {truck.route_distance:.2f} units")
            print(f"  High priority packages: {truck.stats['high']}")
            print(f"  Normal priority packages: {truck.stats['normal']}")
            print(f"  Total weight: {truck.stats['weight']}/{truck.max_capacity} units")
            print(f"  Capacity usage: {truck.stats['usage']:.1f}%")
        
    
