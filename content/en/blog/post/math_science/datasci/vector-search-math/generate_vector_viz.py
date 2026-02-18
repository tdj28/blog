import matplotlib.pyplot as plt
import numpy as np

def create_viz(filename, points, labels, title, highlight_circle=False):
    plt.figure(figsize=(8, 6))
    
    # Extract coordinates
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    
    # Plot points
    plt.scatter(x, y, c='blue', s=100, zorder=5)
    
    # Add labels
    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]), xytext=(10, 10), textcoords='offset points', 
                     fontsize=10, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        
    # Set limits and labels
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.xlabel('Dimension 1 (Abstract)')
    plt.ylabel('Dimension 2 (Abstract)')
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    
    # Draw origin arrow
    for i in range(len(points)):
        plt.arrow(0, 0, x[i], y[i], color='gray', alpha=0.5, width=0.01, head_width=0.05, length_includes_head=True)

    if highlight_circle:
        circle = plt.Circle((x[0], y[0]), 0.3, color='green', fill=False, linestyle='--', linewidth=2)
        plt.gca().add_patch(circle)
        plt.text(x[0]-0.2, y[0]+0.35, "Semantic Neighborhood", color='green', fontsize=9)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

# Pair 1: Semantically Close
points_close = [(0.7, 0.6), (0.85, 0.55)]
labels_close = [
    '"The weather was amazing today..."',
    '"My day was made all the better..."'
]
create_viz('vector_viz_close.png', points_close, labels_close, 'Semantic Similarity: High Cosine Similarity', highlight_circle=True)

# Pair 2: Semantically Far
points_far = [(0.7, 0.6), (-0.6, -0.3)]
labels_far = [
    '"The weather was amazing today..."',
    '"My car broke down..."'
]
create_viz('vector_viz_far.png', points_far, labels_far, 'Semantic Dissimilarity: Low Cosine Similarity', highlight_circle=False)

print("Images generated: vector_viz_close.png, vector_viz_far.png")
