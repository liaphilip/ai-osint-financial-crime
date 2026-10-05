import json
import networkx as nx
import matplotlib.pyplot as plt


def load_data():
    with open("data/sample_data.json", "r") as file:
        return json.load(file)


def build_graph(data):
    graph = nx.Graph()

    company = data["company"]["name"]

    graph.add_node(company, type="company")

    # Domain
    for domain in data["domains"]:
        graph.add_node(domain["domain"], type="domain")
        graph.add_edge(
            company,
            domain["domain"],
            relationship="owns"
        )

    # Job posting
    job = data["job_posting"]["title"]
    graph.add_node(job, type="job_posting")
    graph.add_edge(
        company,
        job,
        relationship="posted"
    )

    # Emails
    for email in data["emails"]:
        address = email["email"]
        graph.add_node(address, type="email")
        graph.add_edge(
            company,
            address,
            relationship="uses"
        )

    # People
    for person in data["people"]:
        name = person["name"]
        graph.add_node(name, type="person")
        graph.add_edge(
            company,
            name,
            relationship="associated_with"
        )

    # Social accounts
    for account in data["social_accounts"]:
        username = account["username"]
        platform = account["platform"]

        node = f"{platform}:{username}"

        graph.add_node(node, type="social_account")
        graph.add_edge(
            name,
            node,
            relationship="has_account"
        )

    # IP addresses
    for ip in data["ips"]:
        address = ip["ip"]

        graph.add_node(address, type="ip")
        graph.add_edge(
            "example.com",
            address,
            relationship="resolves_to"
        )

    return graph


def visualize_graph(graph):
    plt.figure(figsize=(12, 8))

    positions = nx.spring_layout(
        graph,
        seed=42
    )

    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_size=2500,
        font_size=8
    )

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

    plt.title("OSINT Investigation Graph")

    plt.savefig(
        "output/investigation_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    data = load_data()

    graph = build_graph(data)

    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    visualize_graph(graph)