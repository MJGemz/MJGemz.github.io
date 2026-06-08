#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>
#include <cctype>

struct Course {
    std::string courseNumber;
    std::string courseTitle;
    std::vector<std::string> prerequisites;
};

std::vector<Course> courses;

// Convert string to uppercase for case-insensitive comparison
std::string toUpper(std::string str) {
    for (char& c : str) {
        c = std::toupper(c);
    }
    return str;
}

// Load courses from file (supports file names with spaces)
void loadData() {
    std::string filename;
    std::cout << "Enter the course data file name: ";
    std::cin.ignore(); // clear leftover newline
    std::getline(std::cin, filename);

    std::ifstream file(filename);
    if (!file) {
        std::cout << "File could not be opened.\n";
        return;
    }

    courses.clear();
    std::string line;
    while (std::getline(file, line)) {
        Course c;
        size_t pos = 0;
        size_t commaPos = line.find(',');
        c.courseNumber = line.substr(0, commaPos);
        pos = commaPos + 1;

        commaPos = line.find(',', pos);
        if (commaPos != std::string::npos)
            c.courseTitle = line.substr(pos, commaPos - pos);
        else
            c.courseTitle = line.substr(pos);

        pos = commaPos;

        while (pos != std::string::npos && pos + 1 < line.size()) {
            pos++;
            commaPos = line.find(',', pos);
            std::string prereq;
            if (commaPos != std::string::npos)
                prereq = line.substr(pos, commaPos - pos);
            else
                prereq = line.substr(pos);

            if (!prereq.empty())
                c.prerequisites.push_back(prereq);

            pos = commaPos;
        }

        courses.push_back(c);
    }

    std::cout << "Data loaded successfully.\n";
}

// Print all courses sorted alphanumerically
void printCourseList() {
    std::sort(courses.begin(), courses.end(), [](const Course& a, const Course& b) {
        return a.courseNumber < b.courseNumber;
        });

    std::cout << "Here is a sample schedule:\n";
    for (auto& c : courses) {
        std::cout << c.courseNumber << ", " << c.courseTitle << "\n";
    }
}

// Print a course and its prerequisites
void printCourse() {
    std::string input;
    std::cout << "What course do you want to know about? ";
    std::cin >> input;
    std::string inputUpper = toUpper(input);

    bool found = false;
    for (auto& c : courses) {
        if (toUpper(c.courseNumber) == inputUpper) {
            std::cout << c.courseNumber << ", " << c.courseTitle << "\n";

            if (!c.prerequisites.empty()) {
                std::cout << "Prerequisites: ";
                for (size_t i = 0; i < c.prerequisites.size(); i++) {
                    std::cout << c.prerequisites[i]; // just numbers, matches sample
                    if (i + 1 < c.prerequisites.size()) std::cout << ", ";
                }
                std::cout << "\n";
            }

            found = true;
            break;
        }
    }

    if (!found)
        std::cout << "Course not found.\n";
}

int main() {
    int choice = 0;

    std::cout << "Welcome to the course planner.\n";

    while (choice != 9) {
        std::cout << "1. Load Data Structure.\n";
        std::cout << "2. Print Course List.\n";
        std::cout << "3. Print Course.\n";
        std::cout << "9. Exit\n";
        std::cout << "What would you like to do? ";
        std::cin >> choice;

        switch (choice) {
        case 1:
            loadData();
            break;
        case 2:
            printCourseList();
            break;
        case 3:
            printCourse();
            break;
        case 9:
            std::cout << "Thank you for using the course planner!\n";
            break;
        default:
            std::cout << choice << " is not a valid option.\n";
        }
    }
    
    return 0;
}
