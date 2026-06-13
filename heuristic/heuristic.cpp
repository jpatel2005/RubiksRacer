#include <vector>
#include <cmath>
#include <algorithm>
#include <array>

extern "C" {
    struct TargetSquare {
        int color;
        int x;
        int y; 
    };
    // Takes two 1D integer arrays of size 25
    int get_heuristic_cost(const int* puzzle, const int* target) {
        // Compute minimum-weight bipartite matching via brute force search 
        int total_distance = 0;
        int n = 5; // puzzle is 5x5
        int target_indices[9] = {6,7,8,11,12,13,16,17,18};
        TargetSquare targets[9];
        // identify the targets
        for (int i = 0; i < 9; i++) {
            int idx = target_indices[i];
            targets[i].color = target[idx];
            targets[i].x = idx / 5;
            targets[i].y = idx % 5;
        }
        // locate all tiles by color (0 = empty, 1-6 for the colors)
        std::array<std::vector<std::pair<int,int>>, 7> tiles = {};
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) { 
                int idx = i*n+j;
                int color = puzzle[idx];
                tiles[color].push_back({i,j});
            }
        }
        // iterate through each color
        for (int c = 1; c <= 6; c++) {
            std::vector<TargetSquare> color_targets;
            // find the colors in the target
            for (int i = 0; i < 9; i++) {
                if (targets[i].color == c) {
                    color_targets.push_back(targets[i]);
                }
            }
            int k = color_targets.size();
            if (k == 0) {
                continue;
            }
            int min_dist = 1000000007;
            switch (k) {
                case 1:
                    // 1 target, 4 available tiles
                    for (int i = 0; i < 4; i++) {
                        int dist = std::abs(color_targets[0].x - tiles[c][i].first) + std::abs(color_targets[0].y - tiles[c][i].second);
                        if (dist < min_dist) {
                            min_dist = dist;
                        }
                    }
                    break;
                case 2:
                    // 2 targets, 4 available tiles
                    for (int i = 0; i < 4; i++) {
                        for (int j = 0; j < 4; j++) {
                            if (i == j) {
                                continue;
                            }
                            int dist = std::abs(color_targets[0].x - tiles[c][i].first) + std::abs(color_targets[0].y - tiles[c][i].second) +
                                       std::abs(color_targets[1].x - tiles[c][j].first) + std::abs(color_targets[1].y - tiles[c][j].second);
                            if (dist < min_dist) {
                                min_dist = dist;
                            }
                        }
                    }
                    break;
                case 3:
                    // 3 targets, 4 available tiles
                    for (int i = 0; i < 4; i++) {
                        for (int j = 0; j < 4; j++) {
                            if (i == j) {
                                continue;
                            }
                            for (int m = 0; m < 4; m++) {
                                if (i == m || j == m) {
                                    continue;
                                }
                                int dist = std::abs(color_targets[0].x - tiles[c][i].first) + std::abs(color_targets[0].y - tiles[c][i].second) + 
                                           std::abs(color_targets[1].x - tiles[c][j].first) + std::abs(color_targets[1].y - tiles[c][j].second) + 
                                           std::abs(color_targets[2].x - tiles[c][m].first) + std::abs(color_targets[2].y - tiles[c][m].second);
                                if (dist < min_dist) {
                                    min_dist = dist;
                                }
                            }
                        }
                    }
                    break;
                case 4:
                default:
                    // define indices for permutation
                    int permutation[4] = {0,1,2,3};
                    do {
                        int dist = 0;
                        for (int m = 0; m < 4; m++) {
                            dist += std::abs(color_targets[m].x - tiles[c][permutation[m]].first) + std::abs(color_targets[m].y - tiles[c][permutation[m]].second);
                            if (dist >= min_dist) {
                                break;
                            }
                        }
                        if (dist < min_dist) {
                            min_dist = dist;
                        }
                    } while (std::next_permutation(permutation, permutation + 4));
                    break;
            }
            total_distance += min_dist;
        }        
        return total_distance; 
    }
}