import json
import networkx as nx
import matplotlib.pyplot as plt


def load_data():
    with open("data/sample_data.json", "r", encoding="utf-8") as file:
        return json.load(file)


def build_graph(data):
    graph = nx.Graph()

    # -------------------------
    # Company
    # -------------------------
    company = data["company"]["name"]
    domain = data["company"]["domain"]

    graph.add_node(company, type="company")

    # -------------------------
    # Domain
    # -------------------------
    graph.add_node(domain, type="domain")

    graph.add_edge(
        company,
        domain,
        relationship="owns"
    )

    # -------------------------
    # Job Posting
    # -------------------------
    job = data["job_posting"]["title"]

    graph.add_node(
        job,
        type="job_posting"
    )

    graph.add_edge(
        company,
        job,
        relationship="posted"
    )

    # -------------------------
    # Email addresses
    # -------------------------
    for email in data.get("emails", []):

        address = email["email"]

        graph.add_node(
            address,
            type="email"
        )

        graph.add_edge(
            company,
            address,
            relationship="uses"
        )

    # -------------------------
    # People
    # -------------------------
    for person in data.get("people", []):

        name = person["name"]

        graph.add_node(
            name,
            type="person"
        )

        graph.add_edge(
            company,
            name,
            relationship="associated_with"
        )

        # -------------------------
        # Social accounts
        # -------------------------
        for account in data.get("social_accounts", []):

            username = account["username"]
            platform = account["platform"]

            social_node = f"{platform}:{username}"

            graph.add_node(
                social_node,
                type="social_account"
            )

            graph.add_edge(
                name,
                social_node,
                relationship="has_account"
            )

    # -------------------------
    # IP addresses
    # -------------------------
    for ip in data.get("ips", []):

        address = ip["ip"]

        graph.add_node(
            address,
            type="ip"
        )

        graph.add_edge(
            domain,
            address,
            relationship="resolves_to"
        )

    # -------------------------
    # Subdomains
    # -------------------------
    for subdomain in data.get("subdomains", []):

        subdomain_name = subdomain["subdomain"]

        graph.add_node(
            subdomain_name,
            type="subdomain"
        )

        graph.add_edge(
            domain,
            subdomain_name,
            relationship="has_subdomain"
        )

    return graph


def visualize_graph(graph):

    plt.figure(figsize=(14, 9))

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.5
    )

    # Draw nodes and edges
    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_size=2500,
        font_size=8,
        edge_color="gray"
    )

    # Edge relationship labels
    labels = nx.get_edge_attributes(
        graph,
        "relationship"
    )

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=labels,
        font_size=7
    )

    plt.title(
        "OSINT Investigation Graph",
        fontsize=16
    )

    # Save graph
    plt.savefig(
        "output/investigation_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("\nGraph saved to:")
    print("output/investigation_graph.png")

    print("\nNodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    # Display graph
    plt.show()


def main():

    print("=" * 50)
    print("OSINT INVESTIGATION GRAPH")
    print("=" * 50)

    data = load_data()

    graph = build_graph(data)

    visualize_graph(graph)


if __name__ == "__main__":
    main()