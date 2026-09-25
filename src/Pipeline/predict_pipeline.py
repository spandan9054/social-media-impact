import os
import sys
import joblib
import pandas as pd

from src.exception import CustomException


class PredictPipeline:

    def __init__(self):

        try:
            # Get project root
            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )

            # Artifacts folder
            artifact_path = os.path.join(
                project_root,
                "artifacts"
            )

            # Load trained model
            self.model = joblib.load(
                os.path.join(
                    artifact_path,
                    "model.pkl"
                )
            )

            # Load preprocessing objects
            self.preprocessor = joblib.load(
                os.path.join(
                    artifact_path,
                    "preprocessor.pkl"
                )
            )

            self.postprocessor = joblib.load(
                os.path.join(
                    artifact_path,
                    "postprocessor.pkl"
                )
            )

            # Load target label encoder
            self.label_encoder = joblib.load(
                os.path.join(
                    artifact_path,
                    "label_encoder.pkl"
                )
            )

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, input_data):
        """
        Takes raw input data and returns the predicted
        Overall_Impact class.
        """

        try:

            # Convert dictionary to DataFrame
            if isinstance(input_data, dict):
                input_data = pd.DataFrame([input_data])

            # Apply first preprocessing
            input_processed = self.preprocessor.transform(
                input_data
            )

            # Apply post-SMOTENC preprocessing
            input_final = self.postprocessor.transform(
                input_processed
            )

            # Make prediction
            prediction = self.model.predict(
                input_final
            )

            # Convert encoded prediction back to original label
            prediction_label = self.label_encoder.inverse_transform(
                prediction
            )

            return prediction_label[0]

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    predictor = PredictPipeline()

    # Example:
    # Replace these values with actual feature values
    sample_data = {
        # "Age": 20,
        # "Gender": "Male",
        # "Daily_Usage_Hours": 5.0,
        # ...
    }

    prediction = predictor.predict(
        sample_data
    )

    print("Predicted Overall Impact:", prediction)