from rdflib import Graph, Namespace


def load_ontology(ontology_path: str, ontology_format: str = "turtle") -> Graph:
    """
    Load an ontology from a file in the specified format.

    Args:
        ontology_path (str): Path to the ontology file.
        ontology_format (str): Format of the ontology (default is "turtle").

    Returns:
        Graph: rdflib Graph object containing the ontology.
    """
    g = Graph()
    g.parse(ontology_path, format=ontology_format)
    return g


def query_elements(graph: Graph) -> dict:
    """
    Execute a SPARQL query to fetch classes and their identifiers.

    Args:
        graph (Graph): rdflib Graph object containing the ontology.
        namespace (str): Namespace to filter classes (e.g., "http://purl.obolibrary.org/obo/").

    Returns:
        dict: Dictionary where keys are class labels and values are their identifiers.
    """
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?element ?label
    WHERE {{
    {{
        ?element a owl:Class .
        ?element rdfs:label ?label . 
    }}
    UNION
    {{
        ?element a owl:DatatypeProperty .
        ?element rdfs:label ?label .
    }}
    UNION
    {{
        ?element a owl:ObjectProperty .
        ?element rdfs:label ?label .
    }}
    }}
    """
    results = graph.query(query)

    elements_dict = {}
    for row in results:
        class_uri = str(row[0])  # First element: URIRef
        class_label = str(row[1]) if len(row) > 1 and row[1] else class_uri.split("/")[
            -1]  # Second element: Literal, if present
        elements_dict[class_label] = f"<{class_uri}>"

    return elements_dict


def save_dict_to_file(data: dict, output_path: str) -> None:
    """
    Save a dictionary to a text file.

    Args:
        data (dict): Dictionary with data to save.
        output_path (str): Path to the output file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key} : {value}\n")


def main(ontology_path: str,  output_path: str, ontology_format: str = "turtle"):
    """
    Load an ontology, query classes, and save the results to a file.

    Args:
        ontology_path (str): Path to the ontology file.
        namespace (str): Namespace to filter classes.
        prefix (str): Prefix to filter class identifiers.
        output_path (str): Path to the output file.
        ontology_format (str): Format of the ontology (default is "turtle").
    """
    # Load the ontology
    graph = load_ontology(ontology_path, ontology_format)

    # Query classes and their identifiers
    classes_dict = query_elements(graph)

    # Save the results to a file
    save_dict_to_file(classes_dict, output_path)

    # Print the dictionary
    print(classes_dict)

if __name__ == "__main__":
    ontology_path = "./country.ttl"  # Path to the ontology file
    output_path = "./reduce_country.txt"  # Output file
    ontology_format = "turtle"  # Ontology format

    main(ontology_path, output_path, ontology_format)
