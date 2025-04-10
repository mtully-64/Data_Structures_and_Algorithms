import random
from models import Package, Truck
from route_optimizer import RouteOptimizer
from scheduler import Scheduler
from loader import Loader

def generate_packages(num_packages=20):
    packages = {}
    for i in range(num_packages):
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        size = random.randint(1, 5)
        weight = random.randint(1, 10)
        priority = 'High' if random.random() < 0.3 else 'Normal'
        packages[i] = Package(i, x, y, size, weight, priority)
    return packages

def print_package_info(packages):
    high_count = sum(1 for p in packages.values() if p.priority == 'High')
    normal_count = len(packages) - high_count
    print(f"Generated {len(packages)} packages: {high_count} high priority, {normal_count} normal priority")
    for p in packages.values():
        print(f"  {p} (Weight: {p.weight})")

def create_trucks(warehouse):
    truck1 = Truck(1, 50, "High-priority", warehouse)
    truck2 = Truck(2, 100, "Normal", warehouse)
    return truck1, truck2

def run_simulation():
    random.seed(42)
    warehouse = (5, 5)
    packages = generate_packages(20)
    print("\n--- Package Information ---")
    print_package_info(packages)

    truck1, truck2 = create_trucks(warehouse)
    scheduler = Scheduler()
    for package in packages.values():
        scheduler.add(package)

    optimizer = RouteOptimizer(warehouse)
    loader = Loader(truck1, truck2, optimizer)
    print("\nStarting package assignment and route optimization...")
    loader.assign_packages(scheduler, packages)

    truck1.show_route(packages)
    truck1.show_loading_order()
    truck2.show_route(packages)
    truck2.show_loading_order()

    loader.print_summary()

    print("\nGenerating route visualizations...")
    loader.visualize_routes(packages)
    print("Route visualizations saved as 'truck_1_route.png' and 'truck_2_route.png'")
    print("\nLogistics system simulation complete!")

if __name__ == "__main__":
    run_simulation()
