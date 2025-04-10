import heapq

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