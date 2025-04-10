# loader.py
class Loader:
    def __init__(self, high_priority_truck, regular_truck, route_optimizer):
        self.truck1 = high_priority_truck
        self.truck2 = regular_truck
        self.optimizer = route_optimizer

    def assign_packages(self, scheduler, packages_dict):
        cycles = 0
        while not scheduler.is_empty():
            assigned_something = False
            cycles += 1
            remaining_queue_size = len(scheduler.queue)
            for _ in range(remaining_queue_size):
                package = scheduler.get_next()
                if not package:
                    break
                if package.priority == 'High' and self.truck1.has_capacity_for(package):
                    self.truck1.add_package(package)
                    assigned_something = True
                elif self.truck2.has_capacity_for(package):
                    self.truck2.add_package(package)
                    assigned_something = True
                else:
                    scheduler.add(package)
            if not assigned_something and not scheduler.is_empty():
                print(f"Applying aging in cycle {cycles} to prevent starvation")
                scheduler.apply_aging()
                if scheduler.aging_count > 10:
                    print("WARNING: Some packages couldn't be assigned after multiple aging cycles")
                    break

        print("Optimizing delivery routes...")
        self.truck1.route = self.optimizer.find_best_route(self.truck1.route, packages_dict)
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
