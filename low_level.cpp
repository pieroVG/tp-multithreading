#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <Eigen/Dense>
#include <omp.h>
#include <iostream>
#include <vector>

using json = nlohmann::json;

const std::string PROXY_URL = "http://localhost:8000";

struct Task {
    int identifier;
    double time;
    Eigen::VectorXd n;
    Eigen::MatrixXd a;
    Eigen::VectorXd b;
    Eigen::VectorXd x;

    static Task from_json(const json& j) {
        Task t;
        t.identifier = j["identifier"];
        t.time = j.value("time", 0.0);
        
        if (j.contains("n")) {
            auto n_array = j["n"].get<std::vector<double>>();
            t.n = Eigen::Map<Eigen::VectorXd>(n_array.data(), n_array.size());
        }
        
        if (j.contains("a")) {
            auto a_data = j["a"].get<std::vector<std::vector<double>>>();
            int rows = a_data.size();
            int cols = a_data[0].size();
            t.a.resize(rows, cols);
            for (int i = 0; i < rows; i++) {
                for (int k = 0; k < cols; k++) {
                    t.a(i, k) = a_data[i][k];
                }
            }
        }
        
        if (j.contains("b")) {
            auto b_array = j["b"].get<std::vector<double>>();
            t.b = Eigen::Map<Eigen::VectorXd>(b_array.data(), b_array.size());
        }
        
        if (j.contains("x")) {
            auto x_array = j["x"].get<std::vector<double>>();
            t.x = Eigen::Map<Eigen::VectorXd>(x_array.data(), x_array.size());
        }
        
        return t;
    }

    json to_json() const {
        json j;
        j["identifier"] = identifier;
        j["time"] = time;
        
        if (n.size() > 0) {
            j["n"] = std::vector<double>(n.data(), n.data() + n.size());
        }
        
        if (a.size() > 0) {
            std::vector<std::vector<double>> a_vec;
            for (int i = 0; i < a.rows(); i++) {
                std::vector<double> row;
                for (int k = 0; k < a.cols(); k++) {
                    row.push_back(a(i, k));
                }
                a_vec.push_back(row);
            }
            j["a"] = a_vec;
        }
        
        if (b.size() > 0) {
            j["b"] = std::vector<double>(b.data(), b.data() + b.size());
        }
        
        if (x.size() > 0) {
            j["x"] = std::vector<double>(x.data(), x.data() + x.size());
        }
        
        return j;
    }

    void work() {
        auto start = omp_get_wtime();
        if (a.size() > 0 && b.size() > 0) {
            x = a.colPivHouseholderQr().solve(b);
        }
        auto end = omp_get_wtime();
        time = end - start;
    }
};

Task get_task() {
    cpr::Response r = cpr::Get(cpr::Url{PROXY_URL});
    
    if (r.status_code != 200) {
        throw std::runtime_error("Failed to get task");
    }
    
    json j = json::parse(r.text);
    return Task::from_json(j);
}

void post_task(const Task& task) {
    json j = task.to_json();
    std::string payload = j.dump();
    
    cpr::Response r = cpr::Post(
        cpr::Url{PROXY_URL},
        cpr::Header{{"Content-Type", "application/json"}},
        cpr::Body{payload}
    );
    
    if (r.status_code != 200) {
        throw std::runtime_error("Failed to post task");
    }
}

int main() {
    std::cout << "C++ Client starting..." << std::endl;
    std::cout << "Connecting to proxy at " << PROXY_URL << std::endl;
    
    int tasks_processed = 0;
    
    while (true) {
        try {
            std::cout << "Waiting for task..." << std::endl;
            Task task = get_task();
            
            std::cout << "Received task " << task.identifier << std::endl;
            task.work();
            std::cout << "Task " << task.identifier << " completed in " 
                      << task.time << "s" << std::endl;
            
            post_task(task);
            std::cout << "Task " << task.identifier << " sent back" << std::endl;
            
            tasks_processed++;
            
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            break;
        }
    }
    
    std::cout << "Total tasks processed: " << tasks_processed << std::endl;
    return 0;
}