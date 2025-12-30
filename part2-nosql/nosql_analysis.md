# Task 2.1: NoSQL Justification Report  
**FlexiMart – NoSQL Database Analysis**

---

## Problem Context

FlexiMart plans to expand its product catalog to include highly diverse products such as electronics, clothing, footwear, and accessories. Each product category has different attributes, and the system must also support customer reviews and future scalability. This report analyzes the limitations of a relational database for this use case and justifies the adoption of MongoDB as a NoSQL solution.

---

## Section A: Limitations of RDBMS (Relational Databases)  
*(~150 words)*

Conventional relational databases, such as MySQL, are less appropriate for managing extremely varied product catalogs because they rely on a fixed schema. In the case of FlexiMart, different product categories need different characteristics. For instance, shoes need size and color, while laptops need RAM and processor specifications. Many nullable columns or several tables would be needed to represent this variability in a relational model, which would increase complexity and decrease clarity.

In relational systems, frequent schema modifications also become expensive. ALTER TABLE operations, which are dangerous and ineffective at scale, are frequently necessary when introducing new product types. Performance problems and downtime may result from this.

Storing customer reviews as nested data presents another challenge for RDBMSs. Reviews frequently involve one-to-many relationships and joins across multiple tables, which increases query complexity and impacts performance. As data volume rises, relational databases become less flexible for dynamic, content-rich applications like FlexiMart because these joins become slower and more challenging to maintain.

---

## Section B: NoSQL Benefits (MongoDB)  
*(~150 words)*

These challenges are mitigated by MongoDB's flexible, document-based schema. Because each product can be kept as a JSON-like document with attributes specific to its category, laptops, shoes, and other things can coexist in the same collection without creating schema conflicts. This flexibility eliminates the need for frequent schema migrations.

Because MongoDB enables embedded documents, it is ideal for keeping customer reviews directly into product records. Quicker reads and simpler searches without complex joins are made possible by nesting reviews as arrays.

Additionally, MongoDB was designed with horizontal scalability in mind. FlexiMart's support for sharding allows it to spread data over multiple servers as it grows. This ensures excellent availability and performance as traffic and data volume grow. MongoDB's adaptable schema architecture, embedded documents, and horizontal scalability make it a suitable choice for FlexiMart's evolving product catalog and review system.

---

## Section C: Trade-offs of Using MongoDB  
*(~100 words)*

One disadvantage of moving from MySQL to MongoDB is its poorer support for complicated transactions. Although MongoDB supports transactions, relational databases handle multi-table ACID transactions more natively, making them superior for financial or highly relational workflows.

Another trade-off is data consistency. MongoDB often employs an eventual consistency mechanism in distributed situations, which may lead to temporary discrepancies. Additionally, the developer is responsible for enforcing relationships like foreign keys in MongoDB, which increases the risk of data integrity issues if not managed appropriately. Because of this, using MongoDB necessitates careful design and validation logic.

---

## Conclusion

For FlexiMart’s diverse and rapidly evolving product catalog, MongoDB provides greater flexibility, scalability, and simplicity compared to traditional relational databases. While there are trade-offs, the benefits make MongoDB a strong choice for this use case.
