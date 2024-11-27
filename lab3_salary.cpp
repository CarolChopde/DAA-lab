#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <iomanip> // For setting output precision

using namespace std;

// Class to handle reading data from the CSV file
class CSVReader {
public:
    CSVReader(const string& filename) : filename(filename) {}

    vector<vector<string>> readData() {
        ifstream fin(filename);
        vector<vector<string>> data;
        if (!fin.is_open()) {
            cerr << "Error opening file." << endl;
            return data;
        }
        
        string line;

        // Skip the header line
        getline(fin, line);

        while (getline(fin, line)) {
            vector<string> row;
            stringstream s(line);
            string word;

            while (getline(s, word, ',')) {
                row.push_back(word);
            }
            data.push_back(row);
        }

        fin.close();
        return data;
    }

private:
    string filename;
};

// Class to handle gross and net salary calculations
class SalaryCalculator {
public:
    static float calculateGross(float basic, bool metro, float other) {
        float HRA = metro ? basic * 0.05f : basic * 0.04f;
        float PF = basic * 0.12f;
        float gross = basic + HRA + other - PF;
        return gross;
    }

    static float calculateNet(float gross, float inc_tax) {
        float net = gross - inc_tax;
        return net;
    }
};

// Class to find minimum and maximum net salary using divide-and-conquer
class MinMaxFinder {
public:
    pair<float, float> findMinMax(const vector<pair<string,float>>& arr, int i, int j) {
        if (i == j) {
            return {arr[i].second, arr[i].second};
        }
        if (j - i == 1) {
            if (arr[i].second < arr[j].second) {
                return {arr[i].second, arr[j].second};
            } else {
                return {arr[j].second, arr[i].second};
            }
        }

        int mid = (i + j) / 2;

        pair<float, float> left_minmax = findMinMax(arr, i, mid);
        pair<float, float> right_minmax = findMinMax(arr, mid + 1, j);

        float min_val = min(left_minmax.first, right_minmax.first);
        float max_val = max(left_minmax.second, right_minmax.second);

        return {min_val, max_val};
    }
};

int main() {
    CSVReader reader("test.csv");
    vector<vector<string>> data = reader.readData();

    ofstream fout("datatest.csv");
    vector<pair<string, float>> net_sort;

    for (const auto& row : data) {
        // Validate that the row has the correct number of columns
        if (row.size() < 5) {
            cerr << "Invalid data: Not enough columns in the row." << endl;
            return 1; 
        }

        string empID = row[0];

        try {
            // Validate basic salary
            float basic = stof(row[1]);
            if (basic <= 0) {
                cerr << "Invalid data: Basic salary must be greater than 0 for employee ID: " << empID << endl;
                return 1; 
            }

            bool metro = row[2] == "YES";

            // Validate 'other' salary component
            float other = stof(row[3]);
            if (other < 0) {
                cerr << "Invalid data: 'Other' salary component cannot be negative for employee ID: " << empID << endl;
                return 1; 
            }

            // Validate income tax
            float inc_tax = stof(row[4]);
            if (inc_tax < 0) {
                cerr << "Invalid data: Income tax cannot be negative for employee ID: " << empID << endl;
                return 1; 
            }

            // Calculate gross and net salary
            float gross = SalaryCalculator::calculateGross(basic, metro, other);
            float net = SalaryCalculator::calculateNet(gross, inc_tax);

            fout << empID << "," << fixed << setprecision(2) << gross << "," << net << "\n";
            net_sort.push_back({empID, net});
        } catch (const invalid_argument& e) {
            cerr << "Invalid data format for employee ID: " << empID << " - " << e.what() << endl;
            return 1;
        } catch (const out_of_range& e) {
            cerr << "Data out of range for employee ID: " << empID << " - " << e.what() << endl;
            return 1;
        }
    }

    fout.close();

    if (!net_sort.empty()) {
        MinMaxFinder finder;
        auto minmax = finder.findMinMax(net_sort, 0, net_sort.size() - 1);
        cout << "Minimum Net Salary: " << minmax.first << endl;
        cout << "Maximum Net Salary: " << minmax.second << endl;
    } else {
        cout << "No valid salary data found." << endl;
    }

    return 0; // Success
}
