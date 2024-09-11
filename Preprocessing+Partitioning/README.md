# TODO: Document and explain the code
In this file I'll try to deeepen in and tackle all the topics related to the current preprocessing and partitioning steps of the 
OntoGenix pipeline/workflow.

# 0. Introduction/Abstract
This briefing section is needed for people who suffer from "tldr;" condition and want the conclusions before even started reading it. 
So, in conclusion, all the code implemented in this folder helps us have a better understandment of how the data behave and is related 
without a prior knowledge of the area that the data is modeling. In other words, and thanks to human+LLM work, we're now able to provide 
an efficient and improved way to tackle larger datasets so that we can provide to the LLM with more specific information to tackle the 
ontology creation problem. 

To help us achieve this efficiency we had use Machine Learning (ML) and statistical approaches, such as "Domain Knowledge and Practical 
constraints", while some known methods like Clustering-based K-means were discarted for its time and resource cosumption. These methods
helped us find herustics to determine what rows of the dataset were really relevant for the later study of the data. Doing so, we reduce
larger datasets, i.e. half million rows with multiple columns, into more manageable smaller datasets without too much information loss.

# 1. Preprocessing (niy: not implemented yet)
Basically, treating all data as characters (or strings) and converting them to factors (or numbers). After that, we eliminated the 
duplicated rows and (optionaly) removed the rows that contained null data (NA). However, it's possible to not do so if we know beforehand
that NAs have indeed a meaning while interpreting the data. Doing so helped us reduce the size of the dataset by removing redundant data.

[...]

# 2. Cardinality matrix (doc)
In this section we're going to explain the methodology followed to determine the relationships between columns of a dataset and the 
cardinality of that relationship. However, right now, the results are experimental and maybe not all the cases can be represented here.

The used methodolgy in this step is treating two columns of the dataset `A` and `B` where we'll somehow transform these columns to 
mathematical sets and study its possible relationships. In order to do so, we study if they follow the definition of function or not,
in the following way:

<p align="center" width="100%" onclick="href=https://en.wikipedia.org/wiki/Bijection,_injection_and_surjection">
  <img width="33%" src="https://github.com/user-attachments/assets/be552db3-f263-4460-9703-05e25780502f" 
    alt="classes of functions distinguished by the manner in which arguments and images are related or mapped to each other">
</p>

<p align="center" width="100%">
![https://www.mathsisfun.com/sets/injective-surjective-bijective.html](https://github.com/user-attachments/assets/9d537924-5dcd-4bd6-a054-50c2ce34d536){ width="800" height="600" style="display: block; margin: 0 auto" }
</p>

As we can see, there's 4 cases where the relation `A -> B` can be a function and 1 where it's not a function. Among these cases, we
also study the data, i.e. if it contains duplicates, if it contains NAs, etc. Taking that into account, we show, as an example, the
resulting `cardinality matrix` for the "processed eCommerce dataset":

|FIELD      |InvoiceNo|StockCode|Description|Quantity|InvoiceDate|UnitPrice|CustomerID|Country|
|-----------|---------|---------|-----------|--------|-----------|---------|----------|-------|
|InvoiceNo  |-        |1:N      |1:N        |1:N     |1:N        |1:N      |M:1       |M:1    |
|StockCode  |0:N      |-        |0:N        |0:N     |0:N        |0:N      |0:N       |0:N    |
|Description|0:N      |0:N      |-          |0:N     |0:N        |0:N      |0:N       |0:N    |
|Quantity   |0:N      |0:N      |0:N        |-       |0:N        |0:N      |0:N       |0:N    |
|InvoiceDate|0:N      |0:N      |0:N        |0:N     |-          |0:N      |0:N       |0:N    |
|UnitPrice  |0:N      |0:N      |0:N        |0:N     |0:N        |-        |0:N       |0:N    |
|CustomerID |0:N      |0:N      |0:N        |0:N     |0:N        |0:N      |-         |0:N    |
|Country    |0:N      |0:N      |0:N        |0:N     |0:N        |0:N      |0:N       |-      |

The previous table result came from transforming the studied conditions of the `A -> B` relationships. The expanded table from which the 
`cardinality matrix` came is the following:

|FIELD      |IndexA|IndexB|ColumnA|ColumnB|Not a Function (N)|General Function (G)|Injective (I)|Surjective (S)|Bijective (B)|Cardinality (C)|
|-----------|------|------|-------|-------|------------------|--------------------|-------------|--------------|-------------|---------------|
|0          |0     |0     |InvoiceNo|InvoiceNo|False             |False               |False        |False         |False        |-              |
|1          |0     |1     |InvoiceNo|StockCode|True              |False               |False        |False         |False        |1:N            |
|2          |0     |2     |InvoiceNo|Description|True              |False               |False        |False         |False        |1:N            |
|3          |0     |3     |InvoiceNo|Quantity|True              |False               |False        |False         |False        |1:N            |
|4          |0     |4     |InvoiceNo|InvoiceDate|True              |False               |False        |False         |False        |1:N            |
|5          |0     |5     |InvoiceNo|UnitPrice|True              |False               |False        |False         |False        |1:N            |
|6          |0     |6     |InvoiceNo|CustomerID|False             |False               |False        |True          |False        |M:1            |
|7          |0     |7     |InvoiceNo|Country|False             |False               |False        |True          |False        |M:1            |
|8          |1     |0     |StockCode|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|9          |1     |1     |StockCode|StockCode|False             |False               |False        |False         |False        |-              |
|10         |1     |2     |StockCode|Description|True              |False               |False        |False         |False        |0:N            |
|11         |1     |3     |StockCode|Quantity|True              |False               |False        |False         |False        |0:N            |
|12         |1     |4     |StockCode|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|13         |1     |5     |StockCode|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|14         |1     |6     |StockCode|CustomerID|True              |False               |False        |False         |False        |0:N            |
|15         |1     |7     |StockCode|Country|True              |False               |False        |False         |False        |0:N            |
|16         |2     |0     |Description|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|17         |2     |1     |Description|StockCode|True              |False               |False        |False         |False        |0:N            |
|18         |2     |2     |Description|Description|False             |False               |False        |False         |False        |-              |
|19         |2     |3     |Description|Quantity|True              |False               |False        |False         |False        |0:N            |
|20         |2     |4     |Description|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|21         |2     |5     |Description|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|22         |2     |6     |Description|CustomerID|True              |False               |False        |False         |False        |0:N            |
|23         |2     |7     |Description|Country|True              |False               |False        |False         |False        |0:N            |
|24         |3     |0     |Quantity|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|25         |3     |1     |Quantity|StockCode|True              |False               |False        |False         |False        |0:N            |
|26         |3     |2     |Quantity|Description|True              |False               |False        |False         |False        |0:N            |
|27         |3     |3     |Quantity|Quantity|False             |False               |False        |False         |False        |-              |
|28         |3     |4     |Quantity|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|29         |3     |5     |Quantity|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|30         |3     |6     |Quantity|CustomerID|True              |False               |False        |False         |False        |0:N            |
|31         |3     |7     |Quantity|Country|True              |False               |False        |False         |False        |0:N            |
|32         |4     |0     |InvoiceDate|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|33         |4     |1     |InvoiceDate|StockCode|True              |False               |False        |False         |False        |0:N            |
|34         |4     |2     |InvoiceDate|Description|True              |False               |False        |False         |False        |0:N            |
|35         |4     |3     |InvoiceDate|Quantity|True              |False               |False        |False         |False        |0:N            |
|36         |4     |4     |InvoiceDate|InvoiceDate|False             |False               |False        |False         |False        |-              |
|37         |4     |5     |InvoiceDate|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|38         |4     |6     |InvoiceDate|CustomerID|True              |False               |False        |False         |False        |0:N            |
|39         |4     |7     |InvoiceDate|Country|True              |False               |False        |False         |False        |0:N            |
|40         |5     |0     |UnitPrice|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|41         |5     |1     |UnitPrice|StockCode|True              |False               |False        |False         |False        |0:N            |
|42         |5     |2     |UnitPrice|Description|True              |False               |False        |False         |False        |0:N            |
|43         |5     |3     |UnitPrice|Quantity|True              |False               |False        |False         |False        |0:N            |
|44         |5     |4     |UnitPrice|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|45         |5     |5     |UnitPrice|UnitPrice|False             |False               |False        |False         |False        |-              |
|46         |5     |6     |UnitPrice|CustomerID|True              |False               |False        |False         |False        |0:N            |
|47         |5     |7     |UnitPrice|Country|True              |False               |False        |False         |False        |0:N            |
|48         |6     |0     |CustomerID|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|49         |6     |1     |CustomerID|StockCode|True              |False               |False        |False         |False        |0:N            |
|50         |6     |2     |CustomerID|Description|True              |False               |False        |False         |False        |0:N            |
|51         |6     |3     |CustomerID|Quantity|True              |False               |False        |False         |False        |0:N            |
|52         |6     |4     |CustomerID|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|53         |6     |5     |CustomerID|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|54         |6     |6     |CustomerID|CustomerID|False             |False               |False        |False         |False        |-              |
|55         |6     |7     |CustomerID|Country|True              |False               |False        |False         |False        |0:N            |
|56         |7     |0     |Country|InvoiceNo|True              |False               |False        |False         |False        |0:N            |
|57         |7     |1     |Country|StockCode|True              |False               |False        |False         |False        |0:N            |
|58         |7     |2     |Country|Description|True              |False               |False        |False         |False        |0:N            |
|59         |7     |3     |Country|Quantity|True              |False               |False        |False         |False        |0:N            |
|60         |7     |4     |Country|InvoiceDate|True              |False               |False        |False         |False        |0:N            |
|61         |7     |5     |Country|UnitPrice|True              |False               |False        |False         |False        |0:N            |
|62         |7     |6     |Country|CustomerID|True              |False               |False        |False         |False        |0:N            |
|63         |7     |7     |Country|Country|False             |False               |False        |False         |False        |-              |

As we can see, we can easily observe what case is found in each `A -> B` relationship. If the reader wants to deepen in all the current studied
cases, they can be seen in the current [code](https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/edit/main/Preprocessing%2BPartitioning/csv_matrix_analysis.py).

# 3. Feature vector (doc)

# 4. Functional Dependencies (doc)

# 5. Final conclusions (and future work?)

# 6. NOTES
1. CSV to Markdown table converter: https://www.convertcsv.com/csv-to-markdown.htm
