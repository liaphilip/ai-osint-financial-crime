import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


def build_graph(data):
    graph = nx.Graph()

    case_id = data.get("case_id", "unknown_case")

    # Case
    graph.add_node(case_id, type="case")

    # Company
    company = data.get("company", {}).get("name", "Unknown")
    graph.add_node(company, type="company")
    graph.add_edge(
        case_id,
        company,
        relationship="investigates"
    )

    # Domains
    for domain in data.get("domains", []):
        graph.add_node(domain, type="domain")
        graph.add_edge(
            company,
            domain,
            relationship="associated_with"
        )

    # Job posting
    job = data.get("job_posting", {}).get(
        "title",
        "Recruitment posting"
    )

    graph.add_node(job, type="job_posting")
    graph.add_edge(
        company,
        job,
        relationship="posted"
    )

    # Emails
    for email in data.get("emails", []):
        address = (
            email.get("email")
            if isinstance(email, dict)
            else str(email)
        )

        if address:
            graph.add_node(address, type="email")
            graph.add_edge(
                company,
                address,
                relationship="uses"
            )

    # People
    for person in data.get("people", []):
        name = (
            person.get("name")
            if isinstance(person, dict)
            else str(person)
        )

        if name:
            graph.add_node(name, type="person")
            graph.add_edge(
                company,
                name,
                relationship="associated_with"
            )

    # Social accounts
    for account in data.get("social_accounts", []):
        if isinstance(account, dict):
            username = account.get("username", "")
            platform = account.get("platform", "")
            social_node = f"{platform}:{username}"

            if username:
                graph.add_node(
                    social_node,
                    type="social_account"
                )

    # IP addresses
    for ip in data.get("ips", []):
        graph.add_node(ip, type="ip")

        for domain in data.get("domains", []):
            graph.add_edge(
                domain,
                ip,
                relationship="resolves_to"
            )

    # Subdomains
    for subdomain in data.get("subdomains", []):
        name = (
            subdomain.get("subdomain")
            if isinstance(subdomain, dict)
            else str(subdomain)
        )

        if name:
            graph.add_node(name, type="subdomain")

            for domain in data.get("domains", []):
                graph.add_edge(
                    domain,
                    name,
                    relationship="has_subdomain"
                )

    # Evidence
    for evidence in data.get("evidence", []):
        graph.add_node(evidence, type="evidence")
        graph.add_edge(
            case_id,
            evidence,
            relationship="supported_by"
        )

    # Government verification
    if data.get("government_verification"):
        verification_node = f"{case_id}:government_verification"
        graph.add_node(
            verification_node,
            type="government_verification"
        )
        graph.add_edge(
            case_id,
            verification_node,
            relationship="verified_by"
        )

    return graph


def visualize_graph(graph, output_path="output/investigation_graph.png"):
    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.figure(figsize=(14, 9))

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.5
    )

    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_size=2500,
        font_size=8,
        edge_color="gray"
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

    plt.title(
        "OSINT Investigation Graph",
        fontsize=16
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return output_path


if __name__ == "__main__":
    print("Graph module ready.")