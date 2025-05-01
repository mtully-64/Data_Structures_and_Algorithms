class Package:
    """
    Class representing a package to be delivered
    """
    
    # Class variable to track used package IDs, and make sure they are unique
    _used_ids = set()
    _max_id_available = 0
    
    
    def __init__(self, x, y, size, weight, priority):
        
        # Call the ID setter to assign a unique ID
        self._id_setter()
        
        # Then initialize the rest of the instance attributes
        self.coordinates : tuple[int, int] = (x, y)  # location for delivery
        self.size = size  
        self.weight = weight
        self._assign_initial_priority(priority)  # High or Normal
        self.age = 0  # for aging mechanism
    
    
    def __str__(self):
        return f"Package {self.id}: ({self.priority_label} priority) to be delivered at {self.coordinates}"
    
    @property
    def priority(self):
        return self.initial_priority + self.age
    
    @property
    def priority_label(self):
        return 'High' if self.priority >= 5 else 'Normal'
    
    
    def _id_setter(self):
        """
        Setter for the package ID
        """
        new_id = Package._max_id_available 
        
        # Check if the new ID is already in use (shouldn't be, but just in case)
        if new_id in Package._used_ids:
            raise ValueError(f"Error: Package ID {new_id} is already in use")
        
        # Assign the new id if it's not in use
        self.id = new_id
        Package._used_ids.add(new_id)  # Add the new ID to the set of used IDs
        
        Package._max_id_available += 1 # Update the max ID for the next package
    
    
    # Age increases waiting time importance
    def increase_age(self):
        self.age += 1
        return self.age
    
    
    def _assign_initial_priority(self, priority):
        """
        Assigns the initial priority to the package based on its description
        """
        self._initial_priotiy_label = priority # store the label just in case we need it later
        
        if priority == 'High':
            self.initial_priority = 5
        
        else:
            self.initial_priority = 1
        
    

    
    
    