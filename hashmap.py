# This is the HashMap class
class HashMapManager:
    def __init__(self, size=20):
        self.data_array = []
        for i in range(size):
            self.data_array.append([])

    # Insert or update a value based on the key
    def add(self, key, value):
        # Determine which sublist the key-value pair should be placed in
        index = hash(key) % len(self.data_array)
        sub_list = self.data_array[index]

        # Check if the key exists and update
        for element in sub_list:
            # print (key_value)
            if element[0] == key:
                element[1] = value
                return True

        # If the key is not present, add the new key-value pair
        element = [key, value]
        sub_list.append(element)
        return True

    # Retrieve a value by its key
    def get(self, key):
        index = hash(key) % len(self.data_array)
        sub_list = self.data_array[index]
        for item in sub_list:
            if key == item[0]:
                return item[1]
        return None

    # Remove items from hashmap
    def delete(self, key):
        index = hash(key) % len(self.data_array)
        target_list = self.data_array[index]

        # Loop to find the key and remove the corresponding key-value pair
        for item in target_list:
            if item[0] == key:
                target_list.remove(item)
                return True
        return False