#include <Python.h>
#include "customer.h"
#include "vehicle.h"
#include "rental.h"
#include "utils.h"

// Global variables for the linked lists
static Customer *customer_head = NULL;
static Vehicle *vehicle_head = NULL;
static Rental *rental_head = NULL;
static Route *route_head = NULL;

// Initialize the system (load all data)
static PyObject* init_system(PyObject* self, PyObject* args) {
    loadVehicles(&vehicle_head);
    loadCustomers(&customer_head);
    loadRentals(&rental_head);
    loadRoutes(&route_head);
    Py_RETURN_NONE;
}

// Save all data
static PyObject* save_all(PyObject* self, PyObject* args) {
    saveVehicles(vehicle_head);
    saveCustomers(customer_head);
    saveRentals(rental_head);
    Py_RETURN_NONE;
}

// Customer authentication
static PyObject* authenticate_customer(PyObject* self, PyObject* args) {
    const char *username, *password;
    if (!PyArg_ParseTuple(args, "ss", &username, &password))
        return NULL;
    
    Customer *customer = authenticateCustomer(customer_head, username, password);
    if (customer) {
        return Py_BuildValue("{s:i,s:s,s:s,s:s,s:s,s:s}",
                           "id", customer->id,
                           "name", customer->name,
                           "username", customer->username,
                           "email", customer->email,
                           "phone", customer->phone,
                           "status", customer->active ? "active" : "inactive");
    }
    Py_RETURN_NONE;
}

// Admin authentication
static PyObject* authenticate_admin(PyObject* self, PyObject* args) {
    const char *username, *password;
    if (!PyArg_ParseTuple(args, "ss", &username, &password))
        return NULL;
    
    if (authenticateAdmin(username, password)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

// Get all available vehicles
static PyObject* get_available_vehicles(PyObject* self, PyObject* args) {
    PyObject *vehicles_list = PyList_New(0);
    
    for (Vehicle *v = vehicle_head; v != NULL; v = v->next) {
        if (v->available && v->active) {
            PyObject *vehicle_dict = Py_BuildValue(
                "{s:i,s:s,s:s,s:i,s:f,s:f,s:i}",
                "id", v->id,
                "make", v->make,
                "model", v->model,
                "year", v->year,
                "rate_per_day", v->ratePerDay,
                "rate_per_hour", v->ratePerHour,
                "type", (int)v->type
            );
            PyList_Append(vehicles_list, vehicle_dict);
            Py_DECREF(vehicle_dict);
        }
    }
    
    return vehicles_list;
}

// Get customer rentals
static PyObject* get_customer_rentals(PyObject* self, PyObject* args) {
    int customer_id;
    if (!PyArg_ParseTuple(args, "i", &customer_id))
        return NULL;
    
    PyObject *rentals_list = PyList_New(0);
    
    for (Rental *r = rental_head; r != NULL; r = r->next) {
        if (r->customerId == customer_id) {
            PyObject *rental_dict = PyDict_New();
            PyDict_SetItemString(rental_dict, "id", PyLong_FromLong(r->id));
            PyDict_SetItemString(rental_dict, "start_date", PyUnicode_FromString(r->startTime));
            PyDict_SetItemString(rental_dict, "end_date", PyUnicode_FromString(r->endTime));
            
            // Convert status enum to string
            const char *status_str;
            switch (r->status) {
                case RENT_ACTIVE: status_str = "Active"; break;
                case RENT_COMPLETED: status_str = "Completed"; break;
                case RENT_CANCELLED: status_str = "Cancelled"; break;
                default: status_str = "Unknown";
            }
            PyDict_SetItemString(rental_dict, "status", PyUnicode_FromString(status_str));
            
            Vehicle *v = findVehicleById(vehicle_head, r->vehicleId);
            if (v) {
                PyDict_SetItemString(rental_dict, "vehicle", PyUnicode_FromString(v->model));
                PyDict_SetItemString(rental_dict, "vehicle_id", PyLong_FromLong(r->vehicleId));
            }
            PyList_Append(rentals_list, rental_dict);
            Py_DECREF(rental_dict);
        }
    }
    
    return rentals_list;
}

// Create a new rental
static PyObject* create_rental(PyObject* self, PyObject* args) {
    int customer_id, vehicle_id;
    const char *start_date, *end_date;
    
    if (!PyArg_ParseTuple(args, "iiss", &customer_id, &vehicle_id, &start_date, &end_date))
        return NULL;
    
    // Find the customer and vehicle
    Customer *customer = NULL;
    for (Customer *c = customer_head; c != NULL; c = c->next) {
        if (c->id == customer_id) {
            customer = c;
            break;
        }
    }
    
    if (!customer) {
        PyErr_SetString(PyExc_ValueError, "Customer not found");
        return NULL;
    }
    
    Vehicle *vehicle = findVehicleById(vehicle_head, vehicle_id);
    if (!vehicle) {
        PyErr_SetString(PyExc_ValueError, "Vehicle not found");
        return NULL;
    }
    
    if (!vehicle->available) {
        PyErr_SetString(PyExc_ValueError, "Vehicle is not available for rent");
        return NULL;
    }
    
    // Create a new rental
    Rental *new_rental = (Rental *)malloc(sizeof(Rental));
    if (!new_rental) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for rental");
        return NULL;
    }
    
    // Initialize the rental
    new_rental->id = generateUniqueId();
    new_rental->customerId = customer_id;
    new_rental->vehicleId = vehicle_id;
    new_rental->routeId = 0;  // Not using route-based rental in this case
    new_rental->type = RENT_DAILY;  // Default to daily rental
    
    // Copy start and end times
    strncpy(new_rental->startTime, start_date, sizeof(new_rental->startTime) - 1);
    new_rental->startTime[sizeof(new_rental->startTime) - 1] = '\0';
    
    strncpy(new_rental->endTime, end_date, sizeof(new_rental->endTime) - 1);
    new_rental->endTime[sizeof(new_rental->endTime) - 1] = '\0';
    
    // Set status and initial cost
    new_rental->status = RENT_ACTIVE;
    new_rental->totalCost = 0.0f;  // Will be calculated by the rental module
    
    // Add to the rental list
    new_rental->next = rental_head;
    rental_head = new_rental;
    
    // Update vehicle availability
    vehicle->available = 0;  // Mark as rented
    
    // Save changes
    saveRentals(rental_head);
    saveVehicles(vehicle_head);
    
    return Py_BuildValue("i", new_rental->id);
}

// Method definitions
static PyMethodDef RideMateMethods[] = {
    {"init_system", init_system, METH_NOARGS, "Initialize the system by loading all data"},
    {"save_all", save_all, METH_NOARGS, "Save all data to files"},
    {"authenticate_customer", authenticate_customer, METH_VARARGS, "Authenticate a customer"},
    {"authenticate_admin", authenticate_admin, METH_VARARGS, "Authenticate an admin"},
    {"get_available_vehicles", get_available_vehicles, METH_NOARGS, "Get all available vehicles"},
    {"get_customer_rentals", get_customer_rentals, METH_VARARGS, "Get rentals for a customer"},
    {"create_rental", create_rental, METH_VARARGS, "Create a new rental"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef ridemate_module = {
    PyModuleDef_HEAD_INIT,
    "ridemate",  // name of module
    NULL,        // module documentation, may be NULL
    -1,          // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    RideMateMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_ridemate(void) {
    return PyModule_Create(&ridemate_module);
}
