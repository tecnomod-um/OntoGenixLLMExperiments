import pandas as pd
from itertools import combinations
from functools import lru_cache

class DependencyAnalyzer:
    def __init__(self, df: pd.DataFrame, max_key_size: int = 2, max_chunk_size: int = None,
                 check_4NF: bool = False, check_5NF: bool = False, check_partitioning: bool = False):
        """
        Initialize the DependencyAnalyzer with a DataFrame and optional max key size.
        """
        self.df = df.copy()  # Make a copy to avoid modifying the original dataframe
        # Functional Dependencies (FD) and Multi-Valued Dependencies (MVD)
        self.max_key_size = min(abs(max_key_size), df.shape[1]-1)  # max_key_size cannot exceed the number of columns-1
        self.fds = {}  # Dictionary to store functional dependencies
        self.mvds = {}  # Dictionary to store multi-valued dependencies
        # Normal Forms (NF)
        self.check_4NF = check_4NF
        self.check_5NF = check_5NF
        self.decomposed_tables = []  # List to store lists of related column names for decomposed tables (for 4NF)
        self.jds = {}  # Dictionary to store join dependencies (for 5NF)
        # Data partitioning
        self.check_partitioning = check_partitioning
        self.chunks = []  # List of chunks or partitions that can be divided the dataframe
        self.max_chunk_size = max_chunk_size or df.shape[1] // 2  # Default to half the number of columns

    ## Helper Methods

    @lru_cache(maxsize=None)
    def generate_column_combinations(self, num_columns):
        """
        Generate combinations of column indices up to max_key_size to save memory.
        """
        column_combinations = []
        for size in range(1, self.max_key_size + 1):
            column_combinations.extend(combinations(range(num_columns), size))
        return column_combinations

    def analyze_dependencies(self, check_4NF: bool = False, check_5NF: bool = False, check_partitioning: bool = False):
        """
        Analyze functional, multi-valued, and join dependencies in the DataFrame.
        """
        # We can choose what should be analyzed here too
        self.check_4NF = self.check_4NF or check_4NF
        self.check_5NF = self.check_5NF or check_5NF
        self.check_partitioning = self.check_partitioning or check_partitioning
        # Analyze dependencies
        self.check_functional_dependencies()
        self.handle_multivalued_dependencies()
        if self.check_4NF:
            self.perform_4nf_decomposition()  # Check for 4NF condition
        if self.check_5NF:
            self.check_join_dependencies()  # Check for 5NF condition
        if self.check_partitioning:
            self.partition_dataset()

    ## FD

    def check_functional_dependencies(self):
        """
        Check for functional dependencies (FDs) between columns in the dataset.
        It evaluates both single columns and composite keys up to a given size.
        Output format example: "{A,B} -> {C} \n {B} -> {D,E} ".
        """
        names_df = self.df.columns.tolist()

        # Generate combinations of column names up to max_key_size
        column_combinations = self.generate_column_combinations(len(names_df))

        # Iterate over all combinations of column sets (composite keys)
        for X_comb in column_combinations:
            X = tuple(names_df[i] for i in X_comb)  # Composite key columns as tuple for caching
            
            # Evaluate functional dependency X -> Y for each column Y not in X
            for Y in names_df:
                if Y in X:
                    continue  # Skip if Y is already in X (no self-dependency)

                # Check if X -> Y (i.e., if X determines Y)
                if self.is_functional_dependency(X, Y):
                    # Add the functional dependency to the dictionary
                    key_str = "{" + ",".join(X) + "}"
                    if key_str not in self.fds:
                        self.fds[key_str] = set()
                    self.fds[key_str].add(Y)

    @lru_cache(maxsize=None)
    def is_functional_dependency(self, X, Y):
        """
        Check if the set of columns X functionally determines column Y.
        """
        # Ensure that all columns in X and Y exist in the DataFrame
        assert all(col in self.df.columns for col in X), f"Some columns in {X} not found in DataFrame!"
        assert Y in self.df.columns, f"Column {Y} not found in DataFrame!"

        # Use groupby to check uniqueness of X -> Y
        grouped = self.df.groupby(list(X))[Y].nunique().reset_index(name='unique_count')

        # Ensure that the number of unique Y values for each group of X is 1
        return grouped['unique_count'].max() == 1

    ## MVD

    def handle_multivalued_dependencies(self):
        """
        Handle Multi-Valued Dependencies (MVDs) to achieve 4NF.
        If an MVD is detected, decompose the table.
        """
        names_df = self.df.columns.tolist()

        # Generate combinations of column names up to max_key_size
        column_combinations = self.generate_column_combinations(len(names_df))

        # Iterate over all combinations of column sets (composite keys)
        for X_comb in column_combinations:
            X = tuple(names_df[i] for i in X_comb)  # Composite key columns as tuple for caching

            # For each possible pair (combination of 2 elements) of columns {Y, Z} not in X
            for Y, Z in combinations([col for col in names_df if col not in X], 2):
                # Directly check if X ->> Y | X ->> Z without caching to avoid overhead
                if self.is_multivalued_dependency(X, Y, Z):
                    # Add the multi-valued dependency to the dictionary
                    key_str = "{" + ",".join(X) + "}"
                    if key_str not in self.mvds:
                        self.mvds[key_str] = set()
                    self.mvds[key_str].add((Y, Z))

    def is_multivalued_dependency(self, X, Y, Z):
        """
        Check if there is a multi-valued dependency (MVD) X ->> {Y, Z}.
        """
        # Ensure that all columns in X, Y, and Z exist in the DataFrame
        assert all(col in self.df.columns for col in X), f"Some columns in {X} not found in DataFrame!"
        assert Y in self.df.columns, f"Column {Y} not found in DataFrame!"
        assert Z in self.df.columns, f"Column {Z} not found in DataFrame!"

        # Use cached groupby results to avoid recomputation
        df_grouped_XY = self.df.groupby(list(X))[Y].nunique().reset_index(name='count_Y')
        df_grouped_XZ = self.df.groupby(list(X))[Z].nunique().reset_index(name='count_Z')

        # Check if the number of unique values of Y for each X is independent of Z
        merged_df = pd.merge(df_grouped_XY, df_grouped_XZ, on=list(X))
        return (merged_df['count_Y'] == 1).all() or (merged_df['count_Z'] == 1).all()

    ## 4NF

    def perform_4nf_decomposition(self):
        """
        Perform 4NF decomposition of the table based on detected MVDs.
        Creates decomposed tables and stores them as lists of related column names.
        """
        for key_str, mvd_pairs in self.mvds.items():
            determinants = key_str.strip("{}").split(",")

            for (Y, Z) in mvd_pairs:
                # Decompose into two related column lists:
                # Table 1: Determinants + Y
                table_1_columns = determinants + [Y]

                # Table 2: Determinants + Z
                table_2_columns = determinants + [Z]

                # Store decomposed column lists
                self.decomposed_tables.append((table_1_columns, table_2_columns))

    ## 5NF

    def check_join_dependencies(self):
        """
        Check for Join Dependencies (JD) to determine 5NF.
        If a JD is detected, suggest a decomposition.
        """
        names_df = self.df.columns.tolist()

        # Generate combinations of column names up to max_key_size
        column_combinations = self.generate_column_combinations(len(names_df))

        # Iterate over all combinations of column sets (composite keys)
        for X_comb in column_combinations:
            X = tuple(names_df[i] for i in X_comb)  # Composite key columns as tuple for caching

            # For each possible pair (combination of 2 elements) of columns {Y, Z} not in X
            for Y_comb in combinations([col for col in names_df if col not in X], 2):
                Y = list(Y_comb)
                # Directly check join dependencies without caching to avoid overhead
                if self.is_join_dependency(X, tuple(Y)):
                    # Add the join dependency to the dictionary
                    key_str = "{" + ",".join(X) + "}"
                    if key_str not in self.jds:
                        self.jds[key_str] = set()
                    self.jds[key_str].add(tuple(Y))

    def is_join_dependency(self, X, Y):
        """
        Check if there is a Join Dependency (JD) for the given columns X and Y.
        A JD X * Y means the original table can be reconstructed by joining X and Y.
        """
        # Ensure that all columns in X and Y exist in the DataFrame
        assert all(col in self.df.columns for col in X), f"Some columns in {X} not found in DataFrame!"
        assert all(col in self.df.columns for col in Y), f"Some columns in {Y} not found in DataFrame!"

        # Decompose into two projections
        df_proj_X = self.df[list(X)].drop_duplicates()
        df_proj_Y = self.df[list(Y)].drop_duplicates()

        # Determine common columns between the two projections
        common_columns = list(set(X) & set(Y))

        # If no common columns, we cannot perform a natural join that reconstructs the original table
        if not common_columns:
            return False

        # Perform natural join on common columns
        joined_df = pd.merge(df_proj_X, df_proj_Y, on=common_columns, how='inner')

        # Check if the join covers the original table without adding spurious tuples
        original_projection = self.df[list(X) + [col for col in list(Y) if col not in X]].drop_duplicates()
        return joined_df.shape[0] == original_projection.shape[0] and all((joined_df.values == original_projection.values).all(axis=1))

    ## Chunk Partitioning Method

    def partition_dataset(self, sort_columns: bool = True):
        """
        Partition the dataset into chunks based on detected dependencies.
        This method uses a heuristic approach to determine optimal partitions.
        """
        # Initialize the list of chunks
        chunks: list = []

        # Get the list of strong determinants from FDs
        strong_determinants = {key: values for key, values in self.fds.items() if len(values) > 1}

        # Start partitioning based on strong determinants
        for determinant, dependents in strong_determinants.items():
            determinant_columns = determinant.strip("{}").split(",")
            chunk_columns = set(determinant_columns).union(dependents)
            
            # Avoid creating chunks that exceed the maximum chunk size
            if len(chunk_columns) <= self.max_chunk_size:
                chunks.append(list(chunk_columns))

        # Handle remaining columns not covered by strong determinants
        remaining_columns = set(self.df.columns) - set(col for chunk in chunks for col in chunk)
        if remaining_columns:
            chunks.append(list(remaining_columns))

        if sort_columns:
            # Sort each chunk in the order of the original DataFrame columns
            chunks = [
                sorted(chunk, key=lambda col: self.df.columns.get_loc(col))
                for chunk in chunks
            ]
        # Update the list of chunks
        self.chunks = chunks
        # Return the sorted list of chunks
        return chunks

    ## Pretty printing functions

    def pretty_print_fds(self):
        """
        Pretty print the list of functional dependencies.
        """
        if not self.fds:
            print("[FD] No functional dependencies found.")
        else:
            print("\n[FD] Functional Dependencies:")
            for key, values in self.fds.items():
                print(f"\t{key} -> {{{','.join(values)}}}")

    def pretty_print_mvds(self):
        """
        Pretty print the list of multi-valued dependencies (MVDs).
        """
        if not self.mvds:
            print("[MVD] No multi-valued dependencies found.")
        else:
            print("\n[MVD] Multi-Valued Dependencies:")
            for key, values in self.mvds.items():
                for (Y, Z) in values:
                    print(f"\t{key} ->> {{{Y},{Z}}}")

    def pretty_print_decomposed_tables(self):
        """
        Pretty print the decomposed tables resulting from MVDs.
        """
        if not self.decomposed_tables:
            print("[4NF] No decomposed tables found.")
        else:
            print("\n[4NF] Decomposed Tables:")
            for idx, (table1, table2) in enumerate(self.decomposed_tables, 1):
                print(f"* Decomposition {idx}:")
                print("\tTable 1 columns:", table1)
                print("\tTable 2 columns:", table2)

    def pretty_print_jds(self):
        """
        Pretty print the list of join dependencies (JDs) for 5NF.
        """
        if not self.jds:
            print("[5NF] No join dependencies found.")
        else:
            print("\n[5NF] Join Dependencies (JDs):")
            for key, values in self.jds.items():
                for Y in values:
                    print(f"\t{key} * {{{','.join(Y)}}}")

    def pretty_print_partitions(self):
        """
        Pretty print the list of partitions (chunks) resulting from partition_dataset.
        """
        if not self.chunks:
            print("[Chunks] No partitions found.")
        else:
            print("\n[Chunks] Optimal Partitions:")
            for i, chunk in enumerate(self.chunks, 1):
                print(f"\tChunk {i}: {chunk}")

    def pretty_print(self):
        """
        Print the results of FDs, MVDs, JDs, and decomposed tables in a readable format.
        """
        self.pretty_print_fds()
        self.pretty_print_mvds()
        if self.check_4NF:
            self.pretty_print_decomposed_tables()
        if self.check_5NF:
            self.pretty_print_jds()
        if self.check_partitioning:
            self.pretty_print_partitions()

from time import time
if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv('C:/Users/Dragg/Documents/Tecnomod/Code Gines/AmazonRating_data20k2.csv') # eC_processed_data
    
    ###### RUNTIME ###
    ini = time()

    analyzer = DependencyAnalyzer(df, max_key_size=4, check_4NF=True, check_5NF=True, check_partitioning=True)
    analyzer.analyze_dependencies()
    
    ###### RUNTIME ###
    print(time()-ini)

    analyzer.pretty_print()


