Goal: The project shows example tests for different pillars:
- Completeness
- Consistensy
- Integrity
- Timeless
- Uniqieness
- Validity

All tests are stored in directory: `expectations`

Project are based on postgres. 
You can find data in directory `data`
Use scripts from directory `scripts` to create tables and ingest data into DB

In project I emulate data flow 
staging data (tables with prefix STG) -> data warehouse (tables with prefix DWH) -> data marts (table with prefix DM)

Note: I used data from course https://www.udemy.com/course/data-warehouse-etl-testing-data-quality-management-a-z/