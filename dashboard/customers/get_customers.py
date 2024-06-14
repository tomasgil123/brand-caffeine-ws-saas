
import requests


def get_customers(custom_filters, cookie):

    endpoint = "https://www.faire.com/api/v3/crm/b_arceup81f2/get-customers"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    payload = {
            "pagination_data": {
                "page_number": 1,
                "page_size": 20
            },
            "brand_customer_view_query": {
                "customer_tokens": [],
                "customer_filters": custom_filters,
                "excluded_customer_tokens": [],
                "brand_crm_tag_tokens": []
            }
        }
    
    number_customers = 0

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()

            number_customers = data['pagination_data']['total_results']

            return number_customers
        else:
            print(f"Request failed with status code {response.status_code}")
            return number_customers
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return number_customers
    
def get_top_20_customers_without_purchases_last_60_days(cookie, greater_than, less_than, amount, faire_direct=False):

    custom_filters = [
            {
                "filters": [
                    {
                        "comparator": "GREATER_THAN",
                        "datetime_value": greater_than,
                        "field": "LAST_ORDERED",
                        "type": "DATETIME"
                    },
                    {
                        "comparator": "LESS_THAN",
                        "datetime_value": less_than,
                        "field": "LAST_ORDERED",
                        "type": "DATETIME"
                    }
                ],
                "label": "LAST_ORDERED"
            },
            {
                "filters": [
                    {
                        "comparator": "GREATER_THAN",
                        "int_value": amount,
                        "field": "ORDER_AMOUNT_CENTS",
                        "type": "MONEY"
                    }
                ],
                "label": "ORDER_AMOUNT_CENTS"
            }
        ]
    
    if faire_direct:
        custom_filters.append(
            {
                "filters": [
                    {
                        "field": "COMMISSION",
                        "type": "NUMBER",
                        "comparator": "EQUAL_TO",
                        "int_value": 0
                    }
                ],
                "label": "COMMISSION"
            }
        )
    
    return get_customers(custom_filters, cookie)

def get_customers_without_second_purchase_last_60_days(cookie, greater_than, less_than, faire_direct=False):

    custom_filters = [
                {
                    "filters": [
                        {
                            "comparator": "GREATER_THAN",
                            "datetime_value": greater_than,
                            "field": "LAST_ORDERED",
                            "type": "DATETIME"
                        },
                        {
                            "comparator": "LESS_THAN",
                            "datetime_value": less_than,
                            "field": "LAST_ORDERED",
                            "type": "DATETIME"
                        }
                    ],
                    "label": "LAST_ORDERED"
                },
                {
                    "filters": [
                        {
                            "comparator": "EQUAL_TO",
                            "int_value": 1,
                            "field": "ORDER_COUNT",
                            "type": "NUMBER"
                        }
                    ],
                    "label": "ORDER_COUNT"
                }
        ]
    
    if faire_direct:
        custom_filters.append(
            {
                "filters": [
                    {
                        "field": "COMMISSION",
                        "type": "NUMBER",
                        "comparator": "EQUAL_TO",
                        "int_value": 0
                    }
                ],
                "label": "COMMISSION"
            }
        )
    
    return get_customers(custom_filters, cookie)

def get_customers_with_purchase_last_60_days_no_review(cookie):

    custom_filters =[
                {
                    "label": "ORDER_COUNT",
                    "filters": [
                        {
                            "field": "ORDER_COUNT",
                            "type": "NUMBER",
                            "comparator": "GREATER_THAN",
                            "int_value": 1
                        }
                    ]
                },
                {
                    "label": "LAST_ORDER_DELIVERED_AT",
                    "filters": [
                        {
                            "field": "LAST_ORDER_DELIVERED_AT",
                            "type": "DATETIME",
                            "comparator": "RELATIVE_GREATER_THAN_OR_EQUAL_TO",
                            "datetime_value": -5184000000
                        },
                        {
                            "field": "LAST_ORDER_DELIVERED_AT",
                            "type": "DATETIME",
                            "comparator": "RELATIVE_LESS_THAN_OR_EQUAL_TO",
                            "datetime_value": 0
                        }
                    ]
                },
                {
                    "label": "REVIEW_SUBMITTED",
                    "filters": [
                        {
                            "field": "REVIEW_SUBMITTED",
                            "type": "REVIEW_SUBMITTED_ENUM",
                            "comparator": "EQUAL_TO",
                            "review_submitted_type_value": "ORDERED_REVIEW_NOT_SUBMITTED"
                        }
                    ]
                }
        ]
    
    return get_customers(custom_filters, cookie)