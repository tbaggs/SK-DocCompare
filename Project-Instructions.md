The goal of this project is to create a Semantic Kernel Agent that can ready two policy documents and prepare a detailed comparison of the primary and secondary document.    

# Part 1
The goal is to get references to two policy documents (primary and secondary policy).  From there, the agent will analyze each document to determine the following:

## Steps
1. Are these policies related.  Example - Both policies provide guidance for Travel Expense Guidelines.  

2. Identify a list of differences between each document.  Include specific text that represents the difference.

3. Provide guidance on how to incorporate the differences in the secondary document into the primary document

## Notes

- Generate all code in Python using the Semantic Kernel framework.
- The documents will be stored in Azure Blob Storage and will require a SaS token to access each document
- The results should be output in a json with the following structure:


```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PolicyDocumentComparison",
  "type": "object",
  "properties": {
  "documentSimilarity": {
      "type": "boolean",
      "description": "Indicates whether the two documents are considered similar (true) or not (false)."
    },
    "documentDifferences": {
      "type": "array",
      "description": "List of differences between the two documents.",
      "items": {
        "type": "string",
        "description": "A human-readable description of a single difference."
      }
    },
    "documentIntegrationSteps": {
      "type": "array",
      "description": "Step-by-step actions to integrate or reconcile the two documents.",
      "items": {
        "type": "string",
        "description": "A human-readable description of a single integration step."
      }
    }
  },
  "required": ["documentSimilarity", "documentDifferences", "documentIntegrationSteps"],
  "additionalProperties": false
}
  
```

