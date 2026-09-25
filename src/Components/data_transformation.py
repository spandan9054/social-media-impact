from src.Components.data_ingestion import Data
from sklearn.preprocessing import LabelEncoder


class DataProcessing:

    def __init__(self):
        pass

    def encode_y(self, y_train, y_test):
        """
        Encodes the target variable using LabelEncoder.
        The encoder is fitted only on y_train and then used
        to transform y_test.
        """

        label_encoder = LabelEncoder()

        y_train = label_encoder.fit_transform(y_train)

        y_test = label_encoder.transform(y_test)

        return y_train, y_test, label_encoder

    def pipeline_columns(self):
        """
        Identifies numerical and categorical feature columns.
        """

        X, _ = Data.load_data(
            "E:\\Projects\\social_impact\\Social_media_impact_on_life.csv"
        )

        # Numerical columns
        numerical_cols = X.select_dtypes(
            exclude=['bool', 'object']
        ).columns.tolist()

        # Categorical columns which will be ordinal encoded
        label_categorical = [
            'Academic_Level',
            'Social_Comparison_Frequency'
        ]

        # Remaining categorical columns
        categorical_cols = X.select_dtypes(
            include=['bool', 'object']
        ).columns.tolist()

        ohe_categorical = [
            col for col in categorical_cols
            if col not in label_categorical
        ]

        return numerical_cols, label_categorical, ohe_categorical


"""
CORRECTIONS MADE:

1. Removed y_train and y_test from the DataProcessing constructor.

2. y_train and y_test are now passed directly to encode_y():
       encode_y(y_train, y_test)

3. Removed unnecessary loading and splitting of the dataset from
   encode_y(). The split is already performed in the training pipeline.

4. LabelEncoder is fitted only on y_train and then used to transform
   y_test, preventing information leakage from the test set.

5. Corrected the categorical type check from 'str' to 'object'.
   Pandas normally stores text columns as object dtype.

6. Kept Academic_Level and Social_Comparison_Frequency as the
   label/ordinal categorical group and the remaining categorical
   features as the OHE group.
"""