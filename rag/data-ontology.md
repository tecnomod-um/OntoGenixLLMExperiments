# RAG experiments for matching data to ontologies

## Objective
 
Explore the capabilities of an RAG process using ontologies of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform a CSV-Ontology Alignment, which involves providing the model with the ontologies to be used and attempting to find in those ontologies a class that matches each of the column names in the CSV file.

## The content of the RAG

In this experiment, the RAG consisted of the following ontologies:
* AFO ontology: The AFO is an ontology suite that provides a standard vocabulary and semantic model for the representation of laboratory analytical processes. 
* Country ontology (made by me): Describes the demographics, economics, and geography of a country.
* CHEMINF ontology: The chemical information ontology (cheminf) describes information entities about chemical entities. It provides qualitative and quantitative attributes to richly describe chemicals.

The ontologies are available in the directory [ontologies](rag/data-ontology/ontologies).

## GPT models
### RAG performed through OpenAI platform
As in the other experiment, the RAG process is performed through an **assistant agent**. Assistants can call OpenAI’s models with specific instructions to tune their personality and capabilities and can also access multiple tools in parallel, like the File Search tool. The **File Search tool** augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users.

In this case, the assistant used the **GPT-4o model** and the previous three mentioned ontologies will be provided for the alignment task. So, when the model is asked to assign an IRI class to a column name of a CSV file, it will consult the ontologies previously included in a vector store.

<p align="center">
<img width="586" alt="image" src="https://github.com/user-attachments/assets/f2a677f1-60d4-435a-bd24-9f23edd66de9" />
</p>

All the scripts used during the project are included in the directory [scripts](rag/data-ontology/scripts).

### RAG performed through an external vector database
In this process, the three ontologies of interest are divided into parts, which are then transformed into vector embeddings using the Hugging Face model "all-MiniLM-L6-v2." These embeddings are stored in an external vector database (Chroma DB).

Subsequently, the user provides a query to the embedding model by uploading a CSV file. The model performs a similarity search for each column in the CSV, comparing the column names to the stored ontology parts. The goal is to identify and return a set of identifiers from the ontologies that best match the column names.

<p align="center">
 <img width="586" alt="image" src="https://github.com/user-attachments/assets/7b5296ef-3a14-461d-8c8b-8c1692602d60" />
</p>

The set of identifiers is then provided as context to the GPT-4o-mini model by including them in the prompt. This facilitates few-shot prompting, where examples are embedded in the prompt to guide the model toward better performance. These examples serve as conditioning, enabling the model to generate more accurate responses for subsequent queries. From the provided set of identifiers, the model's task is to select the most appropriate identifiers that correspond to the given column name.

<p align="center">
<img width="586" alt="image" src="https://github.com/user-attachments/assets/5b94ccda-0cda-41cf-a93e-6fbdaa6cc8f9" />
</p>

## Evaluation of the RAG models
To evaluate the performance of the RAG models in the task of matching data to ontologies, four CSV files have been used. We classified the model predictions as:
* True Positives (TP): When the model proposes a correct IRI for the column name.
* False Positives (FP): When the model proposes an incorrect IRI for the column name.
* True Negatives (TN): When the model indicates that an adequate IRI does not exist and it is true.
* False Negatives (FN): When the model indicates that an adequate IRI does not exist and it is not true.
### Metrics 
**Precision** is the proportion of correctly identified IRIs (true positives) out of all IRIs returned by the LLM (both true positives and false positives). It measures the accuracy of the LLM in retrieving relevant IRIs when it decides to return one.

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

**Recall** is the proportion of correctly identified IRIs (true positives) out of all actual correct IRIs available in the dataset (the sum of true positives and false negatives). It measures the LLM's ability to find all relevant IRIs for the terms in question.

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

The **F1-score** is the harmonic mean of precision and recall, balancing the two metrics to provide a single score that accounts for both false positives and false negatives. 

$$
\text{F1-score} = \frac{2TP}{2TP + FP + FN}
$$

**Accuracy** measures the proportion of correct predictions (both positive and negative) made by the model relative to the total predictions. That is, it indicates how well the model is performing overall in correctly identifying when it should assign an IRI and when it should not.

$$
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
$$

The **coefficient of variation** (CV) is a statistical measure that represents the ratio of the standard deviation to the mean, usually expressed as a percentage. It is used to assess how much a metric varies depending on the dataset. A higher CV indicates greater relative variability, implying that the metrics for a dataset are more spread out around the mean, while a lower CV suggests more consistency. 

$$
\text{CV} = \frac{\text{Standard deviation}}{Mean} x 100
$$

## Results (4 different approaches)
All the results for each different approach are located in the directory [results](rag/data-ontology/results).
###  RAG performed through OpenAI platform
#### 1 - With only column names 
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.746 |
| Recall     | 0.555 |
| F1-score   | 0.597 |
| Accuracy   | 0.661 |

   </td>
   <td>
    
| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 36.786                   |
| Recall               | 38.033                   |
| F1-score             | 32.289                   |
| Accuracy             | 32.427                   |

   </td>
  </tr>
</table>

* This relatively high CV for the precision suggests that the precision of the model is somewhat inconsistent across different tests. That is, the performance of the model in terms of precision varies considerably.
* The low recall observed indicates that some IRIs are not retrieved by the model, despite having suitable matches within the ontologies used in the RAG process.

#### 2 - Using 10 rows as context (+ column names)
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.764 |
| Recall     | 0.535 |
| F1-score   | 0.613 |
| Accuracy   | 0.667 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 31.016                   |
| Recall               | 33.215                   |
| F1-score             | 29.279                   |
| Accuracy             | 30.292                   |

   </td>
  </tr>
</table>

#### 3 - Description of the CSV file as context (+ column names)
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.650 |
| Recall     | 0.347 |
| F1-score   | 0.433 |
| Accuracy   | 0.505 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 70.252                   |
| Recall               | 94.434                   |
| F1-score             | 87.422                   |
| Accuracy             | 53.149                   |

   </td>
  </tr>
</table>

* As in the case of the column names, the high CV for the precision suggests that the precision of the model is somewhat inconsistent across different tests.

#### 4 - Using 10 rows + CSV file description (+ column names)
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.819 |
| Recall     | 0.556 |
| F1-score   | 0.655 |
| Accuracy   | 0.720 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 8.531                    |
| Recall               | 11.790                   |
| F1-score             |  7.485                   |
| Accuracy             | 14.922                   |

   </td>
  </tr>
</table>

* The precision of each CSV test file is high, indicating that when the model suggests an identifier, it is correct 8 out of 10 times. This reflects a strong ability to avoid false positives.
* However, the low recall percentage reveals that the model struggles to identify all the correct IRIs present in the dataset. This indicates the model misses a significant number of correct IRIs (false negatives).
* This approach results in the lowest CV, indicating that the model demonstrates greater consistency compared to the other approaches.

###  RAG performed through an external vector database
####  1 - Using 10 rows + CSV file description (+ column names)
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.986 |
| Recall     | 0.766 |
| F1-score   | 0.848 |
| Accuracy   | 0.838 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 2.817                    |
| Recall               | 20.906                   |
| F1-score             | 10.933                   |
| Accuracy             | 15.754                   |

   </td>
  </tr>
</table>

* A precision of 0.986 indicates that when the model suggests an IRI for a column name, 98.6% of the suggestions are correct. This exceptionally high precision demonstrates that the model is highly effective at avoiding false positives, almost exclusively proposing correct IRIs.
* A recall of 0.766 means the model correctly identifies 76.6% of the actual matching IRIs. This indicates improved performance in capturing true matches, though some false negatives still persist.
* The F1-score of 0.848, being the harmonic mean of precision and recall, suggests a well-balanced performance that heavily benefits from the high precision while maintaining strong recall.
* An accuracy of 0.838 indicates that 83.8% of all predictions (both identifying correct IRIs and rejecting incorrect ones) are correct. This is a strong indicator of overall performance, showing the model is reliable in the majority of cases.
* The coefficient of variation of the precision is the lowest of all approaches.

### Findings
* The ragged model can assign an adequate IRI to a column name using the classes of the ontologies of interest.
* The search can be limited to only those ontologies included in the RAG process, avoiding the use of other external ontologies.
* The RAG process via OpenAI API seems to underperform when the ontology included in the RAG is large. The larger the ontology, the more difficult it is for the model to interact with it.
* RAG performed through an external vector database using 10 rows from the CSV file along with its description yields the highest precision, recall, and F1-score, making it the most effective of the five methods studied.  Its much higher precision and balanced F1-score make it especially suited for tasks where avoiding false positives is critical. However, its recall, while improved, indicates there is still potential for refinement to ensure fewer correct matches are missed. This approach is much more consistent in precision (lower CV), making it highly reliable for applications where avoiding false positives is crucial. However, the increased variability in recall, F1-score, and slightly in accuracy suggests that while the model performs better overall, its results might fluctuate more depending on the evaluation dataset. These fluctuations are likely tied to the model's difficulty in capturing all true matches (recall).


