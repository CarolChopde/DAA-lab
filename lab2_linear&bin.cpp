#include <iostream>

void linearSearch(int a[], int size, int key) {
    // Perform linear search for the key
    for (int index = 0; index < size; index++) {
        if (a[index] == key) {
            std::cout << "Linear Search : The element was found at index: " << index << std::endl;
            return;
        }
    }
    std::cout << "Linear Search : Element not found." << std::endl;
}

int recBinarySearch(int arr[], int low, int high, int key) {
    // Base case
    if (low > high) {
        return -1;  // Key not found
    }

    // Calculating the middle index
    int mid = low + (high - low) / 2;

    // Check if the key is at mid
    if (arr[mid] == key) {
        return mid;
    }

    // If the key is greater, search in the right half
    if (arr[mid] < key) {
        return recBinarySearch(arr, mid + 1, high, key);
    }

    // If the key is smaller, search in the left half
    return recBinarySearch(arr, low, mid - 1, key);
}

int main() {

    int size, key;
    std::cout << "Enter the no of elements in the array : ";
    std::cin >> size;
    int a[size];

    //accepting input
    std::cout << "Please enter the elements in sorted order.\n";
    for (int index = 0; index < size; index++) {
        std::cout << "Enter element " << index + 1 << " : ";
        std::cin >> a[index];
    }

    std::cout << "Enter target element to be searched: ";
    std::cin >> key;

    // function calls
    linearSearch(a, size, key);

    int result = recBinarySearch(a, 0, size - 1, key);

    if (result != -1) {
        std::cout << "Binary Search: The element was found at index: " << result << std::endl;
    } else {
        std::cout << "Binary Search: Element not found." << std::endl;
    }

    return 0;
}
