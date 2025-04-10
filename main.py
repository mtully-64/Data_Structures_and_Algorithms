import random 
from models import Package, Truck
from route_optimizer import RouteOptimizer
from scheduler import Scheduler
from loader import Loader

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
