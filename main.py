import random
from truck import Truck
from package import Package
from route_optimizer import RouteOptimizer
from scheduler import Scheduler
from loader import Loader


def generate_packages(num_packages: int=20) -> dict[Package]:
    """
    Generate a dictionary of packages with random attributes
    """
    packages = {}
    for i in range(num_packages):
        
        x = random.randint(0, 10) # Random x-coordinate
        y = random.randint(0, 10) # Random y-coordinate
        size = random.randint(1, 5) # Random size between 1 and 5
        weight = random.randint(1, 10) # Random weight between 1 and 10
        
        random_priority = random.random()
        priority = 'High' if random_priority < 0.3 else 'Normal' # 30% chance of high priority
        
        new_package = Package(x, y, size, weight, priority)
        packages[new_package.id] = new_package
    
    # print the information of the packages just generated
    print_package_info(packages)
        
    return packages


def print_package_info(packages: dict[Package]) -> None:
    """
    Print information about the generated packages
    """
    high_count = 0
    normal_count = 0
    print("\n--- Package Information ---")
    
    for package in packages.values():
        if package.priority == "High":
            high_count += 1
        else:
            normal_count += 1
        
        print(package)
    
    print(f"Generated {len(packages)} packages: {high_count} high priority, {normal_count} normal priority")




def create_trucks(
    warehouse: tuple[int, int],
    capacity1: int=100,
    capacity2: int=100,
    ) -> tuple[Truck, Truck]:
    """
    Create two trucks form the same warehouse, one for high-priority and one for normal packages
    """
    
    truck1: Truck = Truck(1, capacity1, "High-priority", warehouse)
    truck2: Truck = Truck(2, capacity2, "Normal", warehouse)
    
    return truck1, truck2




def run_scenario_1():
    """
    In this scenario Truck1 can't have capacity for all high priority package, 
        so some of the high priority packages overflow to Truck2
    """
    
    print("\n\n---------------------")
    print("\n\n--- Running Scenario 1 ---")
    print("Truck1 can't handle all high-priority packages, some overflow to Truck2\n\n")
    
    random.seed(13)
    
    packages = generate_packages(60)
    truck1, truck2 = create_trucks((150, 40))
    data_folder_name = "scenario_1"
    run_simulation(packages, truck1, truck2, data_folder_name)
    


def run_scenario_2():
    """
    In this scenario, both Trucks can handle all the priority packages they were assigned, there are no overflows
        - Truck1 handles all high-priority packages
        - Truck2 handles all normal priority packages
    """
    
    print("\n\n---------------------")
    print("\n\n--- Running Scenario 2 ---")
    print("Truck1 handles all high-priority packages, Truck2 handles all normal priority packages\n\n")
    
    
    random.seed(13)
    
    packages = generate_packages(20)
    truck1, truck2 = create_trucks((40, 90))
    data_folder_name = "scenario_2"
    run_simulation(packages, truck1, truck2, data_folder_name)
    


def run_scenario_3():
    """
    In this scenario Truck2 does not have enough capacity for all normall prioirty packages, 
        so some of the packages normall prioirty overflow to Truck1 after the aging mechanism increases their priority
    """
    
    print("\n\n---------------------")
    print("\n\n--- Running Scenario 3 ---")
    print("Truck2 doesn't have enough capacity for all normal-priority packages, some overflow to Truck1 after aging\n\n")
    
    
    random.seed(13)
    
    packages = generate_packages(30)
    truck1, truck2 = create_trucks((90, 90))
    data_folder_name = "scenario_3"
    run_simulation(packages, truck1, truck2, data_folder_name)

    
    
    



def run_simulation(packages: dict[Package] = None,
                   truck1: Truck = None,
                   truck2: Truck = None,
                   data_folder_name = "data"
                   ) -> None:
    
    random.seed(13) # For reproducibility
    warehouse = (5, 5) # Warehouse coordinates 
    
    if packages is None:
        packages = generate_packages(20)
    
    if truck1 is None or truck2 is None:
        truck1, truck2 = create_trucks(warehouse)

    scheduler = Scheduler()
    for package in packages.values():
        scheduler.add(package)

    optimizer = RouteOptimizer(warehouse, data_folder_name)
    
    loader = Loader(truck1, truck2, optimizer)
    loader.assign_packages(scheduler, packages)

    truck1.show_route(packages)
    truck1.show_loading_order()
    truck2.show_route(packages)
    truck2.show_loading_order()

    loader.print_summary()

    print("\nGenerating route visualizations...")
    loader.visualize_routes(packages)
    print("Route visualizations saved as 'truck_1_route.png' and 'truck_2_route.png'")
    print("\nLogistics system simulation complete!\n\n")



if __name__ == "__main__":
    
    # Run the scenarios
    run_scenario_1()
    run_scenario_2()
    run_scenario_3()


    
    




