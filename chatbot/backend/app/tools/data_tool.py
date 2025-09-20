import pandas as pd


class DataTool:
    def __init__(self, csv_path=None):
        if csv_path is None:
            import os

            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(
                current_dir, "..", "dataset", "simple_dataset.csv"
            )
        self.data = pd.read_csv(csv_path)

    def retrieve_and_generate(self, query):
        query_lower = query.lower()

        # Direct massage type mapping for better accuracy
        massage_mappings = {
            "neck": "Neck and Shoulder Massage",
            "deep tissue": "Deep Tissue Massage",
            "thai": "Thai Massage",
            "hot stone": "Hot Stone Massage",
            "swedish": "Swedish Massage",
            "aromatherapy": "Aromatherapy Massage",
            "sports": "Sports Massage",
            "prenatal": "Prenatal Massage",
            "reflexology": "Reflexology",
            "full body": "Full Body Relaxation",
        }

        # Find the best match
        best_match = None
        for key, massage_type in massage_mappings.items():
            if key in query_lower:
                best_match = massage_type
                break

        if best_match:
            matching_row = self.data[self.data["Massage_Type"] == best_match]
            if not matching_row.empty:
                row = matching_row.iloc[0]
                response = f"The {row['Massage_Type']} costs ${row['Avg_Spending']} and lasts for {row['Duration_Minutes']} minutes."
                return response

        # Fallback to keyword matching if direct mapping fails
        keywords = query_lower.split()
        relevant_rows = self.data[
            self.data["Massage_Type"]
            .str.lower()
            .str.contains("|".join(keywords), na=False)
        ]

        if relevant_rows.empty:
            return "Sorry, I couldn't find information on that massage type. Available types: Swedish, Deep Tissue, Hot Stone, Neck and Shoulder, Aromatherapy, Thai, Sports, Prenatal, Reflexology, Full Body Relaxation."

        def count_matches(row):
            massage_type = row["Massage_Type"].lower()
            return sum(1 for keyword in keywords if keyword in massage_type)

        relevant_rows = relevant_rows.copy()
        relevant_rows["match_count"] = relevant_rows.apply(
            count_matches, axis=1
        )
        relevant_rows = relevant_rows.sort_values(
            by="match_count", ascending=False
        )

        top_row = relevant_rows.iloc[0]
        response = f"The {top_row['Massage_Type']} costs ${top_row['Avg_Spending']} and lasts for {top_row['Duration_Minutes']} minutes."

        return response