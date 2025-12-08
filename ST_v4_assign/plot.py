import matplotlib.pyplot as plt

def read_data(filename):
    iterations = []
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    iterations.append(int(parts[0]))
                    values.append(float(parts[1]))
    return iterations, values

# Read data from both files
fc_iter, fc_vals = read_data('FC_record.txt')
sa_iter, sa_vals = read_data('SA_record.txt')

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(fc_iter, fc_vals, label='First-Choice (FC)', alpha=0.7)
plt.plot(sa_iter, sa_vals, label='Simulated Annealing (SA)', alpha=0.7)

plt.xlabel('Iteration')
plt.ylabel('Objective Value (Tour Cost)')
plt.legend()
plt.grid(True)

output = 'tsp_plot.png'
plt.savefig(output)
