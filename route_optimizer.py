import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import os
from package import Package  # For type hinting


class RouteOptimizer:
    """
    Handles route optimization for delivery trucks
    """
    
    def __init__(self, warehouse=(0, 0)):
        self.warehouse = warehouse # coordinates of the warehouse where packages are loaded
    
    def calc_distance(self, p1, p2):
        """
        Calculate Euclidean distance between two points
           --> p1 and p2 are tuples (x, y) of coordinates
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    
    
    def find_best_route(self, package_ids: list, packages_dict: dict[Package]) -> list[int]:
        """
        Find the best route for a truck to deliver packages using a greedy nearest neighbor approach
        
        :return: List of package IDs in the order they should be delivered
        """
        if not package_ids:
            return []
        
        # Initialize variables
        current_pos: tuple[int, int] = self.warehouse # Start from warehouse
        packages_to_visit = package_ids.copy()  # Copy to avoid modifying the original list
        route = []
        
        # Keep finding closest unvisited package
        while packages_to_visit:
            
            # Find closest package
            min_dist = float('inf')
            closest_idx = -1
            
            for i, pkg_id in enumerate(packages_to_visit):
                package : Package = packages_dict[pkg_id]
                dist = self.calc_distance(current_pos, package.coordinates)
                
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = i
            
            # Add closest to route
            next_pkg_id = packages_to_visit.pop(closest_idx)
            route.append(next_pkg_id)
            
            # Update position
            current_pos: tuple[int, int] = packages_dict[next_pkg_id].coordinates
        
        return route
    
    
    
    
    def make_route_map(self, truck, packages_dict):
        """
        Method to create a route map for the truck
        
        Sources:
            - https://stackoverflow.com/questions/70421292/how-to-plot-routes-in-python
            - https://stackoverflow.com/questions/64846099/how-to-label-these-points-on-the-scatter-plot
            - https://stackoverflow.com/questions/39500265/how-to-manually-create-a-legend
            
        """
        
        plt.figure(figsize=(10, 8))
        
        # Plot warehouse --> coordinates (x, y)
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
            if package.priority_label == 'High':
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
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.join(current_file_path, "data")
        
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        plt.savefig(os.path.join(data_folder, f"truck_{truck.id}_route.png"))
        plt.close()