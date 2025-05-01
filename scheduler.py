import heapq
from package import Package # This is only for type hinting

class Scheduler:
    """
    Class to manage the scheduling of packages using a priority queue
    
    Source:
        - https://docs.python.org/3/library/heapq.html
    """

    def __init__(self):
        self.queue : list = []  # our priority queue
        self.package_ids_in_queue : set = set()
        self.aging_count : int = 0
    
    
    def is_empty(self):
        return len(self.queue) == 0
    
    
    def add(self, package: Package):
        """
        Add package to the queue with its effective priority 
        Higher priority packages come out first (using negative values for max-heap)
        
            Reasoning: Python heapq module implements a min-heap by default (lowest values come out first)
        """
        raw_priority = package.priority
        priority = - raw_priority  # negative to make it a max heap
        
        # Push the package into the queue
        # Why add the package ID?
            # Queue will be based on priority, however in the event of a tie, the package ID number will be used to break it
            # Package id is unique and will always be different (logic in the Pakage class)
        tupple_to_push = (priority, package.id, package)
        heapq.heappush(self.queue, tupple_to_push) 
        
        # track which packages are in the queue
        self.package_ids_in_queue.add(package.id) 
    
    
    def get_next(self):
        """
        Method to get the next package from the queue
        """
        
        # Check if the queue is empty
        if self.is_empty():
            return None
        
        # Get highest priority package 
            #  --> lowest priority number (most negative), and in case of a tie, the lowest package ID
        _, pkg_id, package = heapq.heappop(self.queue)
        
        # Remove the package ID from the set of IDs in the queue
        self.package_ids_in_queue.remove(pkg_id)
        
        return package
    
    
    
    def apply_aging(self):
        """
        Method to apply aging to all packages in the queue, to prevent starvation
        Aging increases the effective priority of all packages in the queue
        """
        
        # We need to rebuild the queue with updated priorities 
        for index, (_, pkg_id, package) in enumerate(self.queue):  # --> O(n) complexity
            
            # Increase the age of the package
            package.increase_age()
            
            # Get the new priority
            new_priority = - package.priority
            
            # Re add the package with the new priority, in place of the old one --> O(1) complexity
            self.queue[index] = (new_priority, pkg_id, package)
            
        
        # To keep the heap property, turn again the queue list into a heap 
        heapq.heapify(self.queue) # --> O(n) complexity
        
        # Register the aging operation
        self.aging_count += 1
        
    
    
