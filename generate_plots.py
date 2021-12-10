# ************************************************************
# generate_plots.py
#
# This python script generates graphs from calculated data.
# ************************************************************

import matplotlib.pyplot as plt


# ----------------------------------
# AVERAGE CLUSTERING COEFFICIENT
# ----------------------------------

with open('average_clustering_calculation.txt') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(float(line))

acc_data = [
    sum(new_lines[0:879])/879,
    sum(new_lines[880:1758])/879,
    sum(new_lines[1759:2637])/879,
    sum(new_lines[2638:3516])/879,
    sum(new_lines[3517:4395])/879,
    sum(new_lines[4396:5274])/879,
    sum(new_lines[5275:6153])/879,
    sum(new_lines[6154:7032])/879,
    sum(new_lines[7033:7911])/879,
    sum(new_lines[7912:8798])/886,
]

x_values = ["10%", "20%", "30%", "40%",
            "50%", "60%", "70%", "80%", "90%", "100%"]
plt.scatter(x_values, acc_data)
plt.plot(x_values, acc_data)
plt.title("Distribution of Average Clustering Coefficient")
plt.xlabel("Percentage")
plt.ylabel("Average Clustering Coefficient")
plt.show()

# ----------------------------------
# GLOBAL CLUSTERING COEFFICIENT
# ----------------------------------

with open('global_eff_calculation.txt') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(float(line))

acc_data = [
    sum(new_lines[0:879])/879,
    sum(new_lines[880:1758])/879,
    sum(new_lines[1759:2637])/879,
    sum(new_lines[2638:3516])/879,
    sum(new_lines[3517:4395])/879,
    sum(new_lines[4396:5274])/879,
    sum(new_lines[5275:6153])/879,
    sum(new_lines[6154:7032])/879,
    sum(new_lines[7033:7911])/879,
    sum(new_lines[7912:8798])/886,
]

x_values = ["10%", "20%", "30%", "40%",
            "50%", "60%", "70%", "80%", "90%", "100%"]
plt.scatter(x_values, acc_data)
plt.plot(x_values, acc_data)
plt.title("Distribution of Global Efficiency")
plt.xlabel("Percentage")
plt.ylabel("Global Efficiency")
plt.show()
