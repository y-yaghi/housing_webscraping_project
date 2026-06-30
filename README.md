# Housing Listing Text Analysis & Price Prediction

## Overview

This project investigates whether housing listing descriptions influence home prices beyond traditional structural features such as square footage, bathrooms, home age, and location.

Using scraped housing listings from Realtor.com through the HomeHarvest Python package, this project combines structured housing data with natural language processing techniques to study how descriptive language affects listing prices.

The main research question is:

**Do listing descriptions influence housing prices beyond structural housing features?**

## Project Motivation

Traditional housing price models usually rely on measurable features such as size, number of rooms, location, and age of the home. However, real estate listings also include descriptive language such as “luxury,” “renovated,” “modern,” and “waterfront.”

This project explores whether those words contain meaningful pricing information or if they are simply marketing language.

## Data Collection

Housing listings were collected from Realtor.com using the HomeHarvest Python package.

Originally, direct web scraping from sites such as Zillow and Realtor.com only returned a small number of listings, around the first 40 homes. Because of this limitation, HomeHarvest was used to collect a larger dataset.

Dataset summary:

- Location: Virginia
- Listings: 9,800
- Original features: 66
- Target variable: log-transformed listing price
- Text feature: listing description

## Methods

The project includes:

- Web scraping / data collection
- Data cleaning and preprocessing
- Missing value handling
- Feature engineering
- Text cleaning
- TF-IDF text representation
- OLS regression
- Ridge regression
- Decision tree modeling
- Grid search hyperparameter tuning
- Model comparison using R², RMSE, and MAE

## Models Evaluated

| Model | Purpose |
|---|---|
| Baseline Regression | Predict price using structured features only |
| OLS Regression | Test statistical significance of text features |
| TF-IDF + Ridge | Best predictive model using text and structure |
| Decision Tree | Interpretable model for price splits |
| Decision Tree with Text | Test whether text improves nonlinear model performance |

## Key Results

| Model | Test R² | Test RMSE |
|---|---:|---:|
| Baseline Model No Text | 0.577 | 0.609 |
| TF-IDF + Ridge | 0.737 | 0.480 |
| Best Tuned TF-IDF + Ridge | 0.817 | 0.400 |
| Decision Tree No Text | 0.466 | 0.684 |
| Decision Tree With Text | 0.503 | 0.660 |

## Main Findings

- Text features improved model performance beyond structural housing features.
- The best model was TF-IDF + Ridge regression.
- Listing descriptions contained measurable pricing signals.
- Words such as “estate,” “waterfront,” and “luxury” were associated with higher prices.
- Words such as “auction,” “lot,” and “septic” were associated with lower prices.
- Text features improved predictive performance and helped explain hidden property value.
