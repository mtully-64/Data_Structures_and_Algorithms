import matplotlib.pyplot as plt
import math


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