# OntoGenix LLM Experiments

This repository contains all experimental data, code, and resources associated with the evaluation of large language models (LLMs) for automated ontology engineering using the OntoGenix pipeline. The study includes both proprietary (OpenAI) and open-source models in their base and fine-tuned variants. Experiments were conducted across a consistent workflow and dataset to ensure comparability.

## 📌 Overview

The experiments presented in this repository aim to assess the effectiveness of LLMs in generating RDF/OWL ontologies from structured data (CSV files). The methodology encompasses:

* Integration of multiple LLMs (GPT and open-source variants) into the OntoGenix ontology construction pipeline.
* Systematic fine-tuning of selected models using paired CSV-ontology datasets.
* Quantitative and qualitative evaluation of the generated ontologies across various dimensions, including syntactic validity and semantic quality.

---

## 🤖 Models Evaluated

### 1. OpenAI GPT Models

#### [Base Models](base-llm/GPT)

* **GPT-3.5-turbo-0125**
* **GPT-4-1106-preview**
* **GPT-4o-2024-08-06**

These models were evaluated directly within the OntoGenix pipeline without further training.

#### [Fine-tuned Models](fine-tuning/GPT)

Due to fine-tuning constraints, the following models were fine-tuned using a curated dataset of 40 CSV-ontology pairs:

* **GPT-3.5-turbo-0125**
* **GPT-4o-2024-08-06**
* **GPT-4o-mini-2024-07-18**

*Note: GPT-4 was not available for fine-tuning at the time of experimentation.*

Training configuration:

* Epochs: 6
* Batch size: 3
* Learning rate multiplier: 0.3

Fine-tuned models were prompted using a simplified single-sentence input format.

### 2. Open-Source Models

#### [Base Models](base-llm/open-source)

The following state-of-the-art open-source LLMs were evaluated (some in quantized formats at 4-bit and 8-bit levels):

* **LLaMA-2**: 7B (8-bit), 13B (4/8-bit and full), 70B (4-bit)
* **LLaMA-3**: 8B (4/8-bit and full), 70B (4-bit)
* **Mistral-7B**
* **Mixtral-8x7B**

Common generation parameters:

* `top_p = 0.8`
* `top_k = 40`
* `temperature = 0.5`
* `max_new_tokens = 4096`

#### [Fine-tuned Models](fine-tuning/open-source)

Fine-tuning was applied to the following models using the same 40 paired CSV-ontology dataset:

* **LLaMA-2-7B**
* **LLaMA-2-13B**
* **LLaMA-3-8B**

Quantized variants (4-bit and 8-bit) were also evaluated for LLaMA-2-7B and LLaMA-3-8B. Larger models (e.g., LLaMA-3-70B, Mixtral-8x7B) were excluded from fine-tuning due to resource limitations.

---

## 📋 Datasets

The experimental framework relies on two categories of datasets:

### 1. **Evaluation Datasets**

Six publicly available CSV datasets were selected from Kaggle to represent diverse commercial domains. These were used to evaluate the performance of both base and fine-tuned models:

| Dataset                        | Rows      | Columns | Description                                       | Link                                                                             |
| ------------------------------ | --------- | ------- | ------------------------------------------------- | -------------------------------------------------------------------------------- |
| Airlines Customer Satisfaction | 129,880   | 23      | Customer feedback and satisfaction data           | [Link](https://www.kaggle.com/datasets/sjleshrac/airlines-customer-satisfaction) |
| Amazon Ratings                 | 2,023,070 | 4       | Product reviews from the Beauty category          | [Link](https://www.kaggle.com/datasets/skillsmuggler/amazon-ratings)             |
| BigBasket Products             | 8,208     | 9       | Product inventory data from an online store       | [Link](https://www.kaggle.com/datasets/chinmayshanbhag/big-basket-products)      |
| Brazilian E-Commerce           | 99,441    | 5       | E-commerce transaction data in Brazil             | [Link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)              |
| Customer Complaint             | 745,392   | 18      | Consumer complaints related to financial products | [Link](https://www.kaggle.com/datasets/utkarshx27/consumer-complaint)            |
| E-commerce (UK)                | 541,909   | 8       | Online retail data for a UK-based vendor          | [Link](https://www.kaggle.com/datasets/carrie1/ecommerce-data)                   |

### 2. **Training Dataset for Fine-Tuning**

A curated dataset of **40 CSV-ontology pairs** was developed to support supervised fine-tuning. Each pair consists of:

* A semantically structured CSV file.
* A manually crafted OWL ontology in Turtle syntax that captures the conceptual model represented by the CSV.

**Features of the training dataset:**

* Domains: e-commerce, logistics, finance, customer relations, and general administration.
* Ontologies follow Linked Data best practices, reusing vocabularies such as `rdf`, `rdfs`, `xsd`, and `owl`.
* RDF serializations were verified to be syntactically valid and semantically coherent using Protégé and RDF validation tools.

This dataset is located in the [`fine-tuning/training_files`](fine-tuning/training_files) directory.

The same dataset was used consistently across fine-tuning procedures for both GPT and open-source models, ensuring comparability of results.

---

## 🔍 Evaluation Methodology

The [generated ontologies](metrics/ontologies) were evaluated using both **quantitative** and **qualitative** methods:

*Note: Only valid ontologies are included in this directory for evaluation purposes. Ontologies deemed invalid have been excluded.*

### Quantitative Evaluation

1. **Syntactic Validation**:

   * RDF validators were employed to detect serialization issues (e.g., Turtle syntax errors, wrong formats, invalid URIs).
   * Error types were categorized (e.g., incorrect prefixes, invalid identifiers, loop errors).

2. **Manual Correction**:

   * Syntactic errors were manually corrected only if the workload was less than that required to model from scratch.
   * This allowed further semantic and structural analysis post-validation.
     
3. **Ontology Quality Tools**:

   * [**OOPS! (Ontology Pitfall Scanner)**](metrics/oops): Identifies modeling pitfalls (17 found types out of 41).
   * [**OQuaRE Metrics**](metrics/oquare/results/metrics/ontologies): 19 ontology quality metrics were computed, covering complexity, cohesion, richness, and reusability.

### Qualitative Evaluation

A deeper inspection of semantic coherence and modeling fidelity was carried out, taking into account the following criteria:

| **Criterion**                  | **Definition**                                                                                                                                               | **Level 1 (Poor)**                                                                                          | **Level 2 (Acceptable)**                                                                                      | **Level 3 (Satisfactory)**                                                                                                           |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| **Clarity and Readability**   | Assesses whether concepts, classes, and properties are defined clearly, consistently, and in an understandable manner.                                       | Entities are unclear, ambiguous, or inconsistent; use of jargon or symbols without proper explanation.       | Most entities are understandable, but some terms are vague or poorly defined.                                 | Entities are consistently clear, coherent, and easily interpreted by both experts and non-experts.                                 |
| **Coverage**                  | Measures how well the ontology captures the information and concepts represented in the source CSV file.                                                    | Many important CSV elements are missing or misrepresented; significant omissions.                             | Main elements are represented, though some details or relationships are missing.                             | All key CSV elements are fully and accurately represented, including relevant details and relationships.                          |
| **Logical Consistency**       | Evaluates whether there are contradictions or formal errors in class hierarchies, properties, or structure.                                                  | Contains logical inconsistencies or structural errors that undermine ontology validity.                       | Minor issues or ambiguities present, but the ontology is mostly logically sound.                              | Free of logical inconsistencies; hierarchies and relationships are structurally valid and coherent.                                |
| **Ontology Architecture Assessment** | Assesses whether the ontology is well-organized, with logical hierarchies and modular design to support reuse, reasoning, search, or classification tasks. | Structure is disorganized, flat, or incoherent; difficult to apply for functional tasks.                      | Some hierarchy and modularity present, but with partial organization or redundancy.                          | Well-structured hierarchy and clear modularization; supports classification, reasoning, and integration.                           |

The results are located in [`(metrics/qualitative_assesment)`]((metrics/qualitative_assesment)) directory.
