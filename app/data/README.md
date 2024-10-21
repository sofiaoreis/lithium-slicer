This directory includes the sfl rankings for each defects4j test case. Each defects4j project includes different `.json` files, one per test case.

```
- Chart
    - 1.json
    - 2.json
    - ...
```

Each file includes the ochiai scores for the locs involved in the test case. 

```
{
    "loc": "1793", 
    "score": 1.0, 
    "class": "org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java"
}, 
{
    "loc": "1613", 
    "score": 0.4472135954999579, 
    "class": "org/jfree/chart/plot/CategoryPlot.java"
}
```

Each line in the ranking shows, respectively, the rank/position, the Java class name, and the ochai score.