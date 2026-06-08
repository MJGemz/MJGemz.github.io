#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>
#include <cctype>
#include <unordered_map>

struct Course {
    std::string courseNumber;
    std::string courseTitle;
    std::vector<std::string> prerequisites;
};

// Main data structures
std::vector<Course> courses;
std::unordered_map<std::string, Course> courseMap;

// Convert string to uppercase for consistent matching
std::string toUpper(std::string str) {
    for (char& c : str) {
        c = std::toupper(c);
    }
    return str;
}

// Check if course already exists (prevents duplicates)
bool courseExists(const std::string& courseNumber) {
    return courseMap.find(toUpper(courseNumber)) != courseMap.end();
}

// Load courses from file
void loadData() {
    std::string filename;
    std::cout << "Enter the course data file name: ";

    std::cin.ignore();
    std::getline(std::cin, filename);

    std::ifstream file(filename);
    if (!file) {
        std::cout << "File could not be opened.\n";
        return;
    }

    courses.clear();
    courseMap.clear();

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

        std::string key = toUpper(c.courseNumber);

        if (!courseExists(c.courseNumber)) {
            courses.push_back(c);
            courseMap[key] = c;
        }
    }

    // Sort ONCE (performance improvement)
    std::sort(courses.begin(), courses.end(),
        [](const Course& a, const Course& b) {
            return a.courseNumber < b.courseNumber;
        });

    std::cout << "Data loaded successfully.\n";
}

// Print full sorted course list
void printCourseList() {
    if (courses.empty()) {
        std::cout << "No data loaded.\n";
        return;
    }

    std::cout << "Here is a sample schedule:\n";

    for (auto& c : courses) {
        std::cout << c.courseNumber << ", " << c.courseTitle << "\n";
    }
}

// Faster lookup using hash map (improved algorithm)
void printCourse() {
    if (courses.empty()) {
        std::cout << "Load data first.\n";
        return;
    }

    std::string input;
    std::cout << "What course do you want to know about? ";
    std::cin >> input;

    std::string key = toUpper(input);

    if (courseMap.find(key) != courseMap.end()) {
        Course c = courseMap[key];

        std::cout << c.courseNumber << ", " << c.courseTitle << "\n";

        if (!c.prerequisites.empty()) {
            std::cout << "Prerequisites: ";

            for (size_t i = 0; i < c.prerequisites.size(); i++) {
                std::cout << c.prerequisites[i];
                if (i + 1 < c.prerequisites.size())
                    std::cout << ", ";
            }
            std::cout << "\n";
        }
    }
    else {
        std::cout << "Course not found.\n";
    }
}

// Menu validation helper
bool validChoice(int choice) {
    return choice == 1 || choice == 2 || choice == 3 || choice == 9;
}

int main() {
    int choice = 0;

    std::cout << "Welcome to the course planner.\n";

    while (choice != 9) {

        std::cout << "\n1. Load Data Structure.\n";
        std::cout << "2. Print Course List.\n";
        std::cout << "3. Print Course.\n";
        std::cout << "9. Exit\n";
        std::cout << "What would you like to do? ";

        std::cin >> choice;

        if (!validChoice(choice)) {
            std::cout << "Invalid option. Try again.\n";
            continue;
        }

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
        }
    }

    return 0;
}
