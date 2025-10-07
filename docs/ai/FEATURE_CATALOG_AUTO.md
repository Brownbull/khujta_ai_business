# Feature Catalog

**Generated:** 2025-10-07T15:32:06.018071
**Total Features:** 6

## FILTER

*6 features*

### `is_weekend`

**Description:** Flag weekend transactions (Saturday/Sunday)

**Type:** `boolean`

**Depends On:** `time_extraction`

**Tags:** time, segmentation

**Version:** 1.0.0

---

### `price_per_unit`

**Description:** Calculate price per unit: revenue / quantity

**Type:** `float`

**Requires:** `quantity_col, revenue_col`

**Tags:** pricing, unit_economics

**Version:** 1.0.0

---

### `profit_margin`

**Description:** Calculate profit margin percentage: (revenue - cost) / revenue * 100

**Type:** `float`

**Requires:** `cost_col, revenue_col`

**Tags:** financial, profitability

**Version:** 1.0.0

---

### `time_extraction`

**Description:** Extract time-based features (hour, weekday, month, etc.) from date column

**Type:** `integer`

**Requires:** `date_col`

**Tags:** time, preprocessing

**Version:** 1.0.0

---

### `time_of_day`

**Description:** Classify transactions by time of day (Morning/Afternoon/Evening/Night)

**Type:** `string`

**Depends On:** `time_extraction`

**Tags:** time, segmentation

**Version:** 1.0.0

---

### `transaction_size_category`

**Description:** Categorize transaction size as Small/Medium/Large based on revenue quartiles

**Type:** `string`

**Requires:** `revenue_col`

**Tags:** segmentation, revenue

**Version:** 1.0.0

---
