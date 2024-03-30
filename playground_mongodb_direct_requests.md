# Examples: MongoDB Compass - Requests

This file contains example queries to local MongoDB.

- **Find Documents by Field Matching:**

  Find all documents where the "position" field contains "Product Manager":

  { "title": { "$regex": "Product Manager", "$options": "i" } }

- **Find Documents by Exact Field Value:**

  Find all documents where the city in the "location" field is "San Francisco":

  { "location": "San Francisco, CA" }

- **Find Documents by Numeric Range: (not applicable for current state of the DB)**

  Find all documents where the "salary" field is greater than 100000:

  { "salary": { "$gt": 100000 } }

- **Find Documents by Multiple Conditions:**

  Find all documents where the company starts with "A" and the position contains "Director":

  { "$and": [{ "company": { "$regex": "^A", "$options": "i" } }, { "title": { "$regex": "Director", "$options": "i" } }] }

- **Find Documents by Date Range:**

  Find all documents where the "publication_date" is after March 29, 2024:

  { "title": { "$regex": "Director", "$options": "i" }, "timestamp": { "$gte": ISODate("2024-03-29T00:00:00Z") } }

- **Find Documents by Array Field: (not applicable for current state of the DB):**

  Find all documents where the "skills" array contains "Python":

  { "skills": "Python" }

- **Find Documents by Array Field Length: (not applicable for current state of the DB):**

  Find all documents where the "skills" array has more than 3 elements:

  { "skills": { "$exists": true, "$gt": { "$size": 3 } } }
