import json
import os

class AreaService:
    def __init__(self, data_file='areas.json'):
        self.data_file = data_file
        self.areas = self._load_data()

    def _load_data(self):
        """Loads data from the JSON file safely."""
        if not os.path.exists(self.data_file):
            print(f"Warning: {self.data_file} not found. Starting with empty data.")
            return []
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: {self.data_file} contains invalid JSON.")
            return []

    def _calculate_overall_score(self, area):
        """
        Calculates the average AreaScore dynamically based on sub-scores.
        You can adjust weights here if needed.
        """
        scores = [
            area.get('water_score', 0),
            area.get('traffic_score', 0),
            area.get('safety_score', 0),
            area.get('growth_score', 0)
        ]
        return round(sum(scores) / len(scores)) if scores else 0

    def browse_all(self, sort_by_score=False):
        """Returns all areas. Optionally sorts them by their calculated AreaScore."""
        results = []
        for area in self.areas:
            area_copy = area.copy()
            area_copy['overall_score'] = self._calculate_overall_score(area)
            results.append(area_copy)
        
        if sort_by_score:
            return sorted(results, key=lambda x: x['overall_score'], reverse=True)
        return results

    def search_area(self, query):
        """Searches areas by name or region (case-insensitive matches)."""
        query = query.lower()
        results = []
        
        for area in self.areas:
            if query in area['name'].lower() or query in area['location'].lower():
                area_copy = area.copy()
                area_copy['overall_score'] = self._calculate_overall_score(area)
                results.append(area_copy)
                
        return results

    def get_area_by_id(self, area_id):
        """Retrieves a specific area's details by its ID."""
        for area in self.areas:
            if area['id'] == area_id:
                area_copy = area.copy()
                area_copy['overall_score'] = self._calculate_overall_score(area)
                return area_copy
        return None


if __name__ == "__main__":
    service = AreaService()

    print("--- 1. Browse All Areas (with Calculated Overall Score) ---")
    all_areas = service.browse_all(sort_by_score=True)
    for area in all_areas:
        print(f"{area['name']} ({area['location']}) -> Overall Score: {area['overall_score']}")

    print("\n--- 2. Search Area (Query: 'Kharghar') ---")
    search_results = service.search_area("Kharghar")
    print(json.dumps(search_results, indent=2))

    print("\n--- 3. Fetch Single Area by ID (ID: 1) ---")
    single_area = service.get_area_by_id(1)
    print(single_area)