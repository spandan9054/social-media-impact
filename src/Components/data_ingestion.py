import pandas as pd
from src.exception import CustomException
import sys
from src.logger import logging
from sklearn.model_selection import train_test_split


class Data:

    @staticmethod
    def load_data(file_path):
        """
        Loads the dataset, removes unnecessary columns,
        separates features (X) and target (y), and returns them.
        """

        logging.info("Data loading started")

        try:
            df = pd.read_csv(file_path)

            # Dropping the index column
            df = df.drop(columns='Student_ID')

            logging.info("Data loaded successfully")

            # Separating input features and target
            X = df.drop(columns='Overall_Impact')
            y = df['Overall_Impact']

            return X, y

        except Exception as e:
            raise CustomException(e, sys)


class SplitData:

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def split_data(self):
        """
        Splits the dataset into training and testing sets.
        Stratification is used to preserve the class distribution.
        """

        try:
            logging.info("Train test split occurred...")

            X_train, X_test, y_train, y_test = train_test_split(
                self.X,
                self.y,
                test_size=0.2,
                random_state=42,
                stratify=self.y
            )

            logging.info("Train test split completed successfully")

            return X_train, X_test, y_train, y_test

        except Exception as e:
            raise CustomException(e, sys)


"""
CORRECTIONS MADE:
1. Converted Data.load_data() into a @staticmethod because it is
    called as Data.load_data() without creating a Data object.

2. Removed the unnecessary __init__() from the Data class.

3. Kept SplitData as an instance class because it receives X and y
    through its constructor.

4. Kept stratified train-test splitting to preserve the distribution
    of Beneficial, Neutral, and Negative classes.

5. Added logging after successful train-test splitting.

6. Kept the existing project structure and functionality unchanged.
"""