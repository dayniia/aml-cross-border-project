import os
import matplotlib.pyplot as plt
import networkx as nx

# Apply modern aesthetic configuration
plt.style.use("dark_background")


def create_fan_out_graph():
    """Generates a Fan-Out money laundering topology (1 Source -> Multiple Accounts)."""
    G = nx.DiGraph()
    source_acc = "Source\n001"
    mule_accs = [f"Mule\n{i:03d}" for i in range(1, 6)]

    for mule in mule_accs:
        G.add_edge(source_acc, mule, weight="$50,000")

    pos = {source_acc: (0, 0)}
    for idx, mule in enumerate(mule_accs):
        pos[mule] = (1.5, (2 - idx) * 0.8)

    return G, pos, "Topology Pattern 1: Structuring & Fan-Out Dispersal", source_acc


def create_cycle_graph():
    """Generates a Cycle money laundering topology (Circular Routing)."""
    G = nx.DiGraph()
    cycle_nodes = [f"Shell Co.\n#{i}" for i in range(1, 6)]

    for i in range(len(cycle_nodes)):
        nxt = cycle_nodes[(i + 1) % len(cycle_nodes)]
        G.add_edge(cycle_nodes[i], nxt, weight="$100,000")

    pos = nx.circular_layout(G)
    return G, pos, "Topology Pattern 2: Layering & Circular Flow", None


def plot_and_save_graphs(output_dir="stage_5_report/visualizations"):
    """Renders high-resolution, production-grade network visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    topologies = [create_fan_out_graph(), create_cycle_graph()]

    for idx, (G, pos, title, primary_node) in enumerate(topologies, 1):
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#0e1117")
        ax.set_facecolor("#0e1117")

        # Define node color schemes
        if primary_node:
            node_colors = [
                "#e63946" if n == primary_node else "#457b9d" for n in G.nodes()
            ]
        else:
            node_colors = "#2a9d8f"

        # Draw nodes with smooth borders
        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=2800,
            node_color=node_colors,
            edgecolors="#ffffff",
            linewidths=2.0,
            ax=ax,
        )

        # Draw labels with clear font styling
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=9,
            font_color="#ffffff",
            font_weight="bold",
            font_family="sans-serif",
            ax=ax,
        )

        # Draw directed curved edges with arrows
        nx.draw_networkx_edges(
            G,
            pos,
            arrowstyle="-|>",
            arrowsize=22,
            edge_color="#f4a261",
            width=2.5,
            connectionstyle="arc3,rad=0.1",
            ax=ax,
        )

        # Title and framing
        plt.title(
            title,
            fontsize=15,
            fontweight="bold",
            color="#f1faee",
            pad=25,
            loc="center",
        )
        plt.axis("off")
        plt.tight_layout()

        # Save with maximum anti-aliasing and DPI precision
        out_path = os.path.join(output_dir, f"pattern_topology_{idx}.png")
        plt.savefig(
            out_path,
            dpi=300,
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
            edgecolor="none",
        )
        plt.close(fig)
        print(f"[+] Re-generated high-quality visualization: {out_path}")


if __name__ == "__main__":
    plot_and_save_graphs()
