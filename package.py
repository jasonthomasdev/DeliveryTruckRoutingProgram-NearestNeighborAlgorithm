# This is the class for each package
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline_time, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "Package #%s shipping to %s, %s, %s %s | Deadline: %s | Weight: %s | Delivery Time: %s | Current Status: %s" % (self.id, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline_time, self.weight, self.delivery_time,
                                                       self.status)

    # Update delivery status
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"