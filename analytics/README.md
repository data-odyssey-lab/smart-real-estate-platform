# Nairobi Real Estate Analytics Platform

##  Executive Summary

This repository contains a comprehensive real estate analytics platform analyzing the Nairobi property market using 665 cleaned listings scraped from Property24 Kenya. The analysis reveals **a two-tier market structure**, identifies **bedroom count as the strongest price predictor**, and provides **actionable insights for buyers and investors**.

**Key Headline Numbers:**
- **665 Listings** across Nairobi's formal market
- **KES 16.5M Median Price** (vs KES 41.33M mean — revealing the impact of ultra-premium outliers)
- **47.22% Affordable** at ≤KES 15M
- **52.2% of market** concentrated in the 100-150K/m² price band
- **77.44% Apartments** — reflecting market supply mix and platform coverage bias

---

##  Location Deep Dive

### Top 10 Neighbourhoods by Absolute Price

| Rank | Neighbourhood | Median Price | Listings | Type |
|------|--------------|--------------|----------|------|
| 1 | Karen | KES 185M | 29 | Ultra-premium |
| 2 | Runda | KES 140M | 22 | Ultra-premium |
| 3 | Loresho | KES 100M | 13 | Ultra-premium |
| 4 | Lavington | KES 85M | 43 | Premium |
| 5 | Spring Valley | KES 57.9M | 16 | Premium |
| 6 | Peponi | KES 59.7M | 12 | Premium |
| 7 | Kitisuru | KES 81M | 6 | Premium |
| 8 | Parklands | KES 65M | 5 | Premium |
| 9 | Garden Estate | KES 55M | 3 | Mid-market |
| 10 | Kiambu Road | KES 40M | 17 | Mid-market |

### Top 10 Neighbourhoods by Price per m² (Value Ranking)

| Rank | Neighbourhood | Price/m² | Median Price | Insight |
|------|--------------|----------|--------------|---------|
| 1 | Loresho | 371K/m² | KES 100M | Most expensive per unit space |
| 2 | Karen | 300K/m² | KES 185M | High absolute + high per m² |
| 3 | Runda | 277K/m² | KES 140M | Premium quality + space |
| 4 | Lavington | 200K/m² | KES 85M | Strong value for premium area |
| 5 | Spring Valley | 167K/m² | KES 57.9M | Good value, urban access |
| 6 | Peponi | 151K/m² | KES 59.7M | Karura forest proximity premium |
| 7 | Kiambu Road | 139K/m² | KES 40M | Balanced value |
| 8 | Westlands | **136K/m²** | KES 17.1M | **Core market value baseline** |
| 9 | Kileleshwa | 110K/m² | KES 12.9M | **Best value for urban location** |
| 10 | Riverside | 134K/m² | KES 15M | Strong value alternative |

**Key Insight:** Kileleshwa offers better price/m² than Westlands while maintaining similar urban accessibility. Syokimau (76K/m²) offers the lowest cost per m² but with SGR/Mombasa Road trade-offs.


---

##  Practical Usage Guidance

### For First-Time Buyers (KES 5-15M Budget)

1. **Target Segment:** 1BR-2BR apartments in Westlands, Kileleshwa, or Kilimani
2. **Price Benchmark:** Look for properties in the 100-150K/m² band
3. **Location Selection:**
   - Westlands: 136K/m², most listings, strong rental demand
   - Kileleshwa: 110K/m², better value, still urban
   - Kilimani: 115K/m², Langata constituency strength
4. **Valuation Check:** Calculate asking price ÷ floor size. If >20% above neighbourhood median in this report, negotiate down
5. **Financing Ease:** 2BR apartments in the 100-150K/m² band are easiest for mortgage approval

### For Buy-to-Let Investors

1. **Optimal Segment:** 1BR + 2BR apartments (317 combined listings)
2. **Target Areas:** Westlands (221), Kileleshwa (80), Kilimani (73)
3. **Target Price:** At or below KES 13M for 2BR (below median)
4. **Rental Demand:** Young professionals + expats drive 1-2BR demand in Western Nairobi
5. **Expected Yield:** 4-6% p.a. in volume markets; 2-3% in luxury areas
6. **Avoid:** Ultra-premium areas (Karen, Runda) unless seeking capital appreciation, as rental yields are depressed relative to purchase price

### For Capital Appreciation (5-10 Year Hold)

1. **Target Areas:** Karen (185M, 300K/m²), Runda (140M, 277K/m²), Loresho (100M, 371K/m²)
2. **Target Segment:** 4BR+ houses, estates, premium properties
3. **Entry Strategy:** Buy at or below neighbourhood median; wait for appreciation
4. **Timeline:** 5-10 year horizon minimum; luxury segment shows slower transaction velocity but strong price floors
5. **International Demand:** These areas attract high-net-worth buyers from diaspora, providing price stability

### For Developers & Platforms

1. **Market Gap:** Premium tier (KES 25-60M) has only 107 listings vs 179 budget + 251 mid = 430 in accessible segment. **Untapped premium supply opportunity**
2. **Geographic Opportunity:** Eastern zones (Embakasi, Kasarani) account for <1% of current coverage. **First platform to map Eastlands comprehensively gains competitive advantage**
3. **Feature Value:** Bedroom count (r=0.687) is most actionable filtering feature after price/m²



---


### Affordability Definition

- **Affordable:** ≤KES 15M (rationale: standard mortgage qualification for middle-income earner in Nairobi)
- **Budget:** ≤KES 10M (entry-level)
- **Mid:** KES 10-25M (largest supply segment)
- **Premium:** KES 25-60M (small segment, market gap)
- **Luxury:** >KES 60M (18+ properties in Karen, Runda, Loresho)

---


















