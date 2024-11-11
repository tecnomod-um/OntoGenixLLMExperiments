# RAG experiments for matching data to ontologies

## Objective
 
Explore the capabilities of an RAG process using ontologies of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform a CSV-Ontology Alignment, which involves providing the model with the ontologies to be used and attempting to find in those ontologies a class that matches each of the column names in the CSV file.

## The content of the RAG

In this experiment, the RAG consisted of the following ontologies:
* AFO ontology: The AFO is an ontology suite that provides a standard vocabulary and semantic model for the representation of laboratory analytical processes. 
* Country ontology (made by me): Describes the demographics, economics, and geography of a country.
* CHEMINF ontology: The chemical information ontology (cheminf) describes information entities about chemical entities. It provides qualitative and quantitative attributes to richly describe chemicals.

## GPT models
As in the other experiment, the RAG process is performed through an **assistant agent**. Assistants can call OpenAI’s models with specific instructions to tune their personality and capabilities and can also access multiple tools in parallel, like the File Search tool. The **File Search tool** augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users.

In this case, the assistant used the **GPT-4o model** and the previous three mentioned ontologies will be provided for the alignment task. So, when the model is asked to assign an IRI class to a column name of a CSV file, it will consult the ontologies previously included in a vector store.

<p align="center">
<img width="586" alt="image" src="https://github.com/user-attachments/assets/f2a677f1-60d4-435a-bd24-9f23edd66de9" />
</p>

### Evaluation of the RAG models
To evaluate the performance of the RAG models in the task of matching data to ontologies, four CSV files have been used. We classified the model predictions as:
* True Positives (TP): When the model proposes a correct IRI for the column name.
* False Positives (FP): When the model proposes an incorrect IRI for the column name.
* True Negatives (TN): When the model indicates that an adequate IRI does not exist and it is true.
* False Negatives (FN): When the model indicates that an adequate IRI does not exist and it is not true.
#### Metrics 
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

### Results
#### With only column names 
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.746 |
| Recall     | 0.555 |
| F1-score   | 0.597 |

   </td>
   <td>
    
| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 36.786                   |
| Recall               | 38.033                   |
| F1-score             | 32.289                   |

   </td>
  </tr>
</table>

* This relatively high coefficient of variation for the precision suggests that the precision of the model is somewhat inconsistent across different tests. THat is, the performance of the model in terms of precision varies considerably.
* The low recall observed indicates that some IRIs are not retrieved by the model, despite having suitable matches within the ontologies used in the RAG process.

#### Using 10 rows as context
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.764 |
| Recall     | 0.535 |
| F1-score   | 0.613 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 31.016                   |
| Recall               | 33.215                   |
| F1-score             | 29.279                   |

   </td>
  </tr>
</table>

#### Description of the CSV file as context
<table>
  <tr>
    <td>
     
| Metric     | Mean |
|------------|-------|
| Precision  | 0.650 |
| Recall     | 0.347 |
| F1-score   | 0.433 |

   </td>
   <td>

| Metric               | Coefficient of Variation |
|----------------------|--------------------------|
| Precision            | 70.252                   |
| Recall               | 94.434                   |
| F1-score             | 87.422                   |

   </td>
  </tr>
</table>

* As in the case of the column names, the high coefficient of variation for the precision suggests that the precision of the model is somewhat inconsistent across different tests.

### Findings
* The ragged model can assign an adequate IRI to a column name using the classes of the ontologies of interest.
* The search can be limited to only those ontologies included in the RAG process, avoiding the use of other external ontologies.
* The RAG process via OpenAI API seems to underperform when the ontology included in the RAG is large. The larger the ontology, the more difficult it is for the model to interact with it.
* Using 10 rows from the CSV file yields the highest precision and F1-score, making it the most effective of the three methods studied. However, the improvement achieved by the rows approach is modest and the coefficient of variation also remains high.


