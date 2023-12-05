#include "ortools/sat/cp_model.h"

using namespace operations_research;
using namespace operations_research::sat;

int main()
{
    CpModelBuilder cp_model;

    int order = 4;
    int ix = order - 1;
    int diameter = order * 2 - 1;
    int max_val = 3 * order * order - 3 * order + 1;
    int total_sum = max_val * (max_val + 1) / 2;

    // Creating the hexagon matrix
    std::map<std::tuple<int, int, int>, IntVar> hexagon;
    for (int i = -ix; i <= ix; ++i)
    {
        for (int j = -ix; j <= ix; ++j)
        {
            for (int k = -ix; k <= ix; ++k)
            {
                if (i + j + k == 0)
                {
                    hexagon[{i, j, k}] = cp_model.NewIntVar(Domain(1, max_val));
                }
                // Note: No need to explicitly set 0 for unused cells in C++
            }
        }
    }

    // Add all different constraint
    std::vector<IntVar> vars;
    for (int i = -ix; i <= ix; ++i)
    {
        for (int j = -ix; j <= ix; ++j)
        {
            for (int k = -ix; k <= ix; ++k)
            {
                if (i + j + k == 0)
                {
                    vars.push_back(hexagon[{i, j, k}]);
                }
            }
        }
    }
    cp_model.AddAllDifferent(vars);

    IntVar sumsto = cp_model.NewIntVar(Domain(0, total_sum));

    // Add sum constraints
    for (int i = -ix; i <= ix; ++i)
    {
        LinearExpr sum_i;
        for (int j = -ix; j <= ix; ++j)
        {
            for (int k = -ix; k <= ix; ++k)
            {
                sum_i += hexagon[{i, j, k}];
            }
        }
        cp_model.AddEquality(sum_i, sumsto);
    }

    for (int j = -ix; j <= ix; ++j)
    {
        LinearExpr sum_j;
        for (int i = -ix; i <= ix; ++i)
        {
            for (int k = -ix; k <= ix; ++k)
            {
                sum_j += hexagon[{i, j, k}];
            }
        }
        cp_model.AddEquality(sum_j, sumsto);
    }

    for (int k = -ix; k <= ix; ++k)
    {
        LinearExpr sum_k;
        for (int i = -ix; i <= ix; ++i)
        {
            for (int j = -ix; j <= ix; ++j)
            {
                sum_k += hexagon[{i, j, k}];
            }
        }
        cp_model.AddEquality(sum_k, sumsto);
    }

    CpSolver solver;
    Model model;

    // Setting solver parameters
    CpSolverResponse response;
    solver.GetParameters().set_max_time_in_seconds(10);
    solver.GetParameters().set_num_search_workers(4);
    solver.GetParameters().set_log_search_progress(true);

    // Solving the model
    response = SolveCpModel(cp_model.Build(), &solver);

    std::cout << "Total Solution Time: " << solverDuration.count() / 1000.0 << " s\n";
    std::cout << "Status: " << CpSolverResponseStatus_Name(response.status()) << "\n";

    // Print the solution
    if (response.status() == CpSolverStatus::OPTIMAL || response.status() == CpSolverStatus::FEASIBLE)
    {
        for (int i = -ix; i <= ix; ++i)
        {
            for (int j = -ix; j <= ix; ++j)
            {
                for (int k = -ix; k <= ix; ++k)
                {
                    if (i + j + k == 0)
                    {
                        std::cout << SolutionIntegerValue(response, hexagon[{i, j, k}]) << "\t";
                    }
                }
            }
            std::cout << "\n";
        }
    }

    return 0;
}
