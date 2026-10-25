import matplotlib.pyplot as plt
import os

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Data
labels = ['Standard System', 'AI-Charge (RL)']
values = [65, 92]  # Percentages
colors = ['#94a3b8', '#0ea5e9']  # Gray for baseline, Brand Blue for AI-Charge

# Plot Setup
plt.figure(figsize=(6, 8), facecolor='white')
bars = plt.bar(labels, values, color=colors, width=0.6)

# Customizing the look
plt.ylim(0, 100)
plt.ylabel('Efficiency Optimization (%)', fontsize=14, fontweight='bold', color='#1e293b')
plt.xticks(fontsize=12, fontweight='bold', color='#1e293b')

# Remove top and right borders for a clean look
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_color('#cbd5e1')
plt.gca().spines['bottom'].set_color('#cbd5e1')

# Add data labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{height}%', ha='center', va='bottom', 
             fontsize=16, fontweight='bold', color='#1e293b')

plt.title('Optimization Performance Gap', fontsize=18, fontweight='bold', pad=30, color='#1e293b')

# Save with high DPI for print/presentation quality
plt.tight_layout()
plt.savefig('assets/rl_graph.png', dpi=300, transparent=True)
print("Graph saved as assets/rl_graph.png")