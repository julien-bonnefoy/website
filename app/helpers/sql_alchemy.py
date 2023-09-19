from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

'''
[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
'''

# ENGINE
engine = create_engine('sqlite:///../data/website-dev.db', echo=True)

# QUERY
query = "SELECT * FROM learning_objects"

# EXECUTE
results = engine.execute([query])
for row in results:
    ...
results.close()

# PERSISTANT CONNECTION
connection = engine.connect()
result = connection.execute([query])
for row in result:
    print(row)  # example
connection.close()

# SESSIONS
Session = sessionmaker(bind=engine)
session = Session()
'''
session.add(): We can pass an instance of a data model into .add() to quickly create a new record to be added in our database.
session.delete(): Similar to the above, .delete() accepts an instance of a data model. If that record exists in our database, it will be staged for deletion.
session.commit(): In both of the above cases, neither change is made until the changes of a session are explicitly committed. At this point, all staged changes are committed at once.
session.close(): Finally, .close() is a clean way of closing our connection when we're done.
'''

# DATA MODELS

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    joined = Column(DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# USE EXAMPLES
new_user = User(username='admin', email='admin@example.com')
session.add(new_user)
session.commit()

session.delete(new_user)
session.commit()

users_1 = User.query.all()
users_2 = User.query.filter(username='todd').all()


# PANDAS
## READ
df = pd.read_sql('SELECT * FROM learning_objects', engine)


## WRITE
df.to_sql('my_table',
          engine,
          if_exists='append',
          schema='my_schema')


# MORE QUERIES
## Example structure of an ORM query

"""
records = session.query(Query).FUNCTION()

# Select records from a SQLAlchemy session

# Calling .query(Customer) on our session isn't a valid query until we add one more method to the chain. 
# All session queries end with a final method to shape/anticipate the result(s) of our query:

# * all() will return all records which match our query as a list of objects. 
#	If we were to use all on the query above, we would receive all customer records with the Python data type List[Customer].
# * first() returns the first record matching our query, despite how many records match the query  
#	(what constitutes "first" depends on how your table is sorted). This is the equivalent of adding 
#	LIMIT 1 to a SQL query. As a result, the Python type to be returned would be Customer.
# * one() is extremely useful for cases where a maximum of one record should exist for the query 
#	we're executing (think of querying by primary key). This syntax is notably useful when verifying whether or not 
#	a record exists prior to creating one.
# * scalar() returns a single value if one exists, None if no values exist, or raises an exception if multiple 
#	records are returned.
# * get([VALUE(S)]) searches against a model's primary key to return rows where the primary key is equal to the 
#	value provided. get() also accepts tuples in the event that multiple foreign keys should be searched. 
#	Lastly, get() can also accept a dictionary and return rows where the columns (dictionary keys) match the values provided.

records = session
    .query(Customer)
    .filter(Customer)
    .first_name == 'Carl')
    .all()

# Fetch records where `first_name` is `Carl`
records = session
    .query(Customer)
    .filter_by(first_name="Carl")
    .all()

# Fetch records where `first_name` begins with the letter `J`
records = session
    .query(Customer)
    .filter(Customer.first_name.like('J%'))
    .all()

# limit([INTEGER]): Limits the number of rows to a maximum of the number provided.
# order_by([COLUMN]): Sorts results by the provided column.  
# offset([INTEGER]): Begins the query at row n.

# Execute a SELECT query on JOINed tables
records = session.query(Customer).join(Order, Order.customer_id == Customer.id).all()

# Execute an outer JOIN
records = session
    .query(ExampleModel1)
    .outerjoin(ExampleModel2)
    .all()

from .models import ExampleModel1, ExampleModel2

# Execute a UNION
records = ExampleModel1.union(ExampleModel2)

# count([COLUMN]): Counts the number of records in a column.
# count(distinct([COLUMN])): Counts the distinct number of records in a column.
# sum([COLUMN]): Adds the numerical values in a column.

# Count number of records with a `first_name` value
records = session
    .query(func.count(Customer.first_name))
    .all()

# Count number of DISTINCT `first_name` values
records = session
    .query(func.count(distinct(Customer.first_name)))
    .all()

# Execute a `GROUP BY` aggregation query
records = session
    .query(func.count(Customer.first_name))
    .group_by(Customer.first_name)
    .all()

# Inserting records via data models
customer = Customer(
    first_name='Todd',
    last_name='Birchard',
    email='fake@example.com',
    preferred_language='English',
    join_date=datetime.now()
)
session.add(customer)
session.commit()

# Inserting records via SQLAlchemy `Table` objects
insert = [TABLE]
    .insert()
    .values(
        first_name='Todd',
        last_name='Jack Jones',
        email='fake@example.com',
        preferred_language='English',
        join_date=datetime.now()
    )

# Updating records via SQLAlchemy `Table` objects
result = [TABLE]
    .update()
    .where([TABLE].c.name == 'Todd')
    .values(email='newemail@example.com')

# Delete records where `first_name` is `Carl`

"""
