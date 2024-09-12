# TODO: Document and explain the code
In this file I'll try to deeepen in and tackle all the topics related to the current preprocessing and partitioning steps of the 
OntoGenix pipeline/workflow.

# 0. Introduction/Abstract
This briefing section is needed for people who suffer from `tldr;` condition and want the conclusions before even started reading it. 
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

# 2. Cardinality matrix
In this section we're going to explain the methodology followed to determine the relationships between columns of a dataset and the 
cardinality of that relationship. However, right now, the results are experimental and maybe not all the cases can be represented here.

The used methodolgy in this step is treating two columns of the dataset `A` and `B` where we'll somehow transform these columns to 
mathematical sets and study its possible relationships. In order to do so, we study if they follow the definition of function or not,
in the following way:

<p align="center" width="100%" onclick="window.location.href=https://en.wikipedia.org/wiki/Bijection,_injection_and_surjection">
  <img width="auto" src="https://github.com/user-attachments/assets/be552db3-f263-4460-9703-05e25780502f" 
    alt="Classes of functions distinguished by the manner in which arguments and images are related or mapped to each other">
</p>


<p align="center" width="100%" onclick="window.location.href=https://www.mathsisfun.com/sets/injective-surjective-bijective.html">
  <img width="auto" src="https://github.com/user-attachments/assets/9d537924-5dcd-4bd6-a054-50c2ce34d536" 
    alt="'Injective, Surjective and Bijective' tells us about how a function behaves. A function is a way of matching the members of a set 'A' to a set 'B'">
</p>

As we can see, there's 4 cases where the relation `A -> B` can be a function and 1 where it's not a function. Among these cases, we
also study the data, i.e. if it contains duplicates, if it contains NAs, etc. Taking that into account, we show, as an example, the
resulting `cardinality matrix` (8x8) for the ["processed eCommerce dataset"](https://github.com/jesualdotomasfernandezbreis/KGCF/blob/main/files/sources/eCommerce/processed_data.csv):

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

The previous table result came from transforming the studied conditions of the `A -> B` relationships. Note that the relationships are not 
bidirectional. Thus, another processing step may be required to infer a more ER Model alike cardinality matrix, so the LLM may allucinate less.

This information is extracted form a expanded table where all the mathematical definition of `function` and its classes are studied. The 
expanded table (8x64) from which the `cardinality matrix` came is the following:

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

NOTE: it took `4.1982338428497314 seconds` to execute the script.

# 3. Feature vector (doc)
In this section we're going to explain the methodology followed to determine the inferred datatypes of the dataset's columns and maybe
some other statistical information about the data distribution. However, right now, the results are experimental and not all the types 
may be represented here.

The used methodolgy in this step is reading through the dataset's elements of each column and try to infer the more alike type for each
element. After that, we sort the results following a ranking method (yet to determine) and we expain the type of data of that column with
the best found datatype (for that column).

## Feature Vector Example:
Here we have the resulting `feature vector (FV)` table for the `ratings_Beauty.csv` (4 x 2023070) dataset:

|FIELD      |XsdDataTypes|Total|NoNull|Unique|
|-----------|------------|-----|------|------|
|UserId     |xsd:string  |2023070|2023070|1210271|
|ProductId  |xsd:string  |2023070|2023070|249274|
|Rating     |xsd:integer |2023070|2023070|5     |
|Timestamp  |xsd:integer |2023070|2023070|4231  |

This result come from the following resulting analysis dictionary, where we only take the most likely datatype as the result 
(however, some hierachy between datatypes may be needed to have better inferred and more descriptive datatypes):
```json
"Feature Vector": {
    "UserId": {
      "xsd:string": 2022969,
      "xsd:hexBinary": 88,
      "xsd:dateTime": 13
    },
    "ProductId": {
      "xsd:string": 2001981,
      "xsd:hexBinary": 19062,
      "xsd:integer": 2027
    },
    "Rating": {
      "xsd:integer": 2023070
    },
    "Timestamp": {
      "xsd:integer": 2023070
    }
  }
```

NOTE: This dataset took `88.04153227806091 seconds` to execute. Smaller dataset may take lesser time.


## NOTES:
All the information and REGEX about the FV's inferred types come from the following URLs:
  - XSD Primitive datatypes: https://www.w3.org/TR/xmlschema11-2/#built-in-primitive-datatypes
  - Valid Any URI: https://www.w3.org/2011/04/XMLSchema/TypeLibrary-IRI-RFC3987.xsd
  - IANA URI Schemes (Permanent ones only): https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml

Standards to be followed in order to have more FAIR alike data:
  - ISO 11179-5: https://en.wikipedia.org/wiki/Data_element_name
  - ISO 8601: https://es.wikipedia.org/wiki/ISO_8601
  - RFC 3987 (IRI): https://www.ietf.org/rfc/rfc3987.txt

Some considerations to take into account while formatting the data:
  - No white space (at the beginning or end). Thus, use `strip()`
  - The decimal separator in numbers must be `.`
  - The date separator may be `-`, but the `/` seperator is allowed if the `strict` case flag is not set.
  - The time sepator must be `:`.

Full Python dictionary:
```python
  xsd_type_dict = {
      # Booleans
          "xsd:boolean":  REGEX_XSD_BOOLEAN, # `boolean` represents the values of two-valued logic.
      # Numeric values
          "xsd:integer":  REGEX_XSD_INTEGER, # `integer` is ·derived· from decimal by fixing the value of ·fractionDigits· to be 0 and disallowing the trailing decimal point. This results in the standard mathematical concept of the integer numbers.  The ·value space· of integer is the infinite set {...,-2,-1,0,1,2,...}. The ·base type· of integer is decimal.
          "xsd:decimal":  REGEX_XSD_DECIMAL, # `decimal` represents a subset of the real numbers, which can be represented by decimal numerals. The ·value space· of decimal is the set of numbers that can be obtained by dividing an integer by a non-negative power of ten, i.e., expressible as i / 10n where i and n are integers and n ≥ 0. Precision is not reflected in this value space; the number 2.0 is not distinct from the number 2.00. The order relation on decimal is the order relation on real numbers, restricted to this subset.
          "xsd:float":    REGEX_XSD_FLOAT, # The `float` datatype is patterned after the IEEE single-precision 32-bit floating point datatype [IEEE 754-2008]. Its value space is a subset of the rational numbers. Floating point numbers are often used to approximate arbitrary real numbers.
          "xsd:double":   REGEX_XSD_DOUBLE, # The `double` datatype is patterned after the IEEE double-precision 64-bit floating point datatype [IEEE 754-2008]. Each floating point datatype has a value space that is a subset of the rational numbers.  Floating point numbers are often used to approximate arbitrary real numbers.
      # Dates, times, and durations. According to the Seven-property Model: https://www.w3.org/TR/xmlschema11-2/#theSevenPropertyModel
          "xsd:date": REGEX_XSD_DATE, # `date` represents top-open intervals of exactly one day in length on the timelines of dateTime, beginning on the beginning moment of each day, up to but not including the beginning moment of the next day). For non-timezoned values, the top-open intervals disjointly cover the non-timezoned timeline, one per day.  For timezoned values, the intervals begin at every minute and therefore overlap.
          "xsd:time": REGEX_XSD_TIME, # `time` represents instants of time that recur at the same point in each calendar day, or that occur in some arbitrary calendar day.
          "xsd:dateTime": REGEX_XSD_DATETIME, # `dateTime` represents instants of time, optionally marked with a particular time zone offset.  Values representing the same instant but having different time zone offsets are equal but not identical.
          "xsd:dateTimeStamp": REGEX_XSD_DATETIMESTAMP, # The `dateTimeStamp` datatype is ·derived· from dateTime by giving the value required to its explicitTimezone facet. The result is that all values of dateTimeStamp are required to have explicit time zone offsets and the datatype is totally ordered.
          "xsd:duration": REGEX_XSD_DURATION, # `duration` is a datatype that represents durations of time. The concept of duration being captured is drawn from those of [ISO 8601], specifically durations without fixed endpoints. For example, "15 days" (whose most common lexical representation in duration is "'P15D'") is a duration value; "15 days beginning 12 July 1995" and "15 days ending 12 July 1995" are not duration values. duration can provide addition and subtraction operations between duration values and between duration/dateTime value pairs, and can be the result of subtracting dateTime values. However, only addition to dateTime is required for XML Schema processing and is defined in the function ·dateTimePlusDuration·.
          "xsd:gYear": REGEX_XSD_GYEAR, # `gYear` represents Gregorian calendar years.
          "xsd:gMonth": REGEX_XSD_GMONTH, # `gMonth` represents whole (Gregorian) months within an arbitrary year—months that recur at the same point in each year. It might be used, for example, to say what month annual Thanksgiving celebrations fall in different countries (--11 in the United States, --10 in Canada, and possibly other months in other countries).
          "xsd:gDay": REGEX_XSD_GDAY, # `gDay` represents whole days within an arbitrary month—days that recur at the same point in each (Gregorian) month. This datatype is used to represent a specific day of the month. To indicate, for example, that an employee gets a paycheck on the 15th of each month. (Obviously, days beyond 28 cannot occur in all months; they are nonetheless permitted, up to 31.)
          "xsd:gYearMonth": REGEX_XSD_GYEARMONTH, # `gYearMonth` represents specific whole Gregorian months in specific Gregorian years.
          "xsd:gMonthDay": REGEX_XSD_GMONTHDAY, # `gMonthDay` represents whole calendar days that recur at the same point in each calendar year, or that occur in some arbitrary calendar year. (Obviously, days beyond 28 cannot occur in all Februaries; 29 is nonetheless permitted.)
      # Binaries
          "xsd:hexBinary": REGEX_XSD_HEXBINARY, # `hexBinary` represents arbitrary hex-encoded binary data.
          "xsd:base64Binary": REGEX_XSD_BASE64BINARY, # `base64Binary` represents arbitrary Base64-encoded binary data. For base64Binary data the entire binary stream is encoded using the Base64 Encoding defined in [RFC 3548], which is derived from the encoding described in [RFC 2045].
      # Text based
          "xsd:anyURI": REGEX_XSD_ANYURI, # `anyURI` represents an Internationalized Resource Identifier Reference (IRI). An anyURI value can be absolute or relative, and may have an optional fragment identifier (i.e., it may be an IRI Reference). This type should be used when the value fulfills the role of an IRI, as defined in [RFC 3987] or its successor(s) in the IETF Standards Track.
  }
```

Other URLS:
    - TODO: Check other date formats: https://en.wikipedia.org/wiki/List_of_date_formats_by_country
    - TODO: Regex verbose: https://docs.python.org/3/howto/regex.html#:~:text=For%20example%2C%20here%E2%80%99s%20a%20RE%20that%20uses%20re.VERBOSE%3B%20see%20how%20much%20easier%20it%20is%20to%20read%3F


# 4. Functional Dependencies (doc)
In this section we're going to explain the methodology followed to determine the relationships between columns of a dataset and the 
functional dependencies between them. However, right now, the results are experimental and maybe not all the cases can be represented.

The used methodology in this step is studying mathematically, and with already existing algorithms, when exists between two columns `A` and `B`
a Functional Dependency (`FD`) or a Multi-Valued Dependency (`MVD`). This can be represented the following way: `A -> B` and `A ->> B`, respectively. 

Knowing the functional dependencies of the columns in the dataset we can now study the relational database normal forms ([NF](https://www.bkent.net/Doc/simple5.htm)).
This methodology follows the [normalization theory in databases](http://www.inf-cr.uclm.es/www/fruiz/bda/doc/teo/bda-t71.pdf). In this theory, we study the fourth
and fifth normal forms (`4NF` and `5NF`) that states if the relation between two columns `A` and `B` can be represented in a similar way as in relational databases.

[...]

Using all the previous information we can create a criterion to separate large datasets into smaller more digestive datasets. This is good for us, so we can create,
in the case of OntoGenx, create smaller ontologies and then its triplets, where we can join those triplets in a common node with the same ID of the smaller datasets.

Now we'll so an example of output for the `AmazonRatings_20k.csv` dataset. This dataset in particular doesn't have any NA value, thus making it easier to process:
```txt
[FD] Functional Dependencies:
        {UserId,ProductId} -> {Rating,Timestamp}

[MVD] Multi-Valued Dependencies:
        {UserId,ProductId} ->> {Rating,Timestamp}

[4NF] Decomposed Tables:
* Decomposition 1:
        Table 1 columns: ['UserId', 'ProductId', 'Rating']
        Table 2 columns: ['UserId', 'ProductId', 'Timestamp']
[5NF] No join dependencies found.

[Chunks] Optimal Partitions:
        Chunk 1: ['UserId', 'ProductId', 'Rating', 'Timestamp']
```
NOTE: The execution of this code took `0.887751579284668 seconds` with a dataset of size 4x20000.

As we can see, we find that both an FD and a MVD exist with the determinant `{UserId,ProductId}` and the implicants `{Rating,Timestamp}`. From that information we
can infer that the determinant could make a great primary key (PK) when trying to access any row of the dataset. 

However, this is just for this particular dataset. It could also happen that an user may purchase again a product so, while the rating and the timestamp may differ, 
the PK would not be valid. For those cases, we propose the use of a new column `FAIR_URI` which will undoubtly identify the instace/row of the dataset we are
trying to access.


# 5. ER Model
The main goal is using all the 3 previous matrixes to summarize the dataset and pass that information to the LLM. With that information and some prompt engineering 
we aim for building a relational database [ER Model](https://www.visual-paradigm.com/VPGallery/datamodeling/EntityRelationshipDiagram.html) alike format:


<p align="center" width="100%" onclick="window.location.href=https://nulab.com/learn/software-development/er-diagrams-vs-eer-diagrams-whats-the-difference/">
  <img width="auto" src="https://github.com/user-attachments/assets/a4ca81f8-808a-4d21-9743-ddadcd5ee48d" 
    alt="Example of ER Model">
</p>


This is because LLM are more prepared and better trained with format that strictly follows the industry standards, such as UML. In particular, we are going to use
the [PlantUML standard](https://plantuml.com/stdlib). Some example of this is the following diagram:

<p align="center" width="100%" onclick="window.location.href=https://www.planttext.com/?text=XP6nJiCm48RtUufJ9YZom5enj6e7AZ5LICnMScfEjUyYdzCA0U-EGn9GfGARV_dpzv_jbMMVSXy3W1rPCAaHGEOS2FSKV6OLQxapTBW9tWotx0_9Hm2entoc45WE-0Q8Tpl9-CBIwDc6U59ky4dhutDBMzLqSmiVyy5rLveZIPxoe_QbUrnlDCPUvZGAvxwY0VXkVNXtPK_SZsw9EsafSVPIqnLmSl-7VOtp2rJTLxXmVUUmYbvUgsd2vU3kr7XujJ_euGgNBAn8cl8Bdm00">
  <img width="auto" src="https://github.com/user-attachments/assets/367d9f1d-8470-440d-aeba-d8a5e7aa3616" 
    alt="Example of PlantUML Class diagram">
</p>


Which come from the following PlantUML text:

```
@startuml

skin rose

title Relationships - Class Diagram


class Dwelling {
  +Int Windows
  +void LockTheDoor()
}

class Apartment
class House
class Commune
class Window
class Door

Dwelling <|-down- Apartment: Inheritance
Dwelling <|-down- Commune: Inheritance
Dwelling <|-down- House: Inheritance
Dwelling "1" *-up- "many" Window: Composition
Dwelling "1" *-up- "many" Door: Composition

@enduml
```

From this point, we transform the UML text formatted diagram into a ontology through prompt engineering using our chosen LLM. 


# 6. Final conclusions (and future work?)
[...]


# 7. NOTES (Tools)
1. CSV to Markdown table converter: https://www.convertcsv.com/csv-to-markdown.htm
2. PlantUML online diagram viewer: https://www.planttext.com/
