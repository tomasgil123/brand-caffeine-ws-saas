
<!-- Competitors - main attributes - summary -->

You are going to receive a string representation of a python dataframe. 

I want you to come up with a summary of differences between {brand} and other brands. 

The summary of differences has to look like the following example: 

Summary of Differences: 1. Fulfillment Times: Latico Leathers has moderate lead times, longer than most but shorter than Sixtease Bags USA. 2. Number of Reviews: It has a moderate number of reviews, more than some brands but fewer than Threaded Pear. 3. First Order Minimum Amount: Latico Leathers requires the highest first order minimum amount among all brands. 4. Reorder Minimum Amount: It has a relatively high reorder minimum amount, especially when compared to Threaded Pear's zero minimum. Also, try to come up with recommendations to be the best on each category.

I want you to just output a bullet point for each summary difference, nothing else.

Make sure the title of each bullet point is in bold. Don't say "it" to refer to the {brand}.

The dataframe will be delimited with four hashtags: ####

<!-- Competitors - main attributes - recommendations -->

You are going to receive a string representation of a python dataframe. 

I want you to come up recommendations for {brand}.

To come up with recommendations do the following:
- Find the best possible value for a dimension. For example, for Fulfillment Times is the lowest value and for reviews is the highest. We will call this value “Best value”
- Find {brand} value for that dimension. We will call this value “client value”
- Get the 50% of that best value found on the previous step. For example, if the best value is 2, then is 1. Another example, if the best value is 500 then is 250. We will call this value just “Best value 50%”
- Calculate the difference between {brand} value for that dimension. For example, if the best value is 2 and {brand} value for that dimension is 5, then the difference is 3. We will call this value “The difference”
- If “Best value 50%” of a dimension is lower “The difference” then:
    - If “Best value” is lower than “client value”, tell {brand} to try to get to “Best value” plus “Best value 50%”
    - If “Best value” is higher than “client value”, tell {brand} to try to get to “client value” plus “Best value 50%”

I want you to just output a bullet point for each recommendation, nothing else. Also, we you write the recommendations don’t mention the internal calculations you had to do to come up with the calculation.

For first order and reorder numbers recommendation should be at least \$250 and \$100 respectively. Don't mention higher values.

Always use round numbers for the recommendations.

Remember adding the symbol $ before first order and reorder numbers.

When writing recommendations add the following to the beginning of the recommendation: 

For fulfillment times: "Retailers on Faire can search Sellers by their fulfillment times. If yours is too long, you may be getting overlooked."
For number of reviews: "On average, reviews on a product can create an 18% lift in sales".
For first order minimum: "First order minimums are a massive barrier to entry on Faire. Because of the sheer number of smaller retailers on the platform, the higher they are, the less likely you are to get an order."
For reorder minimum amount: "Reorder minimums are equally important on Faire and should ALWAYS be lower that the First Order Minimum - even if only by \$25 - \$50."

Make sure the title of each point is in bold.

The dataframe will be delimited with four hashtags: ####

<!-- Competitors - brand values - recommendations -->

You are going to receive a string representation of a python dataframe. 

Find out what makes {brand} different from other brands. Avoid considering things that are equal to all brands. 
Write a recommendation for {brand} to remark each thing that makes it different from others on different parts of its Faire profile.

Here is an example of how you should write recommendations:

1. Eco-Friendly: On your Faire profile, highlight your commitment to sustainability. Use sections like "About Us" or "Sustainability Practices" to detail your eco-friendly initiatives, materials used, and any certifications. Example:
    * "At Latico Leathers, we are dedicated to sustainability. Our products are crafted using eco-friendly materials, ensuring a minimal environmental footprint. Learn more about our sustainable practices "
2. Woman Owned: Emphasize this aspect in sections like "Our Story" or "Meet the Founder". Mention the journey of the woman founder and how it influences the brand's ethos and products. Example:
    * "Latico Leathers is proud to be a woman-owned business. Founded by [Founder's Name], our brand reflects a unique blend of creativity, resilience, and dedication. Discover more about our founder's journey and vision"

Only output the list of recommendations, nothing else.

Make sure the title of each point is in bold.

<!-- Competitors - brand values - summary -->

<!-- Competitors - description - summary -->

Summarize the following description in just two lines:

<!-- end -->