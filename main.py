# WGUPS Delivery Program by Jason Thomas
# Student ID:011014761

import csv
import datetime
import truck
from builtins import ValueError

from hashmap import HashMapManager
from package import Package

# Methods
# Get address number from string literal of address
def get_address(address):
    for row in addr_data:
        if address in row[2]:
            return int(row[0])

# Get the distance between two addresses
def distance_between(x_value, y_value):
    distance = dist_data[x_value][y_value]
    if distance == '':
        distance = dist_data[y_value][x_value]

    return float(distance)

# Load package objects into hash table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zipcode = package[4]
            package_deadline_time = package[5]
            package_weight = package[6]
            package_status = "At Hub"

            # Create package object and insert data into hash table
            package_obj = Package(package_id, package_address, package_city, package_state, package_zipcode, package_deadline_time, package_weight, package_status)
            package_hash_table.add(package_id, package_obj)

# Read the distance, address, and package CSV files
with open("distance_table.csv") as dist_file:
    dist_data = csv.reader(dist_file)
    dist_data = list(dist_data)
with open("address_file.csv") as addr_file:
    addr_data = csv.reader(addr_file)
    addr_data = list(addr_data)
with open("package_file.csv") as addr_file:
    pkg_data = csv.reader(addr_file)
    pkg_data = list(pkg_data)

# Create truck object truck1, truck2, and truck3 and assign packages
truck1 = truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))
truck2 = truck.Truck(16, 18, None, [3, 6, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))

# Create hash table and load packages
package_hash_table = HashMapManager()
load_package_data("package_file.csv", package_hash_table)

# Deliver packages with the nearest neighbor algorithm
def deliver_packages(truck):
    # Place all packages into pending_delivery array
    pending_delivery = []
    for package_id in truck.packages:
        package = package_hash_table.get(package_id)
        pending_delivery.append(package)
    # Clear the truck's package list
    truck.packages.clear()

    # Cycle through pending_delivery until none remain
    # Add the nearest package into the truck.packages list one by one (nearest neighbor implementation)
    while len(pending_delivery) > 0:
        shortest_distance = 2000
        next_package = None
        for package in pending_delivery:
            if distance_between(get_address(truck.address), get_address(package.address)) <= shortest_distance:
                shortest_distance = distance_between(get_address(truck.address), get_address(package.address))
                next_package = package
        # Add next closest package to the truck's package list
        truck.packages.append(next_package.id)
        # Remove the same package from the pending_delivery list
        pending_delivery.remove(next_package)
        # Update mileage driven
        truck.mileage += shortest_distance
        # Update truck's current address to the package it moved to
        truck.address = next_package.address
        # Update the time it took for the truck to drive to the nearest package
        truck.time += datetime.timedelta(hours=shortest_distance / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time


# Load the trucks and deliver the packages
deliver_packages(truck1)
deliver_packages(truck2)
# Ensure truck 3 does not leave until either of the first two trucks have finished their deliveries
truck3.depart_time = min(truck1.time, truck2.time)
deliver_packages(truck3)


class Main:
    # Main Menu User Interface
    print("WGUPS Delivery Program by Jason Thomas")
    print("--------------------------------------")
    print("1. View the status of a specific package.")
    print("2. View the status of all packages at a specific time.")
    print("3. View the total mileage traveled by all trucks.")
    print("4. Exit.")
    choice = input("Enter your choice: ")
    print()

    # User selects option 1 - View the status of a specific package
    if choice == '1':
        try:
            # User inputs a time for the package status
            user_time = input(
                "Enter time (HH:MM:SS format): ")
            (h, m, s) = user_time.split(":")
            user_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # User inputs a package ID
            user_input = input("Enter package ID: ")
            print()
            # Return package status as of user defined time
            package = package_hash_table.get(int(user_input))
            package.update_status(user_timedelta)
            print(str(package))
        except ValueError:
            print("Invalid entry. Program Terminating.")
            exit()
    # User selects option 2 - View the status of all packages at a specific time
    elif choice == '2':
        try:
            user_time = input("Enter time (HH:MM:SS format): ")
            print()
            (h, m, s) = user_time.split(":")
            user_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            # Lookup and display the status of all packages as of user provided time
            for package_id in range(1, 41):
                package = package_hash_table.get(package_id)
                package.update_status(user_timedelta)
                print(str(package))
        except ValueError:
            print("Invalid entry. Program Terminating.")
            exit()
    # User selects option 3 - View the total mileage traveled by all trucks
    elif choice == '3':
        try:
            # Print total mileage for all trucks
            total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
            print("Total mileage traveled by all trucks: ", total_mileage)
        except ValueError:
            print("Invalid entry. Program Terminating.")
            exit()
    else:
        exit()