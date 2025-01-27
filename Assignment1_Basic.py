# 1. Write a function named mortgage payments that takes three parameters (named principal, rate,
# and amortization), and returns a tuple of six values representing the monthly, semi-monthly, bi-
# weekly, weekly, rapid bi-weekly, and rapid weekly payments.

# Calculate the morgage payments based on different payment frequencies
def mortgage_payments(principal, rate, amortization):
    # Caclulate the total number of periods for each case using amortization period (in years)
    monthly_periods = amortization * 12
    semi_monthly_periods = amortization * 24
    bi_weekly_periods = amortization * 26
    weekly_periods = amortization * 52

    # Calculate periodic rates using the nominal interest rate e.g. rate
    monthly_rate = (1 + rate / 2) ** (2 / 12) - 1
    semi_monthly_rate = (1 + rate / 2) ** (2 / 24) - 1
    bi_weekly_rate = (1 + rate / 2) ** (2 / 26) - 1
    weekly_rate = (1 + rate / 2) ** (2 / 52) - 1

    # Function to Calculate the Present Value of Annuity Factor (PVA)
    def pva(r, n):
        return (1 - (1 + r) ** -n) / r

    # Calculate the payment for each period on each case
    monthly_payment = principal / pva(monthly_rate, monthly_periods)
    semi_monthly_payment = principal / pva(semi_monthly_rate, semi_monthly_periods)
    bi_weekly_payment = principal / pva(bi_weekly_rate, bi_weekly_periods)
    weekly_payment = principal / pva(weekly_rate, weekly_periods)

    #Accelerated Bi-weekly payments are also made every two weeks. The payment is equal to half the monthly amount.
    accelerated_bi_weekly_payment = monthly_payment * 13 / 26
    #Accelerated Weekly payments are also made every week. The payment is equal to one-quarter of the monthly amount.
    accelerated_weekly_payment = monthly_payment * 13 / 52

    # Return the result as a tuple
    return (monthly_payment, semi_monthly_payment, bi_weekly_payment, 
            weekly_payment, accelerated_bi_weekly_payment, accelerated_weekly_payment)
    
    
# 2. Your program should prompt the user to enter the principal amount, the quoted interest rate (as a
# percent, for example, 4.85), and the amortization period in years. Use the input() function to prompt
# the user and read the entered values. We will assume that users will provide legitimate input values so
# no validation checks will be performed on the input values. https://cs.stanford.edu/people/
# nick/py/python-input.html has a simple example on using the input() function.

# Request for user to enter the loan amount
principal = float(input("Enter loan amount (in $): "))
# Request for user to enter the annual interest rate in %
rate = float(input("Enter annual interest rate (in %): ")) / 100
# Request for user to enter the amortization period in years
amortization = float(input("Enter amortization period (in years): "))

# 3. Format your output (rounded to the nearest penny) so that it appears as follows:

# Monthly Payment: $610.39
# Semi-monthly Payment: $304.85
# Bi-weekly Payment: $281.38
# Weekly Payment: $140.61
# Rapid Bi-weekly Payment: $305.20
# Rapid Weekly Payment: $152.60

# The above values were obtained for a principal amount of $100,000, a quoted rate of 5.5%, and an
# amortization period of 25 years

# Call the morgage payment function
payments = mortgage_payments(principal, rate, amortization)
print("\n")

# Print the results as formatted
print(f"Monthly Payment: ${payments[0]:.2f}")
print(f"Semi-Monthly Payment: ${payments[1]:.2f}")
print(f"Bi-Weekly Payment: ${payments[2]:.2f}")
print(f"Weekly Payment: ${payments[3]:.2f}")
print(f"Rapid Bi-Weekly Payment: ${payments[4]:.2f}")
print(f"Rapid Weekly Payment: ${payments[5]:.2f}")


# 5. In your write-up,
# (a) provide the link to your GitHub repository.


# (b) paste the output from your program for a principal amount of $500,000, quoted at 5.5%, and amortized over 25 years.

# Monthly Payment: $3051.96
# Semi-Monthly Payment: $1524.25
# Bi-Weekly Payment: $1406.88
# Weekly Payment: $703.07
# Rapid Bi-Weekly Payment: $1525.98
# Rapid Weekly Payment: $762.99

