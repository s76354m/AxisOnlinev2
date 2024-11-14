test_scenarios = {
    "Basic Operations": {
        "Create New Mapping": {
            "steps": [
                "Click 'Create New Mapping' in sidebar",
                "Fill in test data:",
                {
                    "Project ID": "1",
                    "CSP Code": "TEST001",
                    "LOB Type": "MEDICAL",
                    "Description": "Test Medical LOB",
                    "Status": "ACTIVE",
                    "Effective Date": "today's date",
                    "Termination Date": "future date"
                },
                "Click 'Create Mapping' button",
                "Verify success message"
            ]
        },
        "View Mappings": {
            "steps": [
                "Click 'View/Edit Mappings' in sidebar",
                "Verify TEST001 mapping appears in list",
                "Check all columns are visible and correct"
            ]
        }
    },
    "Validation Tests": {
        "Invalid CSP Code": {
            "steps": [
                "Try creating mapping with CSP Code '@#'",
                "Verify error message about alphanumeric requirement"
            ]
        },
        "Invalid Dates": {
            "steps": [
                "Try setting Termination Date before Effective Date",
                "Verify date validation error message"
            ]
        }
    },
    "Filtering": {
        "LOB Type Filter": {
            "steps": [
                "Select 'MEDICAL' from LOB Type dropdown",
                "Verify only medical LOBs shown"
            ]
        },
        "Status Filter": {
            "steps": [
                "Select 'ACTIVE' from Status dropdown",
                "Verify only active mappings shown"
            ]
        }
    }
} 